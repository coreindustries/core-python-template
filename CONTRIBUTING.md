# Contributing to Core Python Template

Thank you for your interest in contributing! This document outlines the process and standards for contributing to this project.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/core-industries/core-python-template.git
cd core-python-template

# Install dependencies (requires uv)
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Start development services
docker-compose up -d postgres redis

# Verify setup
uv run pytest
```

## Code Standards

This project enforces strict standards. All contributions must pass:

| Check | Command | Requirement |
|-------|---------|-------------|
| Linting | `uv run ruff check src/ tests/` | No errors |
| Formatting | `uv run ruff format --check src/ tests/` | Properly formatted |
| Type checking | `uv run mypy src/` | No type errors |
| Tests | `uv run pytest --cov=src --cov-fail-under=100` | 100% coverage |
| Security | `uv run bandit -r src/` | No high/critical issues |

### Before Submitting

Run all checks:

```bash
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
uv run mypy src/
uv run pytest --cov=src --cov-report=term-missing
uv run bandit -r src/
```

## Pull Request Process

1. **Fork the repository** and create a feature branch from `main`
2. **Make your changes** following the code standards above
3. **Write tests** for any new functionality (100% coverage required)
4. **Update documentation** if adding new features or changing behavior
5. **Submit a PR** using the pull request template

### PR Requirements

- Clear description of what the PR does and why
- All CI checks passing
- Tests for new functionality
- Documentation updates if applicable
- No unrelated changes bundled in

## Types of Contributions

### Bug Fixes

- Open an issue first to discuss the bug
- Reference the issue in your PR
- Include a test that reproduces the bug

### New Features

- Open an issue to discuss the feature before implementing
- For significant features, consider writing a PRD in `prd/`
- Ensure the feature fits the project's scope (AI-assisted Python development)

### Documentation

- Improvements to README, CLAUDE.md, or inline documentation
- New examples or tutorials
- Typo fixes (no issue needed)

### Template Improvements

- New skills (slash commands) in `.claude/skills/`
- Hook improvements in `.claude/settings.json`
- Subagent definitions for common tasks

## What We're Looking For

Contributions that enhance AI-assisted development workflows:

- Better Claude Code integration (hooks, skills, agents)
- Improved PRD templates and standards
- Security enhancements
- Developer experience improvements
- Documentation clarity

## What We're Not Looking For

- Framework changes (staying with FastAPI, Typer, Prisma)
- Loosening of code standards (100% coverage, strict typing)
- Features unrelated to the template's purpose
- Breaking changes without discussion

## Code of Conduct

Be respectful and constructive. We're all here to build better tools for AI-assisted development.

## Questions?

Open an issue with the "question" label or start a discussion.
