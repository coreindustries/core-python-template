# /security-scan

Run comprehensive security analysis on the codebase.

## Usage

```
/security-scan [--fix] [--ci]
```

## Arguments

- `--fix`: Attempt to auto-fix issues where possible
- `--ci`: Output in CI-friendly format (JSON)

## Instructions

When this skill is invoked:

1. **Run all security checks in sequence**:

   ### Step 1: Static Security Analysis (Bandit)
   ```bash
   uv run bandit -r src/ -f json -o /tmp/bandit-report.json
   ```
   Parse results and report:
   - HIGH severity issues (must fix)
   - MEDIUM severity issues (should fix)
   - LOW severity issues (consider fixing)

   ### Step 2: Dependency Vulnerability Scan (pip-audit)
   ```bash
   uv run pip-audit --format=json
   ```
   Report:
   - Known vulnerabilities in dependencies
   - Suggested version upgrades
   - CVSS scores where available

   ### Step 3: Security-focused Linting (Ruff)
   ```bash
   uv run ruff check --select=S src/
   ```
   Checks for:
   - S101: Assert usage
   - S102: exec() usage
   - S103: Bad file permissions
   - S104: Binding to all interfaces
   - S105-S107: Hardcoded passwords/secrets
   - S108: Insecure temp file
   - S110: try-except-pass
   - S112: try-except-continue
   - S113: Request without timeout
   - S201-S324: Various security issues

   ### Step 4: Secrets Detection
   ```bash
   uv run detect-secrets scan src/ --all-files
   ```
   Check for:
   - Hardcoded API keys
   - Passwords in code
   - Private keys
   - AWS credentials

   ### Step 5: OWASP Dependency Check (if available)
   ```bash
   # Optional - requires separate installation
   dependency-check --project "project-name" --scan . --format JSON
   ```

2. **Generate Security Report**:

   ```markdown
   # Security Scan Report

   **Scan Date:** YYYY-MM-DD HH:MM:SS
   **Commit:** <current git commit>

   ## Summary

   | Category | Critical | High | Medium | Low |
   |----------|----------|------|--------|-----|
   | Code Issues | X | X | X | X |
   | Dependencies | X | X | X | X |
   | Secrets | X | X | X | X |

   ## Critical Issues (Must Fix)

   ### [ISSUE-001] Hardcoded Secret in config.py:45
   - **Severity:** CRITICAL
   - **Type:** Hardcoded credential
   - **File:** src/project_name/config.py
   - **Line:** 45
   - **Recommendation:** Move to environment variable

   ## High Severity Issues

   ...

   ## Dependency Vulnerabilities

   | Package | Current | Fixed In | CVE | Severity |
   |---------|---------|----------|-----|----------|
   | requests | 2.28.0 | 2.31.0 | CVE-2023-XXXX | HIGH |

   ## Recommendations

   1. Update vulnerable dependencies
   2. Move secrets to environment variables
   3. Add input validation to endpoints

   ## Compliance Status

   - [ ] No critical issues
   - [ ] No high severity issues
   - [ ] No hardcoded secrets
   - [ ] Dependencies up to date
   ```

3. **If `--fix` is specified**:
   - Run `uv run ruff check --fix --select=S src/` for auto-fixable issues
   - Suggest dependency updates with `uv add package@latest`

4. **If `--ci` is specified**:
   - Output JSON format for CI integration
   - Return non-zero exit code if critical/high issues found

5. **Integration with forensic logging**:
   - Log security scan as audit event
   - Include scan results in security event metadata

## Example Output

```
🔒 Security Scan Results
========================

✅ Bandit: 0 critical, 2 medium, 5 low
⚠️  pip-audit: 1 vulnerability found
✅ Ruff Security: All checks passed
✅ Secrets: No secrets detected

📊 Overall: 1 issue requires attention

Run with --fix to auto-fix where possible.
```

## CI Integration

Add to `.github/workflows/ci.yml`:
```yaml
- name: Security Scan
  run: |
    uv run bandit -r src/ -f json -o bandit.json
    uv run pip-audit --format=json > pip-audit.json
    uv run ruff check --select=S src/
```
