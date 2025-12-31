---
prd_version: "1.0"
status: "Active"
last_updated: "2025-01-XX"
---

# 01 – Technical Standards and Tech Stack

## 1. Purpose

This document establishes the technical standards, best practices, and requirements for all code contributions to the project. These standards ensure code quality, maintainability, security, and performance across all components of the system.

## 2. Tech Stack Overview

### 2.1 Backend Languages

- **Python 3.12+**

  - Primary language for market data workers (data ingestion, regime detection, strategy execution, alert monitoring)
  - Uses `asyncio` for I/O concurrency and process pools for CPU-bound work
  - **REQUIRED:** All Python code MUST use type hints (typed Python)
  - Use `mypy` for static type checking
  - Use `uv` for fast dependency management and reproducible environments
  - **REQUIRED** always invoke python via `uv`. NEVER call host os python directly or install modeles in the global space.

- **Node.js / TypeScript**
  - Primary language for API services and frontend
  - **REQUIRED:** Prefer TypeScript over JavaScript for all new code
  - JavaScript files are acceptable only for legacy code or configuration files
  - All new features MUST be implemented in TypeScript

### 2.2 Package Management

- **Python:** `uv` for fast dependency management and reproducible environments
- **Node.js:** `npm` or `bun` (as specified per service)

### 2.3 Database

- **PostgreSQL** with **Prisma** as the schema management tool
- See `02_Tech_stack.md` for detailed database stack information

## 3. Code Quality Standards

### 3.1 DRY Principle (Don't Repeat Yourself)

**REQUIRED:** All code MUST follow the DRY principle.

- Extract common functionality into reusable functions, modules, or utilities
- Avoid code duplication across files, services, or components
- Create shared libraries for common patterns and utilities
- Refactor duplicated code when identified during code reviews
- Use composition and inheritance appropriately to reduce duplication

**Examples:**

- Create utility functions for common operations (e.g., date formatting, validation)
- Extract shared business logic into service classes or modules
- Use configuration files for repeated constants or settings
- Leverage design patterns to avoid repeating implementation patterns

### 3.2 Static Typing Requirements

**REQUIRED:** Static typing MUST be used wherever possible.

#### Python

- All function signatures MUST include type hints
- All class attributes MUST be type-annotated
- Use `typing` module for complex types (Union, Optional, List, Dict, etc.)
- Use `mypy` for static type checking
- Type checking MUST pass before code can be merged

**Example:**

```python
from typing import List, Optional, Dict

def process_items(items: List[str], config: Optional[Dict[str, str]] = None) -> bool:
    """Process a list of items with optional configuration."""
    # Implementation
    return True
```

#### TypeScript/JavaScript

- **REQUIRED:** Prefer TypeScript over JavaScript
- All new files MUST be `.ts` or `.tsx` (not `.js` or `.jsx`)
- All functions MUST have explicit return types
- Use interfaces or types for all object structures
- Avoid `any` type; use `unknown` when type is truly unknown
- Enable strict mode in `tsconfig.json`

**Example:**

```typescript
interface UserConfig {
  id: string;
  name: string;
  email: string;
}

function processUser(config: UserConfig): Promise<boolean> {
  // Implementation
  return Promise.resolve(true);
}
```

### 3.3 Naming Conventions

**REQUIRED:** All code MUST follow these naming conventions.

#### Python

- **Functions and variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private methods/attributes:** Prefix with single underscore `_private_method`
- **Module names:** `snake_case` (lowercase with underscores)

**Example:**

```python
MAX_RETRY_COUNT = 3

class DataProcessor:
    def __init__(self, config: Dict[str, str]):
        self._internal_state = {}
        self.config = config

    def process_data(self, items: List[str]) -> bool:
        # Implementation
        pass
```

#### TypeScript/JavaScript

