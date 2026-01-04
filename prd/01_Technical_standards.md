---
prd_version: "2.0"
status: "Active"
last_updated: "2025-01-02"
---

# 01 – Technical Standards (Python)

## 1. Purpose

This document establishes the technical standards, best practices, and requirements for all Python code contributions. These standards ensure code quality, maintainability, security, and performance.

## 2. Language Requirements

### 2.1 Python 3.13+

- Minimum version: Python 3.12 (3.13+ recommended)
- Use modern Python features (match statements, type unions with `|`, etc.)
- **REQUIRED:** All Python code MUST use type hints
- Use `mypy` for static type checking
- Use `uv` for package management (NEVER use pip directly on host)

### 2.2 Running Python

```bash
# ALWAYS use uv to run Python
uv run python script.py
uv run pytest
uv run mypy src/

# NEVER do this
python script.py  # NO - uses host Python
pip install x     # NO - pollutes host environment
```

## 3. Code Quality Standards

### 3.1 DRY Principle (Don't Repeat Yourself)

**REQUIRED:** All code MUST follow the DRY principle.

- Extract common functionality into reusable functions or modules
- Avoid code duplication across files or services
- Create shared utilities for common patterns
- Refactor duplicated code when identified during reviews

### 3.2 Static Typing Requirements

**REQUIRED:** Static typing MUST be used for all code.

- All function signatures MUST include type hints
- All class attributes MUST be type-annotated
- Use `typing` module for complex types (Union, Optional, etc.)
- Use modern syntax: `list[str]` not `List[str]`, `str | None` not `Optional[str]`
- Type checking MUST pass before code can be merged

```python
from typing import TypeVar
from collections.abc import Sequence

T = TypeVar("T")

def process_items(
    items: Sequence[str],
    config: dict[str, str] | None = None,
) -> bool:
    """Process a list of items with optional configuration."""
    return True

def first_or_none(items: list[T]) -> T | None:
    """Return first item or None if empty."""
    return items[0] if items else None
```

### 3.3 Naming Conventions

**REQUIRED:** All code MUST follow these naming conventions.

| Element | Convention | Example |
|---------|------------|---------|
| Functions/variables | `snake_case` | `process_data`, `user_count` |
| Classes | `PascalCase` | `DataProcessor`, `UserService` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| Private members | `_prefix` | `_internal_state`, `_validate()` |
| Modules | `snake_case` | `data_utils.py`, `user_service.py` |
| Type aliases | `PascalCase` | `UserId = str`, `ConfigDict = dict[str, Any]` |

```python
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

UserId = str

class DataProcessor:
    def __init__(self, config: dict[str, str]) -> None:
        self._internal_state: dict[str, Any] = {}
        self.config = config

    def process_data(self, items: list[str]) -> bool:
        return self._validate_items(items)

    def _validate_items(self, items: list[str]) -> bool:
        return len(items) > 0
```

### 3.4 Code Documentation

**REQUIRED:** All code MUST be documented.

- All modules MUST have a module-level docstring
- All classes MUST have a class-level docstring
- All public functions MUST have docstrings (Google style)
- Complex algorithms MUST include inline comments

```python
"""Module for processing user data.

This module provides utilities for validating and transforming user data
from various sources.
"""

from dataclasses import dataclass


@dataclass
class User:
    """Represents a user in the system.

    Attributes:
        id: Unique identifier for the user.
        email: User's email address.
        name: User's display name.
    """

    id: str
    email: str
    name: str


def validate_email(email: str) -> bool:
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
    return "@" in email and "." in email.split("@")[-1]
```

### 3.5 Project Organization

**REQUIRED:** The project root MUST be kept clean.

**Allowed in root:**
- Configuration: `pyproject.toml`, `docker-compose.yml`, `.gitignore`
- Documentation: `README.md`, `LICENSE`, `CONTRIBUTING.md`
- CI/CD: `.github/workflows/`
- Environment: `.env.example`

**Must be in subdirectories:**
- Source code → `src/`
- Tests → `tests/`
- Scripts → `scripts/`
- Documentation → `docs/`
- PRDs → `prd/`

```
project-root/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       ├── cli.py
│       ├── api/
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── scripts/
│   ├── setup_dev.py
│   └── run_migrations.py
├── prd/
├── prisma/
│   └── schema.prisma
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
└── .gitignore
```

## 4. Testing Requirements

### 4.1 Unit Test Coverage

**REQUIRED:** 100% unit test coverage MUST be maintained.

- All new code MUST have corresponding unit tests
- Use `pytest` as the test framework
- Use `pytest-cov` for coverage reporting
- Use `pytest-asyncio` for async tests

**Coverage thresholds:**
- Statements: 100%
- Branches: 100%
- Functions: 100%
- Lines: 100%

**Test file naming:**
- Co-located: `test_<module>.py` next to source
- Separate: `tests/unit/test_<module>.py`

