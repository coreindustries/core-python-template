# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Python template** for building production-ready applications with AI-assisted development in mind. The template is designed to work optimally with Cursor and Claude Code through PRD-driven development, custom skills, hooks, and enforced code standards.

**Core stack:** FastAPI (APIs) + Typer (CLI) + Prisma (ORM) + PostgreSQL + Python 3.13+

## Critical: Package Management

**ALWAYS use `uv` - NEVER use `pip` or bare `python` commands:**

```bash
# Correct
uv sync                    # Install dependencies
uv add package-name        # Add new package
uv run python script.py    # Run Python
uv run pytest              # Run tests
uv run app serve           # Start API server

# INCORRECT - will break environment
pip install x              # NO
python script.py           # NO
```

## Architecture

### Application Initialization Flow

1. **`main.py`** - FastAPI app with lifespan manager
   - Logging configured FIRST (before any imports that use logging)
   - Database client initialized on startup via `lifespan()` context manager
   - Middleware stack: Request Logging → Prometheus Metrics → CORS
   - Global instances: `_db` (database), audit logger, metrics collector

2. **Database Access Pattern**
   - **Global singleton**: `_db` in `src/project_name/db/__init__.py`
   - **Connection managed via**: `get_db_client()` (startup) and `close_db_client()` (shutdown)
   - **In routes/services**: Use `get_db()` context manager for queries
   ```python
   async with get_db() as db:
       user = await db.user.find_unique(where={"id": user_id})
   ```
   - Prisma client is generated code (not in version control) - always run `uv run prisma generate` after schema changes

3. **Configuration System**
   - **Single source**: `src/project_name/config.py` using `pydantic-settings`
   - Environment variables loaded from `.env` (not committed)
   - Global `settings` singleton created at module import time
   - Settings are immutable after initialization

4. **Logging Architecture**
   - **Two separate loggers**:
     - Application logger: `get_logger(__name__)` for general logs
     - Audit logger: `get_audit_logger()` for security events
   - Configured in `logging/config.py` with forensic requirements:
     - Correlation IDs for request tracing
     - Automatic sensitive data masking (passwords, tokens, etc.)
     - JSON structured output for production
   - Middleware injects correlation ID into all requests

5. **Metrics Collection**
   - **Prometheus format** via `metrics/collector.py`
   - Global singleton: `get_metrics_collector()`
   - Middleware automatically records: request count, latency, in-progress requests
   - Custom metrics via `collector.record_request()` and `collector.record_ai_request()`
   - Exposed at `/metrics` endpoint

### Directory Structure Logic

```
src/project_name/
├── main.py              # FastAPI app + lifespan
├── cli.py               # Typer CLI (entry point: `uv run app`)
├── config.py            # Settings (loaded from .env)
├── api/
│   ├── routes.py        # Main API routes
│   └── metrics.py       # /metrics endpoint
├── models/              # Pydantic models (request/response)
├── services/            # Business logic (NOT API handlers)
├── db/                  # Database connection utilities
├── logging/             # Forensic logging system (6 modules)
│   ├── config.py        # Logger configuration
│   ├── audit.py         # Security event logging
│   ├── middleware.py    # Request logging middleware
│   ├── context.py       # Correlation ID context
│   └── formatters.py    # JSON/text formatters
└── metrics/             # Prometheus metrics (3 modules)
    ├── collector.py     # Metric definitions
    ├── middleware.py    # Auto-instrumentation
    └── config.py        # Metrics settings

tests/
├── unit/                # Fast tests, no I/O
└── integration/         # Tests with database
    └── conftest.py      # Fixtures for db + HTTP client
```

**Key patterns:**
- **Routes** (`api/`) handle HTTP, delegate to **services** for logic
- **Services** contain business logic, use `get_db()` for data access
- **Models** define request/response shapes (Pydantic), NOT database models
- **Database schema** is in `prisma/schema.prisma` (Prisma models, not Python)

## Common Commands

