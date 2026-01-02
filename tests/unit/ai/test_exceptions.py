"""Tests for AI exceptions."""

from project_name.ai.exceptions import (
    AIClientError,
    AuthenticationError,
    ContextLengthExceededError,
    InvalidRequestError,
    ModelNotFoundError,
    RateLimitError,
)


class TestAIClientError:
    """Tests for AIClientError."""

    def test_basic_error(self) -> None:
        """Test basic error creation."""
        error = AIClientError("Something failed")
        assert str(error) == "Something failed"
        assert error.message == "Something failed"
        assert error.provider is None
        assert error.status_code is None

    def test_error_with_details(self) -> None:
        """Test error with provider and status code."""
        error = AIClientError(
            "API error",
            provider="openai",
            status_code=500,
        )

        assert error.provider == "openai"
        assert error.status_code == 500


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_default_message(self) -> None:
        """Test default error message."""
        error = RateLimitError()
        assert error.status_code == 429
        assert "Rate limit" in str(error)

    def test_with_retry_after(self) -> None:
        """Test with retry_after."""
        error = RateLimitError(
            provider="openai",
            retry_after=60.0,
        )

        assert error.retry_after == 60.0
        assert error.provider == "openai"


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_default_message(self) -> None:
        """Test default error message."""
        error = AuthenticationError()
        assert error.status_code == 401
        assert "Authentication" in str(error)


class TestInvalidRequestError:
    """Tests for InvalidRequestError."""

    def test_default_message(self) -> None:
        """Test default error message."""
        error = InvalidRequestError()
        assert error.status_code == 400
        assert "Invalid" in str(error)


class TestModelNotFoundError:
    """Tests for ModelNotFoundError."""

    def test_with_model(self) -> None:
        """Test with model name."""
        error = ModelNotFoundError(
            "Model not found",
            provider="openai",
            model="gpt-5-turbo",
        )

        assert error.status_code == 404
        assert error.model == "gpt-5-turbo"


class TestContextLengthExceededError:
    """Tests for ContextLengthExceededError."""

    def test_with_token_info(self) -> None:
        """Test with token information."""
        error = ContextLengthExceededError(
            "Context too long",
            max_tokens=8192,
            requested_tokens=10000,
        )

        assert error.status_code == 400
        assert error.max_tokens == 8192
        assert error.requested_tokens == 10000
