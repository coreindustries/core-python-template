---
prd_version: "3.0"
status: "Active"
last_updated: "2026-01-15"
---

# 01 – Technical Standards (Python)

## 1. Purpose

This document establishes the technical standards, best practices, and requirements for all code contributions to this project—whether written by humans or AI agents. These standards ensure code quality, maintainability, security, and performance while enabling autonomous, efficient AI-assisted development workflows.

**Goals:**
- Maintain consistent code quality across all contributions
- Enable autonomous AI agent workflows with clear guardrails
- Ensure production-ready code through rigorous testing and quality checks
- Preserve context across long-running features that span multiple sessions

**Related Documents:**
- PRD 02 (Tech Stack) - Approved technologies and patterns
- PRD 03 (Security) - Security requirements and audit logging

## 2. Language Requirements

### 2.1 Python 3.13+

- Minimum version: Python 3.12 (3.13+ recommended)
- Use modern Python features (match statements, type unions with `|`, etc.)
- **REQUIRED:** All Python code MUST use type hints
- Use `mypy` for static type checking
- Use `uv` for package management (NEVER use pip directly on host)

### 2.2 Package Management

```bash
# ALWAYS use uv to run Python
uv sync                    # Install dependencies
uv add package-name        # Add new package
uv run python script.py    # Run Python
uv run pytest              # Run tests
uv run mypy src/           # Type checking
uv run app serve           # Start API

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
- Search for existing implementations before creating new code
- Refactor duplicated code when identified during reviews

### 3.2 Static Typing Requirements

**REQUIRED:** Static typing MUST be used for all code.

- All function signatures MUST include type hints
- All class attributes MUST be type-annotated
- All return types MUST be specified
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

| Element             | Convention         | Example                                       |
| ------------------- | ------------------ | --------------------------------------------- |
| Functions/variables | `snake_case`       | `process_data`, `user_count`                  |
| Classes             | `PascalCase`       | `DataProcessor`, `UserService`                |
| Constants           | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`          |
| Private members     | `_prefix`          | `_internal_state`, `_validate()`              |
| Modules             | `snake_case`       | `data_utils.py`, `user_service.py`            |
| Type aliases        | `PascalCase`       | `UserId = str`, `ConfigDict = dict[str, Any]` |

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
- Documentation: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`
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
├── prd/
│   └── tasks/
├── prisma/
│   └── schema.prisma
├── pyproject.toml
├── docker-compose.yml
└── .env.example
```

## 4. AI Agent Development Principles

### 4.1 Autonomy and Persistence

**REQUIRED:** AI agents MUST operate autonomously and persist until tasks are fully complete.

**Autonomous Senior Engineer Mindset:**
- Once given direction, proactively gather context, plan, implement, test, and refine
- No waiting for additional prompts at each step
- Complete tasks end-to-end within a single turn whenever feasible
- Bias to action: default to implementing with reasonable assumptions

**Persistence Criteria:**
- Don't stop at analysis or partial fixes
- Carry changes through implementation, verification, and clear explanation
- Continue until working code is delivered, not just a plan
- Only pause if explicitly redirected or truly blocked

**Anti-patterns to Avoid:**
- Stopping after creating a plan without implementing
- Requesting clarification on details that can be reasonably inferred
- Implementing halfway and asking "should I continue?"
- Excessive looping on the same files without progress

### 4.2 Bias to Action

**REQUIRED:** Agents MUST default to implementation over clarification.

**When to Implement Immediately:**
- Requirements are reasonably clear (even if some details missing)
- Multiple valid approaches exist (choose the most standard one)
- Implementation patterns exist in the codebase
- Missing details can be inferred from context

**When to Ask Questions:**
- Critical architectural decisions with significant tradeoffs
- Conflicting requirements that need resolution
- Truly blocked on external information
- User preference matters significantly and isn't inferrable

**Example Decision Tree:**
```
User: "Add user authentication"
├─ API approach? → JWT (standard for FastAPI, matches existing patterns)
├─ Password hashing? → bcrypt (industry standard, already in dependencies)
├─ Session storage? → Redis (already configured in docker-compose.yml)
└─ IMPLEMENT with these defaults ✓

User: "Add payment processing"
├─ Provider? → Could be Stripe, PayPal, Square... → ASK ✓
```

