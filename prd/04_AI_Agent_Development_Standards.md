---
prd_version: "1.0"
status: "Active"
last_updated: "2026-01-15"
---

# 04 – AI Agent Development Standards

## 1. Purpose

This document establishes standards and best practices for AI-assisted development in this codebase, specifically optimized for Claude Code and other coding agents. These standards are inspired by OpenAI's Codex-Max prompting patterns and adapted for Python/FastAPI development.

**Goals:**
- Enable autonomous, efficient AI agent workflows
- Maintain code quality while maximizing agent productivity
- Ensure consistency between human and AI-generated code
- Leverage agent capabilities for exploration, implementation, and testing

**Dependencies:**
- PRD 01 (Technical Standards) - All technical standards apply to AI-generated code
- PRD 02 (Tech Stack) - Agents must use approved technologies
- PRD 03 (Security) - Security requirements apply to all code

## 2. Core Agent Principles

### 2.1 Autonomy and Persistence

**REQUIRED:** Agents MUST operate autonomously and persist until tasks are fully complete.

**Autonomous Senior Engineer Mindset:**
- Once given direction, proactively gather context, plan, implement, test, and refine
- No waiting for additional prompts at each step
- Complete tasks end-to-end within a single turn whenever feasible
- Bias to action: default to implementing with reasonable assumptions

**Persistence Criteria:**
- Don't stop at analysis or partial fixes
- Carry changes through implementation, verification, and clear explanation
- Continue until working code is delivered, not just a plan
- Only pause if explicitly redirected or truly blocked

**Anti-patterns:**
- Stopping after creating a plan without implementing
- Requesting clarification on details that can be reasonably inferred
- Implementing halfway and asking "should I continue?"
- Excessive looping on the same files without progress

### 2.2 Bias to Action

**REQUIRED:** Agents MUST default to implementation over clarification.

**When to Implement Immediately:**
- Requirements are reasonably clear (even if some details missing)
- Multiple valid approaches exist (choose the most standard one)
- Implementation patterns exist in the codebase
- Missing details can be inferred from context

**When to Ask Questions:**
- Critical architectural decisions with significant tradeoffs
- Conflicting requirements that need resolution
- Truly blocked on external information
- User preference matters significantly and isn't inferrable

**Example Decision Tree:**
```
User: "Add user authentication"
├─ API approach? → JWT (standard for FastAPI, matches existing patterns)
├─ Password hashing? → bcrypt (industry standard, already in dependencies)
├─ Session storage? → Redis (already configured in docker-compose.yml)
└─ IMPLEMENT with these defaults ✓

User: "Add payment processing"
├─ Provider? → Could be Stripe, PayPal, Square... → ASK ✓
```

## 3. Code Implementation Standards for Agents

### 3.1 Correctness Over Speed

**REQUIRED:** Agents MUST prioritize correctness, clarity, and reliability over implementation speed.

**Quality Criteria:**
- Cover the root cause or core ask, not just symptoms
- Avoid risky shortcuts and speculative changes
- Investigate before implementing to ensure understanding
- No messy hacks just to get code working

**Discerning Engineer Approach:**
- Read enough context before changing files
- Understand existing patterns and follow them
- Consider edge cases and error paths
- Write production-ready code, not just "working" code

### 3.2 Comprehensiveness and Completeness

**REQUIRED:** Agents MUST ensure changes are comprehensive across all relevant surfaces.

**What This Means:**
- If adding a feature to the API, ensure it works in all relevant contexts
- Update related services, models, tests, and documentation
- Wire changes between layers (API → Service → Database)
- Ensure behavior stays consistent across the application

**Example:**
```
Task: Add "archived" status to users

Incomplete (❌):
- Only add field to database schema

Complete (✓):
- Add field to Prisma schema
- Generate migration
- Update UserCreate/UserUpdate Pydantic models
- Add filtering in UserService.list_all()
- Add query param to API endpoint
- Update tests for archived users
- Add audit logging for archive action
```

### 3.3 Behavior-Safe Defaults

**REQUIRED:** Agents MUST preserve intended behavior and UX.

**Rules:**
- Don't change existing behavior without explicit request
- Gate intentional behavior changes with feature flags or configuration
- Add tests when behavior shifts
- Document behavioral changes in commit messages

**Safe vs Unsafe Changes:**
```python
# UNSAFE: Changes default behavior
async def get_users(include_deleted: bool = True):  # Was False
    # Now includes deleted users by default!

# SAFE: Preserves existing behavior
async def get_users(include_deleted: bool = False, include_archived: bool = False):
    # New parameter with safe default
```

