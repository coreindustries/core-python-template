---
prd_version: "1.0"
status: "Active"
last_updated: "2025-01-XX"
---

# 03 – Security Scanning and Code Review

## 1. Purpose

Implement comprehensive security scanning and code review capabilities to identify vulnerabilities in dependencies, detect OWASP Top 10 security violations, and enforce security best practices across Python and Node.js/TypeScript codebases.

Key capabilities:

- Automated vulnerability scanning for Python dependencies (pip/poetry/pyproject.toml).
- Automated vulnerability scanning for Node.js dependencies (package.json, package-lock.json).
- Static code analysis for OWASP Top 10 security violations.
- Security best practices enforcement and reporting.
- Integration with CI/CD pipelines for continuous security monitoring.
- Historical tracking of security issues and remediation status.

## 2. Goals

- **Dependency Security**: Identify known vulnerabilities in all third-party dependencies (Python and Node.js).
- **Code Security**: Detect common security vulnerabilities in application code (SQL injection, XSS, insecure deserialization, etc.).
- **Best Practices**: Enforce security coding standards and best practices.
- **Compliance**: Ensure adherence to OWASP security guidelines.
- **Visibility**: Provide clear reporting and dashboards for security posture.
- **Automation**: Integrate security checks into development workflow and CI/CD pipelines.

## 3. Key Concepts

- **Vulnerability Scan** – automated check of dependencies against known vulnerability databases (CVE, GitHub Advisory, etc.).
- **Security Issue** – a detected vulnerability or security violation in code or dependencies.
- **Security Report** – aggregated results of security scans for a project or scan.
- **Remediation** – action taken to fix or mitigate a security issue.
- **Security Score** – quantitative measure of security posture (0-100).

## 4. Functional Requirements

### FR1 – Python Dependency Vulnerability Scanning

- Scan Python dependencies from:
  - `pyproject.toml` files (Poetry/pip projects).
  - `requirements.txt` files.
  - `setup.py` files.
  - `Pipfile` and `Pipfile.lock` files.
- Check dependencies against vulnerability databases:
  - **Safety DB** (PyUp Safety).
  - **GitHub Advisory Database**.
  - **OSV (Open Source Vulnerabilities)**.
  - **CVE database**.
- Detect:
  - Known CVEs affecting specific package versions.
  - Outdated packages with security patches available.
  - Packages with known security issues but no fixes available.
- Report:
  - Package name and version.
  - Vulnerability ID (CVE, GHSA, etc.).
  - Severity (Critical, High, Medium, Low).
  - Description and impact.
  - Remediation recommendations (upgrade path, workarounds).
  - Affected file locations.

### FR2 – Node.js Dependency Vulnerability Scanning

- Scan Node.js dependencies from:
  - `package.json` files.
  - `package-lock.json` files.
  - `yarn.lock` files.
  - `pnpm-lock.yaml` files.
