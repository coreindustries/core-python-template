#!/bin/bash
# PR description generator hook
# Generates a PR description from commits and changes

set -e

BASE_BRANCH="${1:-main}"
CURRENT_BRANCH=$(git branch --show-current)

echo "📝 Generating PR description for: $CURRENT_BRANCH → $BASE_BRANCH"
echo ""

# Get commits
COMMITS=$(git log "$BASE_BRANCH".."$CURRENT_BRANCH" --oneline)
COMMIT_COUNT=$(echo "$COMMITS" | wc -l | tr -d ' ')

# Get changed files
CHANGED_FILES=$(git diff "$BASE_BRANCH"..."$CURRENT_BRANCH" --name-only)
FILES_COUNT=$(echo "$CHANGED_FILES" | wc -l | tr -d ' ')

# Categorize changes
API_CHANGES=$(echo "$CHANGED_FILES" | grep -c "api/" || echo "0")
MODEL_CHANGES=$(echo "$CHANGED_FILES" | grep -c "models/" || echo "0")
SERVICE_CHANGES=$(echo "$CHANGED_FILES" | grep -c "services/" || echo "0")
TEST_CHANGES=$(echo "$CHANGED_FILES" | grep -c "tests/" || echo "0")
CONFIG_CHANGES=$(echo "$CHANGED_FILES" | grep -c -E "(config|settings|\.env)" || echo "0")

# Generate description
cat << EOF
## Summary

<!-- Describe the changes in this PR -->

## Changes

**$COMMIT_COUNT commits, $FILES_COUNT files changed**

| Category | Files Changed |
|----------|---------------|
| API Routes | $API_CHANGES |
| Models | $MODEL_CHANGES |
| Services | $SERVICE_CHANGES |
| Tests | $TEST_CHANGES |
| Config | $CONFIG_CHANGES |

### Commits

\`\`\`
$COMMITS
\`\`\`

### Files Changed

\`\`\`
$CHANGED_FILES
\`\`\`

## Test Plan

- [ ] Unit tests pass (\`uv run pytest tests/unit/\`)
- [ ] Integration tests pass (\`uv run pytest tests/integration/\`)
- [ ] Coverage maintained at 100%
- [ ] Linting passes (\`uv run ruff check src/\`)
- [ ] Type checking passes (\`uv run mypy src/\`)
- [ ] Security scan clean (\`uv run bandit -r src/\`)

## Checklist

- [ ] Code follows project standards (PRD 01)
- [ ] Documentation updated if needed
- [ ] No hardcoded secrets
- [ ] Error handling is comprehensive
- [ ] Audit logging added for sensitive operations

---
🤖 Generated with Claude Code
EOF
