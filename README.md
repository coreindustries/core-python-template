# Core Python Template

[![CI](https://github.com/coreindustries/core-python-template/actions/workflows/ci.yml/badge.svg)](https://github.com/coreindustries/core-python-template/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A batteries-included Python boilerplate optimized for AI-assisted development with **Cursor** and **Claude Code**.

## Why This Template?

Modern AI coding assistants work best when they have clear context, enforced standards, and guardrails. This template provides:

- **PRD-driven development** — Start by writing Product Requirements Documents (PRDs), then using planning tools (in Cursor or Claude Code) to implement them. We have a basic set of technical standards, security best practices and observability built in.
- **AI-assisted development** — Claude acts as a senior engineer, reviewing code against documented requirements
- **AI-aware tooling** — Skills (slash commands), hooks, and subagents purpose-built for Claude Code
- **Enforced consistency** — Type hints, docstrings, and 100% test coverage aren't optional
- **Security by default** — Sensitive file protection, audit logging, and automated scanning

### The 80/20 Workflow

In practice, ~80% of feature development happens in Cursor with AI assistance:

1. **You** write PRDs describing what you want
2. **Cursor** Plan mode to build a plan for 1 PRD at a time, and then implements features following the documented standards
3. **Claude** Periodically, use claude to review Cursor's work via subagents (code review, security audit, PRD compliance)
4. **You** review, iterate, and approve

The remaining 20% is architecture decisions, edge cases, and the creative work that benefits from human judgment.

## What's Included

### Tech Stack

| Component       | Technology                            |
| --------------- | ------------------------------------- |
| Language        | Python 3.12+ with strict typing       |
| Package Manager | uv (fast, modern)                     |
| API Framework   | FastAPI                               |
| CLI Framework   | Typer + Rich                          |
| Database        | PostgreSQL + Prisma ORM               |
| Caching         | Redis (optional)                      |
| Testing         | pytest (100% coverage required)       |
| Quality         | ruff, mypy strict, bandit, pre-commit |
| Containers      | Docker + docker-compose               |

### AI Development Features

| Feature                 | Purpose                                                   |
| ----------------------- | --------------------------------------------------------- |
| `CLAUDE.md`             | Instructions Claude follows for this codebase             |
| `.claude/settings.json` | Hooks, skills, and subagent definitions                   |
| `.claude/skills/`       | Slash commands (`/new-feature`, `/test`, `/review`, etc.) |
| `prd/`                  | Product requirement documents Claude references           |
| Forensic logging        | Audit trail for security-sensitive operations             |

### Project Standards

| Requirement                 | Enforcement              |
| --------------------------- | ------------------------ |
| Type hints on all functions | mypy strict mode         |
| Google-style docstrings     | ruff rules               |
| 100% test coverage          | pytest-cov fail-under    |
| No secrets in code          | detect-secrets + hooks   |
| Consistent formatting       | ruff format + pre-commit |

## Who Should Use This

**Good fit:**

- You're building APIs, CLIs, or backend services in Python
- You use Cursor, Claude Code, or similar AI coding assistants
- You want guardrails that keep AI-generated code consistent and secure
- You prefer PRD-driven development over ad-hoc feature requests
- You value strict typing, testing, and documentation

**Not a good fit:**

- You need a minimal/lightweight starter (this is opinionated and batteries-included)
- You're building data science notebooks or ML pipelines (consider a data-focused template)
- You don't use AI coding assistants (the `.claude/` tooling won't benefit you)
- You prefer Django, Flask, or other frameworks over FastAPI

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose
- Git

### Setup

```bash
# Clone or use as template
git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT.git
cd YOUR_PROJECT

# Install dependencies
uv sync

# Copy environment file
cp .env.example .env

# Start database and observability services
docker-compose up -d postgres redis prometheus grafana loki

# Or start just databases for minimal setup
# docker-compose up -d postgres redis

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
│   ├── logging/          # Forensic security logging
│   └── utils/            # Helper functions
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── prisma/               # Database schema
│   └── schema.prisma
├── prd/                  # Product Requirements Documents
├── .claude/              # AI automation configuration
│   ├── settings.json     # Hooks and agent definitions
│   ├── skills/           # Slash command definitions
│   └── hooks/            # Hook scripts
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

### Observability & Monitoring

Full observability stack with metrics, logs, and traces:

```bash
# Start observability services
docker-compose up -d prometheus grafana loki promtail jaeger

# Access dashboards
open http://localhost:3000  # Grafana (admin/admin)
open http://localhost:9090  # Prometheus
open http://localhost:16686 # Jaeger
```

**Services:**

- **Prometheus** (`:9090`) - Metrics collection
- **Grafana** (`:3000`) - Visualization dashboards
- **Loki** (`:3100`) - Log aggregation
- **Jaeger** (`:16686`) - Distributed tracing

**What's monitored:**

- HTTP request rates, latency, errors
- In-flight request counts
- AI token usage (if enabled)
- Application logs (JSON structured)
- Custom business metrics

See [observability/README.md](observability/README.md) for detailed documentation.

## Configuration

Configuration is managed via environment variables. See `.env.example` for all options.

| Variable       | Description                  | Default   |
| -------------- | ---------------------------- | --------- |
| `DATABASE_URL` | PostgreSQL connection string | Required  |
| `REDIS_URL`    | Redis connection string      | Optional  |
| `DEBUG`        | Enable debug mode            | `false`   |
| `LOG_LEVEL`    | Logging level                | `INFO`    |
| `API_HOST`     | API bind host                | `0.0.0.0` |
| `API_PORT`     | API bind port                | `8000`    |

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

## Customizing This Template

### Initial Setup

1. **Rename the package**: Replace `project_name` with your actual project name

   ```bash
   # Rename directory
   mv src/project_name src/your_project

   # Update all imports (Claude can help with this)
   # Update pyproject.toml name and scripts
   ```

2. **Update metadata** in `pyproject.toml`:

   - Project name, description, authors
   - Repository URLs
   - License if not MIT

3. **Configure your database**:
   - Edit `prisma/schema.prisma` with your models
   - Run `uv run prisma generate`

### Starting Development with AI

The recommended workflow for new features:

1. **Write a PRD first** — Use `/new-prd` or copy `prd/PRD_TEMPLATE.md`

   ```bash
   # In Claude Code
   /new-prd 04 "User Authentication"
   ```

2. **Let Claude implement** — Reference the PRD in your prompt

   ```
   Implement the user authentication feature described in prd/04_User_Authentication.md
   ```

3. **Review with subagents** — Claude can self-review

   ```
   Review this implementation against the PRD requirements
   Run a security audit on the auth module
   ```

4. **Iterate** — Fix issues, run tests, repeat

### Adding Features Manually

If working without AI assistance:

- Add routes in `src/your_project/api/`
- Add Pydantic models in `src/your_project/models/`
- Add business logic in `src/your_project/services/`
- Add tests in `tests/unit/` and `tests/integration/`
- Run quality checks: `uv run ruff check && uv run mypy src/`

## AI Automations

This boilerplate includes AI-assisted development workflows for Claude Code.

### Skills (Slash Commands)

| Command          | Description                                                             |
| ---------------- | ----------------------------------------------------------------------- |
| `/new-feature`   | Scaffold a complete feature with routes, models, services, and tests    |
| `/new-prd`       | Create a PRD document from template                                     |
| `/security-scan` | Run comprehensive security analysis (bandit, pip-audit, detect-secrets) |
| `/db-migrate`    | Safe database migration workflow with safety checks                     |
| `/test`          | Run tests with coverage and quality gates                               |
| `/lint`          | Run ruff and mypy checks with auto-fix options                          |
| `/review`        | Code review against PRD standards                                       |

### Hooks

**Pre-tool hooks** run before Claude takes actions:

- **sensitive-file-guard** - Blocks modifications to `.env`, secrets, credentials, and key files
- **production-db-guard** - Warns before database migrations in production

**Post-tool hooks** run after Claude completes actions:

- **test-reminder** - Reminds to run tests after source file changes
- **security-scan-reminder** - Reminds to scan after adding dependencies

### Subagents

Specialized agents available for specific tasks:

| Agent              | Purpose                                        |
| ------------------ | ---------------------------------------------- |
| `code-reviewer`    | Review code against project standards          |
| `security-auditor` | Perform security analysis against OWASP Top 10 |
| `test-generator`   | Generate pytest tests with 100% coverage goal  |
| `prd-compliance`   | Check implementations against PRD requirements |

### Configuration

AI automation settings are in `.claude/settings.json`. Skills are defined in `.claude/skills/`.

## Forensic Security Logging

Built-in structured logging with security features:

```python
from project_name.logging import get_logger, AuditLogger, correlation_id

# Standard logging with correlation
logger = get_logger(__name__)
logger.info("Processing request", extra={"user_id": user.id})

# Security audit events
audit = AuditLogger()
audit.auth_success(user_id="123", ip_address="192.168.1.1")
audit.access_denied(user_id="123", resource_type="admin", resource_id="panel")
audit.security_alert(alert_type="brute_force", severity="high", details={...})
```

Features:

- **JSON structured output** - Machine-parseable logs for SIEM integration
- **Correlation IDs** - Track requests across services
- **Sensitive data masking** - Automatic redaction of passwords, tokens, keys
- **Audit trail** - Security events with full context
- **Request middleware** - Automatic HTTP request/response logging

## Documentation

- [Technical Standards](prd/01_Technical_standards.md) - Code quality requirements
- [Tech Stack](prd/02_Tech_stack.md) - Technology choices and rationale
- [Security](prd/03_Security.md) - Security requirements and scanning
- [AI Instructions](CLAUDE.md) - Guide for AI coding assistants

## License

MIT License - see LICENSE file for details.
