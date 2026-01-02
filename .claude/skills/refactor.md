# /refactor

Safely refactor code while maintaining functionality and test coverage.

## Usage

```
/refactor [target] [--pattern <pattern>] [--dry-run]
```

## Arguments

- `target`: File or directory to refactor (default: current file)
- `--pattern <pattern>`: Specific refactoring pattern to apply:
  - `extract-function`: Extract repeated code into functions
  - `extract-class`: Extract related functions into a class
  - `simplify`: Simplify complex logic
  - `modernize`: Update to modern Python patterns (match, type unions, etc.)
  - `dry`: Apply DRY principle (remove duplication)
- `--dry-run`: Show what would be changed without making changes

## Instructions

When this skill is invoked:

1. **Analyze the target code**:
   - Read the target file(s)
   - Identify code smells: duplication, complexity, outdated patterns
   - Check test coverage for affected code
   - Review related files for context

2. **Detect refactoring opportunities**:
   - **DRY violations**: Repeated code blocks that can be extracted
   - **Complex functions**: Functions with high cyclomatic complexity
   - **Outdated patterns**: Old Python patterns that can be modernized
   - **Long functions**: Functions exceeding 30 lines
   - **Magic numbers**: Hardcoded values that should be constants
   - **Deep nesting**: Nested conditionals that can be simplified

3. **Plan the refactoring**:
   - Identify all affected code paths
   - Ensure tests exist for all paths (if not, suggest creating tests first)
   - Plan extraction of common functionality
   - Identify breaking changes

4. **Execute refactoring** (unless `--dry-run`):
   - Extract common code into reusable functions/classes
   - Simplify complex logic
   - Modernize Python syntax
   - Update type hints if needed
   - Maintain all existing functionality
   - Preserve or improve docstrings

5. **Verify after refactoring**:
   - Run tests: `uv run pytest tests/unit/test_<module>.py -v`
   - Check type hints: `uv run mypy src/`
   - Verify linting: `uv run ruff check src/`
   - Ensure 100% test coverage is maintained

## Refactoring Patterns

### Extract Function

**Before:**
```python
async def process_users(users: list[User]) -> list[ProcessedUser]:
    processed = []
    for user in users:
        # Complex validation logic repeated
        if user.email and "@" in user.email and "." in user.email.split("@")[-1]:
            if user.age and 18 <= user.age <= 120:
                processed.append(ProcessedUser(...))
    return processed
```

**After:**
```python
def is_valid_email(email: str) -> bool:
    """Check if email format is valid."""
    return bool(email and "@" in email and "." in email.split("@")[-1])

def is_valid_age(age: int | None) -> bool:
    """Check if age is within valid range."""
    return bool(age and 18 <= age <= 120)

async def process_users(users: list[User]) -> list[ProcessedUser]:
    """Process users with validation."""
    processed = []
    for user in users:
        if is_valid_email(user.email) and is_valid_age(user.age):
            processed.append(ProcessedUser(...))
    return processed
```

### Extract Class

**Before:**
```python
def validate_user_email(email: str) -> bool:
    # validation logic

def format_user_email(email: str) -> str:
    # formatting logic

def normalize_user_email(email: str) -> str:
    # normalization logic
```

**After:**
```python
class EmailProcessor:
    """Handles email validation, formatting, and normalization."""

    @staticmethod
    def validate(email: str) -> bool:
        """Validate email format."""
        # validation logic

    @staticmethod
    def format(email: str) -> str:
        """Format email address."""
        # formatting logic

    @staticmethod
    def normalize(email: str) -> str:
        """Normalize email address."""
        # normalization logic
```

### Modernize Syntax

**Before:**
```python
from typing import Optional, List, Dict

def get_user(user_id: Optional[str]) -> Optional[Dict[str, str]]:
    if user_id is None:
        return None
    # ...
```

**After:**
```python
def get_user(user_id: str | None) -> dict[str, str] | None:
    if user_id is None:
        return None
    # ...
```

## Safety Checks

Before refactoring:
- ✅ All tests pass
- ✅ 100% test coverage exists
- ✅ Type hints are correct
- ✅ No linting errors

After refactoring:
- ✅ All tests still pass
- ✅ Coverage maintained at 100%
- ✅ No new linting errors
- ✅ Functionality unchanged

## Example

```
/refactor src/project_name/services/user.py --pattern dry
```

Analyzes `user.py` for code duplication and extracts common patterns into reusable functions.