- **Functions and variables:** `camelCase`
- **Classes and interfaces:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE` or `UPPER_CAMEL_CASE` for exported constants
- **Private methods/attributes:** Prefix with underscore `_privateMethod` (TypeScript `private` keyword preferred)
- **Component files:** `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- **Utility files:** `camelCase.ts` (e.g., `dateUtils.ts`)

**Example:**

```typescript
const MAX_RETRY_COUNT = 3;

interface UserProfile {
  id: string;
  name: string;
}

class DataProcessor {
  private _internalState: Map<string, string> = new Map();

  public processData(items: string[]): boolean {
    // Implementation
    return true;
  }
}
```

#### Database/Prisma

- **Models:** `PascalCase` (e.g., `UserProfile`, `ScanResult`)
- **Fields:** `camelCase` (e.g., `createdAt`, `userId`)
- **Enums:** `PascalCase` with `SCREAMING_SNAKE_CASE` values (e.g., `ScanStatus` with values `IN_PROGRESS`, `COMPLETED`)

### 3.4 Code Documentation

**REQUIRED:** All code MUST be documented for maintainability.

#### Python

- All modules MUST have a module-level docstring
- All classes MUST have a class-level docstring
- All public functions and methods MUST have docstrings following Google or NumPy style
- Complex algorithms or business logic MUST include inline comments explaining the approach
- Use type hints in docstrings only when they add clarity beyond type annotations

**Example:**

```python
"""Module for processing user data.

This module provides utilities for validating and transforming user data
from various sources.
"""

class UserProcessor:
    """Processes and validates user data.

    This class handles the transformation and validation of user data
    from external sources, ensuring data integrity and consistency.
    """

    def validate_email(self, email: str) -> bool:
        """Validate an email address format.

        Args:
            email: The email address to validate.

        Returns:
            True if the email is valid, False otherwise.

        Raises:
            ValueError: If email is empty or None.
        """
        if not email:
            raise ValueError("Email cannot be empty")
        # Implementation
        return True
```

#### TypeScript

- All exported functions, classes, and interfaces MUST have JSDoc comments
- Complex functions MUST include parameter descriptions and return value descriptions
- Use `@param`, `@returns`, `@throws` tags in JSDoc
- Inline comments for complex logic or non-obvious implementations

**Example:**

```typescript
/**
 * Validates an email address format.
 *
 * @param email - The email address to validate
 * @returns True if the email is valid, False otherwise
 * @throws {Error} If email is empty or undefined
 */
function validateEmail(email: string): boolean {
  if (!email) {
    throw new Error("Email cannot be empty");
  }
  // Implementation
  return true;
}
```

### 3.5 Project Organization

**REQUIRED:** The project root folder MUST be kept clean and organized.

- Only essential configuration and documentation files should reside in the project root
- Utility scripts MUST be moved to a `scripts/` folder (or appropriate subdirectory)
- Keep only the minimum files necessary at the root level
- Organize related files into appropriate directories

**Root Directory Requirements:**

**Allowed Files in Root:**

- Configuration files (e.g., `package.json`, `pyproject.toml`, `docker-compose.yml`, `.gitignore`)
- Documentation files (e.g., `README.md`, `LICENSE`, `CONTRIBUTING.md`)
- CI/CD configuration files (e.g., `.github/workflows/`, `.gitlab-ci.yml`)
- Environment example files (e.g., `.env.example`)
- Project structure documentation (e.g., `PROJECT_STRUCTURE.md`)

**Files That MUST Be Moved:**

- Utility scripts → `scripts/` folder
- One-off scripts → `scripts/` folder
- Admin tools → `scripts/admin/` folder
- Build scripts → `scripts/build/` folder
- Development tools → `scripts/dev/` folder

**Example Structure:**

```
project-root/
├── README.md
├── LICENSE
├── docker-compose.yml
├── .gitignore
├── .env.example
├── package.json
├── pyproject.toml
├── prisma/
├── scripts/
│   ├── admin/
│   │   ├── delete_scans.py
│   │   └── reset_jobs.py
│   ├── build/
│   │   └── build_docker.sh
│   ├── dev/
│   │   └── setup_dev.sh
│   └── utils/
│       └── common_helpers.py
├── src/
├── tests/
└── ...
```

