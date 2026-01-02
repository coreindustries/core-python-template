---
prd_version: "2.0"
status: "Active"
last_updated: "2025-01-02"
---

# 02 – Tech Stack (Python Focused)

## 1. Language & Runtime

### 1.1 Python 3.12+

- Primary language for all backend services, workers, APIs, and CLI tools
- Uses `asyncio` for I/O concurrency and process pools for CPU-bound work
- **REQUIRED:** All Python code MUST use type hints (typed Python)
- Use `mypy` for static type checking

### 1.2 Package Manager: uv

- **uv** is the ONLY supported package manager
- Fast dependency management and reproducible environments
- **CRITICAL:** ALWAYS USE `uv` TO INSTALL PACKAGES AND RUN PYTHON
- **NEVER** install Python packages to the host OS Python environments
- For all scripts, prompts, and tests: use `uv run`

```bash
# Install dependencies
uv sync

# Run Python scripts
uv run python script.py

# Run tests
uv run pytest

# Add a dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name
```

## 2. Database

### 2.1 PostgreSQL

- Used for all structured data
- Local: Dockerized PostgreSQL instance
- Cloud: Any managed PostgreSQL (RDS, Cloud SQL, Aurora, Supabase, etc.)

### 2.2 pgvector Extension

- Used to store and query embeddings for semantic search
- Enables vector similarity search operations
- Required for AI/ML features involving embeddings

### 2.3 Redis (Optional)

- Used for caching when needed
- Cache strategy:
  - All APIs should first check Redis for values
  - Request fresh data if not found or stale
  - TTL-based cache invalidation
  - If TTL = 0, always request from source

## 3. ORM and Schema Management

### 3.1 Prisma (Schema Source of Truth)

- `schema.prisma` defines all database models
- `prisma migrate` manages migrations against PostgreSQL
- Prisma provides type-safe database access

### 3.2 Python Database Access

- **Primary:** Use `prisma-client-py` for Prisma integration
- **Alternative:** SQLAlchemy/SQLModel models that mirror Prisma schema
- Both approaches maintain compatibility with the Prisma schema

```python
# Using prisma-client-py
from prisma import Prisma

async def get_user(user_id: str) -> User | None:
    db = Prisma()
    await db.connect()
    user = await db.user.find_unique(where={"id": user_id})
    await db.disconnect()
    return user
```

## 4. API Framework

### 4.1 FastAPI

- Primary framework for REST APIs
- Automatic OpenAPI documentation
- Native async support
- Pydantic for request/response validation

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: UserCreate) -> dict:
    # Implementation
    return {"id": "123", **user.model_dump()}
```

## 5. CLI Framework

### 5.1 Typer

- Primary framework for CLI tools
- Type hints for argument parsing
- Automatic help generation
- Rich integration for beautiful output

```python
import typer
from rich import print

app = typer.Typer()

@app.command()
def greet(name: str, count: int = 1) -> None:
    """Greet someone by name."""
    for _ in range(count):
        print(f"[green]Hello, {name}![/green]")

if __name__ == "__main__":
    app()
```

## 6. Environment Variables

### 6.1 Requirements

**REQUIRED:** All services MUST use `python-dotenv` for environment variable management.

- Load environment variables at application startup using `load_dotenv()`
- Ignore `.env` and `.environment` in git, Cursor, and Claude
- Validate required environment variables at startup and fail fast

### 6.2 Best Practices

- Never hardcode environment variables in source code
- Use `.env.example` to document required variables (without values)
- Keep `.env`, `.environment`, `.env.local` in `.gitignore`
- Load environment variables once at startup, not per-module
- Use Pydantic Settings for type-safe configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str | None = None
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

## 7. Containerization

### 7.1 Docker Setup

Each component runs as a separate Docker image:

- **postgres** - PostgreSQL with pgvector
- **redis** - Redis cache (optional)
- **app** - Python application

### 7.2 Local Development

- `docker-compose.yml` for local orchestration
- Dev containers for consistent environments
- Volume mounts for hot reloading

```yaml
# Example docker-compose.yml structure
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  app:
    build: .
    depends_on:
      - postgres
      - redis
```

## 8. Testing

### 8.1 Test Framework

- **pytest** - Primary test framework
- **pytest-asyncio** - Async test support
- **pytest-cov** - Coverage reporting
- **httpx** - Async HTTP client for API testing

### 8.2 Coverage Requirements

- 100% unit test coverage required
- Integration tests for all database operations
- E2E tests for critical API flows

## 9. Code Quality Tools

| Tool | Purpose |
|------|---------|
| `ruff` | Linting and formatting (replaces flake8, black, isort) |
| `mypy` | Static type checking |
| `bandit` | Security vulnerability scanning |
| `safety` / `pip-audit` | Dependency vulnerability scanning |
| `pre-commit` | Git hooks for quality checks |

## 10. Project Structure

```
project-root/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py           # FastAPI app entry point
│       ├── cli.py            # CLI entry point
│       ├── api/              # API routes
│       ├── models/           # Pydantic models
│       ├── services/         # Business logic
│       ├── db/               # Database utilities
│       └── utils/            # Shared utilities
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── scripts/                  # Utility scripts
├── prisma/
│   └── schema.prisma
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```
