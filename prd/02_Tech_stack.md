# 02 – Tech Stack

## 1. Backend

### 1.1 Language & Runtime

- **Python 3.12+**
  - Primary language for market data workers (data ingestion, regime detection, strategy execution, alert monitoring).
  - Uses `asyncio` for I/O concurrency and process pools for CPU‑bound work.
- **uv** (package manager)
  - Fast dependency management and reproducible environments.
  - ALWAYS USE UV TO INSTALL PACKAGES AND RUN PYTHON
  - NEVER INSTALL PYTHON PACKAGES TO THE HOST OS PYTHON ENVIRONMENTS
  - CRITICAL: for all scripts, prompts and tests use uv.

### 1.2 Database

- **PostgreSQL**
  - Used for all structured data.
  - Local: Dockerized Postgres instance.
  - Cloud: Any managed Postgres (RDS, Cloud SQL, Aurora, etc.).
- **pgvector extension**

  - Used to store and query embeddings for the semantic layer.

- **Redis**
  - Used for caching
  - All APIs should first check redis for values, request fresh data if not found or stale
  - all apis should have a TTL value, if 0, then request from the source api provider and cache
  - if a number > 0, store the data in redis for that number of seconds. Don't request from the api provider if cache is still valid

### 1.3 ORM and Schema Management

- **Prisma** (Node‑based) as the source of truth for the schema:
  - `schema.prisma` defines all models.
  - `prisma migrate` manages migrations against Postgres.
  - Prisma client is used from the API/Next.js backend.
- Python may:
  - Use Prisma Client Python (where viable), or
  - Use SQLAlchemy/SQLModel models that mirror the Prisma schema.

### 1.4 Environment variables

- **dotenv** (python) use this library for accessing env vars in all python modules
  - ignore .envionrment in all github, cursor, and claude calls, since it includes sensitive data
  - add other protections to this file as required by best practices and our security standards

## 2. Frontend

### 2.1 Framework

- **Next.js (App Router)**
  - Renders dashboards and configuration UIs.
  - Can host API routes or talk to a separate API service.
  - Deployed as a standalone container.

### 2.2 UI Component System

- **shadcn/ui**
  - Tailwind‑based accessible UI primitives.
  - Used for:
    - Navigation and layout.
    - Tables (pages, issues, results).
    - Cards and metrics panels.
    - Forms (scan and project configuration).
    - Modals, sheets, and toasts.

Defined in detail in `12-Observability-and-Metrics.md` (TODO: Create this PRD).

## 4. Containerization

- Each component runs as a separate Docker image:

  - Postgres
  - Redis
  - backend python
  - web interface

- Local orchestration: `docker-compose.yml`.
