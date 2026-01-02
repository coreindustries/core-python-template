"""Prompt template base class.

Type-safe prompt templates with variable validation.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PromptTemplate(BaseModel):
    """Base class for prompt templates.

    Provides type-safe variable substitution and validation.

    Example:
        >>> template = PromptTemplate(
        ...     name="greeting",
        ...     template="Hello, {name}! Welcome to {service}.",
        ...     variables=["name", "service"],
        ... )
        >>> rendered = template.render(name="Alice", service="our app")
        >>> print(rendered)
        Hello, Alice! Welcome to our app.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(description="Template name for identification")
    template: str = Field(description="Template string with {variable} placeholders")
    variables: list[str] = Field(
        default_factory=list,
        description="Required variable names",
    )
    description: str | None = Field(
        default=None,
        description="Human-readable description",
    )

    def render(self, **kwargs: Any) -> str:
        """Render the template with provided variables.

        Args:
            **kwargs: Variable values to substitute.

        Returns:
            Rendered template string.

        Raises:
            ValueError: If required variables are missing.
        """
        # Check for missing required variables
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        return self.template.format(**kwargs)

    def validate_variables(self, **kwargs: Any) -> list[str]:
        """Validate that all required variables are provided.

        Args:
            **kwargs: Variable values to validate.

        Returns:
            List of missing variable names (empty if all present).
        """
        return list(set(self.variables) - set(kwargs.keys()))


class SystemPromptTemplate(PromptTemplate):
    """Template specifically for system prompts.

    Includes additional metadata for system prompt context.

    Example:
        >>> system = SystemPromptTemplate(
        ...     name="assistant",
        ...     template="You are a helpful {role} assistant.",
        ...     variables=["role"],
        ...     persona="helpful",
        ... )
    """

    persona: str | None = Field(
        default=None,
        description="AI persona/character description",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Behavioral constraints for the AI",
    )


# Common templates
SUMMARIZE_TEMPLATE = PromptTemplate(
    name="summarize",
    template="Summarize the following text in {style} style:\n\n{text}",
    variables=["style", "text"],
    description="Summarize text with specified style",
)

EXTRACT_TEMPLATE = PromptTemplate(
    name="extract",
    template="Extract the following information:\n{fields}\n\nText:\n{text}",
    variables=["fields", "text"],
    description="Extract structured information from text",
)

TRANSLATE_TEMPLATE = PromptTemplate(
    name="translate",
    template="Translate the following text to {language}:\n\n{text}",
    variables=["language", "text"],
    description="Translate text to specified language",
)
