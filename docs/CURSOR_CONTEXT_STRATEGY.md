# Cursor Context Strategy

This document explains how Cursor manages context for AI features and how to optimize it for better AI assistance.

## Understanding Context in Cursor

Cursor uses **context** to understand your codebase and provide accurate AI suggestions. Context includes:
- **Indexed files**: Files that are analyzed and searchable
- **Open files**: Files currently open in the editor
- **Chat history**: Previous conversation context
- **Project structure**: Directory organization and file relationships

## Two Types of Ignore Files

### `.cursorignore` (Security & Privacy)

**Purpose**: Prevents files from being **sent to AI models**

**When to use**: For sensitive data that should NEVER reach AI servers

**Examples**:
- Environment files (`.env`, `.env.local`)
- Secrets (`.pem`, `.key`, credentials)
- Logs with PII (audit logs, user data)
- Database dumps

**Impact**: Files in `.cursorignore` are completely excluded from AI features (autocomplete, chat, etc.)

### `.cursorindexingignore` (Performance)

**Purpose**: Prevents files from being **indexed for search**

**When to use**: For files that are large, change frequently, or not useful for AI understanding

**Examples**:
- Dependencies (`.venv/`, `node_modules/`)
- Generated code (`prisma/.client/`)
- Build artifacts (`dist/`, `build/`)
- Cache files (`.cache/`, `__pycache__/`)

**Impact**: Files in `.cursorindexingignore` are not indexed, but may still be accessible if explicitly referenced

## What Gets Indexed

### ✅ Included (Indexed)

**Source Code**
- `src/**/*.py` - All Python source files
- `tests/**/*.py` - All test files
- Configuration files (`pyproject.toml`, `docker-compose.yml`)

**Documentation**
- `README.md` - Project overview
- `docs/**/*.md` - Documentation files
- `prd/**/*.md` - Product Requirements Documents
- `CLAUDE.md` - AI instructions

**Project Structure**
- Directory organization
- File naming patterns
- Import relationships

### ❌ Excluded (Not Indexed)

**Dependencies**
- `.venv/`, `venv/` - Virtual environments
- `node_modules/` - Node.js dependencies
- Lock files (`uv.lock`, `package-lock.json`) - Too large, change frequently

**Generated Code**
- `prisma/.client/` - Generated Prisma client
- `dist/`, `build/` - Build outputs
- `*.pyc`, `__pycache__/` - Python bytecode

**Temporary Files**
- `.cache/`, `.pytest_cache/` - Cache directories
- `*.swp`, `*.swo` - Editor temp files
- `*.log` - Log files

**Sensitive Data** (also in `.cursorignore`)
- `.env*` - Environment files
- `*.pem`, `*.key` - Cryptographic keys
- `logs/`, `audit.log` - Logs with sensitive data

## Optimizing Context for Better AI

### 1. Code Structure

**Good**: Clear, descriptive names
```python
async def get_user_by_email(email: str) -> User | None:
    """Retrieve a user by email address."""
    # ...
```

**Bad**: Vague, unclear names
```python
async def get(e: str) -> U | None:
    # ...
```

### 2. Documentation

**Good**: Comprehensive docstrings
```python
async def create_user(data: UserCreate) -> User:
    """Create a new user account.

    Validates the email format, checks for duplicates, and hashes
    the password before storing in the database.

    Args:
        data: UserCreate model with user information.

    Returns:
        User model representing the created user.

    Raises:
        ValidationError: If email format is invalid.
        DuplicateUserError: If user already exists.
    """
```

**Bad**: No documentation
```python
async def create_user(data: UserCreate) -> User:
    # creates user
```

### 3. Type Hints

**Good**: Complete type information
```python
def process_items(
    items: list[str],
    config: dict[str, str] | None = None,
) -> bool:
    """Process a list of items."""
```

**Bad**: Missing types
```python
def process_items(items, config=None):
    """Process a list of items."""
```

### 4. Comments

**Good**: Explain "why", not "what"
```python
# Use batch query to avoid N+1 problem
users = await db.user.find_many(where={"id": {"in": user_ids}})
```

**Bad**: Obvious comments
```python
# Get users from database
users = await db.user.find_many(where={"id": {"in": user_ids}})
```

## Context Window Management

Cursor has a limited context window. To maximize effectiveness:

### 1. Be Specific in Prompts

**Good**: "Add a POST endpoint to `src/api/users.py` that creates a user following the pattern in `src/api/posts.py`"

**Bad**: "Add an endpoint"

### 2. Reference Files Explicitly

