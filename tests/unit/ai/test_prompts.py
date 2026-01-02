"""Tests for AI prompt templates."""

import pytest

from project_name.ai.prompts.base import (
    EXTRACT_TEMPLATE,
    SUMMARIZE_TEMPLATE,
    TRANSLATE_TEMPLATE,
    PromptTemplate,
    SystemPromptTemplate,
)


class TestPromptTemplate:
    """Tests for PromptTemplate."""

    def test_render_simple(self) -> None:
        """Test simple template rendering."""
        template = PromptTemplate(
            name="greeting",
            template="Hello, {name}!",
            variables=["name"],
        )

        result = template.render(name="Alice")
        assert result == "Hello, Alice!"

    def test_render_multiple_variables(self) -> None:
        """Test template with multiple variables."""
        template = PromptTemplate(
            name="intro",
            template="{greeting}, {name}! Welcome to {place}.",
            variables=["greeting", "name", "place"],
        )

        result = template.render(
            greeting="Hello",
            name="Bob",
            place="Python",
        )
        assert result == "Hello, Bob! Welcome to Python."

    def test_render_missing_variable(self) -> None:
        """Test error on missing variable."""
        template = PromptTemplate(
            name="test",
            template="Hello, {name}!",
            variables=["name"],
        )

        with pytest.raises(ValueError, match="Missing required variables"):
            template.render()

    def test_validate_variables_all_present(self) -> None:
        """Test validation when all variables present."""
        template = PromptTemplate(
            name="test",
            template="{a} {b}",
            variables=["a", "b"],
        )

        missing = template.validate_variables(a="x", b="y")
        assert missing == []

    def test_validate_variables_some_missing(self) -> None:
        """Test validation when variables missing."""
        template = PromptTemplate(
            name="test",
            template="{a} {b}",
            variables=["a", "b"],
        )

        missing = template.validate_variables(a="x")
        assert "b" in missing

    def test_immutable(self) -> None:
        """Test template is immutable."""
        from pydantic import ValidationError  # noqa: PLC0415

        template = PromptTemplate(
            name="test",
            template="Hello",
            variables=[],
        )

        with pytest.raises(ValidationError):
            template.name = "changed"  # type: ignore[misc]


class TestSystemPromptTemplate:
    """Tests for SystemPromptTemplate."""

    def test_with_persona(self) -> None:
        """Test system template with persona."""
        template = SystemPromptTemplate(
            name="assistant",
            template="You are a {role}.",
            variables=["role"],
            persona="helpful",
        )

        assert template.persona == "helpful"
        result = template.render(role="teacher")
        assert result == "You are a teacher."

    def test_with_constraints(self) -> None:
        """Test system template with constraints."""
        template = SystemPromptTemplate(
            name="constrained",
            template="Be {style}.",
            variables=["style"],
            constraints=["Be concise", "Be accurate"],
        )

        assert len(template.constraints) == 2
        assert "Be concise" in template.constraints


class TestBuiltInTemplates:
    """Tests for built-in templates."""

    def test_summarize_template(self) -> None:
        """Test SUMMARIZE_TEMPLATE."""
        result = SUMMARIZE_TEMPLATE.render(
            style="brief",
            text="Long document here...",
        )

        assert "brief" in result
        assert "Long document here..." in result

    def test_extract_template(self) -> None:
        """Test EXTRACT_TEMPLATE."""
        result = EXTRACT_TEMPLATE.render(
            fields="- name\n- email",
            text="Contact info here...",
        )

        assert "name" in result
        assert "email" in result

    def test_translate_template(self) -> None:
        """Test TRANSLATE_TEMPLATE."""
        result = TRANSLATE_TEMPLATE.render(
            language="Spanish",
            text="Hello world",
        )

        assert "Spanish" in result
        assert "Hello world" in result
