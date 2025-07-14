# PostgreSQL MCP Server for Cursor AI

This project provides a PostgreSQL MCP (Model Context Protocol) server that can be integrated with Cursor AI LLMs to provide database management capabilities.

## Features

The MCP server provides the following tools:

- **list_databases**: List all PostgreSQL databases
- **list_tables**: List all tables in the connected database
- **get_table_info**: Get column information for a specific table
- **get_relationships**: Get foreign key relationships between tables
- **execute_query**: Execute raw SQL queries

## Setup for Cursor AI Integration

Your PostgreSQL MCP server is already live at `https://psq-nwrf.onrender.com`!

### 1. Quick Setup (Recommended)

Simply create a `.cursorrules` file in your project root with the configuration below.

### 2. Cursor AI Configuration

Create a `.cursorrules` file in your project root:

```json
{
  "mcpServers": {
    "postgres-mcp": {
      "url": "https://psq-nwrf.onrender.com"
    }
  }
}
```

### 3. Alternative: Global Cursor Configuration

You can also configure the MCP server globally in Cursor:

1. Open Cursor Settings
2. Go to Extensions > MCP Servers
3. Add a new server configuration:
   - Name: `postgres-mcp`
   - URL: `https://psq-nwrf.onrender.com`

## Usage Examples

Once integrated, you can use the tools in Cursor AI conversations:

- "List all databases in my PostgreSQL instance"
- "Show me all tables in the current database"
- "Get the schema for the users table"
- "Show me the foreign key relationships"
- "Execute this SQL query: SELECT * FROM users LIMIT 10"

## API Endpoints

The server also provides REST API endpoints:

- `GET /list_databases` - List all databases
- `GET /list_tables` - List all tables
- `GET /get_table_info?table_name=users` - Get table schema
- `GET /get_relationships` - Get foreign key relationships
- `POST /execute_query?query=SELECT * FROM users` - Execute SQL query

## Running the Server

### MCP Server Mode
```bash
python psq.py
```

### FastAPI Server Mode
```bash
python api.py
```

## Security Notes

- Keep your database credentials secure
- Use environment variables for sensitive information
- Consider using connection pooling for production use
- The server runs with autocommit enabled for queries

## Troubleshooting

1. **Connection Issues**: Verify your database credentials and network connectivity
2. **MCP Server Not Found**: Ensure the server is running and Cursor can access the script
3. **Permission Errors**: Check that your database user has appropriate permissions
