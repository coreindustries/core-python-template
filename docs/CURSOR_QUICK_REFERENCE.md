# Cursor Quick Reference

One-page cheat sheet for using Cursor AI with this Python boilerplate.

## Essential Files

| File | Purpose |
|------|---------|
| `.cursorrules` | **READ FIRST** - Project conventions and patterns |
| `.claude/settings.json` | Hooks, skills, and agents configuration |
| `.cursorignore` | Files excluded from AI (security) |
| `.cursorindexingignore` | Files excluded from indexing (performance) |

## Skills (Slash Commands)

| Command | Purpose | Example |
|---------|---------|---------|
| `/new-feature` | Scaffold feature | `/new-feature payment --with-db` |
| `/new-prd` | Create PRD | `/new-prd 04 "Auth"` |
| `/security-scan` | Security check | `/security-scan --fix` |
| `/db-migrate` | DB migrations | `/db-migrate create --name add_users` |
| `/test` | Run tests | `/test --coverage` |
| `/lint` | Lint & type check | `/lint --fix` |
| `/review` | Code review | `/review --security` |
| `/refactor` | Safe refactoring | `/refactor src/services/user.py` |
| `/document` | Generate docs | `/document src/api/users.py` |
| `/debug` | Debug issues | `/debug "AttributeError" --file src/services/user.py` |
| `/optimize` | Performance | `/optimize src/api/users.py --type database` |

## Hooks (Automatic)

| Hook | When | Action |
|------|------|--------|
| `sensitive-file-guard` | Edit `.env`/secrets | **BLOCKS** modification |
| `production-db-guard` | DB migration in prod | **WARNS** before execution |
| `coverage-gate` | Edit tests | **CHECKS** coverage ≥100% |
| `test-reminder` | Edit `src/**/*.py` | **REMINDS** to run tests |
| `security-scan-reminder` | `uv add` | **SUGGESTS** security scan |
| `documentation-reminder` | Add API/service | **REMINDS** to update docs |
| `prd-compliance-reminder` | Add API route | **SUGGESTS** PRD check |

## Subagents

| Agent | Use For |
|-------|---------|
| `code-reviewer` | Review against standards |
| `security-auditor` | Security analysis (OWASP) |
| `test-generator` | Generate pytest tests |
| `prd-compliance` | Check PRD requirements |

## Common Workflows

### New Feature
```bash
/new-feature <name> --with-db
/test
/document src/api/<name>.py
/security-scan
```

### Debugging
```bash
/debug "<error>" --file <file>
# Review fix
/test
```

### Refactoring
```bash
/refactor <file> --pattern dry --dry-run
/refactor <file> --pattern dry
/test
```

## MCP Tools

| Tool | Purpose | Setup |
|------|---------|-------|
| Supabase | Database ops | See `docs/CURSOR_MCP_SETUP.md` |
| GitHub | Repo management | Requires token |
| Firecrawl | Doc research | Requires API key |
| Context7 | Library docs | No setup needed |

## Context Management

### `.cursorignore` (Security)
- Prevents files from being **sent to AI**
- Use for: `.env`, secrets, logs, credentials

### `.cursorindexingignore` (Performance)
- Prevents files from being **indexed**
- Use for: `.venv/`, `node_modules/`, generated code

## Best Practices

### ✅ Do
- Read `.cursorrules` before asking for changes
- Use skills for common tasks
- Review generated code before committing
- Run tests after AI changes
- Add docstrings to help AI

### ❌ Don't
- Ignore hooks (they prevent mistakes)
- Skip tests (AI can introduce bugs)
- Commit secrets (hooks should prevent)
- Use generic prompts (be specific)
- Ignore lint errors (fix immediately)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| AI doesn't understand code | Check `.cursorrules`, add docstrings |
| Skills not working | Check `.claude/settings.json` |
| Hooks not triggering | Verify hook configuration |
| Poor suggestions | Use specific prompts, reference files |
| MCP tools unavailable | Check Cursor MCP settings |

## Key Commands

```bash
# Development
uv sync                              # Install deps
uv run app serve                     # Start API
docker-compose up -d postgres redis  # Start services

# Quality
uv run ruff check --fix src/         # Lint
uv run mypy src/                     # Type check
uv run pytest --cov=src             # Test with coverage
uv run bandit -r src/                # Security scan

# Database
uv run prisma generate               # Generate client
uv run prisma migrate dev            # Create migration
```

## File Locations

- **Skills**: `.claude/skills/`
- **Hooks**: `.claude/hooks/`
- **Settings**: `.claude/settings.json`
- **Docs**: `docs/CURSOR_*.md`
- **PRDs**: `prd/*.md`

## Getting Help

1. Read `.cursorrules` (project conventions)
2. Check `docs/CURSOR_BEST_PRACTICES.md` (comprehensive guide)
3. Review PRDs in `prd/` (standards)
4. Use specific prompts with file paths

---

**Remember**: Always review AI-generated code before committing!
