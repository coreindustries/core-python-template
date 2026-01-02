#!/bin/bash
# Pre-commit validation hook
# Runs quality checks before allowing commits

set -e

echo "🔍 Running pre-commit checks..."

# Check for sensitive files
SENSITIVE_PATTERNS=(".env" "credentials" "secrets" ".pem" ".key" "password")
STAGED_FILES=$(git diff --cached --name-only)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if echo "$STAGED_FILES" | grep -q "$pattern"; then
        echo "❌ ERROR: Attempting to commit sensitive file matching: $pattern"
        echo "   Remove from staging: git reset HEAD <file>"
        exit 1
    fi
done

# Run ruff check
echo "📋 Running linter..."
if ! uv run ruff check src/ tests/ --quiet; then
    echo "❌ Linting failed. Run: uv run ruff check --fix src/ tests/"
    exit 1
fi

# Run ruff format check
echo "📐 Checking formatting..."
if ! uv run ruff format --check src/ tests/ --quiet; then
    echo "❌ Formatting check failed. Run: uv run ruff format src/ tests/"
    exit 1
fi

# Run mypy
echo "🔍 Running type checker..."
if ! uv run mypy src/ --no-error-summary; then
    echo "❌ Type checking failed. Fix type errors before committing."
    exit 1
fi

# Run tests (quick mode)
echo "🧪 Running tests..."
if ! uv run pytest tests/unit/ -q --tb=no; then
    echo "❌ Tests failed. Fix failing tests before committing."
    exit 1
fi

echo "✅ All pre-commit checks passed!"