```python
# tests/unit/test_user_service.py
import pytest
from project_name.services.user import UserService, User


class TestUserService:
    @pytest.fixture
    def service(self) -> UserService:
        return UserService()

    def test_create_user_success(self, service: UserService) -> None:
        user = service.create_user("test@example.com", "Test User")
        assert user.email == "test@example.com"
        assert user.name == "Test User"

    def test_create_user_invalid_email(self, service: UserService) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            service.create_user("invalid", "Test User")


@pytest.mark.asyncio
async def test_async_operation() -> None:
    result = await some_async_function()
    assert result is not None
```

### 4.2 Integration Testing

**REQUIRED:** Integration tests for all database and external service interactions.

- Test database operations against real (test) database
- Test API endpoints with test client
- Clean up test data after each run
- Use Docker for external dependencies

```python
# tests/integration/test_api.py
import pytest
from httpx import AsyncClient
from project_name.main import app


@pytest.mark.asyncio
async def test_create_user_endpoint() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users",
            json={"email": "test@example.com", "name": "Test"},
        )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## 5. Pre-Commit Requirements

### 5.1 Linting and Formatting

**REQUIRED:** All code MUST pass linting before commits.

**Tools:**
- `ruff` - Linting and formatting (replaces flake8, black, isort)
- `mypy` - Static type checking

**Configuration in `pyproject.toml`:**

```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "SIM",    # flake8-simplify
]

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### 5.2 Security Analysis

**REQUIRED:** Security checks before commits.

**Tools:**
- `bandit` - Static security analysis
- `safety` or `pip-audit` - Dependency vulnerability scanning

**Checks:**
- No hardcoded secrets
- No SQL injection vulnerabilities
- No command injection
- Secure dependency versions

### 5.3 Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.10
    hooks:
      - id: bandit
        args: ["-r", "src/"]
```

## 6. Best Practices

### 6.1 Async/Await

- Use `async/await` for all I/O-bound operations
- Use `asyncio.gather()` for concurrent operations
- Use process pools for CPU-bound work

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def fetch_all_users(user_ids: list[str]) -> list[User]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)

def cpu_intensive_work(data: bytes) -> bytes:
    """Process data in separate process."""
    # CPU-bound work here
    return processed_data

async def process_with_pool(items: list[bytes]) -> list[bytes]:
    """Process items using process pool."""
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        results = await asyncio.gather(
            *[loop.run_in_executor(pool, cpu_intensive_work, item) for item in items]
        )
    return list(results)
```

### 6.2 Error Handling

- Use specific exception types
- Create custom exceptions for domain errors
- Always include context in error messages

```python
class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")


class ValidationError(Exception):
    """Raised when validation fails."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"Validation error on {field}: {message}")


async def get_user(user_id: str) -> User:
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

### 6.3 Data Classes and Pydantic

- Use `dataclasses` for simple data containers
- Use `Pydantic` for validation and serialization
- Use `pydantic-settings` for configuration

```python
from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, Field


# Simple data container
@dataclass
class Point:
    x: float
    y: float


# Validated model
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)


# Configuration
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    debug: bool = False

    class Config:
        env_file = ".env"
```

### 6.4 Context Managers

- Use context managers for resource management
- Create custom context managers when appropriate

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

@asynccontextmanager
async def get_db() -> AsyncGenerator[Database, None]:
    """Provide database connection with automatic cleanup."""
    db = Database()
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()


async def create_user(data: UserCreate) -> User:
    async with get_db() as db:
        return await db.user.create(data=data.model_dump())
```

## 7. Code Review Process

### 7.1 Review Checklist

All code reviews MUST verify:

- [ ] Type hints on all functions and attributes
- [ ] Docstrings on all public functions and classes
- [ ] DRY principle followed
- [ ] Naming conventions followed
- [ ] Unit tests with 100% coverage
- [ ] Integration tests for DB/API operations
- [ ] No hardcoded secrets
- [ ] Security analysis passes
- [ ] Linting passes
- [ ] Error handling is comprehensive

### 7.2 Approval Requirements

- At least one reviewer approval required
- All CI/CD checks MUST pass
- All tests MUST pass
- Coverage MUST not decrease
- Security scans MUST pass

## 8. CI/CD Pipeline

### 8.1 Required Stages

1. **Lint** - Run ruff, mypy
2. **Test** - Run pytest with coverage
3. **Security** - Run bandit, safety/pip-audit
4. **Build** - Build Docker image
5. **Deploy** - Deploy to target environment

### 8.2 Pre-merge Requirements

- All CI stages pass
- Code review approved
- 100% test coverage maintained
- No security vulnerabilities
- Documentation updated if needed

## 9. Environment Variables

**REQUIRED:** Use `python-dotenv` and `pydantic-settings`.

```python
# src/project_name/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Database
    database_url: str

    # Redis (optional)
    redis_url: str | None = None

    # Application
    debug: bool = False
    log_level: str = "INFO"


settings = Settings()
```

## 10. References

- `02_Tech_stack.md` - Technology stack details
- `03_Security.md` - Security requirements
- Python Style Guide: PEP 8
- Type Hints: PEP 484, PEP 604