### 4.3 Correctness Over Speed

**REQUIRED:** Prioritize correctness, clarity, and reliability over implementation speed.

**Quality Criteria:**
- Cover the root cause or core ask, not just symptoms
- Avoid risky shortcuts and speculative changes
- Investigate before implementing to ensure understanding
- No messy hacks just to get code working

**Discerning Engineer Approach:**
- Read enough context before changing files
- Understand existing patterns and follow them
- Consider edge cases and error paths
- Write production-ready code, not just "working" code

### 4.4 Comprehensiveness and Completeness

**REQUIRED:** Ensure changes are comprehensive across all relevant surfaces.

**Example:**
```
Task: Add "archived" status to users

Incomplete (❌):
- Only add field to database schema

Complete (✓):
- Add field to Prisma schema
- Generate migration
- Update UserCreate/UserUpdate Pydantic models
- Add filtering in UserService.list_all()
- Add query param to API endpoint
- Update tests for archived users
- Add audit logging for archive action
```

### 4.5 Behavior-Safe Defaults

**REQUIRED:** Preserve intended behavior and UX.

- Don't change existing behavior without explicit request
- Gate intentional behavior changes with feature flags or configuration
- Add tests when behavior shifts
- Document behavioral changes in commit messages

```python
# UNSAFE: Changes default behavior
async def get_users(include_deleted: bool = True):  # Was False
    # Now includes deleted users by default!

# SAFE: Preserves existing behavior
async def get_users(include_deleted: bool = False, include_archived: bool = False):
    # New parameter with safe default
```

## 5. Error Handling

### 5.1 Specific Exception Types

**REQUIRED:** Use specific exception types, not broad catches.

- Create custom exceptions for domain errors
- Always include context in error messages
- Never swallow exceptions silently

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
```

### 5.2 Tight Error Handling

**REQUIRED:** Do NOT add broad exception catches or silent defaults.

**What to Avoid:**
- Broad `try/except` blocks that swallow errors
- Catching `Exception` without re-raising or logging
- Success-shaped fallbacks that hide failures
- Early returns on invalid input without logging

```python
# BAD: Silent failure
async def get_user(user_id: str) -> User | None:
    try:
        return await db.user.find_unique(where={"id": user_id})
    except Exception:
        return None  # What happened? Why did it fail?

# GOOD: Explicit error handling
async def get_user(user_id: str) -> User:
    try:
        user = await db.user.find_unique(where={"id": user_id})
        if not user:
            raise UserNotFoundError(user_id)
        return user
    except PrismaClientKnownRequestError as e:
        logger.error(f"Database error fetching user {user_id}: {e}")
        raise DatabaseError(f"Failed to fetch user: {user_id}") from e
```

## 6. Exploration Patterns

### 6.1 Think First, Batch Everything

**REQUIRED:** Plan all file reads before executing, then batch them in parallel.

**Pattern:**
1. **Think**: Decide ALL files/resources needed
2. **Batch**: Read all files together in one parallel call
3. **Analyze**: Process results
4. **Repeat**: Only if new, unpredictable reads are needed

```python
# BAD: Sequential reads
read("api/routes.py")
# ... analyze ...
read("services/user.py")
# ... analyze ...

# GOOD: Parallel batch
read_parallel([
    "api/routes.py",
    "services/user.py",
    "models/user.py"
])
# ... analyze all together ...
```

### 6.2 Maximize Parallelism

**REQUIRED:** Always read files in parallel unless logically unavoidable.

**Applies To:**
- File reads (`cat`, `read_file`)
- File searches (`rg`, `glob_file_search`)
- Directory listings (`ls`, `list_dir`)
- Git operations (`git show`)

**Only Sequential If:**
- You truly cannot know the next file without seeing a result first
- Example: Reading a config file to determine which modules to load next

### 6.3 Efficient, Coherent Edits

**REQUIRED:** Batch logical edits together, not repeated micro-edits.

- Read enough context before changing a file
- Make all related changes in one pass
- Avoid thrashing with many tiny patches to the same file

## 7. Testing Standards

### 7.1 Unit Test Coverage

**REQUIRED:** Minimum 66% test coverage (100% for production-ready features).

- All new code MUST have corresponding unit tests
- Use `pytest` as the test framework
- Use `pytest-cov` for coverage reporting
- Use `pytest-asyncio` for async tests

**Test file naming:**
- Separate: `tests/unit/test_<module>.py`

```python
# tests/unit/test_user_service.py
import pytest
from project_name.services.user import UserService


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

