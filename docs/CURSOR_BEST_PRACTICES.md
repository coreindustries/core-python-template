# Cursor Best Practices Guide

This comprehensive guide covers how to effectively use Cursor AI with this Python boilerplate template to maximize productivity and code quality.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding the Setup](#understanding-the-setup)
3. [Using Skills (Slash Commands)](#using-skills-slash-commands)
4. [Working with Hooks](#working-with-hooks)
5. [Leveraging Subagents](#leveraging-subagents)
6. [MCP Tool Integration](#mcp-tool-integration)
7. [Context Management](#context-management)
8. [Common Workflows](#common-workflows)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### Initial Setup

1. **Read the `.cursorrules` file**: This contains all project conventions and patterns
2. **Review PRDs**: Understand the project standards in `prd/` directory
3. **Check `.claude/settings.json`**: See what skills and hooks are configured
4. **Set up MCP tools** (optional): See [CURSOR_MCP_SETUP.md](./CURSOR_MCP_SETUP.md)

### First Steps

```bash
# 1. Install dependencies
uv sync

# 2. Start services
docker-compose up -d postgres redis

# 3. Generate Prisma client
uv run prisma generate

# 4. Run tests to verify setup
uv run pytest
```

## Understanding the Setup

### File Structure

```
.
├── .cursorrules              # Project rules and conventions (READ THIS FIRST)
├── .cursorignore             # Files excluded from AI context (security)
├── .cursorindexingignore     # Files excluded from indexing (performance)
├── .claude/
│   ├── settings.json         # Hooks, skills, and agents configuration
│   ├── skills/               # Custom slash commands
│   └── hooks/                # Automation scripts
└── docs/
    ├── CURSOR_BEST_PRACTICES.md    # This file
    ├── CURSOR_MCP_SETUP.md         # MCP tool setup
    └── CURSOR_CONTEXT_STRATEGY.md  # Context management
```

### Key Files Explained

**`.cursorrules`**
- Contains all project conventions
- Defines code patterns and anti-patterns
- Specifies tool usage (uv, prisma, pytest)
- **Always read this before asking AI to make changes**

**`.claude/settings.json`**
- Configures automated hooks
- Defines available skills
- Sets up subagents
- References MCP tools

**`.cursorignore` vs `.cursorindexingignore`**
- `.cursorignore`: Prevents files from being sent to AI (security)
- `.cursorindexingignore`: Prevents files from being indexed (performance)
- See [CURSOR_CONTEXT_STRATEGY.md](./CURSOR_CONTEXT_STRATEGY.md) for details

## Using Skills (Slash Commands)

Skills are custom commands that automate common workflows. They're defined in `.claude/skills/`.

### Available Skills

| Skill | Purpose | Example |
|-------|---------|---------|
| `/new-feature` | Scaffold complete feature | `/new-feature user_profile --with-db` |
| `/new-prd` | Create PRD document | `/new-prd 04 "User Authentication"` |
| `/security-scan` | Run security analysis | `/security-scan --fix` |
| `/db-migrate` | Manage migrations | `/db-migrate create --name add_users` |
| `/test` | Run tests with coverage | `/test --coverage` |
| `/lint` | Lint and type check | `/lint --fix` |
| `/review` | Code review | `/review --security` |
| `/refactor` | Safe refactoring | `/refactor src/services/user.py --pattern dry` |
| `/document` | Generate documentation | `/document src/api/users.py --type docstrings` |
| `/debug` | Debug issues | `/debug "AttributeError" --file src/services/user.py` |
| `/optimize` | Performance optimization | `/optimize src/api/users.py --type database` |

### Best Practices for Skills

1. **Be specific**: Provide file paths and options when needed
2. **Review output**: Skills generate code; always review before committing
3. **Run tests**: After using `/new-feature`, run tests to verify
4. **Check coverage**: Use `/test --coverage` to ensure 100% coverage

### Example Workflow

```bash
# 1. Create a new feature
/new-feature payment --with-db --crud

# 2. Review generated code
# (AI shows you the created files)

# 3. Run tests
/test

# 4. Generate documentation
/document src/api/payment.py --type docstrings

# 5. Security check
/security-scan
```

## Working with Hooks

Hooks automate actions before/after tool calls and on errors. They're configured in `.claude/settings.json`.

### Hook Types

**Pre-tool Hooks** (run before actions):
- `sensitive-file-guard`: Blocks editing `.env` and secrets
- `production-db-guard`: Warns before production DB operations
- `coverage-gate`: Checks test coverage before committing tests

**Post-tool Hooks** (run after actions):
- `test-reminder`: Reminds to run tests after code changes
- `security-scan-reminder`: Suggests security scan after dependency changes
- `documentation-reminder`: Reminds to update docs for new features
- `prd-compliance-reminder`: Suggests PRD compliance check

**Error Hooks** (run on errors):
- `lint-error-helper`: Suggests fixes for lint errors
- `test-error-helper`: Suggests fixes for test failures

### Understanding Hook Behavior

Hooks are **automatic** - they run without you doing anything. They provide:
- **Safety**: Prevent dangerous operations (editing secrets)
- **Reminders**: Suggest next steps (run tests, update docs)
- **Help**: Provide solutions when errors occur

### Customizing Hooks

Edit `.claude/settings.json` to:
- Add new hooks
- Modify existing hook commands
- Change when hooks trigger

See `.claude/settings.local.json.example` for project-specific overrides.

## Leveraging Subagents

Subagents are specialized AI assistants for specific tasks. They're defined in `.claude/settings.json`.

### Available Agents

**`code-reviewer`**
- Reviews code against project standards
- Checks type hints, docstrings, naming
- Verifies test coverage
- Suggests improvements

**`security-auditor`**
- Performs security analysis
- Checks OWASP Top 10 compliance
- Identifies vulnerabilities
- Provides remediation examples

**`test-generator`**
- Generates pytest tests
- Ensures 100% coverage
- Creates unit and integration tests
- Follows existing test patterns

**`prd-compliance`**
- Checks implementation against PRDs
- Reports compliance gaps
- Suggests PRD updates if needed

### Using Subagents

Subagents are invoked automatically when you use certain skills, or you can reference them in chat:

```
User: "Review this code for security issues"
AI: [Uses security-auditor agent to analyze code]
```

## MCP Tool Integration

MCP (Model Context Protocol) tools extend Cursor's capabilities. See [CURSOR_MCP_SETUP.md](./CURSOR_MCP_SETUP.md) for setup.

### Recommended Tools

- **Supabase MCP**: Database operations and migrations
- **GitHub MCP**: Repository management and PRs
- **Firecrawl MCP**: Documentation research
- **Context7 MCP**: Library documentation lookup

### Using MCP Tools

Once configured, MCP tools are available in chat:

```
User: "Query the database for active users"
AI: [Uses Supabase MCP to execute query]

User: "Show me FastAPI authentication examples"
AI: [Uses Firecrawl MCP to scrape documentation]
```

## Context Management

Cursor uses context to understand your codebase. Proper context management improves AI suggestions.

### What Gets Indexed

**Included** (useful for AI):
- Source code (`src/`)
- Tests (`tests/`)
- PRDs (`prd/`)
- Configuration files (`pyproject.toml`, `docker-compose.yml`)
- Documentation (`docs/`, `README.md`)

**Excluded** (not useful):
- Dependencies (`.venv/`, `node_modules/`)
- Generated code (`prisma/.client/`)
- Build artifacts (`dist/`, `build/`)
- Cache files (`.cache/`, `__pycache__/`)

### Improving Context

1. **Use descriptive names**: Function/class names help AI understand purpose
2. **Add docstrings**: Docstrings provide context for AI
3. **Write clear comments**: Comments explain "why", not "what"
4. **Structure code well**: Follow project organization standards

See [CURSOR_CONTEXT_STRATEGY.md](./CURSOR_CONTEXT_STRATEGY.md) for detailed strategies.

## Common Workflows

### Feature Development

```bash
# 1. Create feature scaffold
/new-feature user_profile --with-db

# 2. Review generated code
# (AI shows created files)

# 3. Customize the feature
# (Edit generated files as needed)

# 4. Run tests
/test

# 5. Generate documentation
/document src/api/user_profile.py --type docstrings

# 6. Security check
/security-scan

# 7. Code review
/review src/api/user_profile.py
```

### Debugging

```bash
# 1. Get error details
/debug "AttributeError: 'NoneType' object has no attribute 'email'" --file src/services/user.py

# 2. Review suggested fix
# (AI provides explanation and code fix)

# 3. Apply fix
# (AI makes the change)

# 4. Verify
/test
```

### Refactoring

```bash
# 1. Identify refactoring target
/refactor src/services/user.py --pattern dry --dry-run

# 2. Review suggested changes
# (AI shows what would change)

# 3. Apply refactoring
/refactor src/services/user.py --pattern dry

# 4. Verify tests still pass
/test
```

### Performance Optimization

```bash
# 1. Analyze performance
/optimize src/api/users.py --type database --profile

# 2. Review suggestions
# (AI identifies bottlenecks)

# 3. Apply optimizations
# (AI makes changes)

# 4. Verify improvements
/test
```

## Troubleshooting

### AI Doesn't Understand My Code

**Problem**: AI suggestions don't match project patterns

**Solutions**:
1. Check `.cursorrules` is up to date
2. Ensure code follows naming conventions
3. Add docstrings to help AI understand
4. Review PRDs for project standards

### Skills Not Working

**Problem**: Slash commands don't execute

**Solutions**:
1. Check `.claude/settings.json` has skill enabled
2. Verify skill file exists in `.claude/skills/`
3. Check skill syntax matches expected format
4. Review Cursor logs for errors

### Hooks Not Triggering

**Problem**: Hooks don't run when expected

**Solutions**:
1. Verify hook configuration in `.claude/settings.json`
2. Check file patterns match your files
3. Ensure hook commands are executable
4. Review Cursor logs for hook errors

### Poor AI Suggestions

**Problem**: AI suggestions are inaccurate

**Solutions**:
1. Improve code context (add docstrings)
2. Use more specific prompts
3. Reference `.cursorrules` in your prompt
4. Provide examples of desired patterns

### MCP Tools Not Available

**Problem**: MCP tools don't work

**Solutions**:
1. Verify MCP server configuration in Cursor settings
2. Check API keys are correct
3. Ensure MCP server is running
4. Review [CURSOR_MCP_SETUP.md](./CURSOR_MCP_SETUP.md)

## Best Practices Summary

### Do's ✅

- **Read `.cursorrules`** before asking for changes
- **Use skills** for common tasks (faster than manual)
- **Review generated code** before committing
- **Run tests** after AI makes changes
- **Add docstrings** to help AI understand code
- **Use specific prompts** with file paths
- **Reference PRDs** when asking for features

### Don'ts ❌

- **Don't ignore hooks** - they prevent mistakes
- **Don't skip tests** - AI can introduce bugs
- **Don't commit secrets** - hooks should prevent this
- **Don't use generic prompts** - be specific
- **Don't ignore lint errors** - fix them immediately
- **Don't bypass security scans** - run them regularly

## Getting Help

1. **Check documentation**: Read relevant docs in `docs/`
2. **Review `.cursorrules`**: Contains project-specific guidance
3. **Check PRDs**: Standards are documented in `prd/`
4. **Review examples**: Look at existing code for patterns
5. **Ask specific questions**: Provide context and file paths

## Next Steps

1. **Set up MCP tools**: See [CURSOR_MCP_SETUP.md](./CURSOR_MCP_SETUP.md)
2. **Understand context**: Read [CURSOR_CONTEXT_STRATEGY.md](./CURSOR_CONTEXT_STRATEGY.md)
3. **Customize settings**: Create `.claude/settings.local.json` for project overrides
4. **Practice workflows**: Try the common workflows above
5. **Share knowledge**: Document team-specific patterns

## Quick Reference

See [CURSOR_QUICK_REFERENCE.md](./CURSOR_QUICK_REFERENCE.md) for a one-page cheat sheet.
