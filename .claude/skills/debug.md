# /debug

Intelligently debug issues by analyzing errors, logs, and code patterns.

## Usage

```
/debug [error_message] [--file <file>] [--traceback] [--logs]
```

## Arguments

- `error_message`: Error message or description of the issue
- `--file <file>`: Specific file to analyze
- `--traceback`: Analyze full traceback if available
- `--logs`: Analyze log files for related errors

## Instructions

When this skill is invoked:

1. **Gather context**:
   - Read error message and traceback (if provided)
   - Analyze the file where error occurred
   - Check related files (imports, dependencies)
   - Review recent changes (if available)
   - Check log files if `--logs` is specified

2. **Identify the issue**:
   - Parse error type and message
   - Locate the exact line causing the error
   - Understand the error context
   - Identify root cause (not just symptoms)

3. **Analyze patterns**:
   - Check for common error patterns:
     - `AttributeError`: Missing attribute or None value
     - `TypeError`: Type mismatch or None operation
     - `KeyError`: Missing dictionary key
     - `ValueError`: Invalid value or format
     - `ImportError`: Missing import or circular dependency
     - `AssertionError`: Test failure or assertion issue
   - Look for related issues in similar code
   - Check for type hint mismatches

4. **Provide solution**:
   - Explain the root cause clearly
   - Provide specific fix with code example
   - Suggest defensive programming improvements
   - Recommend tests to prevent regression
   - Include type hints if missing

5. **Verify the fix**:
   - Run tests: `uv run pytest tests/unit/test_<module>.py -v`
   - Check type hints: `uv run mypy src/`
   - Verify the error is resolved

## Common Debug Patterns

### AttributeError: 'NoneType' object has no attribute 'X'

**Analysis:**
- Object is None when attribute is accessed
- Missing None check before attribute access

**Fix:**
```python
# Before (unsafe)
result = await get_user(user_id)
email = result.email  # Error if result is None

# After (safe)
result = await get_user(user_id)
if result is None:
    raise UserNotFoundError(user_id)
email = result.email
```

### TypeError: unsupported operand type(s)

**Analysis:**
- Type mismatch in operation
- Missing type conversion or validation

**Fix:**
```python
# Before
def add_numbers(a, b):
    return a + b  # Error if a or b is None/string

# After
def add_numbers(a: int | float, b: int | float) -> int | float:
    """Add two numbers."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a + b
```

### KeyError: 'key_name'

**Analysis:**
- Dictionary key doesn't exist
- Missing key check or default value

**Fix:**
```python
# Before
value = data["key"]  # Error if key doesn't exist

# After
value = data.get("key", default_value)  # Safe with default
# or
if "key" not in data:
    raise ValueError("Missing required key: 'key'")
value = data["key"]
```

### ImportError / ModuleNotFoundError

**Analysis:**
- Missing dependency or incorrect import path
- Circular import issue

**Fix:**
```python
# Check if dependency is installed
# Run: uv sync

# Check import path
# Use: from project_name.module import Class

# For circular imports, use TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project_name.other import OtherClass
```

## Debug Workflow

1. **Reproduce the error**:
   - Run the failing code
   - Capture full traceback
   - Note the exact error message

2. **Analyze the traceback**:
   - Identify the file and line number
   - Check the call stack
   - Understand the execution flow

3. **Examine the code**:
   - Read the problematic function
   - Check input types and values
   - Verify assumptions about data

4. **Check related code**:
   - Review function calls
   - Check data flow
   - Verify type hints match reality

5. **Apply fix**:
   - Make minimal change to fix issue
   - Add defensive checks if needed
   - Update type hints if incorrect

6. **Test the fix**:
   - Run the code that was failing
   - Run related tests
   - Verify no regressions

## Log Analysis

When `--logs` is specified:
- Read log files (logs/*.log, audit.log)
- Search for related errors
- Check correlation IDs
- Analyze error patterns over time
- Identify common failure points

## Example

```
/debug "AttributeError: 'NoneType' object has no attribute 'email'" --file src/project_name/services/user.py
```

Analyzes the error in `user.py`, identifies where None is returned, and provides a fix with proper None checking.
