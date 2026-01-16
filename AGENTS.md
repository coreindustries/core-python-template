# AGENTS.md

This file provides AI agent instructions for working with this Python template. These instructions are automatically injected into coding agent conversations.

## General Approach

- **Bias to action**: Once given direction, proactively gather context, plan, implement, test, and refine without waiting for additional prompts at each step
- **Persist until complete**: Carry tasks through to full implementation, verification, and clear explanation of outcomes
- **Default to implementation with reasonable assumptions**: Don't end with clarifications unless truly blocked
- **Tools over terminal**: Use dedicated tools (`read_file`, `list_dir`, `glob_file_search`, `apply_patch`) instead of shell commands when possible
- **Parallel tool calls**: When multiple tool calls can run independently (file searches, reads), execute them in parallel
- **Think first, then batch**: Before tool calls, decide ALL files needed, then issue one parallel batch

## Code Implementation Standards

### Correctness Over Speed
- Optimize for correctness, clarity, and reliability over implementation speed
- Avoid risky shortcuts and speculative changes
- Cover the root cause, not just symptoms
- Investigate before implementing to ensure full understanding

### Conform to Codebase Conventions
- **Follow existing patterns**: This project uses FastAPI (APIs), Typer (CLI), Prisma (ORM)
- **Package management**: ALWAYS use `uv` commands (`uv run python`, `uv run pytest`, `uv add package`)
- **Never use**: `pip install`, bare `python` commands (will break environment)
- **Database access**: Use `async with get_db() as db:` context manager (singleton pattern)
- **Configuration**: Global `settings` singleton in `src/project_name/config.py`
- **Logging**: Use `get_logger(__name__)` for app logs, `get_audit_logger()` for security events

### Type Safety and Documentation
- **REQUIRED**: Type hints on ALL functions, class attributes, return types
- **REQUIRED**: Google-style docstrings on ALL public functions/classes
- Use modern Python syntax: `str | None` not `Optional[str]`, `list[str]` not `List[str]`
- Run `uv run mypy src/` frequently during development

### DRY Principle
- Search for existing implementations before creating new helpers
- Extract common functionality into reusable functions
- Reuse existing patterns from the codebase
- If you find duplication, refactor it

### Tight Error Handling
- No broad try/catch blocks or silent failures
- Propagate errors explicitly rather than swallowing them
- No early-return on invalid input without logging
- Use specific exception types, create custom exceptions for domain errors

### Efficient Edits
- Read enough context before changing files
- Batch logical edits together instead of many tiny patches
- Use `apply_patch` for single-file edits (model is trained on this format)
- For auto-generated files or bulk search-replace, scripting may be more efficient

## Exploration and File Reading

**Think first, batch everything:**
1. Decide ALL files/resources needed before ANY tool call
2. If you need multiple files, read them together in parallel
3. Only make sequential calls if you truly cannot know the next file without seeing a result first
4. Maximize parallelism always

**Pattern:**
- Plan all needed reads → issue one parallel batch → analyze results → repeat only if new, unpredictable reads arise
- This applies to: `rg`, `ls`, `git show`, `cat`, file reads, searches

## Testing Requirements

### Coverage Standards
- **Minimum**: 66% test coverage (configured in pyproject.toml)
- **Target**: 100% test coverage for new features
- Run tests frequently: `uv run pytest tests/unit/test_<module>.py -v`
- Check coverage: `uv run pytest --cov=src --cov-fail-under=66`

### Test Types
- **Unit tests** (`tests/unit/`): Fast tests, no I/O, mock external dependencies
- **Integration tests** (`tests/integration/`): Real PostgreSQL, API tests with AsyncClient
- Mark integration tests: `@pytest.mark.integration`
- Use `@pytest.mark.asyncio` for async tests

### Test-Driven Development
- Write tests alongside or before implementation
- Ensure tests exist before refactoring
- Run full test suite before committing: `uv run pytest`

## Database and Prisma Patterns

### Schema Changes
1. Edit `prisma/schema.prisma`
2. Run `uv run prisma generate` (regenerates Python client)
3. Create migration: `uv run prisma migrate dev --name add_feature`
4. Or push directly in dev: `uv run prisma db push`

### JSON Fields
- Writing: Requires `json.dumps()` for dict → string
  ```python
  await db.embedding.create(data={
      "content": "text",
      "metadata": json.dumps({"key": "value"})  # String required
  })
  ```
- Reading: Returns dict directly (no parsing needed)

