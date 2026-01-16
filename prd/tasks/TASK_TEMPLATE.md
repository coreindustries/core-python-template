# Feature: [Feature Name] (PRD [XX])

**PRD:** `prd/[XX]_[Feature_Name].md`

**Status:** [Not Started | In Progress | Blocked | Completed]

**Started:** YYYY-MM-DD

**Agent Sessions:** [Number of sessions spent on this feature]

**Last Updated:** YYYY-MM-DD HH:MM

**Estimated Completion:** YYYY-MM-DD

---

## Context

Brief description of what this feature implements. Include:
- Overall goal and purpose
- Key architectural decisions made
- Why certain approaches were chosen over alternatives
- Any important constraints or requirements

**Important:** This section is critical for context recovery after compression. Include enough detail that a new agent session can understand the feature without re-reading the entire PRD.

---

## Tasks

### Phase 1: [Phase Name - e.g., Core Implementation]

- [ ] Task 1.1: [Task description]
  - [ ] Subtask 1.1.1
  - [ ] Subtask 1.1.2
- [ ] Task 1.2: [Task description]
- [x] Task 1.3: [Completed task] ✓
- [ ] Task 1.4: [Task description] (IN PROGRESS)
  - [x] Subtask 1.4.1 ✓
  - [ ] Subtask 1.4.2
  - [ ] Subtask 1.4.3

### Phase 2: [Phase Name - e.g., Testing & Validation]

- [ ] Task 2.1: [Task description]
- [ ] Task 2.2: [Task description]

### Phase 3: [Phase Name - e.g., Documentation & Deployment]

- [ ] Task 3.1: [Task description]
- [ ] Task 3.2: [Task description]

---

## Progress Summary

- **Phase 1:** 60% complete (3/5 tasks done)
- **Phase 2:** 0% complete (0/4 tasks done)
- **Phase 3:** 0% complete (0/2 tasks done)
- **Overall:** 27% complete (3/11 tasks done)

---

## Blockers

**Current Blockers:**
1. [Blocker description] - Blocking Task X.Y
   - **Severity:** [Critical | Important | Minor]
   - **Status:** [Investigating | Waiting | Resolved]
   - **Resolution:** [How to resolve or who is working on it]

**Resolved Blockers:**
- [Resolved blocker] - Resolved on YYYY-MM-DD by [solution]

---

## Key Files

List all important files with line numbers for key sections:

**Core Implementation:**
- `src/project_name/api/[feature].py` - API endpoints
- `src/project_name/services/[feature].py` - Business logic
- `src/project_name/models/[feature].py` - Pydantic models
- `prisma/schema.prisma:XX` - Database schema

**Tests:**
- `tests/unit/test_[feature].py` - Unit tests
- `tests/integration/test_[feature].py` - Integration tests

**Configuration:**
- `.env.example:XX` - Required environment variables
- `src/project_name/config.py:XX` - Configuration settings

**Documentation:**
- `docs/[feature].md` - Feature documentation
- `prd/[XX]_[Feature_Name].md` - Original PRD

---

## Decisions Made

Document all significant decisions to preserve context:

1. **Decision:** [Decision title]
   - **Date:** YYYY-MM-DD
   - **Rationale:** Why this approach was chosen
   - **Alternatives Considered:** Other options and why they were rejected
   - **Impact:** What this affects

2. **Decision:** Using JWT with Redis for session storage
   - **Date:** 2026-01-15
   - **Rationale:** Need distributed session management across multiple API instances
   - **Alternatives Considered:**
     - Local-only JWT (rejected: no session revocation)
     - Database sessions (rejected: too slow for high-frequency auth checks)
   - **Impact:** Requires Redis dependency, adds complexity but enables scalability

---

## Technical Notes

**Key Patterns Used:**
- [Pattern name]: [Brief description and file location]

**Dependencies Added:**
- `package-name==version` - [Why it was added]

**Database Changes:**
- Migration `YYYYMMDD_migration_name` - [What changed]

**Security Considerations:**
- [Security concern and how it's addressed]

**Performance Considerations:**
- [Performance consideration and optimization applied]

---

## Testing Status

**Unit Tests:**
- Coverage: XX% (target: 100%)
- Files: `tests/unit/test_[feature].py`
- Status: [Not Started | In Progress | Complete]

**Integration Tests:**
- Coverage: [Endpoints covered]
- Files: `tests/integration/test_[feature].py`
- Status: [Not Started | In Progress | Complete]

**Manual Testing:**
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Security testing completed
- [ ] Performance testing completed

---

## Next Session Priorities

**Immediate Next Steps (Start Here):**
1. [Highest priority task - what to do next]
2. [Second priority task]
3. [Third priority task]

**After That:**
- [Follow-up tasks]
- [Additional work needed]

**Before Marking Complete:**
- [ ] All tests pass
- [ ] Coverage ≥66% (or 100% if target)
- [ ] Documentation updated
- [ ] Code review completed
- [ ] PRD requirements verified
- [ ] Migration tested (if applicable)

---

## Session Log

**Session 1 (YYYY-MM-DD HH:MM - HH:MM):**
- Completed: [Tasks completed]
- Issues encountered: [Any problems]
- Decisions made: [Key decisions]
- Next: [What to do next]

**Session 2 (YYYY-MM-DD HH:MM - HH:MM):**
- Completed: [Tasks completed]
- Issues encountered: [Any problems]
- Decisions made: [Key decisions]
- Next: [What to do next]

---

## Git Commits

Reference commits related to this feature for traceability:

- `abc1234` - feat: add [feature component] [PRD-XX Task 1.1]
- `def5678` - test: add unit tests for [feature] [PRD-XX Task 2.1]
- `ghi9012` - docs: document [feature] API [PRD-XX Task 3.1]

---

## Notes

Any additional notes, warnings, or context that doesn't fit elsewhere:

- [Important note]
- [Gotcha or warning]
- [Reference to related work]