**Enforcement:**

- Code reviews MUST verify that new scripts are placed in appropriate directories
- Existing scripts in the root SHOULD be moved to `scripts/` during refactoring
- No new utility scripts should be added to the root directory

## 4. Testing Requirements

### 4.1 Unit Test Coverage

**REQUIRED:** 100% unit test coverage MUST be maintained.

- All new code MUST have corresponding unit tests
- All functions, methods, and classes MUST be covered by unit tests
- Test coverage MUST be measured and verified before code can be merged
- Use coverage tools:
  - **Python:** `pytest-cov` or `coverage.py`
  - **TypeScript:** `jest` with coverage reporting or `nyc`

**Coverage Requirements:**

- **Statements:** 100%
- **Branches:** 100%
- **Functions:** 100%
- **Lines:** 100%

**Test Organization:**

- Unit tests MUST be co-located with source code or in dedicated test directories
- Test files MUST follow naming convention: `test_*.py` (Python) or `*.test.ts` (TypeScript)
- Tests MUST be independent and not rely on execution order
- Use fixtures and mocks appropriately to isolate units under test

**Example Structure:**

```
src/
  utils/
    date_utils.py
    test_date_utils.py
```

or

```
src/
  utils/
    dateUtils.ts
tests/
  unit/
    dateUtils.test.ts
```

### 4.2 Integration Testing

**REQUIRED:** End-to-end integration testing MUST be implemented for all features.

- All features that interact with external systems (databases, APIs, services) MUST have integration tests
- Integration tests MUST verify the complete flow from input to output
- Integration tests MUST run against test databases or mocked external services
- Integration tests MUST be runnable in CI/CD pipelines

**Integration Test Requirements:**

- Test database interactions (queries, transactions, migrations)
- Test API endpoints (request/response cycles, error handling)
- Test service-to-service communication
- Test worker job processing end-to-end
- Test authentication and authorization flows

**Test Organization:**

- Integration tests MUST be clearly separated from unit tests
- Use test databases that mirror production schema
- Clean up test data after each test run
- Use Docker containers for external dependencies when possible

**Example Structure:**

```
tests/
  integration/
    test_api_endpoints.py
    test_database_operations.py
    test_worker_jobs.py
```

## 5. Pre-Commit Requirements

### 5.1 Linting

**REQUIRED:** All code MUST pass linting checks before commits.

#### Python

- Use `ruff` or `flake8` for linting
- Use `black` for code formatting (or `ruff format`)
- Use `mypy` for type checking
- All linting errors MUST be resolved before code can be committed
- Configure pre-commit hooks to run linters automatically

**Configuration:**

- `.ruff.toml` or `pyproject.toml` for ruff configuration
- `pyproject.toml` for black configuration
- `mypy.ini` or `pyproject.toml` for mypy configuration

#### TypeScript/JavaScript

- Use `ESLint` for linting
- Use `Prettier` for code formatting
- Use `tsc --noEmit` for type checking
- All linting errors MUST be resolved before code can be committed
- Configure pre-commit hooks or CI checks to enforce linting

**Configuration:**

- `.eslintrc.js` or `.eslintrc.json` for ESLint rules
- `.prettierrc` for Prettier configuration
- `tsconfig.json` with strict mode enabled

**Pre-commit Hook Setup:**

```bash
# Install pre-commit (Python)
pip install pre-commit
pre-commit install

# Or use husky (Node.js)
npm install --save-dev husky
npx husky install
```

### 5.2 Security Analysis

**REQUIRED:** Security analysis MUST be performed before commits.

- Run security vulnerability scanners on dependencies
- Check for known security vulnerabilities in third-party packages
- Review code for common security issues (SQL injection, XSS, etc.)
- Use automated security scanning tools in CI/CD

