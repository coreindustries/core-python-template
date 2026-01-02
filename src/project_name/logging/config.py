"""Logging configuration.

Configures structured JSON logging with security-focused settings.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Literal

from project_name.logging.formatters import JsonFormatter, MaskingFilter


def configure_logging(
    level: str = "INFO",
    json_output: bool = True,
    log_file: Path | None = None,
    max_bytes: int = 10_485_760,  # 10 MB
    backup_count: int = 10,
    enable_masking: bool = True,
    environment: Literal["development", "staging", "production"] = "development",
) -> None:
    """Configure application logging with forensic capabilities.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        json_output: Use JSON structured logging (recommended for production).
        log_file: Optional file path for log output.
        max_bytes: Maximum log file size before rotation.
        backup_count: Number of backup files to keep.
        enable_masking: Enable sensitive data masking in logs.
        environment: Deployment environment.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create formatter
    if json_output:
        formatter: logging.Formatter = JsonFormatter(environment=environment)
    else:
        fmt_str = (
            "%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(correlation_id)s | %(message)s"
        )
        formatter = logging.Formatter(fmt=fmt_str, datefmt="%Y-%m-%dT%H:%M:%S%z")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if enable_masking:
        console_handler.addFilter(MaskingFilter())

    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        if enable_masking:
            file_handler.addFilter(MaskingFilter())

        root_logger.addHandler(file_handler)

    # Security audit log (separate file for forensics)
    if log_file:
        audit_log_file = log_file.parent / "audit.log"
        audit_handler = logging.handlers.RotatingFileHandler(
            filename=audit_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count * 2,  # Keep more audit logs
            encoding="utf-8",
        )
        audit_handler.setFormatter(JsonFormatter(environment=environment))
        audit_handler.setLevel(logging.INFO)

        if enable_masking:
            audit_handler.addFilter(MaskingFilter())

        # Only audit logger writes to this file
        audit_logger = logging.getLogger("audit")
        audit_logger.addHandler(audit_handler)
        audit_logger.propagate = False  # Don't duplicate to root

    # Set levels for noisy libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