### 3.4 Tight Error Handling

**REQUIRED:** Agents MUST NOT add broad exception catches or silent defaults.

**What to Avoid:**
- Broad `try/except` blocks that swallow errors
- Catching `Exception` without re-raising or logging
- Success-shaped fallbacks that hide failures
- Early returns on invalid input without logging

**Correct Pattern:**
```python
# BAD: Silent failure
async def get_user(user_id: str) -> User | None:
    try:
        return await db.user.find_unique(where={"id": user_id})
    except Exception:
        return None  # What happened? Why did it fail?

# GOOD: Explicit error handling
async def get_user(user_id: str) -> User:
    try:
        user = await db.user.find_unique(where={"id": user_id})
        if not user:
            raise UserNotFoundError(user_id)
        return user
    except PrismaClientKnownRequestError as e:
        logger.error(f"Database error fetching user {user_id}: {e}")
        raise DatabaseError(f"Failed to fetch user: {user_id}") from e
```

### 3.5 Efficient, Coherent Edits

**REQUIRED:** Agents MUST batch logical edits together, not make repeated micro-edits.

**Best Practices:**
- Read enough context before changing a file
- Make all related changes in one pass
- Avoid thrashing with many tiny patches to the same file
- Use `apply_patch` tool for single-file edits (agents are trained on this format)

**When to Use Different Approaches:**
- `apply_patch`: Single file, targeted changes
- Scripting: Auto-generated files (package.json), bulk search-replace
- Formatting tools: `gofmt`, `ruff format`, etc. (not manual edits)

## 4. Exploration and File Reading Patterns

### 4.1 Think First, Batch Everything

**REQUIRED:** Agents MUST plan all file reads before executing, then batch them in parallel.

**Pattern:**
1. **Think**: Decide ALL files/resources needed
2. **Batch**: Read all files together in one parallel call
3. **Analyze**: Process results
4. **Repeat**: Only if new, unpredictable reads are needed

**Anti-pattern:**
```python
# BAD: Sequential reads
read(api/routes.py)
# ... analyze ...
read(services/user.py)
# ... analyze ...
read(models/user.py)
# ... analyze ...

# GOOD: Parallel batch
read_parallel([
    "api/routes.py",
    "services/user.py",
    "models/user.py"
])
# ... analyze all together ...
```

### 4.2 Maximize Parallelism

**REQUIRED:** Always read files in parallel unless logically unavoidable.

**Applies To:**
- File reads (`cat`, `read_file`)
- File searches (`rg`, `glob_file_search`)
- Directory listings (`ls`, `list_dir`)
- Git operations (`git show`)

**Only Sequential If:**
- You truly cannot know the next file without seeing a result first
- Example: Reading a config file to determine which modules to load next

## 5. Testing Standards for Agents

### 5.1 Test Coverage Requirements

**REQUIRED for New Features:**
- Minimum 66% coverage (project standard)
- Target 100% coverage for production-ready features
- Write tests alongside or before implementation

**Test Types:**
```python
# Unit test (fast, no I/O)
class TestEmailValidator:
    def test_valid_email(self) -> None:
        assert validate_email("user@example.com") is True

# Integration test (real database)
@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user_endpoint(integration_client: AsyncClient) -> None:
    response = await integration_client.post("/users", json={...})
    assert response.status_code == 201
```

### 5.2 Test-Driven Development Pattern

**REQUIRED when refactoring:** Ensure tests exist before modifying code.

**Pattern:**
1. Verify tests exist and pass
2. Make changes
3. Verify tests still pass
4. Add new tests for new behavior
5. Verify coverage hasn't decreased

**Commands to Run Frequently:**
```bash
# After writing a function
uv run pytest tests/unit/test_module.py::test_function -v

# Check coverage
uv run pytest --cov=src --cov-fail-under=66

# Full test suite before commit
uv run pytest
```

## 6. Plan and TODO Management

### 6.1 When to Create Plans

**Skip Plans For:**
- Straightforward tasks (easiest ~25% of work)
- Single-step changes
- Obvious fixes

**Create Plans For:**
- Multi-step features
- Complex refactorings
- Cross-cutting changes
- Tasks requiring coordination across multiple files

### 6.2 Plan Discipline

**REQUIRED:** Plans MUST be reconciled before finishing a task.