**Tools:**

- **Python:** `safety`, `bandit`, `pip-audit`
- **Node.js:** `npm audit`, `snyk`, `retire.js`

**Security Checks:**

- Dependency vulnerability scanning
- Static code analysis for security issues
- Secrets scanning (no hardcoded API keys, passwords, etc.)
- Input validation and sanitization review
- Authentication and authorization checks

**Pre-commit Configuration:**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "src/"]
  - repo: https://github.com/pyupio/safety
    rev: 2.3.5
    hooks:
      - id: safety
```

### 5.3 Performance Evaluation

**REQUIRED:** Performance evaluation MUST be conducted before commits.

- Profile code for performance bottlenecks
- Measure execution time for critical paths
- Check memory usage and leaks
- Verify database query performance
- Ensure no significant performance regressions

**Performance Requirements:**

- New features MUST not degrade existing performance by more than 5%
- Database queries MUST be optimized and use appropriate indexes
- API endpoints MUST respond within acceptable time limits
- Worker jobs MUST complete within expected timeframes

**Tools:**

- **Python:** `cProfile`, `py-spy`, `memory_profiler`
- **TypeScript/Node.js:** `clinic.js`, `0x`, Node.js built-in profiler
- **Database:** Query analysis tools, `EXPLAIN ANALYZE` for PostgreSQL

**Performance Testing:**

- Benchmark critical functions and compare against baselines
- Load testing for API endpoints
- Stress testing for worker processes
- Monitor resource usage (CPU, memory, I/O)

## 6. Best Practices

### 6.1 Python Best Practices

- **Use async/await** for I/O-bound operations
- **Use process pools** for CPU-bound operations
- **Follow PEP 8** style guide (enforced by linters)
- **Use context managers** for resource management (`with` statements)
- **Handle exceptions explicitly** with specific exception types
- **Use dataclasses or Pydantic** for data models
- **Leverage type hints** for all function signatures
- **Use dependency injection** for testability
- **Follow SOLID principles** in class design

**Example:**

```python
from dataclasses import dataclass
from typing import Optional
import asyncio

@dataclass
class User:
    id: str
    name: str
    email: str

async def fetch_user(user_id: str) -> Optional[User]:
    """Fetch user data asynchronously."""
    # Implementation
    pass
```

### 6.2 Node.js/TypeScript Best Practices

- **Use async/await** instead of callbacks or raw promises
- **Handle errors** with try-catch blocks and proper error types
- **Use dependency injection** for testability
- **Follow functional programming** patterns where appropriate
- **Use const/let** appropriately (prefer const)
- **Avoid side effects** in pure functions
- **Use proper error handling** with custom error classes
- **Leverage TypeScript features** (generics, utility types, etc.)
- **Follow React best practices** (hooks, component composition)

**Example:**

```typescript
interface ApiResponse<T> {
  data: T;
  error?: string;
}