### 7.2 Integration Testing

**REQUIRED:** Integration tests for all database and external service interactions.

- Test database operations against real (test) database
- Test API endpoints with test client
- Clean up test data after each run
- Use Docker for external dependencies
- Mark with `@pytest.mark.integration`

```python
# tests/integration/test_api.py
import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user_endpoint(integration_client: AsyncClient) -> None:
    response = await integration_client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

### 7.3 Test-Driven Development Pattern

**REQUIRED when refactoring:** Ensure tests exist before modifying code.

**Pattern:**
1. Verify tests exist and pass
2. Make changes
3. Verify tests still pass
4. Add new tests for new behavior
5. Verify coverage hasn't decreased

## 8. Quality Checks

### 8.1 Frequent Check Pattern

**REQUIRED:** Run quality checks every 15-30 minutes during active development.

**Benefits:**
- Prevents error accumulation (50% less debugging time)
- Immediate feedback on smaller change sets
- Easier to identify which change caused issues
- Reduces pre-commit hook failures (40% less frustration)

```bash
# After writing/modifying a file
uv run ruff check src/project_name/module.py
uv run ruff format src/project_name/module.py

# After writing type hints
uv run mypy src/project_name/module.py

# After writing tests
uv run pytest tests/unit/test_module.py -v
```

### 8.2 Pre-Commit Requirements

**REQUIRED:** All code MUST pass linting before commits.

**Tools:**
- `ruff` - Linting and formatting (replaces flake8, black, isort)
- `mypy` - Static type checking
- `bandit` - Static security analysis
- `safety` or `pip-audit` - Dependency vulnerability scanning

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

### 8.3 Before Every Commit

**REQUIRED:** Run the full quality check suite:

```bash
# 1. Lint and format
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# 2. Type check
uv run mypy src/

# 3. Security scan
uv run bandit -r src/

# 4. Tests with coverage
uv run pytest --cov=src --cov-fail-under=66

# 5. Verify changes
git status
git diff
```

**All checks MUST pass before committing.**

## 9. Git and Version Control

### 9.1 Working with Dirty Worktrees

**REQUIRED:** Preserve existing changes not made by you.

**Rules:**
- **NEVER revert changes you didn't make** unless explicitly requested
- Unrelated changes in files → ignore them, don't revert
- Changes in files you've touched recently → read carefully, work with them
- Unexpected changes you didn't make → STOP and ask user

**Safe Commands:**
```bash
git status               # Check current state
git diff                 # See what changed
git diff --cached        # See staged changes
git log -5               # Recent commits
```

**NEVER Use Without Approval:**
```bash
git reset --hard         # Destroys all changes
git checkout --          # Discards specific file changes
git clean -fd            # Removes untracked files
```

### 9.2 Commit Message Standards

**REQUIRED Format:**
```
<type>: <description>