### Development Workflow
```bash
# Setup (first time)
uv sync
cp .env.example .env
docker-compose up -d postgres redis
uv run prisma generate
uv run prisma db push  # Or: uv run prisma migrate deploy

# Daily development
uv run app serve --reload         # Start API at http://localhost:8000
uv run app info                   # Show current config
docker-compose up -d postgres redis  # Start dependencies

# Before committing
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
uv run mypy src/
uv run pytest --cov=src --cov-fail-under=66
```

### Testing
```bash
uv run pytest                     # All tests
uv run pytest tests/unit          # Unit tests only
uv run pytest tests/integration   # Integration tests only
uv run pytest tests/unit/test_config.py::test_settings_load -v  # Single test
uv run pytest -x                  # Stop on first failure
uv run pytest --cov=src --cov-report=term-missing  # With coverage
uv run pytest -m "not slow"       # Skip slow tests
```

### Database
```bash
uv run prisma generate            # Generate Python client (after schema changes)
uv run prisma migrate dev --name add_users  # Create migration
uv run prisma migrate deploy      # Apply migrations (production)
uv run prisma db push             # Push schema without migration (dev only)
uv run prisma studio              # Open database GUI
```

### Code Quality
```bash
uv run ruff check src/ tests/     # Lint
uv run ruff check --fix src/      # Auto-fix linting issues
uv run ruff format src/           # Format code
uv run mypy src/                  # Type check
uv run bandit -r src/             # Security scan
```

## Code Standards (Enforced)

1. **Type hints required** on all functions, class attributes, return types
2. **Google-style docstrings** required on all public functions/classes
3. **66% test coverage** minimum (configured in `pyproject.toml`)
4. **mypy strict mode** - no `Any` types without justification
5. **Modern Python syntax**: `str | None` not `Optional[str]`, `list[str]` not `List[str]`

### Example: Proper Function Definition
```python
async def get_user(user_id: str, include_deleted: bool = False) -> User | None:
    """Retrieve a user by ID.

    Args:
        user_id: Unique identifier for the user.
        include_deleted: Whether to include soft-deleted users.

    Returns:
        User object if found, None otherwise.

    Raises:
        ValidationError: If user_id format is invalid.
    """
    async with get_db() as db:
        return await db.user.find_unique(where={"id": user_id})
```

## PRD-Driven Development

All features should reference PRDs in `prd/` directory:

- **`prd/01_Technical_standards.md`** - Code quality requirements (DRY, typing, naming)
- **`prd/02_Tech_stack.md`** - Technology decisions and justifications
- **`prd/03_Security.md`** - Security requirements (OWASP Top 10, secrets, audit logging)
- **`prd/PRD_TEMPLATE.md`** - Template for new feature PRDs

### PRD Branching Workflow

Each PRD is developed on its own dedicated branch for isolated development and focused code reviews:

```
main ──────────────────────────────────────────────────────────►
       │                                    ▲
       │ create prd branch                  │ merge PR
       ▼                                    │
prd/04-user-authentication ────────────────►│
       │                              ▲     │
       │ create feature branch        │     │
       ▼                              │     │
feat/user_profile ───────────────────►│     │
```

**Branch naming conventions:**
- PRD branches: `prd/{number}-{title-kebab-case}` (e.g., `prd/04-user-authentication`)
- Feature branches: `feat/{feature_name}` (e.g., `feat/user_profile`)

**Workflow steps:**
1. Create a PRD branch: `/new-prd 04 "User Authentication"`
2. Develop features on the PRD branch: `/new-feature user_profile --prd 04`
3. Features target their parent PRD branch for PRs
4. PRD branch merges to `main` when complete

### When implementing features:
1. Read relevant PRDs first
2. Follow patterns in PRD 01 (Technical Standards)
3. Use security patterns from PRD 03
4. Create new PRD for significant features using `/new-prd`

## Prisma ORM Patterns

