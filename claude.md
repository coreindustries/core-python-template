# Instructions for Using claude.md

## What is claude.md?

`claude.md` is a special file that provides context and instructions to AI assistants (like Claude) when working with your project. This file helps AI understand your project's specific requirements, conventions, and preferences.

## How to Use This File

### 1. Add Project-Specific Context

Include information that helps AI assistants understand your project:

- **Project Overview**: Brief description of what the project does
- **Key Technologies**: Main frameworks, libraries, and tools you're using
- **Architecture Patterns**: How your codebase is organized
- **Coding Conventions**: Style preferences, naming conventions, etc.
- **Common Patterns**: Reusable patterns or utilities in your codebase
- **Important Files**: Key files or directories AI should be aware of

### 2. Add AI Assistant Instructions

Specify how you want AI assistants to behave:

- **Code Style Preferences**: How you want code formatted or structured
- **Testing Requirements**: Whether tests should be written, what testing framework
- **Documentation Standards**: How documentation should be written
- **Error Handling**: Preferred error handling patterns
- **Performance Considerations**: Any performance requirements or optimizations

### 3. Reference Your PRDs

Since this is a PRD-driven project:

- Reference your technical standards document: `prd/0_Technical_standards_and_tech_stack.md`
- Mention that PRDs should be followed when implementing features
- Note that PRDs are the source of truth for requirements

### 4. Keep It Updated

- Update `claude.md` as your project evolves
- Add new conventions or patterns as they emerge
- Remove outdated information
- Keep it concise but comprehensive

## Example Structure

Here's a suggested structure for your `claude.md`:

```markdown
# Project Context for AI Assistants

## Project Overview

[Brief description of your project]

## Tech Stack

- Backend: [Your backend stack]
- Frontend: [Your frontend stack]
- Database: [Your database]
- Other tools: [Other important tools]

## Key Conventions

- [Important coding conventions]
- [Naming patterns]
- [File organization]

## PRD-Driven Development

- All features must follow PRDs in the `prd/` directory
- Reference `prd/0_Technical_standards_and_tech_stack.md` for technical standards
- Use `prd/PRD_TEMPLATE.md` as a template for new PRDs

## Code Style

- [Your specific code style preferences]
- [Linting/formatting tools]
- [Type safety requirements]

## Common Patterns

- [Reusable patterns in your codebase]
- [Utility functions or helpers]
- [Architecture patterns]

## Important Files/Directories

- `prd/` - Product Requirements Documents
- [Other important paths]
```

## Tips

1. **Be Specific**: The more specific you are, the better AI assistants can help you
2. **Use Examples**: Include code examples of patterns you want followed
3. **Reference Files**: Point to existing files that demonstrate your conventions
4. **Keep It Focused**: Don't include everything—focus on what's most important for AI assistants to know
5. **Version Control**: Commit `claude.md` to your repository so it's available to all team members

## How AI Assistants Use This File

When you work with an AI assistant in this project:

1. The AI will read `claude.md` to understand your project context
2. It will follow the conventions and patterns you've specified
3. It will reference your PRDs and technical standards
4. It will generate code that matches your style and requirements

---

**Note**: This file is currently empty. Populate it with your project-specific information to get the most value from AI assistants.
