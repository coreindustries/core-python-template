# Claude Code Instructions

## Project Overview

This is a **Python-focused boilerplate** for building production-ready applications with:

- **FastAPI** for REST APIs
- **Typer** for CLI tools
- **Prisma** (prisma-client-py) for database access
- **PostgreSQL** with pgvector for vector embeddings
- **Redis** for caching (optional)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Package Manager | uv (ALWAYS use uv, never pip) |
| API Framework | FastAPI |
| CLI Framework | Typer |
| Database | PostgreSQL + pgvector |
| ORM | Prisma (prisma-client-py) |
| Validation | Pydantic |
| Testing | pytest, pytest-asyncio, pytest-cov |
| Linting | ruff (replaces black, flake8, isort) |
| Type Checking | mypy (strict mode) |
| Security | bandit, pip-audit |
| Containers | Docker, docker-compose |

## Critical Rules

### Package Management

```bash
# ALWAYS use uv
uv sync                    # Install dependencies
uv add package-name        # Add dependency
uv run python script.py    # Run Python
uv run pytest              # Run tests

# NEVER do this
pip install x              # NO!
python script.py           # NO - use uv run
```

### Code Standards

1. **Type hints required** on ALL functions and class attributes
2. **Docstrings required** on all public functions/classes (Google style)
3. **100% test coverage** required
4. **ruff** for linting and formatting
5. **mypy strict mode** for type checking

### File Organization

```
src/project_name/       # Source code
├── main.py             # FastAPI app
├── cli.py              # Typer CLI
├── config.py           # Settings (pydantic-settings)
├── api/                # API routes
├── models/             # Pydantic models
├── services/           # Business logic
├── db/                 # Database utilities
└── utils/              # Helpers
tests/                  # Test files
├── unit/               # Unit tests
└── integration/        # Integration tests
scripts/                # Utility scripts
prisma/                 # Prisma schema
prd/                    # Product Requirements Documents
```

### Environment Variables

- Use `pydantic-settings` for configuration
- Store in `.env` file (never commit)
- Document in `.env.example`
- Load once at startup via `config.py`

### Database

- Prisma schema is source of truth: `prisma/schema.prisma`
- Generate client: `uv run prisma generate`
- Run migrations: `uv run prisma migrate deploy`
- Use async client from `project_name.db`

### Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=term-missing

# Specific test
uv run pytest tests/unit/test_config.py -v
```

### Docker

```bash
# Start services (Postgres, Redis)
docker-compose up -d postgres redis

# Run app in container
docker-compose up app

# Full stack
docker-compose up
```

## PRD-Driven Development

All features must follow PRDs in the `prd/` directory:

- `prd/01_Technical_standards.md` - Code standards and best practices
- `prd/02_Tech_stack.md` - Technology stack details
- `prd/03_Security.md` - Security requirements
- `prd/PRD_TEMPLATE.md` - Template for new PRDs

## Common Patterns

### FastAPI Route

```python
from fastapi import APIRouter, HTTPException, status
from project_name.models import UserCreate, User
from project_name.services import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate) -> User:
    """Create a new user."""
    service = UserService()
    return await service.create(data)
```

### Pydantic Model

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
```

### Database Query

```python
from project_name.db import get_db

async def get_user(user_id: str) -> User | None:
    async with get_db() as db:
        return await db.user.find_unique(where={"id": user_id})
```

### CLI Command

```python
import typer
from rich import print

app = typer.Typer()

@app.command()
def greet(name: str) -> None:
    """Greet someone."""
    print(f"[green]Hello, {name}![/green]")
```

## When Making Changes

1. **Read existing code first** - Understand patterns before modifying
2. **Follow existing conventions** - Match the codebase style
3. **Write tests** - 100% coverage required
4. **Run checks** before committing:
   ```bash
   uv run ruff check src/ tests/
   uv run ruff format src/ tests/
   uv run mypy src/
   uv run pytest
   ```
5. **Update documentation** if adding new patterns

## Useful Commands

```bash
# Development
uv sync                              # Install deps
uv run app serve                     # Start API server
uv run app info                      # Show config
docker-compose up -d postgres redis  # Start services

# Quality
uv run ruff check --fix src/         # Lint and fix
uv run ruff format src/              # Format
uv run mypy src/                     # Type check
uv run bandit -r src/                # Security scan

# Database
uv run prisma generate               # Generate client
uv run prisma migrate dev            # Create migration
uv run prisma migrate deploy         # Apply migrations

# Testing
uv run pytest                        # Run tests
uv run pytest -x                     # Stop on first failure
uv run pytest --cov=src              # With coverage
```

## Skills (Slash Commands)

This project includes custom skills for common workflows:

| Skill | Description | Usage |
|-------|-------------|-------|
| `/new-feature` | Scaffold a new feature with routes, models, services, tests | `/new-feature user_profile --with-db` |
| `/new-prd` | Create a new PRD from template | `/new-prd 04 "User Authentication"` |
| `/security-scan` | Run comprehensive security analysis | `/security-scan --fix` |
| `/db-migrate` | Manage Prisma migrations | `/db-migrate create --name add_users` |
| `/test` | Run tests with coverage | `/test --coverage` |
| `/lint` | Run linting and type checking | `/lint --fix` |
| `/review` | Review code against standards | `/review --security` |

### Skill Details

**`/new-feature <name> [--with-db] [--crud]`**
- Creates: `api/{name}.py`, `models/{name}.py`, `services/{name}.py`, `tests/unit/test_{name}.py`
- Adds Prisma model if `--with-db`
- Registers router automatically

**`/security-scan [--fix] [--ci]`**
- Runs: bandit, pip-audit, ruff security rules, detect-secrets
- Generates security report with severity ratings
- CI mode outputs JSON for pipeline integration

**`/review [target] [--prd <num>] [--security]`**
- Checks against PRD 01 standards
- Reports: type coverage, docstrings, naming, tests
- Security focus checks OWASP Top 10

## Hooks

Automated hooks for quality and security:

| Hook | Trigger | Action |
|------|---------|--------|
| Sensitive file guard | Edit/Write to .env, secrets | Blocks modification |
| Test reminder | Edit src/**/*.py | Reminds to run tests |
| Security scan reminder | uv add | Suggests security scan |
| Production DB guard | prisma migrate in prod | Requires confirmation |

## Subagents

Available task agents for complex operations:

| Agent | Use Case | Invoke With |
|-------|----------|-------------|
| `code-reviewer` | Review changes against standards | Task tool |
| `security-auditor` | Deep security analysis | Task tool |
| `test-generator` | Generate tests for new code | Task tool |
| `prd-compliance` | Check PRD requirements | Task tool |

## Forensic Security Logging

All operations are logged for audit:

```python
from project_name.logging import get_audit_logger, AuditAction

audit = get_audit_logger()

# Log authentication
audit.auth_success(user_id="123", ip_address="1.2.3.4")
audit.auth_failure(identifier="user@example.com", reason="invalid_password")

# Log data access
audit.data_access(user_id="123", resource_type="user", action=AuditAction.DATA_READ)

# Log security events
audit.security_alert(alert_type="brute_force", ip_address="1.2.3.4")
```

Logs include:
- Correlation IDs for request tracing
- Automatic sensitive data masking
- JSON structured output for log aggregation
- Separate audit.log for security events
