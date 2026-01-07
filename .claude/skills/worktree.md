# /worktree

Manage git worktrees for parallel AI agent development with Claude Code or Cursor.

## Usage

```
/worktree create <name> [base-branch]   # Create a new worktree
/worktree list                           # List all worktrees
/worktree remove <name>                  # Remove a worktree
```

## Arguments

- `name`: Name for the worktree (used in path and branch name)
- `base-branch`: Optional branch to base the worktree on (defaults to HEAD)

## Instructions

When this skill is invoked:

### For `/worktree create <name> [base-branch]`:

1. **Run the worktree script**:
   ```bash
   ./scripts/worktree.sh create <name> [base-branch]
   ```

2. **The script automatically**:
   - Creates a new branch: `worktree/<name>`
   - Creates worktree at: `../worktrees/<name>`
   - Copies `.env` file from main repo
   - Copies local config files (`.claude/settings.local.json`, `.secrets.baseline`)
   - Runs `uv sync` to install dependencies

3. **After creation, inform the user**:
   - Path to the new worktree
   - How to start Claude Code in that worktree
   - The branch name created

### For `/worktree list`:

1. **Run**:
   ```bash
   ./scripts/worktree.sh list
   ```

2. **Show all worktrees** with their branches and paths

### For `/worktree remove <name>`:

1. **Run**:
   ```bash
   ./scripts/worktree.sh remove <name>
   ```

2. **Confirm branch deletion** if prompted

## Examples

### Create worktrees for parallel development:

```
/worktree create auth-feature main
/worktree create api-refactor main
/worktree create bug-fix-123
```

### Parallel agent workflow:

```bash
# Terminal 1: Main repo
claude

# Terminal 2: Auth feature (separate Claude instance)
cd ../worktrees/auth-feature && claude

# Terminal 3: API refactor (separate Claude instance)
cd ../worktrees/api-refactor && claude
```

## Parallel Development Best Practices

### When to use worktrees:

- **Independent features**: Two features with no shared code changes
- **Bug fixes**: Quick fix while main development continues
- **Experimentation**: Try different approaches in parallel
- **Code review**: Review PR in separate worktree while continuing work

### When NOT to use worktrees:

- **Dependent changes**: Features that modify the same files
- **Sequential work**: Tasks that must be done in order
- **Small tasks**: Overhead not worth it for quick changes

### Environment isolation:

Each worktree gets its own:
- `.env` file (copied from main)
- Virtual environment (`.venv/`)
- Node modules (if applicable)
- Prisma client (needs `uv run prisma generate`)

### Database considerations:

By default, all worktrees share the same database. For true isolation:

1. Edit `.env` in each worktree to use a different database name
2. Run migrations in each worktree
3. Or use Docker to spin up separate PostgreSQL instances

### Merging work back:

```bash
# In main repo
git checkout main
git merge worktree/auth-feature
git merge worktree/api-refactor

# Clean up
/worktree remove auth-feature
/worktree remove api-refactor
```

## Directory Structure

After creating worktrees:

```
parent-directory/
├── core-python-template/     # Main repository
│   ├── .env
│   ├── scripts/worktree.sh
│   └── ...
└── worktrees/                 # Worktree directory
    ├── auth-feature/          # Worktree 1
    │   ├── .env               # Copied from main
    │   └── ...
    └── api-refactor/          # Worktree 2
        ├── .env               # Copied from main
        └── ...
```
