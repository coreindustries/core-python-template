"""Tests for AI token tracking."""

from project_name.ai.tracking import (
    TokenTracker,
    TokenUsageRecord,
    get_token_tracker,
)


class TestTokenUsageRecord:
    """Tests for TokenUsageRecord."""

    def test_default_values(self) -> None:
        """Test default record values."""
        record = TokenUsageRecord()
        assert record.prompt_tokens == 0
        assert record.completion_tokens == 0
        assert record.total_tokens == 0
        assert record.model == ""
        assert record.provider == ""

    def test_cost_calculation_gpt4o_mini(self) -> None:
        """Test cost calculation for gpt-4o-mini."""
        record = TokenUsageRecord(
            prompt_tokens=1000000,  # 1M tokens for easier calculation
            completion_tokens=1000000,
            model="gpt-4o-mini",
        )

        # gpt-4o-mini: $0.15/1M input, $0.60/1M output
        expected_cost = 0.15 + 0.60  # $0.75 total
        assert record.cost_usd is not None
        assert abs(record.cost_usd - expected_cost) < 0.01

    def test_cost_calculation_unknown_model(self) -> None:
        """Test cost calculation for unknown model returns None."""
        record = TokenUsageRecord(
            prompt_tokens=1000,
            model="unknown-model",
        )
        assert record.cost_usd is None

    def test_metadata(self) -> None:
        """Test record metadata."""
        record = TokenUsageRecord(
            model="gpt-4o-mini",
            metadata={"request_id": "123"},
        )
        assert record.metadata == {"request_id": "123"}


class TestTokenTracker:
    """Tests for TokenTracker."""

    def test_empty_tracker(self) -> None:
        """Test empty tracker."""
        tracker = TokenTracker()
        assert tracker.record_count == 0

        total = tracker.get_total()
        assert total.total_tokens == 0

    def test_record_usage(self) -> None:
        """Test recording token usage."""
        tracker = TokenTracker()

        tracker.record(
            TokenUsageRecord(
                prompt_tokens=100,
                completion_tokens=50,
                total_tokens=150,
                model="gpt-4o-mini",
            )
        )

        assert tracker.record_count == 1

        total = tracker.get_total()
        assert total.prompt_tokens == 100
        assert total.completion_tokens == 50
        assert total.total_tokens == 150

    def test_multiple_records(self) -> None:
        """Test multiple records aggregation."""
        tracker = TokenTracker()

        tracker.record(TokenUsageRecord(prompt_tokens=100, completion_tokens=50))
        tracker.record(TokenUsageRecord(prompt_tokens=200, completion_tokens=100))

        total = tracker.get_total()
        assert total.prompt_tokens == 300
        assert total.completion_tokens == 150
        assert total.total_tokens == 450

    def test_get_by_model(self) -> None:
        """Test aggregation by model."""
        tracker = TokenTracker()

        tracker.record(
            TokenUsageRecord(prompt_tokens=100, model="gpt-4o-mini")
        )
        tracker.record(
            TokenUsageRecord(prompt_tokens=200, model="gpt-4o-mini")
        )
        tracker.record(
            TokenUsageRecord(prompt_tokens=300, model="gpt-4o")
        )

        by_model = tracker.get_by_model()

        assert "gpt-4o-mini" in by_model
        assert by_model["gpt-4o-mini"].prompt_tokens == 300

        assert "gpt-4o" in by_model
        assert by_model["gpt-4o"].prompt_tokens == 300

    def test_clear(self) -> None:
        """Test clearing records."""
        tracker = TokenTracker()

        tracker.record(TokenUsageRecord(prompt_tokens=100))
        assert tracker.record_count == 1

        tracker.clear()
        assert tracker.record_count == 0


class TestGetTokenTracker:
    """Tests for get_token_tracker function."""

    def test_returns_singleton(self) -> None:
        """Test that function returns singleton."""
        tracker1 = get_token_tracker()
        tracker2 = get_token_tracker()
        assert tracker1 is tracker2