**Good**: "Update the `UserService` class in `src/services/user.py`"

**Bad**: "Update the user service"

### 3. Use Skills for Common Tasks

**Good**: `/new-feature payment --with-db`

**Bad**: "Create a payment feature with database model, API routes, service, and tests"

### 4. Break Large Changes into Steps

**Good**:
1. "Create the database model"
2. "Add the service layer"
3. "Create API routes"
4. "Write tests"

**Bad**: "Create the entire payment feature"

## Indexing Strategy

### What to Index

**Always Index**:
- Source code (`.py` files in `src/` and `tests/`)
- Configuration files (`pyproject.toml`, `docker-compose.yml`)
- Documentation (`*.md` files)
- Schema files (`prisma/schema.prisma`)

**Never Index**:
- Dependencies (use MCP tools for library docs)
- Generated code (generated from indexed sources)
- Build artifacts (outputs, not inputs)
- Cache files (temporary, not source)

### Performance Considerations

**Large Files**:
- Very large files (>10k lines) may be partially indexed
- Consider splitting large files into modules
- Use `.cursorindexingignore` for extremely large files

**Frequently Changing Files**:
- Lock files change on every dependency update
- Generated code changes when sources change
- Exclude these to reduce re-indexing overhead

## Best Practices

### 1. Keep Source Code Indexed

✅ **Do**: Keep all source code in `src/` and `tests/` indexed
❌ **Don't**: Exclude source code from indexing

### 2. Exclude Dependencies

✅ **Do**: Exclude `.venv/`, `node_modules/` from indexing
❌ **Don't**: Try to index dependencies (use MCP tools instead)

### 3. Protect Sensitive Data

✅ **Do**: Add all sensitive files to `.cursorignore`
❌ **Don't**: Allow secrets to be sent to AI models

### 4. Document Your Code

✅ **Do**: Add docstrings and type hints
❌ **Don't**: Rely on AI to guess function purposes

### 5. Use Clear Naming

✅ **Do**: Use descriptive, consistent names
❌ **Don't**: Use abbreviations or unclear names

## Troubleshooting Context Issues

### AI Doesn't Understand My Code

**Symptoms**: AI suggestions don't match project patterns

**Solutions**:
1. Check if code is indexed (not in `.cursorindexingignore`)
2. Add docstrings to functions/classes
3. Improve naming conventions
4. Reference `.cursorrules` in prompts

### AI Suggests Wrong Patterns

**Symptoms**: AI uses patterns not in the project

**Solutions**:
1. Ensure `.cursorrules` is up to date
2. Check PRDs for project standards
3. Provide examples of correct patterns
4. Use skills that follow project patterns

### Slow Indexing

**Symptoms**: Cursor is slow, indexing takes long

**Solutions**:
1. Check `.cursorindexingignore` excludes large files
2. Exclude dependencies and generated code
3. Split very large files into smaller modules
4. Clear Cursor cache if needed

### Missing Context

**Symptoms**: AI doesn't know about related files

**Solutions**:
1. Open related files in editor
2. Reference files explicitly in prompts
3. Use skills that understand project structure
4. Check import relationships are clear

## File Organization for Better Context

### Recommended Structure

```
src/project_name/
├── __init__.py           # Module docstring
├── main.py               # FastAPI app (indexed)
├── config.py             # Configuration (indexed)
├── api/                  # API routes (indexed)
│   ├── __init__.py
│   └── users.py          # Clear, descriptive names
├── services/             # Business logic (indexed)
│   ├── __init__.py
│   └── user_service.py   # Descriptive names
├── models/               # Pydantic models (indexed)
│   ├── __init__.py
│   └── user.py
└── db/                   # Database utilities (indexed)
    ├── __init__.py
    └── client.py
```

### Naming Conventions

**Good**:
- `user_service.py` - Clear purpose
- `get_user_by_email()` - Descriptive function name
- `UserService` - Clear class name

**Bad**:
- `us.py` - Unclear abbreviation
- `get()` - Vague function name
- `Service` - Too generic

## Summary

**Key Principles**:
1. **Index source code**, exclude dependencies
2. **Protect sensitive data** with `.cursorignore`
3. **Optimize performance** with `.cursorindexingignore`
4. **Document code** for better AI understanding
5. **Use clear naming** to help AI understand purpose

**Remember**:
- `.cursorignore` = Security (never send to AI)
- `.cursorindexingignore` = Performance (don't index)
- Both serve different purposes and may overlap

For more details on using Cursor effectively, see [CURSOR_BEST_PRACTICES.md](./CURSOR_BEST_PRACTICES.md).
