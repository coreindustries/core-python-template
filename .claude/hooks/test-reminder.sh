#!/bin/bash
# Test reminder hook
# Reminds to run tests when source files are changed

FILE="$1"

# Check if it's a Python source file
if [[ "$FILE" == src/*.py ]]; then
    # Check if there's a corresponding test file
    BASENAME=$(basename "$FILE" .py)
    TEST_FILE="tests/unit/test_${BASENAME}.py"

    echo ""
    echo "💡 Source file modified: $FILE"
    echo ""

    if [ -f "$TEST_FILE" ]; then
        echo "   Run related tests:"
        echo "   uv run pytest $TEST_FILE -v"
    else
        echo "   ⚠️  No test file found at: $TEST_FILE"
        echo "   Consider creating tests for this module."
    fi

    echo ""
    echo "   Run all tests:"
    echo "   uv run pytest --cov=src --cov-report=term-missing"
    echo ""
fi
