"""Log formatters and filters for forensic logging.

Provides JSON structured logging and sensitive data masking.
"""

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any, ClassVar

from project_name.logging.context import get_correlation_id, get_request_context


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging.

    Produces logs in a format suitable for log aggregation systems
    (ELK, Splunk, CloudWatch, etc.) with forensic metadata.
    """

    def __init__(self, environment: str = "development") -> None:
        """Initialize formatter.

        Args:
            environment: Deployment environment name.
        """
        super().__init__()
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record to format.

        Returns:
            JSON formatted log string.
        """
        # Base log structure
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": self.environment,
        }

        # Add correlation ID for request tracing
        correlation_id = get_correlation_id()
        if correlation_id:
            log_entry["correlation_id"] = correlation_id

        # Add request context if available
        request_context = get_request_context()
        if request_context:
            log_entry["request"] = request_context

        # Add source location
        log_entry["source"] = {
            "file": record.pathname,
            "line": record.lineno,
            "function": record.funcName,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields from record
        extra_fields = {
            k: v
            for k, v in record.__dict__.items()
            if k
            not in {
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "exc_info",
                "exc_text",
                "thread",
                "threadName",
                "taskName",
                "message",
            }
        }
        if extra_fields:
            log_entry["extra"] = extra_fields

        return json.dumps(log_entry, default=str, ensure_ascii=False)


class MaskingFilter(logging.Filter):
    """Filter that masks sensitive data in log messages.

    Prevents accidental logging of passwords, tokens, API keys, etc.
    """

    # Patterns for sensitive data
    PATTERNS: ClassVar[list[tuple[re.Pattern[str], str]]] = [
        # Passwords in URLs
        (re.compile(r"(://[^:]+:)[^@]+(@)"), r"\1****\2"),
        # API keys and tokens (common formats)
        (re.compile(r"(api[_-]?key[\"']?\s*[:=]\s*[\"']?)[a-zA-Z0-9_-]+"), r"\1****"),
        (re.compile(r"(token[\"']?\s*[:=]\s*[\"']?)[a-zA-Z0-9_.-]+"), r"\1****"),
        (re.compile(r"(bearer\s+)[a-zA-Z0-9_.-]+", re.IGNORECASE), r"\1****"),
        (re.compile(r"(authorization[\"']?\s*[:=]\s*[\"']?)[^\s\"']+"), r"\1****"),
        # Secret keys
        (
            re.compile(r"(secret[_-]?key[\"']?\s*[:=]\s*[\"']?)[a-zA-Z0-9_-]+"),
            r"\1****",
        ),
        # Passwords in JSON/dict
        (re.compile(r"(password[\"']?\s*[:=]\s*[\"']?)[^\"',\s}]+"), r"\1****"),
        # Credit card numbers (basic pattern)
        (re.compile(r"\b(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?)\d{4}\b"), r"\1****"),
        # SSN pattern
        (re.compile(r"\b(\d{3})-(\d{2})-\d{4}\b"), r"\1-\2-****"),
        # Email addresses (partial masking)
        (re.compile(r"([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"), r"***@\2"),
        # AWS keys
        (re.compile(r"(AKIA)[A-Z0-9]{16}"), r"\1****************"),
        # Private keys
        (
            re.compile(
                r"-----BEGIN [A-Z ]+ PRIVATE KEY-----.*?"
                r"-----END [A-Z ]+ PRIVATE KEY-----",
                re.DOTALL,
            ),
            r"[REDACTED PRIVATE KEY]",
        ),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """Apply masking to log record.

        Args:
            record: Log record to filter.

        Returns:
            Always True (record is not filtered out, just modified).
        """
        # Mask the main message
        if record.msg:
            record.msg = self._mask_sensitive_data(str(record.msg))

        # Mask args if present
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: self._mask_sensitive_data(str(v)) for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    self._mask_sensitive_data(str(arg)) for arg in record.args
                )

        return True

    def _mask_sensitive_data(self, text: str) -> str:
        """Apply all masking patterns to text.

        Args:
            text: Text to mask.

        Returns:
            Text with sensitive data masked.
        """
        for pattern, replacement in self.PATTERNS:
            text = pattern.sub(replacement, text)
        return text
