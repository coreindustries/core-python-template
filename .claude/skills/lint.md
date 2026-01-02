# /lint

Run code quality checks including linting, formatting, and type checking.

## Usage

```
/lint [target] [--fix] [--strict]
```

## Arguments

- `target`: Specific file or directory (default: `src/ tests/`)
- `--fix`: Auto-fix issues where possible
- `--strict`: Fail on warnings (for CI)

## Instructions

When this skill is invoked:

### Full Lint Pipeline

Run all checks in sequence:

1. **Ruff Linting**:
   ```bash
   uv run ruff check src/ tests/
   ```

2. **Ruff Formatting Check**:
   ```bash
   uv run ruff format --check src/ tests/
   ```

3. **Type Checking (mypy)**:
   ```bash
   uv run mypy src/
   ```

4. **Report Results**:
   ```
   ==================== Lint Results ====================

   📋 Ruff Linting
   ✅ No issues found

   📐 Ruff Formatting
   ⚠️  2 files need formatting:
      - src/project_name/api/routes.py
      - tests/unit/test_config.py

   🔍 Type Checking (mypy)
   ✅ No type errors

   ==================== Summary ====================
   ✅ Linting: Passed
   ⚠️  Formatting: 2 issues (run with --fix)
   ✅ Type Checking: Passed

   Run '/lint --fix' to auto-fix formatting issues.
   ```

### With --fix Flag

```bash
# Fix linting issues
uv run ruff check --fix src/ tests/

# Fix formatting
uv run ruff format src/ tests/
```

Report what was fixed:
```
🔧 Auto-fixed issues:

Linting:
- src/project_name/api/routes.py: Removed unused import (F401)
- src/project_name/services/user.py: Sorted imports (I001)

Formatting:
- src/project_name/api/routes.py: Reformatted
- tests/unit/test_config.py: Reformatted

✅ All issues fixed!
```

### Specific Checks

Run individual checks:

```bash
# Linting only
uv run ruff check src/

# Formatting only
uv run ruff format --check src/

# Type checking only
uv run mypy src/

# Security rules only
uv run ruff check --select=S src/
```

### Pre-commit Integration

For pre-commit hooks:
```bash
uv run pre-commit run --all-files
```

This runs:
- ruff (linting + formatting)
- mypy
- bandit
- detect-secrets

### Ruff Rules Explained

The project uses these rule sets:

| Code | Category | Description |
|------|----------|-------------|
| E | pycodestyle | Style errors |
| W | pycodestyle | Style warnings |
| F | pyflakes | Logical errors |
| I | isort | Import sorting |
| B | bugbear | Bug risks |
| C4 | comprehensions | Better comprehensions |
| UP | pyupgrade | Modern Python |
| SIM | simplify | Simplifications |
| S | bandit | Security |
| ARG | unused-args | Unused arguments |
| PTH | pathlib | Use pathlib |
| RUF | ruff | Ruff-specific |

### Type Checking Details

mypy is configured with strict mode:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

Common type errors and fixes:

| Error | Fix |
|-------|-----|
| Missing return type | Add `-> ReturnType` |
| Missing parameter type | Add `: ParamType` |
| Incompatible types | Check type compatibility |
| Missing imports | Add type stubs or `# type: ignore` |

### CI Mode (--strict)

For CI pipelines:
```bash
uv run ruff check src/ tests/ --output-format=github
uv run ruff format --check src/ tests/
uv run mypy src/ --no-error-summary
```

Returns non-zero exit code on any issue.

## Quality Standards

From `prd/01_Technical_standards.md`:

- ✅ All functions must have type hints
- ✅ All classes must have docstrings
- ✅ No unused imports
- ✅ Imports sorted (isort)
- ✅ Line length ≤ 88 characters
- ✅ No security issues (bandit rules)

## Example Output

```
$ /lint

🔍 Running code quality checks...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Ruff Linting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All 15 files passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 Ruff Formatting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All files formatted correctly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Type Checking (mypy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Success: no issues found in 15 source files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All checks passed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
