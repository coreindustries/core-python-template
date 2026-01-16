# AGENTS.md

Quick reference for AI agents. **Full details: `prd/04_AI_Agent_Development_Standards.md`**

## Core Principles

**Autonomy:** Bias to action. Implement with reasonable assumptions rather than requesting clarification.

**Persistence:** Complete tasks end-to-end. Don't stop at plans or partial fixes.

**Quality:** Correctness over speed. No risky shortcuts, tight error handling, DRY principle.

## Efficient Exploration

```python
# BAD: Sequential reads
read("api/routes.py")
read("services/user.py")

# GOOD: Parallel batch (think first, then batch)
read_parallel(["api/routes.py", "services/user.py", "models/user.py"])
```

## Code Standards Quick Reference

- **Type hints** on everything (functions, attributes, returns)
- **Google docstrings** on public functions/classes
- **Modern syntax:** `str | None` not `Optional[str]`, `list[str]` not `List[str]`
- **Error handling:** No broad `except Exception:`, propagate errors explicitly
- **DRY:** Search for existing implementations before creating new

## Quality Check Loop

```bash
# During development (every 15-30 min)
uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/
uv run mypy src/
uv run pytest tests/unit/test_module.py -v

# Before commits
uv run pytest --cov=src --cov-fail-under=66
```

## Project-Specific Patterns

```python
# Database (always context manager, singleton)
async with get_db() as db:
    user = await db.user.find_unique(where={"id": user_id})

# Audit logging
from project_name.logging import get_audit_logger, AuditAction
audit = get_audit_logger()
audit.data_access(user_id="x", resource_type="user", action=AuditAction.DATA_READ)

# JSON fields in Prisma
await db.model.create(data={"metadata": json.dumps({"k": "v"})})  # dumps() required
```

## Git Hygiene

- **Never revert** changes you didn't make
- **Never use** `git reset --hard` without explicit approval
- **Commit format:** `<type>: <description>` with `Co-Authored-By: Claude`

## Context Recovery (After Compression)

1. Read `prd/00_PRD_index.md` → Find "In Progress" features
2. Read `prd/tasks/{feature}_tasks.md` → Load context and progress
3. Review "Next Session Priorities" → Continue where left off
4. Update task file every 30-60 minutes with `/checkpoint`

## Task Tracking

For long-running features:
- Create: `prd/tasks/{feature}_tasks.md` (use template)
- Update: Every 30-60 min or after milestones
- Commit IDs: `[PRD-XX Task Y.Z]` in commit messages

## Common Gotchas

1. Use `uv run` always (never `pip` or bare `python`)
2. Run `uv run prisma generate` after schema changes
3. Use `get_db()` context manager (never create `Prisma()` directly)
4. JSON fields need `json.dumps()` when writing to Prisma
5. Mark integration tests with `@pytest.mark.integration`

## Skills Reference

| Skill | Purpose |
|-------|---------|
| `/new-feature` | Scaffold feature with routes, models, services, tests |
| `/checkpoint` | Update task file with progress |
| `/test` | Run tests with coverage |
| `/refactor` | Safely refactor code |
| `/lint` | Format and check code |

## Deep Reference

- **Full agent standards:** `prd/04_AI_Agent_Development_Standards.md`
- **Task template:** `prd/tasks/TASK_TEMPLATE.md`
- **Code standards:** `prd/01_Technical_standards.md`
- **Security:** `prd/03_Security.md`
