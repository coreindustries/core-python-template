# Python Project Boilerplate

A production-ready Python boilerplate with FastAPI, Typer, Prisma, and best practices baked in.

## Features

- **FastAPI** - Modern async REST API framework
- **Typer** - Beautiful CLI interface
- **Prisma** - Type-safe database access with prisma-client-py
- **PostgreSQL + pgvector** - Database with vector search support
- **Redis** - Optional caching layer
- **uv** - Fast Python package management
- **Docker** - Containerized development and deployment
- **100% Type Coverage** - Strict mypy configuration
- **Full Test Suite** - pytest with async support
- **CI/CD Ready** - GitHub Actions workflow included
- **Pre-commit Hooks** - Automated code quality checks

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/your-project.git
cd your-project

# Install dependencies
uv sync

# Copy environment file
cp .env.example .env

# Start database services
docker-compose up -d postgres redis

# Generate Prisma client
uv run prisma generate

# Run database migrations
uv run prisma migrate deploy

# Start the development server
uv run app serve --reload
```

### Verify Installation

```bash
# Check the API
curl http://localhost:8000/health

# Run tests
uv run pytest

# Run linting
uv run ruff check src/
```

## Project Structure

```
.
├── src/project_name/     # Application source code
│   ├── main.py           # FastAPI application
│   ├── cli.py            # Typer CLI
│   ├── config.py         # Configuration management
│   ├── api/              # API routes
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   ├── db/               # Database utilities
│   └── utils/            # Helper functions
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── prisma/               # Database schema
│   └── schema.prisma
├── scripts/              # Utility scripts
├── prd/                  # Product Requirements Documents
├── .github/workflows/    # CI/CD pipelines
├── pyproject.toml        # Python project configuration
├── docker-compose.yml    # Docker services
├── Dockerfile            # Container build
└── CLAUDE.md             # AI assistant instructions
```

## Development

### Commands

```bash
# Install dependencies
uv sync

# Run API server (with hot reload)
uv run app serve --reload

# Run CLI
uv run app --help
uv run app info

# Run tests
uv run pytest
uv run pytest --cov=src --cov-report=html

# Linting and formatting
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run ruff check --fix src/

# Type checking
uv run mypy src/

# Security scanning
uv run bandit -r src/
uv run pip-audit
```

### Pre-commit Hooks

```bash
# Install hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

### Database

```bash
# Generate Prisma client
uv run prisma generate

# Create migration
uv run prisma migrate dev --name migration_name

# Apply migrations
uv run prisma migrate deploy

# Open Prisma Studio
uv run prisma studio
```

### Docker

```bash
# Start all services
docker-compose up

# Start only database services
docker-compose up -d postgres redis

# Build production image
docker build --target production -t app:latest .

# Run production container
docker run -p 8000:8000 app:latest
```

## Configuration

Configuration is managed via environment variables. See `.env.example` for all options.

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Optional |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `API_HOST` | API bind host | `0.0.0.0` |
| `API_PORT` | API bind port | `8000` |

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=100

# Run specific tests
uv run pytest tests/unit/test_config.py -v

# Run with parallel execution
uv run pytest -n auto
```

## Customizing This Boilerplate

When using this boilerplate for a new project:

1. **Rename the package**: Replace `project_name` with your actual project name
   - Update `src/project_name/` directory name
   - Update imports in all files
   - Update `pyproject.toml` project name and scripts

2. **Update configuration**:
   - Edit `pyproject.toml` with your project details
   - Update `.env.example` with your required variables
   - Modify `docker-compose.yml` service names if needed

3. **Define your data model**:
   - Edit `prisma/schema.prisma` with your models
   - Run `uv run prisma generate` to create the client

4. **Implement your features**:
   - Add routes in `src/project_name/api/`
   - Add models in `src/project_name/models/`
   - Add services in `src/project_name/services/`

5. **Write tests**:
   - Add unit tests in `tests/unit/`
   - Add integration tests in `tests/integration/`

## Documentation

- [Technical Standards](prd/01_Technical_standards.md) - Code quality requirements
- [Tech Stack](prd/02_Tech_stack.md) - Technology choices and rationale
- [Security](prd/03_Security.md) - Security requirements and scanning
- [AI Instructions](CLAUDE.md) - Guide for AI coding assistants

## License

MIT License - see LICENSE file for details.