**Plan Lifecycle:**
1. Create plan with clear steps
2. Update plan after completing each step (mark as Done)
3. Before finishing, ensure every item is:
   - **Done**: Completed successfully
   - **Blocked**: With one-sentence reason and targeted question
   - **Cancelled**: With reason for cancellation
4. No in_progress or pending items when finishing

**Promise Discipline:**
- Don't commit to tests/refactors unless doing them NOW
- Label optional work as "Next steps" (excluded from committed plan)
- Don't create TODOs for work you won't do immediately

### 6.3 Deliverable is Working Code

**REQUIRED:** Never end with only a plan.

**Correct Flow:**
```
User: "Add user authentication"
Agent:
1. Creates plan (internal, using plan tool)
2. Implements authentication
3. Tests implementation
4. Presents working code with explanation
5. Optionally suggests next steps
```

**Incorrect Flow:**
```
User: "Add user authentication"
Agent:
1. Creates plan
2. Shows plan to user
3. Asks "Should I proceed?" ❌
```

## 7. Git and Version Control Patterns

### 7.1 Working with Dirty Worktrees

**REQUIRED:** Agents MUST preserve existing changes not made by them.

**Rules:**
- **NEVER revert changes you didn't make** unless explicitly requested
- Unrelated changes in files → ignore them, don't revert
- Changes in files you've touched recently → read carefully, work with them
- Unexpected changes you didn't make → STOP and ask user

**Safe Commands:**
```bash
git status               # Check current state
git diff                 # See what changed
git diff --cached        # See staged changes
git log -5               # Recent commits
```

**NEVER Use Without Approval:**
```bash
git reset --hard         # Destroys all changes
git checkout --          # Discards specific file changes
git clean -fd            # Removes untracked files
```

### 7.2 Commit Message Standards

**REQUIRED Format:**
```
<type>: <description>

<body (optional)>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Example:**
```
feat: add user authentication with JWT

Implements JWT-based authentication with Redis session storage.
Includes login, logout, and token refresh endpoints with full
test coverage and audit logging.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 7.3 Commit Hygiene

**Before Every Commit:**
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

**All checks MUST pass before committing.**

## 8. Quality Checks During Development

### 8.1 Frequent Check Pattern

**REQUIRED:** Run quality checks every 15-30 minutes during active development.

**Benefits:**
- Prevents error accumulation (50% less debugging time)
- Immediate feedback on smaller change sets
- Easier to identify which change caused issues
- Reduces pre-commit hook failures (40% less frustration)

**Quick Check Commands:**
```bash
# After writing/modifying a file
uv run ruff check src/project_name/module.py
uv run ruff format src/project_name/module.py

# After writing type hints
uv run mypy src/project_name/module.py

# After writing tests
uv run pytest tests/unit/test_module.py -v
```

### 8.2 IDE Integration

**Recommended:** Configure editor to run checks on save.

