# PRD Index – Python Boilerplate

## Core Infrastructure

- [x] 01_Technical_standards.md - Python technical standards, best practices, and AI agent development patterns
- [x] 02_Tech_stack.md - Python technology stack (FastAPI, Typer, Prisma, PostgreSQL)

## Security

- [x] 03_Security.md - Security scanning and code review system

## Observability

- [ ] 12_Observability_and_Metrics.md - Monitoring and observability standards (TODO)

## Tech Stack Summary

| Component | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| Package Manager | uv |
| API Framework | FastAPI |
| CLI Framework | Typer |
| Database | PostgreSQL + pgvector |
| ORM | Prisma (prisma-client-py) |
| Testing | pytest, pytest-asyncio, pytest-cov |
| Linting | ruff, mypy |
| Security | bandit, safety/pip-audit |
| Containers | Docker, docker-compose |

## Task Tracking

**Task Files Directory:** `prd/tasks/`

For long-running features that span multiple sessions, create task files to track progress and preserve context across context compression events.

**Template:** `prd/tasks/TASK_TEMPLATE.md`

**Example:** `prd/tasks/example_user_auth_tasks.md`

**Active Features (In Progress):**
- None currently (this is a template)

**Completed Features:**
- 01_Technical_standards - Implementation complete (includes AI agent development standards)
- 02_Tech_stack - Implementation complete
- 03_Security - Implementation complete

**How to Use:**
1. Create task file when feature will span >1 session: `prd/tasks/{feature}_tasks.md`
2. Update task file every 30-60 minutes during implementation
3. Reference task file in PRD "Implementation Status" section
4. Use `/checkpoint` skill to update automatically
5. Include task IDs in commits: `[PRD-XX Task Y.Z]`

**Recovery After Context Compression:**
1. Read `prd/00_PRD_index.md` to find "In Progress" features
2. Read corresponding task file: `prd/tasks/{feature}_tasks.md`
3. Review "Next Session Priorities" and "Decisions Made"
4. Continue from last incomplete task

## Implementation Order

1. **Phase 1: Foundation (Complete)**
   - Technical standards (including AI agent patterns) → Tech stack
   - Security scanning system

2. **Phase 2: Core Features**
   - [Add future PRDs as they're created]
   - When creating PRDs, add task file reference and status

3. **Phase 3: Advanced Features**
   - Observability and Metrics
   - [Add future PRDs]
