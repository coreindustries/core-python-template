# Cursor MCP Setup Guide

This guide explains how to set up and use Model Context Protocol (MCP) tools with Cursor to enhance your development workflow.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows AI assistants to interact with external tools and services. MCP servers provide additional capabilities beyond what's built into Cursor, such as database operations, API integrations, and specialized tooling.

## Recommended MCP Tools for Python Development

### 1. Supabase MCP

**Purpose**: Database operations, migrations, and schema management

**Use Cases**:
- Execute SQL queries safely
- Manage Prisma migrations
- Check database schema
- View logs and errors
- Generate TypeScript types

**Setup**:
1. Install Supabase CLI (if not already installed)
2. Configure in Cursor Settings → MCP Servers
3. Add your Supabase project URL and API key

**Configuration Example**:
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
```

**Usage in Cursor**:
- "Query the users table for active users"
- "Show me the database schema"
- "Check for recent errors in the database logs"
- "Generate TypeScript types from the Prisma schema"

### 2. GitHub MCP

**Purpose**: Repository management, PR creation, and issue tracking

**Use Cases**:
- Create pull requests
- Review code changes
- Manage issues
- Check repository status
- View commit history

**Setup**:
1. Generate a GitHub Personal Access Token with appropriate permissions
2. Configure in Cursor Settings → MCP Servers

**Configuration Example**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Usage in Cursor**:
- "Create a PR for the current branch"
- "Show me open issues"
- "Review the latest commits"
- "Check CI/CD status"

### 3. Firecrawl MCP

**Purpose**: Web scraping and documentation research

**Use Cases**:
- Scrape documentation from websites
- Research library APIs
- Extract information from web pages
- Generate documentation summaries

**Setup**:
1. Sign up for Firecrawl API (free tier available)
2. Get your API key
3. Configure in Cursor Settings → MCP Servers

**Configuration Example**:
```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "fc-your-api-key"  # pragma: allowlist secret
      }
    }
  }
}
```

**Usage in Cursor**:
- "Scrape the FastAPI documentation for authentication examples"
- "Get the latest Prisma migration guide"
- "Research best practices for async Python"

### 4. Context7 MCP

**Purpose**: Quick access to library documentation

**Use Cases**:
- Look up function signatures
- Find code examples
- Understand library APIs
- Get usage patterns

**Setup**:
1. No API key required (public service)
2. Configure in Cursor Settings → MCP Servers

**Configuration Example**:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "env": {}
    }
  }
}
```

**Usage in Cursor**:
- "Show me examples of using FastAPI dependencies"
- "How do I use Pydantic validators?"
- "Find Prisma query examples"

### 5. Figma MCP (Optional)

**Purpose**: Design-to-code workflows

**Use Cases**:
- Extract design specifications
- Generate component code from designs
- Sync design tokens
- Review design implementations

**Setup**:
1. Install Figma desktop app
2. Generate Figma API token
3. Configure in Cursor Settings → MCP Servers

**Configuration Example**:
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "figd_your_token"
      }
    }
  }
}
```

## Setting Up MCP in Cursor

### Step 1: Access Cursor Settings

1. Open Cursor
2. Go to **Settings** (Cmd/Ctrl + ,)
3. Navigate to **Features** → **MCP Servers**

### Step 2: Add MCP Server

1. Click **Add Server**
2. Enter server configuration (see examples above)
3. Save configuration
4. Restart Cursor if needed

### Step 3: Verify Installation

1. Open Cursor Chat
2. Try a command that uses MCP (e.g., "Query the database")
3. Check if MCP tools are available in the chat interface

## MCP Integration with Project Workflows

### Database Operations

Instead of manually running Prisma commands, use Supabase MCP:

```
User: "Show me all tables in the database"
AI: [Uses Supabase MCP to query schema]

User: "Create a migration for adding a user_profile table"
AI: [Uses Supabase MCP to generate migration]
```

### Documentation Research

When implementing new features, use Firecrawl MCP:

```
User: "I need to implement OAuth2. Show me FastAPI examples"
AI: [Uses Firecrawl MCP to scrape FastAPI OAuth docs]
```

### Code Examples

When learning a new library, use Context7 MCP:

```
User: "How do I use Prisma's findMany with filters?"
AI: [Uses Context7 MCP to find Prisma examples]
```

## Best Practices

### 1. Security

- **Never commit API keys**: Store MCP configuration in Cursor settings, not in code
- **Use environment variables**: For sensitive tokens, use environment variables
- **Limit permissions**: Grant MCP servers only the permissions they need
- **Rotate tokens**: Regularly rotate API keys and tokens

### 2. Performance

- **Cache results**: MCP tools may make external API calls; cache when possible
- **Batch operations**: Group related MCP operations together
- **Use selectively**: Don't use MCP for operations that can be done locally

### 3. Error Handling

- **Check availability**: Verify MCP server is running before using
- **Handle failures**: MCP operations can fail; have fallback strategies
- **Log operations**: Keep track of MCP operations for debugging

## Troubleshooting

### MCP Server Not Responding

1. Check server configuration in Cursor settings
2. Verify API keys are correct
3. Check network connectivity
4. Review Cursor logs for errors

### Permission Errors

1. Verify API tokens have correct permissions
2. Check service account permissions (for Supabase)
3. Review GitHub token scopes

### Performance Issues

1. Check MCP server logs
2. Verify API rate limits aren't exceeded
3. Consider caching frequently accessed data

## Example Workflows

### Feature Development with MCP

1. **Research**: Use Firecrawl MCP to research best practices
2. **Database**: Use Supabase MCP to check schema and create migrations
3. **Documentation**: Use Context7 MCP to find code examples
4. **Version Control**: Use GitHub MCP to create PRs

### Debugging with MCP

1. **Database**: Use Supabase MCP to check for data issues
2. **Logs**: Use Supabase MCP to view application logs
3. **History**: Use GitHub MCP to review recent changes

## Configuration Reference

See `.claude/settings.json` for MCP server references. Enable servers as needed for your project:

```json
{
  "mcp": {
    "servers": {
      "supabase": {
        "enabled": true,
        "note": "Configure in Cursor MCP settings"
      },
      "github": {
        "enabled": true,
        "note": "Requires GitHub token"
      }
    }
  }
}
```

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [Cursor MCP Documentation](https://docs.cursor.com/mcp)
- [Supabase MCP Server](https://github.com/supabase/mcp-server-supabase)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers)

## Next Steps

1. Choose MCP tools relevant to your project
2. Configure them in Cursor settings
3. Test with simple queries
4. Integrate into your development workflow
5. Share configurations with your team