### Schema Definition (`prisma/schema.prisma`)
- Source of truth for database structure
- **After changing schema**: `uv run prisma generate` (regenerates Python client)
- **JSON fields**: Prisma requires JSON strings, not dicts:
  ```python
  # Correct
  await db.embedding.create(data={
      "content": "text",
      "metadata": json.dumps({"key": "value"})  # String
  })

  # Reading returns dict directly
  found = await db.embedding.find_unique(where={"id": id})
  found.metadata  # Already a dict
  ```

### Vector Column Pattern (pgvector)
- Vector columns added via raw SQL migration (in `prisma/migrations/add_vector_column.sql`)
- Prisma doesn't support vector type natively
- Access via raw queries: `await db.query_raw(...)`

## Testing Patterns

### Unit Tests (`tests/unit/`)
- No database, no network I/O
- Mock external dependencies
- Fast execution (< 1s total)

### Integration Tests (`tests/integration/`)
- Use real PostgreSQL (from `docker-compose`)
- Fixtures in `conftest.py`:
  - `db`: Connected Prisma client
  - `integration_client`: AsyncClient for API tests
- Database setup: `uv run prisma db push` before running tests
- Cleanup: Tests should clean up created data (or use transactions)

### Example: Integration Test
```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user(db: Prisma) -> None:
    """Test user creation."""
    user = await db.user.create(data={"email": "test@example.com"})
    assert user.id is not None

    # Cleanup
    await db.user.delete(where={"id": user.id})
```

## CLI Entry Point

The CLI is defined in `src/project_name/cli.py` and exposed as `app` command:

```bash
uv run app --help          # Show all commands
uv run app serve           # Start FastAPI server
uv run app serve --reload  # With auto-reload
uv run app info            # Show configuration
```

**To add new CLI commands**: Add functions to `cli.py` with `@app.command()` decorator.

## Environment Variables

Required variables (in `.env`):
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection (optional)
- `LOG_LEVEL` - DEBUG, INFO, WARNING, ERROR, CRITICAL
- `ENVIRONMENT` - development, staging, production

See `.env.example` for full list and defaults.

## Forensic Security Logging

All security-relevant events must be logged via audit logger:

```python
from project_name.logging import get_audit_logger, AuditAction, SecurityEvent

audit = get_audit_logger()

# Authentication events
audit.auth_success(user_id="123", ip_address="1.2.3.4")
audit.auth_failure(identifier="user@example.com", reason="invalid_password")

# Data access
audit.data_access(user_id="123", resource_type="user", action=AuditAction.DATA_READ)

# Security alerts
audit.security_alert(alert_type="brute_force", ip_address="1.2.3.4")
```

Logs include:
- Correlation IDs (automatic, per-request)
- Sensitive data masking (automatic for passwords, tokens, API keys)
- Structured JSON format for aggregation
- Separate audit log file for compliance

## Docker & Observability

```bash
# Minimal setup (just databases)
docker-compose up -d postgres redis

# Full observability stack
docker-compose up -d  # Includes Prometheus, Grafana, Loki, Jaeger

# Access services
# - API: http://localhost:8000
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
# - Jaeger: http://localhost:16686
```

Observability config in `observability/` directory - see `observability/README.md` for details.

## Common Gotchas

1. **Always run `uv run prisma generate` after changing schema** - the Python client is generated code
2. **JSON fields in Prisma require `json.dumps()`** when writing, but return dicts when reading
3. **Database client is a singleton** - don't create new `Prisma()` instances, use `get_db()`
4. **Logging must be configured before other imports** - `configure_logging()` called at top of `main.py`
5. **Test markers**: Use `@pytest.mark.integration` for tests requiring database
6. **Coverage set to 66%** - this is intentional, template has example code not fully tested

## When Renaming This Template

Search and replace `project_name` with your actual project name in:
- `pyproject.toml` (`[project]` section and `[project.scripts]`)
- All imports in `src/` and `tests/`
- `docker-compose.yml` (service names)
- Rename `src/project_name/` directory

Then: `uv sync` to regenerate lockfile.
