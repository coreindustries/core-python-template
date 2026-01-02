# /new-prd

Create a new Product Requirements Document from the project template.

## Usage

```
/new-prd <prd_number> <title>
```

## Arguments

- `prd_number`: Two-digit number for the PRD (e.g., `04`, `15`)
- `title`: Title of the PRD in Title Case

## Instructions

When this skill is invoked:

1. **Validate inputs**:
   - PRD number should be 2 digits (01-99)
   - Check that `prd/{prd_number}_*.md` doesn't already exist
   - Title should be descriptive

2. **Read the template** from `prd/PRD_TEMPLATE.md`

3. **Create the new PRD** at `prd/{prd_number}_{title_snake_case}.md`:
   - Replace template placeholders with actual values
   - Set version to "0.1"
   - Set status to "Draft"
   - Set last_updated to current date

4. **PRD Structure** (from template):
   ```markdown
   ---
   prd_version: "0.1"
   status: "Draft"
   last_updated: "YYYY-MM-DD"
   ---

   # {prd_number} – {Title}

   ## 1. Overview

   ### 1.1 Purpose
   [Brief description of what this PRD covers]

   ### 1.2 Scope
   [What is in scope and out of scope]

   ### 1.3 Goals
   - [ ] Goal 1
   - [ ] Goal 2

   ## 2. Requirements

   ### 2.1 Functional Requirements
   [List functional requirements]

   ### 2.2 Non-Functional Requirements
   [Performance, security, scalability requirements]

   ## 3. Technical Design

   ### 3.1 Architecture
   [High-level architecture]

   ### 3.2 Data Model
   [Database schema if applicable]

   ### 3.3 API Design
   [API endpoints if applicable]

   ## 4. Implementation

   ### 4.1 Dependencies
   [Required packages, services]

   ### 4.2 Configuration
   [Environment variables, settings]

   ### 4.3 Migration Plan
   [Database migrations, deployment steps]

   ## 5. Testing

   ### 5.1 Test Cases
   [Key test scenarios]

   ### 5.2 Acceptance Criteria
   [Definition of done]

   ## 6. References

   - Related PRDs
   - External documentation
   ```

5. **Update the PRD index** at `prd/00_PRD_index.md`:
   - Add the new PRD to the appropriate section
   - Mark as `[ ]` (not complete)

6. **After creation**, remind the user to:
   - Fill in the Overview section
   - Define requirements before implementation
   - Get stakeholder review for Draft status
   - Update status to "Active" when approved

## Example

```
/new-prd 04 "User Authentication"
```

Creates:
- `prd/04_User_authentication.md` with template filled in
- Updates `prd/00_PRD_index.md` with reference

## PRD Workflow

```
Draft → Review → Active → Deprecated
  ↓
Rejected
```

- **Draft**: Initial creation, being written
- **Review**: Ready for stakeholder review
- **Active**: Approved and in use
- **Deprecated**: No longer applicable
- **Rejected**: Did not pass review