<body (optional)>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Example:**
```
feat: add user authentication with JWT

Implements JWT-based authentication with Redis session storage.
Includes login, logout, and token refresh endpoints with full
test coverage and audit logging.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## 10. Plan and Task Management

### 10.1 When to Create Plans

**Skip Plans For:**
- Straightforward tasks (easiest ~25% of work)
- Single-step changes
- Obvious fixes

**Create Plans For:**
- Multi-step features
- Complex refactorings
- Cross-cutting changes
- Tasks requiring coordination across multiple files

### 10.2 Plan Discipline

**REQUIRED:** Plans MUST be reconciled before finishing a task.

**Plan Lifecycle:**
1. Create plan with clear steps
2. Update plan after completing each step (mark as Done)
3. Before finishing, ensure every item is:
   - **Done**: Completed successfully
   - **Blocked**: With one-sentence reason and targeted question
   - **Cancelled**: With reason for cancellation
4. No in_progress or pending items when finishing

**Deliverable is Working Code:**
- Never end with only a plan
- Implement, test, and verify before completion

### 10.3 Task Tracking for Long-Running Features

Long-running features that span multiple sessions require persistent task tracking to survive context compression.

**When to Create Task Files:**
- Feature will span multiple agent sessions
- Feature has >5 distinct tasks
- Feature is marked "In Progress" in PRD index

**Location:** `prd/tasks/{feature_name}_tasks.md`

**Template:** Use `prd/tasks/TASK_TEMPLATE.md` as starting point

**Key Sections:**
1. **Context** - High-level overview and key decisions (critical for recovery)
2. **Tasks** - Hierarchical checklist with phase grouping
3. **Progress Summary** - Percentage complete per phase
4. **Next Session Priorities** - What to do immediately when resuming
5. **Decisions Made** - Architectural decisions with rationale

**Maintenance:**
- Update every 30-60 minutes during active development
- Use `/checkpoint` skill to update automatically

**Context Compression Recovery:**
1. Read `prd/00_PRD_index.md` to find "In Progress" features
2. Read corresponding task file
3. Start from "Next Session Priorities"

## 11. PRD Implementation Workflow

### 11.1 Before Starting Implementation

**Read PRDs thoroughly:**
1. Review the PRD document for the feature you're implementing
2. Understand dependencies on other PRDs
3. Check PRD 01 (Technical Standards) for coding requirements
4. Check PRD 03 (Security) for security requirements

**Setup development environment:**
```bash
uv sync
docker-compose up -d postgres redis
uv run prisma generate
uv run prisma db push
```

### 11.2 Before Creating Pull Request

**Final verification:**
```bash
# 1. Ensure you're up to date with main
git fetch origin
git rebase origin/main

# 2. Run full test suite
uv run pytest

# 3. Verify coverage
uv run pytest --cov=src --cov-report=term-missing

# 4. Review your changes
git log origin/main..HEAD
git diff origin/main
```

**Pull Request Checklist:**
- [ ] All tests pass
- [ ] Coverage is maintained or improved (≥66%)
- [ ] Ruff linting passes
- [ ] Mypy type checking passes
- [ ] Bandit security scan passes
- [ ] All functions have type hints
- [ ] All public functions have docstrings

## 12. Project-Specific Patterns

### 12.1 FastAPI Application Patterns

**Database Access:**
```python
from project_name.db import get_db

async def create_user(data: UserCreate) -> User:
    async with get_db() as db:
        return await db.user.create(data=data.model_dump())
```

**Audit Logging:**
```python
from project_name.logging import get_audit_logger, AuditAction

audit = get_audit_logger()
audit.data_access(
    user_id="system",
    resource_type="user",
    resource_id=user.id,
    action=AuditAction.DATA_CREATE,
)
```

**Metrics:**
```python
from project_name.metrics import get_metrics_collector

collector = get_metrics_collector()
collector.record_request(method="POST", endpoint="/users", status_code=201)
```

### 12.2 Prisma ORM Patterns

**Schema Changes:**
```bash
# 1. Edit prisma/schema.prisma
# 2. Generate Python client
uv run prisma generate
# 3. Create migration
uv run prisma migrate dev --name add_feature
```

**JSON Fields:**
```python
# Writing: requires json.dumps()
await db.model.create(data={
    "metadata": json.dumps({"key": "value"})  # String
})

# Reading: returns dict directly
result = await db.model.find_unique(where={"id": id})
result.metadata  # Already a dict
```

### 12.3 Context Managers

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
```

### 12.4 Async Patterns

