# /checkpoint

Update task file with current progress during long-running feature implementation.

## Usage

```
/checkpoint [feature_name] [--create]
```

## Arguments

- `feature_name`: Name of the feature (optional if only one task file exists)
- `--create`: Create new task file if it doesn't exist

## Instructions

When this skill is invoked:

### Agent Behavior (Codex-Max Pattern)

**Autonomy:**
- Complete the checkpoint update end-to-end
- Analyze current git status and recent commits to infer progress
- Update task file automatically based on evidence
- Don't just ask "what should I update" - figure it out

**Thoroughness:**
- Review git log since last checkpoint
- Check file modifications (git status)
- Identify completed tasks from commit messages
- Update progress percentages
- Add new decisions if architectural choices were made

### Implementation Steps

1. **Identify the task file**:
   ```bash
   # If feature_name provided
   Read: prd/tasks/{feature_name}_tasks.md

   # If not provided, list available task files
   ls prd/tasks/*.md

   # If only one exists (excluding TASK_TEMPLATE.md), use it
   # If multiple exist, ask user which one
   ```

2. **Gather current state (parallel read)**:
   ```bash
   Read in parallel:
     - prd/tasks/{feature}_tasks.md  # Current task file
     - git log since last checkpoint  # Recent commits
     - git status                     # Current changes
     - git diff HEAD                  # Uncommitted changes
   ```

3. **Analyze progress**:
   - Extract task IDs from recent commits (`[PRD-XX Task Y.Z]`)
   - Map commits to tasks in task file
   - Identify tasks that should be marked complete
   - Identify new files created (add to "Key Files" section)
   - Check for architectural decisions in commit messages or code

4. **Update task file**:
   - Mark completed tasks with `[x]`
   - Update "IN PROGRESS" marker to current task
   - Update "Progress Summary" percentages
   - Add session log entry with timestamp
   - Update "Next Session Priorities" if priorities changed
   - Add "Key Files" if new files were created
   - Add "Decisions Made" if new architectural choices
   - Add "Git Commits" references
   - Update "Last Updated" timestamp

5. **Present checkpoint summary**:
   ```markdown
   **Checkpoint Updated:** `prd/tasks/{feature}_tasks.md`

   **Progress:**
   - Phase 1: 60% → 80% (2 more tasks completed)
   - Overall: 27% → 40%

   **Completed Since Last Checkpoint:**
   - [x] Task 1.5: Implement JWT token generation
   - [x] Task 1.6: Create authentication endpoints

   **Currently Working On:**
   - [ ] Task 1.7: Add authentication middleware (IN PROGRESS)

   **Recent Commits:**
   - abc1234 - feat: add JWT token generation [PRD-04 Task 1.5]
   - def5678 - feat: add auth endpoints [PRD-04 Task 1.6]

   **Next Session Priorities Updated:**
   1. Complete authentication middleware
   2. Add rate limiting
   3. Write integration tests
   ```

## Creating New Task Files

If `--create` flag is used and task file doesn't exist:

1. **Verify PRD exists**:
   ```bash
   # Look for PRD in prd/ directory
   ls prd/*{feature_name}*.md
   ```

2. **Copy template**:
   ```bash
   cp prd/tasks/TASK_TEMPLATE.md prd/tasks/{feature_name}_tasks.md
   ```

3. **Initialize task file**:
   - Set feature name and PRD reference
   - Set status to "Not Started" or "In Progress"
   - Set started date to today
   - Initialize agent sessions count to 1
   - Prompt user for initial tasks or extract from PRD

4. **Update PRD index**:
   - Add task file reference to `prd/00_PRD_index.md`
   - Mark PRD as "In Progress" if appropriate

## Task Progress Analysis

### Automatic Task Completion Detection

Detect completed tasks by:
1. **Commit messages** with task IDs: `[PRD-04 Task 1.5]`
2. **File existence**: If task says "Create file X" and file exists, mark complete
3. **Test coverage**: If task says "Add tests" and tests exist with good coverage, mark complete
4. **Recent git activity**: Files mentioned in tasks that have recent commits

### Progress Calculation

```python
# Phase progress
phase_complete = completed_tasks / total_tasks_in_phase
phase_percentage = int(phase_complete * 100)

# Overall progress
total_complete = sum(completed_tasks_all_phases)
total_tasks = sum(total_tasks_all_phases)
overall_percentage = int((total_complete / total_tasks) * 100)
```

## Session Log Entry Format

```markdown
**Session X (YYYY-MM-DD HH:MM - HH:MM):**
- Completed: [List of tasks completed]
- Issues encountered: [Any problems or blockers]
- Decisions made: [Key architectural decisions]
- Next: [What to do next session]
```

## Examples

### Basic checkpoint

```
/checkpoint user_auth
```

Analyzes progress on user_auth feature and updates task file.

### Create new task file

```
/checkpoint payment_processing --create
```

Creates `prd/tasks/payment_processing_tasks.md` from template and initializes it.

### Checkpoint during implementation

```
Agent: Working on user authentication...
[implements JWT token generation]
Agent: Let me checkpoint this progress.
/checkpoint user_auth
Agent: Checkpoint updated. Phase 1 is now 60% complete (3/5 tasks done).
```

## Best Practices

**When to Checkpoint:**
- Every 30-60 minutes during active development
- After completing a significant task or milestone
- Before ending a session
- After making architectural decisions
- When switching to a different feature

**What to Update:**
- Always: Task checkboxes, progress percentages, last updated timestamp
- Usually: Session log entry, next session priorities
- As needed: Decisions made, key files, blockers

**Commit After Checkpoint:**
```bash
git add prd/tasks/{feature}_tasks.md
git commit -m "chore: checkpoint progress on {feature} [PRD-XX]"
```

## Integration with Other Skills

**Works well with:**
- `/new-feature` - Auto-create task file for new features
- `/commit` - Reference task IDs in commit messages for auto-tracking
- Context compression recovery - Task file enables resuming work after compression

## Notes

- Task files are the **primary mechanism** for surviving context compression
- The "Context" and "Decisions Made" sections are most critical for recovery
- Regular checkpointing prevents loss of progress and context
- Task IDs in commits enable automatic progress tracking
- Update "Next Session Priorities" to make resumption effortless
