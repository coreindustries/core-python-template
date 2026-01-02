"""AI client exceptions.

Custom exceptions for AI client operations.
"""


class AIClientError(Exception):
    """Base exception for AI client errors.

    Attributes:
        message: Error message.
        provider: AI provider name.
        status_code: HTTP status code if applicable.
    """

    def __init__(
        self,
        message: str,
        provider: str | None = None,
        status_code: int | None = None,
    ) -> None:
        """Initialize AI client error.

        Args:
            message: Error message.
            provider: AI provider name.
            status_code: HTTP status code if applicable.
        """
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.status_code = status_code


class RateLimitError(AIClientError):
    """Raised when API rate limit is exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        provider: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Error message.
            provider: AI provider name.
            retry_after: Seconds to wait before retrying.
        """
        super().__init__(message, provider, status_code=429)
        self.retry_after = retry_after


class AuthenticationError(AIClientError):
    """Raised when API authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        provider: str | None = None,
    ) -> None:
        """Initialize authentication error.

        Args:
            message: Error message.
            provider: AI provider name.
        """
        super().__init__(message, provider, status_code=401)


class InvalidRequestError(AIClientError):
    """Raised when the request is invalid."""

    def __init__(
        self,
        message: str = "Invalid request",
        provider: str | None = None,
    ) -> None:
        """Initialize invalid request error.

        Args:
            message: Error message.
            provider: AI provider name.
        """
        super().__init__(message, provider, status_code=400)


class ModelNotFoundError(AIClientError):
    """Raised when the requested model is not found."""

    def __init__(
        self,
        message: str = "Model not found",
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize model not found error.

        Args:
            message: Error message.
            provider: AI provider name.
            model: Model name that was not found.
        """
        super().__init__(message, provider, status_code=404)
        self.model = model


class ContextLengthExceededError(AIClientError):
    """Raised when input exceeds model context length."""

    def __init__(
        self,
        message: str = "Context length exceeded",
        provider: str | None = None,
        max_tokens: int | None = None,
        requested_tokens: int | None = None,
    ) -> None:
        """Initialize context length exceeded error.

        Args:
            message: Error message.
            provider: AI provider name.
            max_tokens: Maximum allowed tokens.
            requested_tokens: Tokens in the request.
        """
        super().__init__(message, provider, status_code=400)
        self.max_tokens = max_tokens
        self.requested_tokens = requested_tokens