### Database Access Pattern
```python
from project_name.db import get_db

async def get_user(user_id: str) -> User | None:
    async with get_db() as db:
        return await db.user.find_unique(where={"id": user_id})
```

## Security and Audit Logging

### Security Events
Log all security-relevant events via audit logger:
```python
from project_name.logging import get_audit_logger, AuditAction

audit = get_audit_logger()

# Authentication
audit.auth_success(user_id="123", ip_address="1.2.3.4")
audit.auth_failure(identifier="user@example.com", reason="invalid_password")

# Data access
audit.data_access(user_id="123", resource_type="user", action=AuditAction.DATA_READ)

# Security alerts
audit.security_alert(alert_type="brute_force", ip_address="1.2.3.4")
```

### Security Practices
- Never hardcode secrets (use `.env` and `pydantic-settings`)
- Validate input at API boundaries
- Run security scan before commits: `uv run bandit -r src/`
- Check dependency vulnerabilities: `uv run pip-audit`
- Review PRD 03 (Security) for OWASP Top 10 requirements

## Git and Version Control

### Editing Constraints
- You may be in a dirty git worktree
- **NEVER revert existing changes you didn't make** unless explicitly requested
- If there are unrelated changes in files, ignore them and don't revert
- If you see unexpected changes you didn't make, STOP and ask the user
- **NEVER use destructive commands** like `git reset --hard` or `git checkout --` without approval
- Don't amend commits unless explicitly requested

### Commit Guidelines
When creating commits:
1. Run quality checks first: `uv run ruff check --fix src/ tests/`
2. Run type check: `uv run mypy src/`
3. Run tests: `uv run pytest --cov=src --cov-fail-under=66`
4. Use conventional commit format:
   ```
   <type>: <description>

   <body (optional)>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```
5. Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Plans and TODOs

### When to Use Plans
- Skip planning for straightforward tasks (easiest ~25%)
- Do not make single-step plans
- Never end with only a plan (plans guide edits, working code is the deliverable)

### Plan Discipline
- Update plan after completing each sub-task
- Before finishing, reconcile every TODO: mark as Done, Blocked (with reason + question), or Cancelled (with reason)
- Do not end with in_progress/pending items
- Avoid committing to tests/refactors unless doing them now
- Label optional work as "Next steps" and exclude from committed plan

### Plan Updates
- For plan updates, only update via plan tool
- Don't message the user mid-turn about your plan

## Quality Checks During Development

**Run frequently (every 15-30 minutes):**
```bash
# Linting and formatting
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Type checking
uv run mypy src/

# Run specific test file
uv run pytest tests/unit/test_<module>.py -v

# Coverage check
uv run pytest --cov=src --cov-fail-under=66
```

**Benefits of frequent checks:**
- Prevents error accumulation
- Immediate feedback for easier debugging
- Smaller change sets
- Reduces pre-commit hook failures

## Pre-Commit Requirements

Before EVERY commit, run full quality suite:
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

All checks MUST pass before committing.

## PRD-Driven Development

### Required Reading
Before implementing features:
1. **PRD 01 (Technical Standards)**: Code quality, typing, naming, and AI agent development patterns
2. **PRD 02 (Tech Stack)**: Technology decisions and justifications
3. **PRD 03 (Security)**: Security requirements and OWASP Top 10 compliance

### Implementation Workflow
1. Read relevant PRDs first
2. Understand dependencies on other PRDs
3. Follow patterns from PRD 01
4. Use security patterns from PRD 03
5. Create new PRD for significant features using `PRD_TEMPLATE.md`

## Special Patterns for This Project

### FastAPI Application Initialization
- Logging configured FIRST in `main.py` (before imports that use logging)
- Database initialized on startup via `lifespan()` context manager
- Middleware stack: Prometheus Metrics → Request Logging → CORS
- Global instances: `_db` (database), audit logger, metrics collector

### Metrics Collection
```python
from project_name.metrics import get_metrics_collector

collector = get_metrics_collector()
collector.record_ai_request(
    provider="openai",
    model="gpt-4",
    operation="chat",
    duration=0.5,
    prompt_tokens=100,
    completion_tokens=50,
)
```

### Service Layer Pattern
```python
from project_name.services import BaseService

class UserService(BaseService[User, UserCreate, UserUpdate]):
    async def get_by_id(self, entity_id: str) -> User | None:
        async with get_db() as db:
            result = await db.user.find_unique(where={"id": entity_id})
            return User.model_validate(result) if result else None
```