**VS Code Settings:**
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "ruff",
  "editor.formatOnSave": true,
  "python.linting.mypyEnabled": true
}
```

## 9. PRD-Driven Development for Agents

### 9.1 Reading PRDs

**REQUIRED Before Implementation:**
1. Read PRD 01 (Technical Standards) - always
2. Read PRD 02 (Tech Stack) - for technology choices
3. Read PRD 03 (Security) - for security-relevant features
4. Read PRD 04 (AI Agent Standards) - this document
5. Read feature-specific PRD if it exists

**Check Dependencies:**
- Every PRD has a "Dependencies" section
- Read referenced PRDs for context and consistency
- Ensure implementation aligns with dependencies

### 9.2 Creating New PRDs

**When to Create PRD:**
- Significant new features (>3 files)
- Architectural changes
- New external integrations
- Security-relevant features

**Use `PRD_TEMPLATE.md` as starting point.**

## 10. Task Tracking for Long-Running Features

### 10.1 Purpose

Long-running features that span multiple sessions require persistent task tracking to survive context compression. Task files provide:
- **Context preservation**: Key decisions and architectural choices documented
- **Progress tracking**: Clear visibility into what's done and what's next
- **Session continuity**: Agents can resume work exactly where they left off
- **Accountability**: Audit trail of implementation progress

### 10.2 When to Create Task Files

Create a task file (`prd/tasks/{feature}_tasks.md`) when:
- Feature will span multiple agent sessions
- Feature has >5 distinct tasks
- Feature is marked "In Progress" in PRD index
- Context compression is likely before completion

### 10.3 Task File Structure

**Location:** `prd/tasks/{feature_name}_tasks.md`

**Template:** Use `prd/tasks/TASK_TEMPLATE.md` as starting point

**Key Sections:**
1. **Context** - High-level overview and key decisions (critical for recovery)
2. **Tasks** - Hierarchical checklist with phase grouping
3. **Progress Summary** - Percentage complete per phase
4. **Blockers** - Current and resolved blockers
5. **Key Files** - File paths with line numbers
6. **Decisions Made** - Architectural decisions with rationale
7. **Technical Notes** - Patterns, dependencies, security considerations
8. **Next Session Priorities** - What to do immediately when resuming
9. **Session Log** - Brief notes from each session
10. **Git Commits** - Commit references with task IDs

### 10.4 Task File Maintenance

**During Implementation:**
```bash
# Every 30-60 minutes or after significant milestones:
1. Mark completed tasks with [x]
2. Update "IN PROGRESS" marker to current task
3. Add new decisions to "Decisions Made"
4. Update "Next Session Priorities"
5. Add session log entry
```

**Use `/checkpoint` skill** to update task file automatically.

### 10.5 Context Compression Recovery

**When starting a new session:**

1. **Identify active work:**
   ```bash
   Read: prd/00_PRD_index.md  # Find "In Progress" features
   ```

2. **Load task state (parallel):**
   ```bash
   Read in parallel:
     - prd/tasks/{feature}_tasks.md
     - prd/{XX}_{Feature_Name}.md
     - Key files from tasks.md
   ```

3. **Resume work:**
   - Start from "Next Session Priorities"
   - Review "Decisions Made" for context
   - Check "Blockers" for issues
   - Mark current task as "IN PROGRESS"

### 10.6 Task ID Format

**In Commits:**
```bash
git commit -m "feat: add JWT token generation [PRD-04 Task 1.5]"
```

**Format:** `[PRD-{XX} Task {Phase}.{Number}]`

**Benefits:**
- Traceability from git history to task file
- Easy to reconstruct progress from commits
- Links implementation to requirements

### 10.7 Integration with PRD Index

**In PRD:**
```markdown
## Implementation Status

**Task Tracker:** `prd/tasks/04_user_auth_tasks.md`
**Status:** In Progress (Phase 1: 60% complete)
**Last Updated:** 2026-01-15
```

**In Task File:**
```markdown
**PRD:** `prd/04_User_Authentication.md`
```

### 10.8 Example Task Files

- **Template:** `prd/tasks/TASK_TEMPLATE.md`
- **Example:** `prd/tasks/example_user_auth_tasks.md`

### 10.9 Best Practices

**Do:**
- ✅ Update task file every 30-60 minutes during active development
- ✅ Include context in "Decisions Made" (critical after compression)
- ✅ Use "Next Session Priorities" for easy resumption
- ✅ Reference files with line numbers (`file.py:42`)
- ✅ Track blockers prominently
- ✅ Include task IDs in git commits

**Don't:**
- ❌ Let task file get stale (update regularly)
- ❌ Skip "Context" section (most important for recovery)
- ❌ Mark tasks complete before they're fully done
- ❌ Forget to update "Next Session Priorities" when ending session
- ❌ Mix multiple features in one task file

### 10.10 Alternative Approaches

**JSON Task State (optional):**
```json
// For programmatic access
{
  "prd": "04_User_Authentication",
  "status": "in_progress",
  "phase": 1,
  "current_task": "Implement JWT token refresh",
  "tasks": {"completed": [...], "pending": [...]}
}
```

**Git Commit Breadcrumbs:**
- Include task IDs in commits for traceability
- Reconstruct progress from git log if needed

**Checkpoint Comments in Code:**
```python
# AGENT_CHECKPOINT: 2026-01-15 - JWT generation done, refresh logic next
```

## 11. Presenting Work to Users

### 10.1 Communication Style

**Default:** Concise, friendly coding teammate tone.

**Structure:**
- Use natural language with high-level headings (when helpful)
- For substantial work: lead with quick explanation, then details
- For simple confirmations: skip heavy formatting
- Reference file paths only (don't dump large files)

**File References:**
```
# Clickable references with line numbers
Updated user authentication in `src/project_name/api/auth.py:42`
Added test coverage in `tests/unit/test_auth.py:128`
Modified schema in `prisma/schema.prisma:15`
```

### 10.2 Presenting Changes

**Structure:**
1. Quick explanation of what changed
2. Details on where and why
3. Logical next steps (if applicable)
4. Use numeric lists for multiple options

**Example:**
```
Added JWT authentication with Redis session storage.

