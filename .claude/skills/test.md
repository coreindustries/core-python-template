# /test

Run tests with coverage reporting and quality gates.

## Usage

```
/test [target] [--coverage] [--watch] [--failed] [--verbose]
```

## Arguments

- `target`: Specific test file, directory, or test name (optional)
- `--coverage`: Generate coverage report (default: true)
- `--watch`: Watch mode for continuous testing
- `--failed`: Re-run only failed tests
- `--verbose`: Verbose output

## Instructions

When this skill is invoked:

### Agent Behavior (Codex-Max Pattern)

**Autonomy:**
- Complete test execution and analysis end-to-end
- If tests fail, analyze failures and suggest specific fixes
- If coverage is low, identify missing test cases and offer to implement them
- Don't just report results - provide actionable next steps

**Thoroughness:**
- Run full quality suite, not just tests:
  ```bash
  uv run ruff check src/ tests/        # Linting
  uv run mypy src/                     # Type checking
  uv run pytest --cov=src --cov-fail-under=66  # Tests with coverage
  ```
- Report on all aspects: tests, coverage, linting, type checking

**Problem-Solving:**
- If tests fail:
  1. Show the failure details with file:line references
  2. Analyze the root cause
  3. Suggest or implement the fix
  4. Re-run tests to verify
- If coverage is low:
  1. Identify uncovered lines (show file:line references)
  2. Suggest test cases to add
  3. Offer to implement the missing tests

**Presentation:**
- Lead with overall status (pass/fail, coverage %)
- Group results logically (by test file or category)
- Use file:line references for failures and missing coverage
- Provide clear next steps

### Default Run (All Tests)

1. **Run pytest with coverage**:
   ```bash
   uv run pytest tests/ \
     --cov=src \
     --cov-report=term-missing \
     --cov-report=html:htmlcov \
     --cov-fail-under=100 \
     -v
   ```

2. **Report results**:
   ```
   ==================== Test Results ====================

   ✅ Passed: 42
   ❌ Failed: 0
   ⏭️  Skipped: 2
   ⏱️  Duration: 3.45s

   ==================== Coverage ====================

   Name                              Stmts   Miss  Cover
   -----------------------------------------------------
   src/project_name/__init__.py          2      0   100%
   src/project_name/main.py             45      0   100%
   src/project_name/config.py           32      0   100%
   ...
   -----------------------------------------------------
   TOTAL                               523      0   100%

   ✅ Coverage requirement met (100%)

   📊 HTML report: htmlcov/index.html
   ```

### Specific Target

```bash
# Test a specific file
/test tests/unit/test_config.py

# Test a specific class
/test tests/unit/test_api.py::TestHealthCheck

# Test a specific function
/test tests/unit/test_api.py::test_health_check

# Test a directory
/test tests/integration/
```

### Watch Mode

```bash
uv run pytest-watch tests/ -- --cov=src
```

Or using pytest-xdist:
```bash
uv run pytest tests/ -f  # --looponfail
```

### Failed Tests Only

```bash
uv run pytest --lf  # --last-failed
```

### Coverage Analysis

1. **If coverage < 100%**:
   ```
   ⚠️  Coverage below requirement: 95% (required: 100%)

   Missing coverage in:
   - src/project_name/services/user.py:45-52 (error handling)
   - src/project_name/api/auth.py:78-85 (edge case)

   Suggested tests to add:
   1. Test error handling in UserService.create()
   2. Test authentication timeout scenario
   ```

2. **Generate coverage report**:
   ```bash
   uv run coverage html
   open htmlcov/index.html
   ```

### Integration Tests

When running integration tests:

1. **Check Docker services**:
   ```bash
   docker-compose ps
   ```
   Verify postgres and redis are running.

2. **Run with integration marker**:
   ```bash
   uv run pytest tests/integration/ -m integration
   ```

3. **Database setup**:
   - Tests use a separate test database
   - Auto-cleanup after each test

### Test Categories

Use markers to run specific test types:

```bash
# Unit tests only
uv run pytest -m unit

# Integration tests only
uv run pytest -m integration

# Slow tests excluded
uv run pytest -m "not slow"

# Security-focused tests
uv run pytest -m security
```

### Parallel Execution

For faster test runs:
```bash
uv run pytest -n auto  # Use all CPU cores
uv run pytest -n 4     # Use 4 workers
```

## Quality Gates

The test skill enforces these quality gates:

| Gate | Requirement | Action on Failure |
|------|-------------|-------------------|
| Coverage | 100% | Block merge |
| All tests pass | 0 failures | Block merge |
| No skipped (without reason) | Documented skips only | Warn |
| Performance | No test > 5s | Warn |

## CI Integration

For CI, use:
```bash
uv run pytest tests/ \
  --cov=src \
  --cov-report=xml \
  --cov-fail-under=100 \
  --junitxml=test-results.xml \
  -n auto
```

## Example Output

```
$ /test

🧪 Running tests...

tests/unit/test_config.py::TestSettings::test_default_values PASSED
tests/unit/test_config.py::TestSettings::test_is_development PASSED
tests/unit/test_config.py::TestSettings::test_is_production PASSED
tests/unit/test_api.py::test_health_check PASSED
tests/unit/test_api.py::test_root_endpoint PASSED

==================== 5 passed in 0.45s ====================

📊 Coverage: 100% ✅
📁 HTML Report: htmlcov/index.html
```
