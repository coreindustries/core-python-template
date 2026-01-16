# CLAUDE.md

Project guidance for Claude Code. **For detailed agent patterns, see `AGENTS.md`.**

## Overview

**Stack:** FastAPI + Typer + Prisma + PostgreSQL + Python 3.13+

## Critical: Use `uv` for Everything

```bash
uv sync                    # Install deps
uv add package             # Add package
uv run python script.py    # Run Python
uv run pytest              # Run tests
uv run app serve           # Start API

# NEVER use: pip install, python script.py
```

## Architecture

**Entry Points:**
- `src/project_name/main.py` - FastAPI app with lifespan manager
- `src/project_name/cli.py` - Typer CLI (`uv run app`)

**Key Patterns:**
- Database: `async with get_db() as db:` (singleton, don't create new Prisma instances)
- Config: `from project_name.config import settings` (pydantic-settings)
- Logging: `get_logger(__name__)` for app, `get_audit_logger()` for security
- Metrics: `get_metrics_collector()` exposed at `/metrics`

**Directory Structure:**
```
src/project_name/
├── main.py, cli.py, config.py  # Entry points + config
├── api/                        # Routes (delegate to services)
├── services/                   # Business logic
├── models/                     # Pydantic request/response
├── db/                         # Database utilities
├── logging/                    # Forensic logging (6 modules)
└── metrics/                    # Prometheus metrics

tests/unit/                     # Fast, no I/O
tests/integration/              # Real database
prisma/schema.prisma            # Database schema (source of truth)
```

## Essential Commands

```bash
# Development
uv run app serve --reload              # Start API
docker-compose up -d postgres redis    # Dependencies

# Database
uv run prisma generate                 # After schema changes (required!)
uv run prisma migrate dev --name x     # Create migration
uv run prisma db push                  # Push without migration (dev)

# Quality (run before commits)
uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/
uv run mypy src/
uv run pytest --cov=src --cov-fail-under=66

# Testing
uv run pytest tests/unit -v            # Unit only
uv run pytest tests/integration        # Integration only
uv run pytest -x                       # Stop on first failure
```

## Code Standards

1. **Type hints** on all functions/attributes/returns
2. **Google-style docstrings** on public functions/classes
3. **66% coverage minimum** (100% for new features)
4. **Modern syntax:** `str | None` not `Optional[str]`
5. **DRY:** Search for existing implementations first

## Prisma Patterns

```python
# Database access (always use context manager)
async with get_db() as db:
    user = await db.user.find_unique(where={"id": user_id})

# JSON fields: dumps() when writing, dict when reading
await db.model.create(data={"metadata": json.dumps({"key": "val"})})
result.metadata  # Already a dict
```

## Testing

- **Unit** (`tests/unit/`): No I/O, mock externals, fast
- **Integration** (`tests/integration/`): Real DB, use fixtures `db`, `integration_client`
- **Markers**: `@pytest.mark.integration`, `@pytest.mark.asyncio`

## Common Gotchas

1. **Run `uv run prisma generate`** after schema changes (client is generated)
2. **JSON fields need `json.dumps()`** when writing to Prisma
3. **Database is singleton** - use `get_db()`, never `Prisma()`
4. **Logging configured first** - `configure_logging()` at top of `main.py`
5. **Test markers required** - `@pytest.mark.integration` for DB tests

## PRDs & Documentation

| Document | Purpose |
|----------|---------|
| `prd/01_Technical_standards.md` | Code quality, typing, naming |
| `prd/02_Tech_stack.md` | Technology decisions |
| `prd/03_Security.md` | OWASP, secrets, audit logging |
| `prd/04_AI_Agent_Development_Standards.md` | Agent patterns (detailed) |
| `AGENTS.md` | Agent quick reference |
| `.claude/skills/` | Slash commands |

## Audit Logging (Security Events)

```python
from project_name.logging import get_audit_logger, AuditAction
audit = get_audit_logger()
audit.auth_success(user_id="123", ip_address="1.2.3.4")
audit.data_access(user_id="123", resource_type="user", action=AuditAction.DATA_READ)
```

## Environment

Required in `.env`: `DATABASE_URL`, `LOG_LEVEL`, `ENVIRONMENT`
See `.env.example` for full list.

## Renaming Template

Replace `project_name` in: `pyproject.toml`, imports in `src/` and `tests/`, `docker-compose.yml`, directory name. Then `uv sync`.
