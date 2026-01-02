# /review

Review code changes against project standards and best practices.

## Usage

```
/review [target] [--prd <prd_number>] [--security] [--diff]
```

## Arguments

- `target`: File, directory, or git ref to review (default: staged changes)
- `--prd <number>`: Check compliance with specific PRD
- `--security`: Focus on security review
- `--diff`: Review only changed lines (git diff)

## Instructions

When this skill is invoked:

### 1. Gather Changes

```bash
# Staged changes
git diff --cached --name-only

# Or specific target
git diff HEAD~1 --name-only

# Or all uncommitted
git diff --name-only
```

### 2. Read Project Standards

Load and parse:
- `prd/01_Technical_standards.md`
- `prd/02_Tech_stack.md`
- `prd/03_Security.md`
- `CLAUDE.md`

### 3. Review Checklist

For each changed file, check:

#### Code Quality (from PRD 01)
- [ ] Type hints on all functions and attributes
- [ ] Docstrings on all public functions/classes (Google style)
- [ ] DRY principle followed (no code duplication)
- [ ] Naming conventions followed (snake_case, PascalCase)
- [ ] No hardcoded values (use constants/config)
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate

#### Security (from PRD 03)
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS protection (output encoding)
- [ ] Authentication/authorization checks
- [ ] Sensitive data handling (masking in logs)
- [ ] Rate limiting considerations

#### Testing
- [ ] Unit tests added for new code
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Mocks used appropriately

#### Architecture (from PRD 02)
- [ ] Follows project structure
- [ ] Uses approved dependencies
- [ ] Async patterns correct
- [ ] Database operations use Prisma

### 4. Generate Review Report

```markdown
# Code Review Report

**Reviewed:** 5 files
**Reviewer:** Claude Code
**Date:** YYYY-MM-DD

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Code Quality | ⚠️ | 2 |
| Security | ✅ | 0 |
| Testing | ❌ | 1 |
| Architecture | ✅ | 0 |

## Findings

### 🔴 Critical

#### [CR-001] Missing tests for new service
**File:** `src/project_name/services/payment.py`
**Lines:** 1-85
**Standard:** PRD 01, Section 4.1

New service added without corresponding tests. Coverage requirement
is 100%.

**Recommendation:**
Create `tests/unit/test_payment.py` with tests for:
- `PaymentService.process_payment()`
- `PaymentService.refund()`
- Error handling scenarios

---

### 🟡 Warning

#### [CR-002] Missing docstring
**File:** `src/project_name/api/payment.py`
**Line:** 23
**Standard:** PRD 01, Section 3.4

```python
async def process_payment(data: PaymentRequest) -> PaymentResponse:
    # Missing docstring
```

**Recommendation:**
Add Google-style docstring:
```python
async def process_payment(data: PaymentRequest) -> PaymentResponse:
    """Process a payment request.

    Args:
        data: Payment request data.

    Returns:
        Payment response with transaction ID.

    Raises:
        PaymentError: If payment processing fails.
    """
```

---

#### [CR-003] Consider using constant
**File:** `src/project_name/services/payment.py`
**Line:** 45
**Standard:** PRD 01, Section 3.1

```python
if amount > 10000:  # Magic number
```

**Recommendation:**
```python
MAX_PAYMENT_AMOUNT = 10000

if amount > MAX_PAYMENT_AMOUNT:
```

---

### 🟢 Good Practices Observed

- ✅ Proper type hints throughout
- ✅ Consistent naming conventions
- ✅ Appropriate error handling
- ✅ Audit logging for sensitive operations

## Action Items

1. [ ] Add tests for PaymentService (Critical)
2. [ ] Add docstrings to new functions (Warning)
3. [ ] Extract magic numbers to constants (Suggestion)

## Approval Status

❌ **Changes Requested**

Please address critical issues before merging.
```

### 5. Security-Focused Review (--security)

Additional checks:
- OWASP Top 10 vulnerabilities
- Authentication bypass risks
- Authorization flaws
- Cryptographic issues
- Injection vulnerabilities
- Sensitive data exposure

### 6. PRD Compliance Review (--prd)

```bash
/review --prd 04
```

Checks implementation against specific PRD requirements:
- Feature completeness
- API contract compliance
- Data model alignment
- Configuration requirements

## Review Severity Levels

| Level | Icon | Action Required |
|-------|------|-----------------|
| Critical | 🔴 | Must fix before merge |
| Warning | 🟡 | Should fix |
| Suggestion | 🔵 | Consider for improvement |
| Note | ⚪ | Information only |

## Integration

### Pre-PR Review
```bash
/review --diff
```

### Post-Implementation Review
```bash
/review src/project_name/features/new_feature/ --prd 05
```

### Security Audit
```bash
/review --security
```

## Example Output

```
$ /review

🔍 Reviewing changes...

Files changed: 3
- src/project_name/api/payment.py (new)
- src/project_name/services/payment.py (new)
- src/project_name/models/payment.py (new)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Review Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 1 Critical issue
🟡 2 Warnings
🔵 1 Suggestion

See full report above.

❌ Changes requested - please address critical issues.
```