**Changes:**
- `src/project_name/api/auth.py` - Login, logout, refresh endpoints
- `src/project_name/services/auth.py` - Token generation and validation
- `src/project_name/models/auth.py` - Request/response schemas
- `tests/unit/test_auth.py` - Full test coverage (100%)

**Next steps:**
1. Run `uv run app serve --reload` to test the endpoints
2. Create a migration: `uv run prisma migrate dev --name add_auth`
3. Update environment variables for JWT secret (see .env.example)
```

### 10.3 Code Review Responses

**If User Asks for "Review":**
- Prioritize: bugs, risks, behavioral regressions, missing tests
- **Findings FIRST** (ordered by severity with file:line references)
- Then: open questions or assumptions
- Change summary as secondary detail
- If no findings: state explicitly, mention residual risks

## 11. Project-Specific Agent Patterns

### 11.1 FastAPI Application Patterns

**Database Access:**
```python
from project_name.db import get_db

async def create_user(data: UserCreate) -> User:
    async with get_db() as db:
        return await db.user.create(data=data.model_dump())
```

**Audit Logging:**
```python
from project_name.logging import get_audit_logger, AuditAction

audit = get_audit_logger()
audit.data_access(
    user_id="system",
    resource_type="user",
    resource_id=user.id,
    action=AuditAction.DATA_CREATE,
)
```

**Metrics:**
```python
from project_name.metrics import get_metrics_collector

collector = get_metrics_collector()
collector.record_request(method="POST", endpoint="/users", status_code=201)
```

### 11.2 Prisma ORM Patterns

**Schema Changes:**
```bash
# 1. Edit prisma/schema.prisma
# 2. Generate Python client
uv run prisma generate
# 3. Create migration
uv run prisma migrate dev --name add_feature
```

**JSON Fields:**
```python
# Writing: requires json.dumps()
await db.model.create(data={
    "metadata": json.dumps({"key": "value"})  # String
})

# Reading: returns dict directly
result = await db.model.find_unique(where={"id": id})
result.metadata  # Already a dict
```

### 11.3 Service Layer Pattern

**Base Service Usage:**
```python
from project_name.services import BaseService
from project_name.models.user import User, UserCreate, UserUpdate

class UserService(BaseService[User, UserCreate, UserUpdate]):
    async def get_by_id(self, entity_id: str) -> User | None:
        async with get_db() as db:
            result = await db.user.find_unique(where={"id": entity_id})
            return User.model_validate(result) if result else None
```

## 12. Common Agent Gotchas

### 12.1 Package Management
- ❌ NEVER: `pip install`, `python script.py`
- ✓ ALWAYS: `uv run python script.py`, `uv add package`

### 12.2 Database Client
- ❌ NEVER: Create new `Prisma()` instances
- ✓ ALWAYS: Use `async with get_db() as db:`

### 12.3 Prisma Schema
- ❌ NEVER: Forget to run `uv run prisma generate` after schema changes
- ✓ ALWAYS: Generate client after every schema modification

### 12.4 JSON Fields
- ❌ NEVER: Pass dict directly to Prisma JSON field
- ✓ ALWAYS: Use `json.dumps()` when writing, read returns dict

### 12.5 Test Markers
- ❌ NEVER: Forget `@pytest.mark.integration` for database tests
- ✓ ALWAYS: Mark integration tests properly

### 12.6 Logging Configuration
- ❌ NEVER: Import logging before `configure_logging()` is called
- ✓ ALWAYS: Logging is configured first in `main.py`

### 12.7 Git Operations
- ❌ NEVER: Use `git reset --hard` without explicit approval
- ✓ ALWAYS: Preserve existing changes you didn't make

### 12.8 Coverage
- Current template: 66% (intentional for template code)
- Production projects: Can be raised to 100%

## 13. References

**PRDs:**
- PRD 01 (Technical Standards) - Code quality requirements
- PRD 02 (Tech Stack) - Technology stack details
- PRD 03 (Security) - Security requirements

**External:**
- OpenAI Codex Prompting Guide: https://cookbook.openai.com/examples/gpt-5/codex_prompting_guide
- Claude Code Documentation: https://claude.com/claude-code
- Anthropic Agent SDK: https://github.com/anthropics/anthropic-sdk-python

**Project Files:**
- `CLAUDE.md` - Project overview for Claude Code
- `AGENTS.md` - Auto-injected agent instructions
- `.claude/skills/` - Custom slash commands
- `.claude/agents/` - Custom agent definitions