- Check dependencies against vulnerability databases:
  - **npm audit** (npm's built-in vulnerability scanner).
  - **GitHub Advisory Database**.
  - **Snyk Vulnerability Database**.
  - **OSV (Open Source Vulnerabilities)**.
- Detect:
  - Known CVEs affecting specific package versions.
  - Outdated packages with security patches available.
  - Packages with known security issues but no fixes available.
  - Transitive dependency vulnerabilities.
- Report:
  - Package name and version.
  - Vulnerability ID (CVE, GHSA, etc.).
  - Severity (Critical, High, Medium, Low).
  - Description and impact.
  - Remediation recommendations (upgrade path, workarounds).
  - Dependency tree path (for transitive vulnerabilities).
  - Affected file locations.

### FR3 – OWASP Security Violation Detection

- Perform static code analysis to detect OWASP Top 10 violations with language-specific best practices:

  1. **A01:2021 – Broken Access Control**

     **Python Best Practices:**

     - Use decorators for route-level authorization (e.g., Flask-Login, Django permissions).
     - Implement role-based access control (RBAC) middleware.
     - Validate user permissions before data access.
     - Use parameterized queries with user context validation.
     - Avoid exposing internal IDs or direct object references.

     **Node.js/TypeScript Best Practices:**

     - Implement middleware for route protection (e.g., Express middleware, NestJS guards).
     - Use JWT claims for authorization, not just authentication.
     - Validate user permissions at the API layer.
     - Implement resource-level access control checks.
     - Use parameterized queries with user context.

     **Detection:**

     - Missing authentication/authorization checks on endpoints.
     - Insecure direct object references (IDOR vulnerabilities).
     - Missing function-level access control.
     - Privilege escalation vulnerabilities.
     - Missing authorization checks in API routes.

  2. **A02:2021 – Cryptographic Failures**

     **Python Best Practices:**

     - Use `cryptography` library for encryption (not `pycrypto`).
     - Use `secrets` module for random number generation (not `random`).
     - Use `bcrypt` or `argon2` for password hashing (not MD5/SHA1).
     - Store secrets in environment variables or secret management systems.
     - Use TLS 1.2+ for all external communications.
     - Encrypt sensitive data at rest.

     **Node.js/TypeScript Best Practices:**

     - Use `crypto` module for encryption (prefer `crypto.createCipheriv` with AES-256-GCM).
     - Use `crypto.randomBytes()` for secure random generation.
     - Use `bcrypt` or `argon2` for password hashing (never MD5/SHA1).
     - Store secrets in environment variables or secret management (AWS Secrets Manager, HashiCorp Vault).
     - Enforce HTTPS/TLS 1.2+ for all connections.
     - Use secure cookie flags (HttpOnly, Secure, SameSite).

     **Detection:**

     - Use of weak encryption algorithms (DES, MD5, SHA1, RC4).
     - Hardcoded secrets and credentials in code.
     - Insecure random number generation (`random` module in Python, `Math.random()` in JS).
     - Missing HTTPS/TLS enforcement.
     - Plaintext storage of sensitive data.

  3. **A03:2021 – Injection**

     **Python Best Practices:**

     - Use parameterized queries with ORMs (SQLAlchemy, Django ORM).
     - Use prepared statements for raw SQL queries.
     - Validate and sanitize all user inputs.
     - Use input validation libraries (e.g., `pydantic`, `marshmallow`).
     - Escape shell commands or use `subprocess` with argument lists.
     - Use NoSQL query builders that prevent injection.

     **Node.js/TypeScript Best Practices:**

     - Use parameterized queries with ORMs (TypeORM, Prisma, Sequelize).
     - Use prepared statements for raw SQL queries.
     - Validate inputs with schemas (Zod, Joi, Yup).
     - Sanitize user inputs before processing.
     - Use `child_process.execFile()` instead of `exec()` for shell commands.
     - Escape NoSQL queries or use query builders.

     **Detection:**

     - SQL injection vulnerabilities (string concatenation in queries).
     - Command injection vulnerabilities (unsafe shell execution).
     - NoSQL injection vulnerabilities (unsanitized user input in queries).
     - LDAP injection vulnerabilities.
     - XPath injection vulnerabilities.
     - Template injection vulnerabilities (Jinja2, EJS, etc.).

  4. **A04:2021 – Insecure Design**

     **Python Best Practices:**

     - Implement security by design principles.
     - Use secure defaults in frameworks (Django security middleware, Flask security extensions).
     - Implement comprehensive input validation at API boundaries.
     - Use threat modeling during design phase.
     - Implement rate limiting and throttling.
     - Design with least privilege principle.

     **Node.js/TypeScript Best Practices:**

     - Implement security by design principles.
     - Use secure defaults (Helmet.js for Express, NestJS security features).
     - Implement input validation at API boundaries.
     - Use rate limiting middleware (express-rate-limit, @nestjs/throttler).
     - Implement request size limits.
     - Design with least privilege principle.

     **Detection:**

     - Missing security controls in application design.
     - Insecure default configurations.
     - Missing input validation at boundaries.
     - Missing rate limiting.
     - Missing request size limits.

  5. **A05:2021 – Security Misconfiguration**

     **Python Best Practices:**

     - Remove default credentials and change admin passwords.
     - Configure security headers (Django security middleware, Flask-Talisman).
     - Exclude sensitive files from version control (`.env`, `.git`, `*.key`).
     - Use environment-specific configurations.
     - Disable debug mode in production.
     - Configure CORS properly (allow specific origins, not `*`).

     **Node.js/TypeScript Best Practices:**

     - Remove default credentials and change admin passwords.
     - Use Helmet.js for security headers.
     - Exclude sensitive files from version control (`.env`, `.git`, `*.key`).
     - Use environment-specific configurations.
     - Disable debug/verbose logging in production.
     - Configure CORS properly (specific origins, credentials handling).

     **Detection:**

     - Default credentials in code or configuration.
     - Missing security headers (CSP, X-Frame-Options, HSTS, etc.).
     - Exposed sensitive files (`.env`, `.git`, credentials files).
     - Insecure CORS configurations (`Access-Control-Allow-Origin: *`).
     - Debug mode enabled in production.
     - Verbose error messages exposing system information.

  6. **A06:2021 – Vulnerable and Outdated Components**

     - Covered by FR1 and FR2 (dependency scanning).
     - Additionally detect:
       - Outdated framework versions.
       - Known vulnerable patterns in dependencies.
       - Abandoned or unmaintained packages.

  7. **A07:2021 – Identification and Authentication Failures**

     **Python Best Practices:**

     - Enforce strong password policies (minimum length, complexity).
     - Implement password strength validation.
     - Use secure session management (secure cookies, session expiration).
     - Implement multi-factor authentication (MFA).
     - Protect against brute force attacks (rate limiting, account lockout).
     - Use secure password reset flows (time-limited tokens).
     - Implement session fixation protection.

     **Node.js/TypeScript Best Practices:**

     - Enforce strong password policies (minimum length, complexity).
     - Implement password strength validation.
     - Use secure session management (httpOnly, secure cookies, expiration).
     - Implement multi-factor authentication (MFA).
     - Protect against brute force attacks (rate limiting, account lockout).
     - Use secure password reset flows (time-limited tokens).
     - Implement session fixation protection.
     - Use JWT with short expiration times and refresh tokens.

     **Detection:**

     - Weak password policies (short passwords, no complexity requirements).
     - Session fixation vulnerabilities.
     - Missing multi-factor authentication.
     - Insecure session management (predictable session IDs, no expiration).
     - Missing brute force protection.
     - Insecure password reset flows.

  8. **A08:2021 – Software and Data Integrity Failures**

     **Python Best Practices:**

     - Avoid insecure deserialization (use JSON instead of pickle for untrusted data).
     - Validate data integrity with checksums or signatures.
     - Use dependency pinning and lock files.
     - Verify package signatures when installing dependencies.
     - Implement CI/CD pipeline security (signed commits, protected branches).
     - Use dependency verification tools.

     **Node.js/TypeScript Best Practices:**

     - Avoid insecure deserialization (use JSON.parse, avoid `eval()`).
     - Validate data integrity with checksums or signatures.
     - Use dependency lock files (`package-lock.json`, `yarn.lock`).
     - Verify package integrity (npm audit, yarn audit).
     - Implement CI/CD pipeline security (signed commits, protected branches).
     - Use dependency verification tools.
     - Avoid `eval()` and `Function()` constructors with user input.

     **Detection:**

     - Insecure deserialization (pickle in Python, `eval()` in JavaScript).
     - Missing integrity checks on data or dependencies.
     - Insecure CI/CD pipelines (unprotected branches, unsigned commits).
     - Missing dependency verification.

  9. **A09:2021 – Security Logging and Monitoring Failures**

     **Python Best Practices:**

     - Log all authentication attempts (success and failure).
     - Log authorization failures and access control violations.
     - Log security-relevant events (data access, configuration changes).
     - Implement log monitoring and alerting.
     - Use structured logging (JSON format).
     - Protect log files from unauthorized access.
     - Implement log retention policies.

     **Node.js/TypeScript Best Practices:**

     - Log all authentication attempts (success and failure).
     - Log authorization failures and access control violations.
     - Log security-relevant events (data access, configuration changes).
     - Implement log monitoring and alerting (Winston, Pino with monitoring integration).
     - Use structured logging (JSON format).
     - Protect log files from unauthorized access.
     - Implement log retention policies.

     **Detection:**

     - Missing security event logging.
     - Insufficient log monitoring.
     - Missing alerting for security events.
     - Logs not protected from tampering.
     - Missing log retention policies.

  10. **A10:2021 – Server-Side Request Forgery (SSRF)**

      **Python Best Practices:**

  - Validate and whitelist allowed URLs/domains.
  - Use URL parsing libraries to validate URLs.
  - Block access to private/internal IP ranges.
  - Use outbound proxy with restrictions.
  - Implement request timeouts.
  - Validate response content types.

  **Node.js/TypeScript Best Practices:**

  - Validate and whitelist allowed URLs/domains.
  - Use URL parsing libraries (`url` module, `whatwg-url`).
  - Block access to private/internal IP ranges (127.0.0.1, 10.x.x.x, 192.168.x.x).
  - Use outbound proxy with restrictions.
  - Implement request timeouts.
  - Validate response content types.
  - Use libraries like `ssrf-filter` for protection.

  **Detection:**

  - Unvalidated user-controlled URLs in HTTP requests.
  - Missing URL validation.
  - Insecure internal network access.
  - Missing IP address filtering.

- **Language Support:**

  - Python (using Bandit, Semgrep, Pylint security plugins).
  - TypeScript/JavaScript (using ESLint security plugins, Semgrep, Snyk Code).
  - SQL (using SQLFluff security rules).

- **Reporting:**
  - Violation type (OWASP category and specific vulnerability).
  - Severity (Critical, High, Medium, Low).
  - File path and line numbers.
  - Code snippet with context.
  - Description and impact.
  - Language-specific remediation guidance with code examples.

### FR4 – Security Best Practices Review

- Enforce security coding standards with language-specific guidance:

  - **Secrets Management**

    **Python Best Practices:**

    - Use environment variables with `python-dotenv` or `python-decouple`.
    - Use secret management services (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault).
    - Never commit `.env` files or hardcode secrets.
    - Use `python-keyring` for secure credential storage.
    - Rotate secrets regularly.
    - Use different secrets for different environments.

    **Node.js/TypeScript Best Practices:**

    - Use environment variables with `dotenv` package.
    - Use secret management services (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault).
    - Never commit `.env` files or hardcode secrets.
    - Use `keytar` for secure credential storage on desktop apps.
    - Rotate secrets regularly.
    - Use different secrets for different environments.

    **Detection:**

    - Hardcoded API keys, passwords, tokens in source code.
    - Secrets in environment variables without proper protection.
    - Secrets committed to version control.
    - Common secret patterns (AWS keys, database passwords, JWT secrets).

  - **Input Validation**

    **Python Best Practices:**

    - Use validation libraries (`pydantic`, `marshmallow`, `cerberus`).
    - Validate all user inputs at API boundaries.
    - Sanitize inputs before processing.
    - Use parameterized queries to prevent injection.
    - Validate file uploads (type, size, content).
    - Use HTML escaping for output (`html.escape`, `markupsafe`).

    **Node.js/TypeScript Best Practices:**

    - Use validation libraries (`Zod`, `Joi`, `Yup`, `class-validator`).
    - Validate all user inputs at API boundaries.
    - Sanitize inputs before processing (`validator.js`, `sanitize-html`).
    - Use parameterized queries to prevent injection.
    - Validate file uploads (type, size, content).
    - Use output encoding for HTML (`he`, `sanitize-html`).

    **Detection:**

    - Missing input sanitization.
    - Insufficient input validation.
    - Missing output encoding.
    - Direct use of user input in queries or commands.

  - **Error Handling**

    **Python Best Practices:**

    - Log errors with appropriate detail (use structured logging).
    - Don't expose stack traces to end users.
    - Use generic error messages for users.
    - Log security-relevant errors (authentication failures, authorization violations).
    - Use exception handling appropriately (don't catch-all silently).

    **Node.js/TypeScript Best Practices:**

    - Log errors with appropriate detail (use structured logging with Winston/Pino).
    - Don't expose stack traces to end users.
    - Use generic error messages for users.
    - Log security-relevant errors (authentication failures, authorization violations).
    - Use error handling appropriately (don't catch-all silently).
    - Implement error boundaries in React applications.

    **Detection:**

    - Information disclosure in error messages.
    - Stack traces exposed to users.
    - Missing error logging.
    - Overly verbose error messages revealing system internals.

  - **Authentication & Authorization**

    **Python Best Practices:**

    - Use established authentication libraries (Django Auth, Flask-Login, FastAPI Security).
    - Enforce strong password policies (minimum length, complexity).
    - Implement rate limiting for login attempts.
    - Use secure session management (secure cookies, expiration).
    - Implement CSRF protection (Django CSRF middleware, Flask-WTF).
    - Use JWT with short expiration times and refresh tokens.
    - Implement multi-factor authentication (MFA).

    **Node.js/TypeScript Best Practices:**

    - Use established authentication libraries (`passport.js`, `next-auth`, `@nestjs/passport`).
    - Enforce strong password policies (minimum length, complexity).
    - Implement rate limiting for login attempts (`express-rate-limit`, `@nestjs/throttler`).
    - Use secure session management (httpOnly, secure cookies, expiration).
    - Implement CSRF protection (`csurf`, `@nestjs/csrf`).
    - Use JWT with short expiration times and refresh tokens.
    - Implement multi-factor authentication (MFA).

    **Detection:**

    - Weak password requirements.
    - Missing rate limiting on authentication endpoints.
    - Insecure session management.
    - Missing CSRF protection.
    - Missing MFA implementation.

  - **Data Protection**

    **Python Best Practices:**

    - Encrypt sensitive data at rest (use `cryptography` library).
    - Use secure data storage (encrypted databases, secure file storage).
    - Implement data retention policies.
    - Use secure data transmission (TLS/SSL).
    - Implement data masking for logs and debugging.
    - Use secure deletion for sensitive data.

    **Node.js/TypeScript Best Practices:**

    - Encrypt sensitive data at rest (use `crypto` module or libraries).
    - Use secure data storage (encrypted databases, secure file storage).
    - Implement data retention policies.
    - Use secure data transmission (TLS/SSL).
    - Implement data masking for logs and debugging.
    - Use secure deletion for sensitive data.

    **Detection:**

    - Missing encryption for sensitive data.
    - Insecure data storage.
    - Missing data retention policies.
    - Plaintext storage of sensitive information.

  - **API Security**

    **Python Best Practices:**

    - Implement API authentication (API keys, OAuth2, JWT).
    - Use rate limiting (`flask-limiter`, Django rate limiting).
    - Validate all API requests.
    - Use HTTPS for all API endpoints.
    - Implement request signing for sensitive operations.
    - Use API versioning.
    - Implement proper CORS policies.

    **Node.js/TypeScript Best Practices:**

    - Implement API authentication (API keys, OAuth2, JWT).
    - Use rate limiting (`express-rate-limit`, `@nestjs/throttler`).
    - Validate all API requests (use validation middleware).
    - Use HTTPS for all API endpoints.
    - Implement request signing for sensitive operations.
    - Use API versioning.
    - Implement proper CORS policies.

    **Detection:**

    - Missing API authentication.
    - Insufficient rate limiting.
    - Missing request validation.
    - Insecure API endpoints (HTTP instead of HTTPS).
    - Overly permissive CORS policies.

  - **Configuration Security**

    **Python Best Practices:**

    - Use secure default configurations.
    - Remove debug mode in production.
    - Configure security headers (Django security middleware, Flask-Talisman).
    - Disable unnecessary features and endpoints.
    - Use environment-specific configurations.
    - Secure configuration file access.

    **Node.js/TypeScript Best Practices:**

    - Use secure default configurations.
    - Remove debug/verbose logging in production.
    - Configure security headers (Helmet.js).
    - Disable unnecessary features and endpoints.
    - Use environment-specific configurations.
    - Secure configuration file access.

    **Detection:**

    - Insecure default configurations.
    - Missing security headers.
    - Exposed debug endpoints.
    - Debug mode enabled in production.
    - Verbose logging in production.

- **Reporting:**
  - Best practice violation type.
  - Severity (Critical, High, Medium, Low, Info).
  - File path and line numbers.
  - Code snippet with context.
  - Description and recommended fix.
  - Language-specific remediation examples.

### FR5 – Security Reporting and Dashboard

- Generate security reports for:
  - Individual scans (vulnerabilities found during a scan).
  - Projects (aggregated security posture).
  - Historical trends (security score over time).
- Report metrics:
  - Total vulnerabilities by severity.
  - Vulnerabilities by type (dependency, OWASP violation, best practice).
  - Security score (0-100).
  - Remediation progress.
  - Time to remediation.
- Dashboard features:
  - Security score visualization.
  - Vulnerability trend charts.
  - Top vulnerabilities list.
  - Remediation status.
  - Compliance status (OWASP Top 10 coverage).

### FR6 – CI/CD Integration

- Integrate security scans into CI/CD pipelines:
  - Run dependency scans on every build.
  - Run code security scans on pull requests.
  - Block deployments if critical vulnerabilities are found (configurable).
  - Generate security reports as build artifacts.
- Support for:
  - GitHub Actions.
  - GitLab CI/CD.
  - Jenkins.
  - CircleCI.
  - Generic webhook triggers.

## 5. Technical Implementation

### 5.1 Python Dependency Scanning Service

**Technology Stack:**

- Use **Safety** (PyUp Safety) for Python vulnerability scanning.
- Use **pip-audit** (Python Packaging Authority) as alternative/additional scanner.
- Use **OSV.dev API** for comprehensive vulnerability database queries.

**Implementation:**

Create a new service: `services/security-scanner/`

```python
# services/security-scanner/src/python_scanner.py
from typing import List, Dict
import subprocess
import json
from pathlib import Path

class PythonDependencyScanner:
    """Scans Python dependencies for known vulnerabilities."""

    def scan_pyproject(self, pyproject_path: Path) -> List[Dict]:
        """Scan pyproject.toml for vulnerabilities."""
        # Extract dependencies from pyproject.toml
        # Run safety check or pip-audit
        # Return list of vulnerabilities
        pass

    def scan_requirements(self, requirements_path: Path) -> List[Dict]:
        """Scan requirements.txt for vulnerabilities."""
        pass

    def get_vulnerability_details(self, package: str, version: str) -> Dict:
        """Query OSV API for vulnerability details."""
        pass
```

**Dependencies:**

- `safety` (PyUp Safety CLI).
- `pip-audit` (Pip-audit).
- `requests` (for OSV API queries).

### 5.2 Node.js Dependency Scanning Service

**Technology Stack:**

- Use **npm audit** (built-in npm vulnerability scanner).
- Use **yarn audit** for Yarn projects.
- Use **pnpm audit** for pnpm projects.
- Use **Snyk** (via CLI or API) for comprehensive scanning.
- Use **GitHub Advisory API** for additional vulnerability data.
- Use **OSV.dev API** for comprehensive vulnerability database queries.

**Implementation:**

**Python Implementation:**

```python
# services/security-scanner/src/node_scanner.py
from typing import List, Dict
import subprocess
import json
from pathlib import Path

class NodeDependencyScanner:
    """Scans Node.js dependencies for known vulnerabilities."""

    def scan_package_json(self, package_json_path: Path) -> List[Dict]:
        """Scan package.json for vulnerabilities using npm audit."""
        # Run: npm audit --json
        # Parse results and return vulnerabilities
        pass

    def scan_with_snyk(self, project_path: Path) -> List[Dict]:
        """Scan using Snyk CLI (if configured)."""
        pass

    def get_vulnerability_details(self, package: str, version: str) -> Dict:
        """Query GitHub Advisory API or OSV API for vulnerability details."""
        pass
```

**Node.js/TypeScript Implementation:**

```typescript
// services/security-scanner/src/node_scanner.ts
import { exec } from "child_process";
import { promisify } from "util";
import { readFile } from "fs/promises";
import { join } from "path";

const execAsync = promisify(exec);

interface Vulnerability {
  package: string;
  version: string;
  vulnerabilityId: string;
  severity: "critical" | "high" | "medium" | "low";
  description: string;
  remediation?: string;
}

export class NodeDependencyScanner {
  /**
   * Scans package.json for vulnerabilities using npm audit.
   */
  async scanPackageJson(packageJsonPath: string): Promise<Vulnerability[]> {
    // Run: npm audit --json
    // Parse results and return vulnerabilities
    const { stdout } = await execAsync("npm audit --json", {
      cwd: packageJsonPath,
    });
    return this.parseAuditResults(JSON.parse(stdout));
  }

  /**
   * Scan using Snyk CLI (if configured).
   */
  async scanWithSnyk(projectPath: string): Promise<Vulnerability[]> {
    // Run: snyk test --json
    // Parse results and return vulnerabilities
    const { stdout } = await execAsync("snyk test --json", {
      cwd: projectPath,
    });
    return this.parseSnykResults(JSON.parse(stdout));
  }

  /**
   * Query GitHub Advisory API or OSV API for vulnerability details.
   */
  async getVulnerabilityDetails(
    packageName: string,
    version: string
  ): Promise<Record<string, unknown>> {
    // Query OSV API: https://api.osv.dev/v1/query
    // or GitHub Advisory API
    // Return detailed vulnerability information
    return {};
  }

  private parseAuditResults(auditOutput: any): Vulnerability[] {
    // Parse npm audit JSON output
    return [];
  }

  private parseSnykResults(snykOutput: any): Vulnerability[] {
    // Parse Snyk JSON output
    return [];
  }
}
```

**Dependencies:**

- `npm`, `yarn`, or `pnpm` (for package manager audit commands).
- `snyk` CLI (optional, for enhanced scanning).
- `node-fetch` or `axios` (for API queries in Node.js implementation).

### 5.3 OWASP Security Violation Scanner

**Technology Stack:**

- Use **Semgrep** for multi-language static analysis (Python, TypeScript, JavaScript).
- Use **Bandit** for Python-specific security scanning.
- Use **ESLint** with security plugins (`eslint-plugin-security`, `eslint-plugin-node`) for TypeScript/JavaScript.
- Use **Snyk Code** for additional security analysis (supports both Python and Node.js).
- Use **SQLFluff** with security rules for SQL.

**Implementation:**

**Python Implementation:**

```python
# services/security-scanner/src/owasp_scanner.py
from typing import List, Dict
import subprocess
import json
from pathlib import Path

class OWASPScanner:
    """Scans code for OWASP Top 10 violations."""

    def scan_python(self, codebase_path: Path) -> List[Dict]:
        """Scan Python code using Bandit and Semgrep."""
        # Run Bandit: bandit -r . -f json
        # Run Semgrep: semgrep --config=auto --json
        # Merge results and categorize by OWASP Top 10
        findings = []
        findings.extend(self._run_bandit(codebase_path))
        findings.extend(self._run_semgrep(codebase_path, "python"))
        return self.categorize_by_owasp(findings)

    def scan_typescript(self, codebase_path: Path) -> List[Dict]:
        """Scan TypeScript/JavaScript code using ESLint and Semgrep."""
        # Run ESLint with security plugins
        # Run Semgrep
        # Merge results
        findings = []
        findings.extend(self._run_eslint(codebase_path))
        findings.extend(self._run_semgrep(codebase_path, "typescript"))
        return self.categorize_by_owasp(findings)

    def scan_sql(self, sql_files: List[Path]) -> List[Dict]:
        """Scan SQL files for injection vulnerabilities."""
        pass

    def categorize_by_owasp(self, findings: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize findings by OWASP Top 10 categories."""
        categorized = {}
        for finding in findings:
            category = self._map_to_owasp_category(finding)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(finding)
        return categorized

    def _run_bandit(self, path: Path) -> List[Dict]:
        # Implementation for Bandit scanning
        pass

    def _run_semgrep(self, path: Path, language: str) -> List[Dict]:
        # Implementation for Semgrep scanning
        pass

    def _run_eslint(self, path: Path) -> List[Dict]:
        # Implementation for ESLint scanning
        pass

    def _map_to_owasp_category(self, finding: Dict) -> str:
        # Map finding to OWASP Top 10 category
        pass
```

**Node.js/TypeScript Implementation:**

```typescript
// services/security-scanner/src/owasp_scanner.ts
import { exec } from "child_process";
import { promisify } from "util";
import { readdir, stat } from "fs/promises";
import { join } from "path";

const execAsync = promisify(exec);

interface SecurityFinding {
  rule: string;
  severity: "critical" | "high" | "medium" | "low";
  file: string;
  line: number;
  message: string;
  owaspCategory: string;
}

export class OWASPScanner {
  /**
   * Scans Python code using Bandit and Semgrep.
   */
  async scanPython(codebasePath: string): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = [];
    findings.push(...(await this.runBandit(codebasePath)));
    findings.push(...(await this.runSemgrep(codebasePath, "python")));
    return this.categorizeByOwasp(findings);
  }

  /**
   * Scans TypeScript/JavaScript code using ESLint and Semgrep.
   */
  async scanTypeScript(codebasePath: string): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = [];
    findings.push(...(await this.runEslint(codebasePath)));
    findings.push(...(await this.runSemgrep(codebasePath, "typescript")));
    return this.categorizeByOwasp(findings);
  }

  /**
   * Scans SQL files for injection vulnerabilities.
   */
  async scanSql(sqlFiles: string[]): Promise<SecurityFinding[]> {
    // Implementation for SQL scanning
    return [];
  }

  /**
   * Categorizes findings by OWASP Top 10 categories.
   */
  private categorizeByOwasp(
    findings: SecurityFinding[]
  ): Record<string, SecurityFinding[]> {
    const categorized: Record<string, SecurityFinding[]> = {};
    for (const finding of findings) {
      const category = finding.owaspCategory;
      if (!categorized[category]) {
        categorized[category] = [];
      }
      categorized[category].push(finding);
    }
    return categorized;
  }

  private async runBandit(path: string): Promise<SecurityFinding[]> {
    // Implementation for Bandit scanning
    return [];
  }

  private async runSemgrep(
    path: string,
    language: string
  ): Promise<SecurityFinding[]> {
    // Implementation for Semgrep scanning
    return [];
  }

  private async runEslint(path: string): Promise<SecurityFinding[]> {
    // Implementation for ESLint scanning
    return [];
  }
}
```

**Dependencies:**

- `bandit` (Python security linter).
- `semgrep` (multi-language static analysis).
- `eslint` with `eslint-plugin-security` and `eslint-plugin-node` (TypeScript/JavaScript).
- `snyk` CLI (optional, for Snyk Code analysis).
- `sqlfluff` (SQL linter with security rules).

### 5.4 Best Practices Scanner

**Technology Stack:**

- Use **Semgrep** with custom rules for best practices (supports both Python and Node.js).
- Use **detect-secrets** (Yelp) for secret detection (Python and Node.js).
- Use **truffleHog** for secrets in Git history (language-agnostic).
- Use **gitleaks** for secrets detection (language-agnostic).
- Use **npm-audit-resolver** or **yarn-audit-fix** for Node.js dependency best practices.

**Implementation:**

**Python Implementation:**

```python
# services/security-scanner/src/best_practices_scanner.py
from typing import List, Dict
import subprocess
from pathlib import Path

class BestPracticesScanner:
    """Scans code for security best practices violations."""

    def scan_secrets(self, codebase_path: Path) -> List[Dict]:
        """Detect hardcoded secrets using detect-secrets."""
        # Run: detect-secrets scan --all-files
        findings = []
        findings.extend(self._run_detect_secrets(codebase_path))
        return findings

    def scan_git_history(self, repo_path: Path) -> List[Dict]:
        """Scan Git history for committed secrets using truffleHog/gitleaks."""
        # Run: gitleaks detect --source . --report-path report.json
        # or: trufflehog filesystem --directory .
        findings = []
        findings.extend(self._run_gitleaks(repo_path))
        return findings

    def scan_security_headers(self, config_files: List[Path]) -> List[Dict]:
        """Check for missing security headers in configuration."""
        # Check Flask, Django, FastAPI configs for security headers
        findings = []
        for config_file in config_files:
            findings.extend(self._check_security_headers(config_file))
        return findings

    def scan_input_validation(self, codebase_path: Path) -> List[Dict]:
        """Check for missing input validation using Semgrep."""
        # Run Semgrep with custom rules for input validation
        findings = []
        findings.extend(self._run_semgrep_validation_rules(codebase_path))
        return findings

    def _run_detect_secrets(self, path: Path) -> List[Dict]:
        # Implementation for detect-secrets
        pass

    def _run_gitleaks(self, path: Path) -> List[Dict]:
        # Implementation for gitleaks
        pass

    def _check_security_headers(self, config_file: Path) -> List[Dict]:
        # Implementation for security header checking
        pass

    def _run_semgrep_validation_rules(self, path: Path) -> List[Dict]:
        # Implementation for Semgrep validation rules
        pass
```

**Node.js/TypeScript Implementation:**

```typescript
// services/security-scanner/src/best_practices_scanner.ts
import { exec } from "child_process";
import { promisify } from "util";
import { readdir, readFile } from "fs/promises";
import { join } from "path";

const execAsync = promisify(exec);

interface BestPracticeFinding {
  type: string;
  severity: "critical" | "high" | "medium" | "low" | "info";
  file: string;
  line: number;
  message: string;
  recommendation: string;
}

export class BestPracticesScanner {
  /**
   * Detect hardcoded secrets using detect-secrets or similar tools.
   */
  async scanSecrets(codebasePath: string): Promise<BestPracticeFinding[]> {
    const findings: BestPracticeFinding[] = [];
    findings.push(...(await this.runDetectSecrets(codebasePath)));
    return findings;
  }

  /**
   * Scan Git history for committed secrets using gitleaks or truffleHog.
   */
  async scanGitHistory(repoPath: string): Promise<BestPracticeFinding[]> {
    const findings: BestPracticeFinding[] = [];
    findings.push(...(await this.runGitleaks(repoPath)));
    return findings;
  }

  /**
   * Check for missing security headers in configuration files.
   */
  async scanSecurityHeaders(
    configFiles: string[]
  ): Promise<BestPracticeFinding[]> {
    const findings: BestPracticeFinding[] = [];
    for (const configFile of configFiles) {
      findings.push(...(await this.checkSecurityHeaders(configFile)));
    }
    return findings;
  }

  /**
   * Check for missing input validation using Semgrep.
   */
  async scanInputValidation(
    codebasePath: string
  ): Promise<BestPracticeFinding[]> {
    const findings: BestPracticeFinding[] = [];
    findings.push(...(await this.runSemgrepValidationRules(codebasePath)));
    return findings;
  }

  private async runDetectSecrets(path: string): Promise<BestPracticeFinding[]> {
    // Implementation for detect-secrets or similar Node.js tools
    return [];
  }

  private async runGitleaks(path: string): Promise<BestPracticeFinding[]> {
    // Implementation for gitleaks
    return [];
  }

  private async checkSecurityHeaders(
    configFile: string
  ): Promise<BestPracticeFinding[]> {
    // Check Express, NestJS, Next.js configs for security headers
    return [];
  }

  private async runSemgrepValidationRules(
    path: string
  ): Promise<BestPracticeFinding[]> {
    // Implementation for Semgrep validation rules
    return [];
  }
}
```

**Dependencies:**

- `detect-secrets` (Yelp) - works with both Python and Node.js projects.
- `truffleHog` or `gitleaks` (Git secrets scanner, language-agnostic).
- `semgrep` (for custom rule-based scanning, supports multiple languages).
- `npm-audit-resolver` or `yarn-audit-fix` (for Node.js dependency best practices).

### 5.5 Security Worker

Create a worker service that orchestrates all security scans. This can be implemented in either Python or Node.js/TypeScript:

**Python Implementation:**

```python
# workers/security/src/scanner_worker.py
from typing import Dict, List
from database import Database  # Generic database interface
from models import SecurityIssue, SecurityReport, Scan

class SecurityScannerWorker:
    """Worker that performs security scans for a project/scan."""

    def __init__(self, db: Database):
        self.db = db
        self.python_scanner = PythonDependencyScanner()
        self.node_scanner = NodeDependencyScanner()
        self.owasp_scanner = OWASPScanner()
        self.best_practices_scanner = BestPracticesScanner()

    async def scan_project(self, project_id: str) -> SecurityReport:
        """Perform comprehensive security scan for a project."""
        # 1. Scan Python dependencies
        python_vulns = await self.python_scanner.scan_project(project_id)
        # 2. Scan Node.js dependencies
        node_vulns = await self.node_scanner.scan_project(project_id)
        # 3. Scan code for OWASP violations
        owasp_findings = await self.owasp_scanner.scan_project(project_id)
        # 4. Scan for best practices violations
        best_practice_findings = await self.best_practices_scanner.scan_project(project_id)
        # 5. Generate security report
        report = self._generate_report(python_vulns, node_vulns, owasp_findings, best_practice_findings)
        # 6. Store results in database
        return await self.db.save_security_report(report)

    async def scan_scan(self, scan_id: str) -> SecurityReport:
        """Perform security scan for a specific scan."""
        pass

    def _generate_report(self, *args) -> SecurityReport:
        # Aggregate all findings into a security report
        pass
```

**Node.js/TypeScript Implementation:**

```typescript
// workers/security/src/scanner_worker.ts
import { Database } from "./database"; // Generic database interface
import { SecurityIssue, SecurityReport, Scan } from "./models";
import { PythonDependencyScanner } from "./python_scanner";
import { NodeDependencyScanner } from "./node_scanner";
import { OWASPScanner } from "./owasp_scanner";
import { BestPracticesScanner } from "./best_practices_scanner";

export class SecurityScannerWorker {
  private pythonScanner: PythonDependencyScanner;
  private nodeScanner: NodeDependencyScanner;
  private owaspScanner: OWASPScanner;
  private bestPracticesScanner: BestPracticesScanner;

  constructor(private db: Database) {
    this.pythonScanner = new PythonDependencyScanner();
    this.nodeScanner = new NodeDependencyScanner();
    this.owaspScanner = new OWASPScanner();
    this.bestPracticesScanner = new BestPracticesScanner();
  }

  /**
   * Perform comprehensive security scan for a project.
   */
  async scanProject(projectId: string): Promise<SecurityReport> {
    // 1. Scan Python dependencies
    const pythonVulns = await this.pythonScanner.scanProject(projectId);
    // 2. Scan Node.js dependencies
    const nodeVulns = await this.nodeScanner.scanProject(projectId);
    // 3. Scan code for OWASP violations
    const owaspFindings = await this.owaspScanner.scanProject(projectId);
    // 4. Scan for best practices violations
    const bestPracticeFindings = await this.bestPracticesScanner.scanProject(
      projectId
    );
    // 5. Generate security report
    const report = this.generateReport(
      pythonVulns,
      nodeVulns,
      owaspFindings,
      bestPracticeFindings
    );
    // 6. Store results in database
    return await this.db.saveSecurityReport(report);
  }

  /**
   * Perform security scan for a specific scan.
   */
  async scanScan(scanId: string): Promise<SecurityReport> {
    // Implementation for scan-specific security scanning
    return {} as SecurityReport;
  }

  private generateReport(...args: unknown[]): SecurityReport {
    // Aggregate all findings into a security report
    return {} as SecurityReport;
  }
}
```

### 5.6 Database Schema

**Schema Design:**

The following schema can be implemented using any ORM or database framework (Prisma, SQLAlchemy, TypeORM, Sequelize, etc.):

**Tables:**

1. **SecurityReport Table:**

   - `id` (Primary Key, String/UUID)
   - `scan_id` (Foreign Key, nullable, references Scan table)
   - `project_id` (Foreign Key, references Project table)
   - `security_score` (Integer, 0-100, default: 100)
   - `total_issues` (Integer, default: 0)
   - `critical_issues` (Integer, default: 0)
   - `high_issues` (Integer, default: 0)
   - `medium_issues` (Integer, default: 0)
   - `low_issues` (Integer, default: 0)
   - `info_issues` (Integer, default: 0)
   - `created_at` (Timestamp)
   - `updated_at` (Timestamp)

2. **SecurityIssue Table:**
   - `id` (Primary Key, String/UUID)
   - `report_id` (Foreign Key, references SecurityReport table)
   - `issue_type` (Enum: SecurityIssueType)
   - `severity` (Enum: SecuritySeverity)
   - `title` (String)
   - `description` (Text)
   - `file_path` (String, nullable)
   - `line_number` (Integer, nullable)
   - `code_snippet` (Text, nullable)
   - `vulnerability_id` (String, nullable) - CVE, GHSA, etc.
   - `package_name` (String, nullable)
   - `package_version` (String, nullable)
   - `remediation` (Text, nullable)
   - `status` (Enum: SecurityStatus, default: OPEN)
   - `created_at` (Timestamp)
   - `updated_at` (Timestamp)
   - `resolved_at` (Timestamp, nullable)

**Enums:**

1. **SecurityIssueType:**

   - `PYTHON_DEPENDENCY`
   - `NODE_DEPENDENCY`
   - `OWASP_BROKEN_ACCESS_CONTROL`
   - `OWASP_CRYPTOGRAPHIC_FAILURES`
   - `OWASP_INJECTION`
   - `OWASP_INSECURE_DESIGN`
   - `OWASP_SECURITY_MISCONFIGURATION`
   - `OWASP_VULNERABLE_COMPONENTS`
   - `OWASP_AUTHENTICATION_FAILURES`
   - `OWASP_DATA_INTEGRITY_FAILURES`
   - `OWASP_LOGGING_FAILURES`
   - `OWASP_SSRF`
   - `BEST_PRACTICE_SECRETS`
   - `BEST_PRACTICE_INPUT_VALIDATION`
   - `BEST_PRACTICE_ERROR_HANDLING`
   - `BEST_PRACTICE_AUTHENTICATION`
   - `BEST_PRACTICE_DATA_PROTECTION`
   - `BEST_PRACTICE_API_SECURITY`
   - `BEST_PRACTICE_CONFIGURATION`

2. **SecuritySeverity:**

   - `CRITICAL`
   - `HIGH`
   - `MEDIUM`
   - `LOW`
   - `INFO`

3. **SecurityStatus:**
   - `OPEN`
   - `IN_PROGRESS`
   - `RESOLVED`
   - `ACCEPTED_RISK`
   - `FALSE_POSITIVE`

**Relationships:**

- `SecurityReport` belongs to a `Project` (and optionally a `Scan`).
- `SecurityIssue` belongs to a `SecurityReport`.
- Multiple `SecurityReport` records can exist for a project (historical tracking).

**Indexes:**

- Index on `SecurityReport.project_id` for fast project lookups.
- Index on `SecurityReport.scan_id` for scan-based queries.
- Index on `SecurityReport.created_at` for time-based queries.
- Index on `SecurityIssue.report_id` for report-based queries.
- Index on `SecurityIssue.issue_type` for filtering by issue type.
- Index on `SecurityIssue.severity` for severity-based filtering.
- Index on `SecurityIssue.status` for status-based filtering.
- Index on `SecurityIssue.vulnerability_id` for CVE/GHSA lookups.

### 5.7 Database Migration

**Migration Steps:**

1. **Create Migration:**

   Use your project's migration tool to create a new migration:

   ```bash
   [migration_tool] [migration_command] --name 20251204000000_add_security_scanning
   ```

   Examples:

   - Prisma: `bunx prisma migrate dev --name 20251204000000_add_security_scanning`
   - Alembic (Python): `alembic revision -m "add_security_scanning"`
   - TypeORM (TypeScript): `typeorm migration:create -n AddSecurityScanning`
   - Sequelize: `sequelize migration:generate --name add-security-scanning`

2. **Migration Contents:**

   - Create `SecurityReport` table.
   - Create `SecurityIssue` table.
   - Create `SecurityIssueType` enum (or equivalent in your database).
   - Create `SecuritySeverity` enum (or equivalent in your database).
   - Create `SecurityStatus` enum (or equivalent in your database).
   - Add foreign key constraints.
   - Add indexes for performance.

3. **Migration SQL (PostgreSQL Example):**

   ```sql
   CREATE TYPE "SecurityIssueType" AS ENUM (
     'PYTHON_DEPENDENCY',
     'NODE_DEPENDENCY',
     'OWASP_BROKEN_ACCESS_CONTROL',
     'OWASP_CRYPTOGRAPHIC_FAILURES',
     'OWASP_INJECTION',
     'OWASP_INSECURE_DESIGN',
     'OWASP_SECURITY_MISCONFIGURATION',
     'OWASP_VULNERABLE_COMPONENTS',
     'OWASP_AUTHENTICATION_FAILURES',
     'OWASP_DATA_INTEGRITY_FAILURES',
     'OWASP_LOGGING_FAILURES',
     'OWASP_SSRF',
     'BEST_PRACTICE_SECRETS',
     'BEST_PRACTICE_INPUT_VALIDATION',
     'BEST_PRACTICE_ERROR_HANDLING',
     'BEST_PRACTICE_AUTHENTICATION',
     'BEST_PRACTICE_DATA_PROTECTION',
     'BEST_PRACTICE_API_SECURITY',
     'BEST_PRACTICE_CONFIGURATION'
   );

   CREATE TYPE "SecuritySeverity" AS ENUM (
     'CRITICAL',
     'HIGH',
     'MEDIUM',
     'LOW',
     'INFO'
   );

   CREATE TYPE "SecurityStatus" AS ENUM (
     'OPEN',
     'IN_PROGRESS',
     'RESOLVED',
     'ACCEPTED_RISK',
     'FALSE_POSITIVE'
   );

   CREATE TABLE "SecurityReport" (
     "id" TEXT NOT NULL,
     "scanId" TEXT,
     "projectId" TEXT NOT NULL,
     "securityScore" INTEGER NOT NULL DEFAULT 100,
     "totalIssues" INTEGER NOT NULL DEFAULT 0,
     "criticalIssues" INTEGER NOT NULL DEFAULT 0,
     "highIssues" INTEGER NOT NULL DEFAULT 0,
     "mediumIssues" INTEGER NOT NULL DEFAULT 0,
     "lowIssues" INTEGER NOT NULL DEFAULT 0,
     "infoIssues" INTEGER NOT NULL DEFAULT 0,
     "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
     "updatedAt" TIMESTAMP(3) NOT NULL,

     CONSTRAINT "SecurityReport_pkey" PRIMARY KEY ("id")
   );

   CREATE TABLE "SecurityIssue" (
     "id" TEXT NOT NULL,
     "reportId" TEXT NOT NULL,
     "issueType" "SecurityIssueType" NOT NULL,
     "severity" "SecuritySeverity" NOT NULL,
     "title" TEXT NOT NULL,
     "description" TEXT NOT NULL,
     "filePath" TEXT,
     "lineNumber" INTEGER,
     "codeSnippet" TEXT,
     "vulnerabilityId" TEXT,
     "packageName" TEXT,
     "packageVersion" TEXT,
     "remediation" TEXT,
     "status" "SecurityStatus" NOT NULL DEFAULT 'OPEN',
     "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
     "updatedAt" TIMESTAMP(3) NOT NULL,
     "resolvedAt" TIMESTAMP(3),

     CONSTRAINT "SecurityIssue_pkey" PRIMARY KEY ("id")
   );

   ALTER TABLE "SecurityReport" ADD CONSTRAINT "SecurityReport_scanId_fkey"
     FOREIGN KEY ("scanId") REFERENCES "Scan"("id") ON DELETE CASCADE ON UPDATE CASCADE;

   ALTER TABLE "SecurityReport" ADD CONSTRAINT "SecurityReport_projectId_fkey"
     FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE CASCADE ON UPDATE CASCADE;

   ALTER TABLE "SecurityIssue" ADD CONSTRAINT "SecurityIssue_reportId_fkey"
     FOREIGN KEY ("reportId") REFERENCES "SecurityReport"("id") ON DELETE CASCADE ON UPDATE CASCADE;

   CREATE INDEX "SecurityReport_projectId_idx" ON "SecurityReport"("projectId");
   CREATE INDEX "SecurityReport_scanId_idx" ON "SecurityReport"("scanId");
   CREATE INDEX "SecurityReport_createdAt_idx" ON "SecurityReport"("createdAt");
   CREATE INDEX "SecurityIssue_reportId_idx" ON "SecurityIssue"("reportId");
   CREATE INDEX "SecurityIssue_issueType_idx" ON "SecurityIssue"("issueType");
   CREATE INDEX "SecurityIssue_severity_idx" ON "SecurityIssue"("severity");
   CREATE INDEX "SecurityIssue_status_idx" ON "SecurityIssue"("status");
   CREATE INDEX "SecurityIssue_vulnerabilityId_idx" ON "SecurityIssue"("vulnerabilityId");
   ```

   **Note:** The above SQL is PostgreSQL-specific. Adapt the syntax for your database system:

   - **MySQL/MariaDB:** Use `ENUM` type or `VARCHAR` with CHECK constraints.
   - **SQLite:** Use `TEXT` with CHECK constraints (no native ENUM support).
   - **SQL Server:** Use `NVARCHAR` with CHECK constraints or user-defined types.
   - **MongoDB:** Use document structure with validation schemas.

### 5.8 API Endpoints

**Security Report Endpoints:**

```typescript
// GET /api/projects/:projectId/security/reports
// Get all security reports for a project

// GET /api/projects/:projectId/security/reports/:reportId
// Get a specific security report with issues

// GET /api/projects/:projectId/security/reports/latest
// Get the latest security report

// POST /api/projects/:projectId/security/scan
// Trigger a new security scan

// GET /api/projects/:projectId/security/issues
// Get all security issues (with filtering)

// PATCH /api/security/issues/:issueId
// Update security issue status (e.g., mark as resolved)

// GET /api/projects/:projectId/security/score
// Get current security score and trends
```

### 5.9 Dashboard Integration

Add security section to the dashboard:

- **Security Overview Page:**

  - Current security score.
  - Vulnerabilities by severity (pie chart).
  - Vulnerabilities by type (bar chart).
  - Security score trend over time (line chart).
  - Top 10 critical issues.

- **Security Issues Page:**

  - Filterable table of all security issues.
  - Filters: severity, type, status, date range.
  - Issue details modal with code snippets.
  - Bulk actions (mark as resolved, accept risk, etc.).

- **Security Report Page:**
  - Detailed view of a specific security report.
  - Comparison with previous reports.
  - Remediation recommendations.

## 6. Configuration

### 6.1 Environment Variables

```bash
# Security Scanner Configuration
SECURITY_SCANNER_ENABLED=true
SECURITY_SCAN_ON_SCAN_COMPLETE=true
SECURITY_SCAN_ON_SCHEDULE=true
SECURITY_SCAN_SCHEDULE="0 2 * * *"  # Daily at 2 AM

# Python Scanner
SAFETY_API_KEY=optional_api_key
PIP_AUDIT_ENABLED=true
OSV_API_ENABLED=true

# Node.js Scanner
NPM_AUDIT_ENABLED=true
SNYK_TOKEN=optional_snyk_token
SNYK_ENABLED=false

# OWASP Scanner
SEMGREP_ENABLED=true
BANDIT_ENABLED=true
ESLINT_SECURITY_ENABLED=true

# Best Practices Scanner
DETECT_SECRETS_ENABLED=true
GITLEAKS_ENABLED=true
TRUFFLEHOG_ENABLED=false

# CI/CD Integration
SECURITY_BLOCK_ON_CRITICAL=true
SECURITY_BLOCK_ON_HIGH=false
SECURITY_FAIL_SCORE_THRESHOLD=70  # Fail if score < 70
```

### 6.2 Scanner Configuration Files

**Semgrep Configuration** (`semgrep-config.yml`):

```yaml
rules:
  - id: owasp-top10
    patterns:
      - pattern-either:
          - pattern: $X = $Y
          - pattern-inside: |
              $DB.query(...)
              ...
              $X
    message: "Potential SQL injection vulnerability"
    severity: ERROR
    languages: [python, javascript, typescript]
    metadata:
      category: "owasp-top10"
      owasp: "A03:2021 - Injection"
```

**Bandit Configuration** (`bandit-config.ini`):

```ini
[bandit]
exclude_dirs = tests,venv,node_modules
skips = B101  # Skip assert_used test
```

## 7. Error Handling

### 7.1 Scanner Failures

- **Dependency Scanner Failures:**

  - If a vulnerability database is unavailable, log warning and continue with other scanners.
  - If a package manager command fails, log error and skip that scan type.
  - Partial results are acceptable (scan what we can).

- **Code Scanner Failures:**
  - If a static analysis tool crashes, log error and continue with other tools.
  - If a file cannot be parsed, skip it and log warning.
  - Continue scanning other files even if some fail.

### 7.2 Error Reporting

- Log all scanner errors to monitoring system (Loki).
- Include error details in security report metadata.
- Alert on repeated scanner failures.

## 8. Performance Considerations

### 8.1 Scanning Performance

- **Dependency Scans:**

  - Cache vulnerability database queries (TTL: 24 hours).
  - Run dependency scans in parallel for multiple projects.
  - Use incremental scanning (only scan changed dependencies).

- **Code Scans:**
  - Run code scans in parallel by file/directory.
  - Cache results for unchanged files (using content hash).
  - Limit code snippet size in reports (truncate long snippets).

### 8.2 Database Performance

- Index security issues by severity, status, and type for fast filtering.
- Use pagination for security issues lists.
- Archive old security reports (keep last 12 months, archive older).

### 8.3 Resource Usage

- Limit concurrent security scans (max 5 per worker).
- Set timeouts for scanner processes (5 minutes per scan type).
- Monitor memory usage (some scanners can be memory-intensive).

## 9. Security Considerations

### 9.1 Scanner Security

- Run security scanners in isolated containers.
- Do not execute untrusted code during scanning.
- Validate all scanner outputs before storing in database.
- Sanitize file paths and code snippets before display.

### 9.2 API Security

- Require authentication for all security API endpoints.
- Implement rate limiting on scan trigger endpoints.
- Validate project access permissions before scanning.
- Do not expose sensitive vulnerability details to unauthorized users.

### 9.3 Data Protection

- Do not store full code snippets for large files (truncate).
- Encrypt sensitive vulnerability data at rest.
- Implement data retention policies for security reports.

## 10. Future Enhancements

- **Runtime Security Scanning:**

  - Dynamic application security testing (DAST).
  - Runtime vulnerability detection.
  - Penetration testing automation.

- **Advanced Features:**

  - Machine learning for false positive reduction.
  - Automated remediation suggestions (auto-fix PRs).
  - Integration with vulnerability management platforms (Jira, ServiceNow).
  - Security compliance reporting (SOC 2, ISO 27001).

- **Enhanced Scanning:**

  - Container image scanning (Docker, Kubernetes).
  - Infrastructure as Code scanning (Terraform, CloudFormation).
  - Cloud configuration scanning (AWS, GCP, Azure security checks).

- **Collaboration:**

  - Assign security issues to team members.
  - Security issue comments and discussions.
  - Integration with Slack/Teams for security alerts.

- **Metrics and Analytics:**
  - Security debt tracking.
  - Mean time to remediation (MTTR) metrics.
  - Security trend analysis and predictions.