async function fetchUser(userId: string): Promise<ApiResponse<User>> {
  try {
    const response = await fetch(`/api/users/${userId}`);
    const data = await response.json();
    return { data };
  } catch (error) {
    return {
      data: null as unknown as User,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
```

### 6.3 Environment Variable Management

**REQUIRED:** All services MUST use the `dotenv` library for environment variable management.

#### Python

- **REQUIRED:** Use `python-dotenv` library for all environment variable access
- Load environment variables at application startup using `load_dotenv()`
- Never access `os.environ` directly without loading dotenv first
- Validate required environment variables at startup

**Example:**

```python
from dotenv import load_dotenv
import os

# Load environment variables at startup
load_dotenv()

# Access environment variables
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is required")
```

#### Node.js/TypeScript

- **REQUIRED:** Use `dotenv` package for all environment variable access
- Load environment variables at application startup using `dotenv.config()`
- Next.js has built-in `.env` file support, but `dotenv` should be used for explicit configuration in non-Next.js services
- Validate required environment variables at startup

**Example:**

```typescript
import dotenv from "dotenv";

// Load environment variables at startup
dotenv.config();

// Access environment variables
const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error("DATABASE_URL environment variable is required");
}
```

#### Best Practices

- **Never hardcode** environment variables in source code
- **Use `.env.example`** files to document required environment variables (without values)
- **Keep sensitive files in `.gitignore`**: `.environment`, `.env.local`, `.env`
- **Load once at startup**: Load environment variables once at application startup, not per-module
- **Fail fast**: Validate required environment variables at startup and fail immediately if missing
- **Type safety**: Use TypeScript types or Python dataclasses for environment variable configuration

## 7. Code Review Process

### 7.1 Review Checklist

All code reviews MUST verify:

- [ ] Code follows DRY principle
- [ ] Static typing is used appropriately
- [ ] Naming conventions are followed
- [ ] Code is properly documented
- [ ] Project organization is maintained (scripts in `scripts/` folder, root kept clean)
- [ ] Unit tests achieve 100% coverage
- [ ] Integration tests are included for new features
- [ ] Linting passes without errors
- [ ] Security analysis passes
- [ ] Performance evaluation is acceptable
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is comprehensive
- [ ] Code follows language-specific best practices

### 7.2 Approval Requirements

- At least one senior developer approval required
- All CI/CD checks MUST pass
- All tests MUST pass
- Code coverage MUST not decrease
- Security scans MUST pass
- Performance benchmarks MUST meet requirements

## 8. Continuous Integration/Continuous Deployment

### 8.1 CI/CD Pipeline Requirements

All CI/CD pipelines MUST include:

1. **Linting Stage**

   - Run linters for all changed files
   - Fail build if linting errors exist

2. **Type Checking Stage**

   - Run type checkers (mypy, tsc)
   - Fail build if type errors exist

3. **Unit Test Stage**

   - Run all unit tests
   - Generate coverage reports
   - Fail build if coverage drops below 100%
   - Fail build if any test fails

4. **Integration Test Stage**

   - Run all integration tests
   - Fail build if any test fails

5. **Security Scan Stage**

   - Scan dependencies for vulnerabilities
   - Run static security analysis
   - Fail build if critical vulnerabilities found

6. **Performance Benchmark Stage**

   - Run performance benchmarks
   - Compare against baseline
   - Fail build if significant regression detected

7. **Build Stage**
   - Build Docker images
   - Verify build artifacts

### 8.2 Pre-merge Requirements

Before code can be merged:

- All CI/CD stages MUST pass
- Code review MUST be approved
- All tests MUST pass
- Coverage MUST be at 100%
- No security vulnerabilities
- Performance benchmarks MUST pass

## 9. Documentation Standards

### 9.1 Code Documentation

- All public APIs MUST be documented
- Complex algorithms MUST include explanatory comments
- Configuration options MUST be documented
- Examples MUST be provided for public APIs

### 9.2 Project Documentation

- README files MUST be kept up to date
- Architecture decisions MUST be documented
- API documentation MUST be generated and maintained
- Deployment procedures MUST be documented

## 10. Enforcement

### 10.1 Automated Enforcement

- Pre-commit hooks enforce linting and formatting
- CI/CD pipelines enforce all quality gates
- Automated tools prevent merging code that doesn't meet standards

### 10.2 Manual Enforcement

- Code reviews verify adherence to standards
- Regular code audits identify areas for improvement
- Team training ensures understanding of standards

## 11. Exceptions and Waivers

Exceptions to these standards may be granted only with:

- Written approval from technical leadership
- Documented justification for the exception
- Plan for addressing the exception in future work
- Risk assessment of the exception

## 12. References

- `02_Tech_stack.md` - Detailed tech stack information
- `03_Security.md` - Security-specific requirements
- `12_Observability_and_Metrics.md` - Monitoring and observability standards (TODO: Create this PRD)