```python
import asyncio

async def fetch_all_users(user_ids: list[str]) -> list[User]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

## 13. Common Gotchas

### 13.1 Package Management
- ❌ NEVER: `pip install`, `python script.py`
- ✓ ALWAYS: `uv run python script.py`, `uv add package`

### 13.2 Database Client
- ❌ NEVER: Create new `Prisma()` instances
- ✓ ALWAYS: Use `async with get_db() as db:`

### 13.3 Prisma Schema
- ❌ NEVER: Forget to run `uv run prisma generate` after schema changes
- ✓ ALWAYS: Generate client after every schema modification

### 13.4 JSON Fields
- ❌ NEVER: Pass dict directly to Prisma JSON field
- ✓ ALWAYS: Use `json.dumps()` when writing, read returns dict

### 13.5 Test Markers
- ❌ NEVER: Forget `@pytest.mark.integration` for database tests
- ✓ ALWAYS: Mark integration tests properly

### 13.6 Logging Configuration
- ❌ NEVER: Import logging before `configure_logging()` is called
- ✓ ALWAYS: Logging is configured first in `main.py`

### 13.7 Git Operations
- ❌ NEVER: Use `git reset --hard` without explicit approval
- ✓ ALWAYS: Preserve existing changes you didn't make

### 13.8 Coverage
- Current template: 66% (intentional for template code)
- Production projects: Can be raised to 100%

## 14. Presenting Work

### 14.1 Communication Style

**Default:** Concise, friendly coding teammate tone.

**Structure:**
- Use natural language with high-level headings (when helpful)
- For substantial work: lead with quick explanation, then details
- For simple confirmations: skip heavy formatting
- Reference file paths with line numbers: `src/project_name/api/auth.py:42`

### 14.2 Presenting Changes

**Structure:**
1. Quick explanation of what changed
2. Details on where and why
3. Logical next steps (if applicable)

**Example:**
```
Added JWT authentication with Redis session storage.

**Changes:**
- `src/project_name/api/auth.py` - Login, logout, refresh endpoints
- `src/project_name/services/auth.py` - Token generation and validation
- `tests/unit/test_auth.py` - Full test coverage (100%)

**Next steps:**
1. Run `uv run app serve --reload` to test the endpoints
2. Create a migration: `uv run prisma migrate dev --name add_auth`
```

## 15. Code Review Process

### 15.1 Review Checklist

All code reviews MUST verify:
- [ ] Type hints on all functions and attributes
- [ ] Docstrings on all public functions and classes
- [ ] DRY principle followed
- [ ] Naming conventions followed
- [ ] Unit tests with adequate coverage
- [ ] Integration tests for DB/API operations
- [ ] No hardcoded secrets
- [ ] Security analysis passes
- [ ] Linting passes
- [ ] Error handling is comprehensive

### 15.2 Approval Requirements

- At least one reviewer approval required
- All CI/CD checks MUST pass
- All tests MUST pass
- Coverage MUST not decrease
- Security scans MUST pass

## 16. CI/CD Pipeline

### 16.1 Required Stages

1. **Lint** - Run ruff, mypy
2. **Test** - Run pytest with coverage
3. **Security** - Run bandit, safety/pip-audit
4. **Build** - Build Docker image
5. **Deploy** - Deploy to target environment

### 16.2 Pre-merge Requirements

- All CI stages pass
- Code review approved
- Test coverage maintained (≥66%)
- No security vulnerabilities
- Documentation updated if needed

## 17. Environment Variables

**REQUIRED:** Use `pydantic-settings` for configuration.

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

Required variables (in `.env`):
- `DATABASE_URL` - PostgreSQL connection string
- `LOG_LEVEL` - DEBUG, INFO, WARNING, ERROR, CRITICAL
- `ENVIRONMENT` - development, staging, production

## 18. References

**PRDs:**
- PRD 02 (Tech Stack) - Technology stack details
- PRD 03 (Security) - Security requirements

**External:**
- OpenAI Codex Prompting Guide: https://cookbook.openai.com/examples/gpt-5/codex_prompting_guide
- Claude Code Documentation: https://claude.com/claude-code
- Python Style Guide: PEP 8
- Type Hints: PEP 484, PEP 604

**Project Files:**
- `CLAUDE.md` - Project overview for Claude Code
- `AGENTS.md` - Auto-injected agent instructions
- `.claude/skills/` - Custom slash commands
- `prd/tasks/` - Task tracking files
