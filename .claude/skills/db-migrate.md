# /db-migrate

Manage Prisma database migrations with validation and safety checks.

## Usage

```
/db-migrate <action> [--name <migration_name>]
```

## Actions

- `status` - Show migration status
- `create` - Create a new migration
- `apply` - Apply pending migrations
- `reset` - Reset database (development only)
- `generate` - Regenerate Prisma client

## Instructions

When this skill is invoked:

### Action: `status`

1. **Check migration status**:
   ```bash
   uv run prisma migrate status
   ```

2. **Report**:
   - Pending migrations
   - Applied migrations
   - Schema drift detection

### Action: `create`

1. **Validate schema**:
   ```bash
   uv run prisma validate
   ```
   If validation fails, report errors and stop.

2. **Check for breaking changes**:
   - Dropping columns
   - Changing column types
   - Removing required fields
   - Warn user if detected

3. **Create migration**:
   ```bash
   uv run prisma migrate dev --name <migration_name> --create-only
   ```

4. **Review generated SQL**:
   - Show the migration SQL
   - Highlight potentially dangerous operations:
     - `DROP TABLE`
     - `DROP COLUMN`
     - `ALTER COLUMN` type changes
     - Truncating data

5. **After creation**, remind user to:
   - Review the migration SQL in `prisma/migrations/`
   - Test migration on a copy of production data
   - Apply with `/db-migrate apply`

### Action: `apply`

1. **Check environment**:
   ```bash
   echo $ENVIRONMENT
   ```
   - If production, require confirmation
   - If development, proceed

2. **Backup reminder**:
   - For staging/production: "Have you backed up the database?"

3. **Apply migrations**:
   ```bash
   uv run prisma migrate deploy
   ```

4. **Regenerate client**:
   ```bash
   uv run prisma generate
   ```

5. **Verify**:
   - Run a basic health check query
   - Log migration as audit event

### Action: `reset`

1. **Safety check**:
   - ONLY allow in development environment
   - Require explicit confirmation

2. **Reset database**:
   ```bash
   uv run prisma migrate reset --force
   ```

3. **Regenerate client**:
   ```bash
   uv run prisma generate
   ```

### Action: `generate`

1. **Regenerate Prisma client**:
   ```bash
   uv run prisma generate
   ```

2. **Verify generation**:
   - Check that client was generated
   - Report any type generation issues

## Migration Best Practices

Display these when creating migrations:

1. **Always create migrations in development first**
2. **Review SQL before applying**
3. **Test on staging before production**
4. **Back up production database before migrating**
5. **Use transactions for multi-step migrations**
6. **Have a rollback plan**

## Example Workflow

```bash
# 1. Make schema changes
# Edit prisma/schema.prisma

# 2. Create migration
/db-migrate create --name add_user_preferences

# 3. Review generated SQL
# Check prisma/migrations/YYYYMMDD_add_user_preferences/

# 4. Apply migration
/db-migrate apply

# 5. Verify
/db-migrate status
```

## Safety Checks

Before any destructive operation:

```markdown
⚠️  WARNING: This migration contains potentially destructive changes:

- DROP COLUMN: users.legacy_field
- ALTER COLUMN: orders.amount (integer → decimal)

These changes may result in data loss.

Recommendations:
1. Back up affected tables before proceeding
2. Test on a copy of production data
3. Have a rollback migration ready

Continue? [y/N]
```

## Audit Logging

All migration operations are logged:

```python
audit.log_event(
    SecurityEvent(
        action=AuditAction.CONFIG_CHANGE,
        actor_id=user_id,
        resource_type="database_migration",
        resource_id=migration_name,
        details=f"Applied migration: {migration_name}",
        metadata={"environment": environment},
    )
)
```