### File References
When referencing files in responses:
- Use inline code to make paths clickable: `src/app.ts:42`
- Use absolute, workspace-relative, or bare filename paths
- Optionally include line/column (1-based): `:line[:column]` or `#Lline[Ccolumn]`
- Examples: `src/app.ts`, `src/app.ts:42`, `main.rs:12:5`

## Common Commands

```bash
# Development
uv run app serve --reload         # Start API with auto-reload
uv run app info                   # Show current config

# Database
uv run prisma generate            # Generate Python client
uv run prisma migrate dev --name add_feature  # Create migration
uv run prisma db push             # Push schema (dev only)
uv run prisma studio              # Open database GUI

# Testing
uv run pytest                     # All tests
uv run pytest tests/unit          # Unit tests only
uv run pytest tests/integration   # Integration tests
uv run pytest -x                  # Stop on first failure
uv run pytest --cov=src --cov-report=term-missing

# Code quality
uv run ruff check src/ tests/     # Lint
uv run ruff check --fix src/      # Auto-fix
uv run ruff format src/           # Format
uv run mypy src/                  # Type check
uv run bandit -r src/             # Security scan

# Dependencies
uv sync                           # Install dependencies
uv add package-name               # Add package
uv add --dev package-name         # Add dev dependency
```

## Context Compression Recovery

When starting a new session on an in-progress feature (after context compression or in a new conversation):

### Startup Protocol

1. **Identify Active Work:**
   ```bash
   # Read PRD index to find "In Progress" features
   Read: prd/00_PRD_index.md
   ```

2. **Load Task State (Parallel Read):**
   ```bash
   # Read all in parallel
   Read in parallel:
     - prd/tasks/{feature}_tasks.md        # Current progress and next steps
     - prd/{XX}_{Feature_Name}.md          # Feature requirements
     - Key files listed in tasks.md        # Implementation files
   ```

3. **Review Context:**
   - Check "Next Session Priorities" section in tasks.md
   - Review "Decisions Made" to understand architectural choices
   - Check "Blockers" for any known issues
   - Note current task marked as "IN PROGRESS"

4. **Continue Work:**
   - Start from the first incomplete task in "Next Session Priorities"
   - Mark task as "IN PROGRESS" in tasks.md
   - Implement the task following all standards
   - Update tasks.md after each milestone

5. **Checkpoint Regularly:**
   - Update tasks.md every 30-60 minutes
   - Mark tasks as complete when done
   - Add new decisions to "Decisions Made"
   - Update "Next Session Priorities" before ending session

### Task File Structure

All long-running features should have a task file:
- **Location:** `prd/tasks/{feature_name}_tasks.md`
- **Template:** `prd/tasks/TASK_TEMPLATE.md`
- **Example:** `prd/tasks/example_user_auth_tasks.md`

### When to Create Task Files

Create a task file when:
- Feature will span multiple sessions
- Feature has >5 distinct tasks
- Feature is marked "In Progress" in PRD index
- Feature requires context preservation across sessions

### Checkpoint Command

Use `/checkpoint` skill to update task file automatically during implementation.

## Common Gotchas

1. **Always run `uv run prisma generate`** after schema changes (Python client is generated code)
2. **JSON fields require `json.dumps()`** when writing, but return dicts when reading
3. **Database client is singleton** - don't create new `Prisma()` instances, use `get_db()`
4. **Logging must be configured first** - `configure_logging()` called at top of `main.py`
5. **Test markers**: Use `@pytest.mark.integration` for tests requiring database
6. **Coverage is 66%** - this is intentional for template, can be raised to 100% for real projects
7. **Use `uv run` prefix** - never use bare `python` or `pip` commands

## Presenting Work

- Default: concise, friendly coding teammate tone
- Use natural language with high-level headings when helpful
- For substantial work, summarize clearly with structure
- Skip heavy formatting for simple confirmations
- Don't dump large files you've written, reference paths only
- Offer logical next steps briefly (tests, commits, build)
- Lead with quick explanation of changes, then details on context
- Use numeric lists for multiple suggestions (user can respond with number)

## Review Requests

If user asks for a "review":
- Default to code review mindset
- Prioritize: bugs, risks, behavioral regressions, missing tests
- Findings FIRST (ordered by severity with file:line references)
- Then: open questions or assumptions
- Change summary as secondary detail
- If no findings: state explicitly, mention residual risks/testing gaps
