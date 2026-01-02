"""Token usage tracking utilities.

Track and aggregate token usage across AI requests.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from project_name.logging import get_logger


logger = get_logger(__name__)


# Approximate costs per 1M tokens (as of 2024)
MODEL_COSTS: dict[str, dict[str, float]] = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    "text-embedding-3-large": {"input": 0.13, "output": 0.0},
}


@dataclass
class TokenUsageRecord:
    """Record of token usage for a single request.

    Attributes:
        prompt_tokens: Tokens in the prompt.
        completion_tokens: Tokens in the completion.
        total_tokens: Total tokens used.
        model: Model used.
        provider: AI provider name.
        timestamp: When the request was made.
        cost_usd: Estimated cost in USD.
        metadata: Additional metadata.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    provider: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    cost_usd: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Calculate cost after initialization."""
        if self.cost_usd is None and self.model:
            self.cost_usd = self._calculate_cost()

    def _calculate_cost(self) -> float | None:
        """Calculate estimated cost based on model and tokens.

        Returns:
            Estimated cost in USD, or None if model not found.
        """
        # Match model prefix (check longer keys first to avoid partial matches)
        model_key = None
        for key in sorted(MODEL_COSTS.keys(), key=len, reverse=True):
            if self.model.startswith(key):
                model_key = key
                break

        if model_key is None:
            return None

        costs = MODEL_COSTS[model_key]
        input_cost = (self.prompt_tokens / 1_000_000) * costs["input"]
        output_cost = (self.completion_tokens / 1_000_000) * costs["output"]
        return input_cost + output_cost


class TokenTracker:
    """Track token usage across multiple requests.

    Provides aggregation and reporting for token consumption.

    Example:
        >>> tracker = TokenTracker()
        >>> tracker.record(TokenUsageRecord(
        ...     prompt_tokens=100,
        ...     completion_tokens=50,
        ...     model="gpt-4o-mini",
        ...     provider="openai",
        ... ))
        >>> total = tracker.get_total()
        >>> print(f"Total tokens: {total.total_tokens}")
    """

    def __init__(self) -> None:
        """Initialize token tracker."""
        self._records: list[TokenUsageRecord] = []

    def record(self, usage: TokenUsageRecord) -> None:
        """Record token usage from a request.

        Args:
            usage: Token usage record to store.
        """
        self._records.append(usage)
        logger.info(
            "Token usage recorded",
            extra={
                "event_type": "ai_token_usage",
                "model": usage.model,
                "provider": usage.provider,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "cost_usd": usage.cost_usd,
            },
        )

    def get_total(self) -> TokenUsageRecord:
        """Get total aggregated usage across all records.

        Returns:
            Aggregated TokenUsageRecord with totals.
        """
        total_prompt = sum(r.prompt_tokens for r in self._records)
        total_completion = sum(r.completion_tokens for r in self._records)
        total_cost = sum(r.cost_usd or 0.0 for r in self._records)

        return TokenUsageRecord(
            prompt_tokens=total_prompt,
            completion_tokens=total_completion,
            total_tokens=total_prompt + total_completion,
            cost_usd=total_cost if total_cost > 0 else None,
        )

    def get_by_model(self) -> dict[str, TokenUsageRecord]:
        """Get usage aggregated by model.

        Returns:
            Dictionary mapping model names to aggregated usage.
        """
        by_model: dict[str, list[TokenUsageRecord]] = {}
        for record in self._records:
            if record.model not in by_model:
                by_model[record.model] = []
            by_model[record.model].append(record)

        result: dict[str, TokenUsageRecord] = {}
        for model, records in by_model.items():
            total_prompt = sum(r.prompt_tokens for r in records)
            total_completion = sum(r.completion_tokens for r in records)
            total_cost = sum(r.cost_usd or 0.0 for r in records)
            result[model] = TokenUsageRecord(
                prompt_tokens=total_prompt,
                completion_tokens=total_completion,
                total_tokens=total_prompt + total_completion,
                model=model,
                cost_usd=total_cost if total_cost > 0 else None,
            )
        return result

    def clear(self) -> None:
        """Clear all recorded usage."""
        self._records.clear()

    @property
    def record_count(self) -> int:
        """Get number of recorded usages.

        Returns:
            Number of usage records.
        """
        return len(self._records)


# Global tracker instance
_tracker: TokenTracker | None = None


def get_token_tracker() -> TokenTracker:
    """Get the global token tracker instance.

    Returns:
        TokenTracker singleton instance.
    """
    global _tracker  # noqa: PLW0603
    if _tracker is None:
        _tracker = TokenTracker()
    return _tracker
