"""Security audit logging.

Provides structured audit logging for security events and user actions.
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from project_name.logging.context import get_correlation_id, get_request_context


class AuditAction(str, Enum):
    """Standard audit action types for security events."""

    # Authentication
    LOGIN_SUCCESS = "auth.login.success"
    LOGIN_FAILURE = "auth.login.failure"
    LOGOUT = "auth.logout"
    PASSWORD_CHANGE = "auth.password.change"  # noqa: S105  # nosec B105  # pragma: allowlist secret  # Enum value
    PASSWORD_RESET_REQUEST = "auth.password.reset_request"  # noqa: S105  # nosec B105  # pragma: allowlist secret
    PASSWORD_RESET_COMPLETE = "auth.password.reset_complete"  # noqa: S105  # nosec B105  # pragma: allowlist secret
    MFA_ENABLED = "auth.mfa.enabled"
    MFA_DISABLED = "auth.mfa.disabled"
    MFA_CHALLENGE = "auth.mfa.challenge"
    TOKEN_ISSUED = "auth.token.issued"  # noqa: S105  # nosec B105  # pragma: allowlist secret  # Enum value
    TOKEN_REVOKED = "auth.token.revoked"  # noqa: S105  # nosec B105  # pragma: allowlist secret  # Enum value
    TOKEN_REFRESH = "auth.token.refresh"  # noqa: S105  # nosec B105  # pragma: allowlist secret  # Enum value
    SESSION_CREATED = "auth.session.created"
    SESSION_EXPIRED = "auth.session.expired"
    SESSION_INVALIDATED = "auth.session.invalidated"

    # Authorization
    ACCESS_GRANTED = "authz.access.granted"
    ACCESS_DENIED = "authz.access.denied"
    PERMISSION_CHANGED = "authz.permission.changed"
    ROLE_ASSIGNED = "authz.role.assigned"
    ROLE_REMOVED = "authz.role.removed"

    # Data operations
    DATA_CREATE = "data.create"
    DATA_READ = "data.read"
    DATA_UPDATE = "data.update"
    DATA_DELETE = "data.delete"
    DATA_EXPORT = "data.export"
    DATA_IMPORT = "data.import"

    # User management
    USER_CREATE = "user.create"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"
    USER_ACTIVATE = "user.activate"
    USER_DEACTIVATE = "user.deactivate"

    # Security events
    SECURITY_ALERT = "security.alert"
    RATE_LIMIT_EXCEEDED = "security.rate_limit"
    SUSPICIOUS_ACTIVITY = "security.suspicious"
    BRUTE_FORCE_DETECTED = "security.brute_force"
    INVALID_INPUT = "security.invalid_input"
    INJECTION_ATTEMPT = "security.injection"

    # System events
    CONFIG_CHANGE = "system.config.change"
    SERVICE_START = "system.service.start"
    SERVICE_STOP = "system.service.stop"
    HEALTH_CHECK = "system.health_check"

    # API events
    API_REQUEST = "api.request"
    API_RESPONSE = "api.response"
    API_ERROR = "api.error"
    WEBHOOK_SENT = "api.webhook.sent"
    WEBHOOK_RECEIVED = "api.webhook.received"


class SecurityEventSeverity(str, Enum):
    """Severity levels for security events."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class SecurityEvent:
    """Structured security event for audit logging.

    Attributes:
        action: The type of action being logged.
        actor_id: ID of the user/service performing the action.
        actor_type: Type of actor (user, service, system).
        resource_type: Type of resource affected.
        resource_id: ID of the resource affected.
        severity: Severity level of the event.
        outcome: Whether the action succeeded or failed.
        reason: Reason for failure if outcome is failure.
        ip_address: IP address of the actor.
        user_agent: User agent string.
        details: Additional event details.
        metadata: Extra metadata for the event.
    """

    action: AuditAction
    actor_id: str | None = None
    actor_type: str = "user"
    resource_type: str | None = None
    resource_id: str | None = None
    severity: SecurityEventSeverity = SecurityEventSeverity.INFO
    outcome: str = "success"
    reason: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    details: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary for logging.

        Returns:
            Dictionary representation of the event.
        """
        event_dict: dict[str, Any] = {
            "event_type": "security_audit",
            "timestamp": datetime.now(UTC).isoformat(),
            "action": self.action.value,
            "actor": {
                "id": self.actor_id,
                "type": self.actor_type,
            },
            "severity": self.severity.value,
            "outcome": self.outcome,
        }

        # Add correlation ID if available
        correlation_id = get_correlation_id()
        if correlation_id:
            event_dict["correlation_id"] = correlation_id

        # Add request context if available
        request_context = get_request_context()
        if request_context:
            event_dict["request_context"] = request_context

        # Add optional fields
        if self.resource_type or self.resource_id:
            event_dict["resource"] = {
                "type": self.resource_type,
                "id": self.resource_id,
            }

        if self.reason:
            event_dict["reason"] = self.reason

        if self.ip_address:
            event_dict["ip_address"] = self.ip_address

        if self.user_agent:
            event_dict["user_agent"] = self.user_agent

        if self.details:
            event_dict["details"] = self.details

        if self.metadata:
            event_dict["metadata"] = self.metadata

        return event_dict


class AuditLogger:
    """Security audit logger for forensic logging.

    Provides methods for logging security events with structured data.
    Uses a dedicated 'audit' logger that can be configured to write
    to a separate audit log file.
    """

    def __init__(self, logger_name: str = "audit") -> None:
        """Initialize audit logger.

        Args:
            logger_name: Name of the logger to use.
        """
        self._logger = logging.getLogger(logger_name)

    def log_event(self, event: SecurityEvent) -> None:
        """Log a security event.

        Args:
            event: Security event to log.
        """
        level = self._severity_to_level(event.severity)
        self._logger.log(
            level, event.details or event.action.value, extra=event.to_dict()
        )

    def auth_success(
        self,
        user_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        method: str = "password",
        **metadata: Any,
    ) -> None:
        """Log successful authentication.

        Args:
            user_id: ID of the authenticated user.
            ip_address: Client IP address.
            user_agent: Client user agent.
            method: Authentication method used.
            **metadata: Additional metadata.
        """
        self.log_event(
            SecurityEvent(
                action=AuditAction.LOGIN_SUCCESS,
                actor_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details=f"User {user_id} authenticated successfully via {method}",
                metadata={"auth_method": method, **metadata},
            )
        )

    def auth_failure(
        self,
        identifier: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        reason: str = "invalid_credentials",
        **metadata: Any,
    ) -> None:
        """Log failed authentication attempt.

        Args:
            identifier: User identifier attempted (email, username).
            ip_address: Client IP address.
            user_agent: Client user agent.
            reason: Reason for failure.
            **metadata: Additional metadata.
        """
        self.log_event(
            SecurityEvent(
                action=AuditAction.LOGIN_FAILURE,
                actor_id=identifier,
                severity=SecurityEventSeverity.WARNING,
                outcome="failure",
                reason=reason,
                ip_address=ip_address,
                user_agent=user_agent,
                details=f"Authentication failed for {identifier}: {reason}",
                metadata=metadata,
            )
        )

    def access_denied(
        self,
        user_id: str | None,
        resource_type: str,
        resource_id: str | None = None,
        action: str = "access",
        reason: str = "insufficient_permissions",
        **metadata: Any,
    ) -> None:
        """Log access denial.

        Args:
            user_id: ID of the user denied access.
            resource_type: Type of resource.
            resource_id: ID of the resource.
            action: Action that was denied.
            reason: Reason for denial.
            **metadata: Additional metadata.
        """
        self.log_event(
            SecurityEvent(
                action=AuditAction.ACCESS_DENIED,
                actor_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                severity=SecurityEventSeverity.WARNING,
                outcome="failure",
                reason=reason,
                details=f"Access denied: {action} on {resource_type}/{resource_id}",
                metadata={"denied_action": action, **metadata},
            )
        )

    def data_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str | None = None,
        action: AuditAction = AuditAction.DATA_READ,
        **metadata: Any,
    ) -> None:
        """Log data access.

        Args:
            user_id: ID of the user accessing data.
            resource_type: Type of resource accessed.
            resource_id: ID of the resource.
            action: Type of data action.
            **metadata: Additional metadata.
        """
        self.log_event(
            SecurityEvent(
                action=action,
                actor_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                details=(
                    f"Data {action.value.split('.')[-1]}: {resource_type}/{resource_id}"
                ),
                metadata=metadata,
            )
        )

    def security_alert(
        self,
        alert_type: str,
        severity: SecurityEventSeverity = SecurityEventSeverity.WARNING,
        actor_id: str | None = None,
        ip_address: str | None = None,
        details: str | None = None,
        **metadata: Any,
    ) -> None:
        """Log a security alert.

        Args:
            alert_type: Type of security alert.
            severity: Severity of the alert.
            actor_id: ID of the actor involved.
            ip_address: IP address involved.
            details: Alert details.
            **metadata: Additional metadata.
        """
        self.log_event(
            SecurityEvent(
                action=AuditAction.SECURITY_ALERT,
                actor_id=actor_id,
                severity=severity,
                ip_address=ip_address,
                details=details or f"Security alert: {alert_type}",
                metadata={"alert_type": alert_type, **metadata},
            )
        )

    def rate_limit_exceeded(
        self,
        ip_address: str,
        endpoint: str,
        limit: int,
        window: int,
        user_id: str | None = None,
        **metadata: Any,
    ) -> None:
        """Log rate limit exceeded event.

        Args:
            ip_address: Client IP address.
            endpoint: Endpoint that was rate limited.
            limit: Rate limit value.
            window: Time window in seconds.
            user_id: User ID if authenticated.
            **metadata: Additional metadata.
        """
        self.log_event(
            SecurityEvent(
                action=AuditAction.RATE_LIMIT_EXCEEDED,
                actor_id=user_id,
                severity=SecurityEventSeverity.WARNING,
                ip_address=ip_address,
                details=f"Rate limit exceeded: {endpoint} ({limit}/{window}s)",
                metadata={
                    "endpoint": endpoint,
                    "limit": limit,
                    "window": window,
                    **metadata,
                },
            )
        )

    @staticmethod
    def _severity_to_level(severity: SecurityEventSeverity) -> int:
        """Convert severity to logging level.

        Args:
            severity: Security event severity.

        Returns:
            Logging level integer.
        """
        mapping = {
            SecurityEventSeverity.DEBUG: logging.DEBUG,
            SecurityEventSeverity.INFO: logging.INFO,
            SecurityEventSeverity.WARNING: logging.WARNING,
            SecurityEventSeverity.ERROR: logging.ERROR,
            SecurityEventSeverity.CRITICAL: logging.CRITICAL,
        }
        return mapping.get(severity, logging.INFO)


# Global audit logger instance
_audit_logger: AuditLogger | None = None


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance.

    Returns:
        AuditLogger instance.
    """
    global _audit_logger  # noqa: PLW0603
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
