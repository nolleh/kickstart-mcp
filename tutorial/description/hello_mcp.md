# Hello MCP: Getting Started with Model Context Protocol

This tutorial will guide you through setting up and using Model Context Protocol (MCP) with different hosts.

## Prerequisites

- Python 3.8 or higher
- Node.js (for filesystem operations)
- Basic understanding of command line operations

## Choosing Your MCP Host

When you start the kickstart-mcp tool, you'll be presented with three options:

1. Claude
2. Cursor
3. Custom

Let's explore each option:

### 1. Claude Setup

If you choose Claude, the tool will automatically configure MCP for Claude Desktop. Here's what you need to do:

1. Download and install Claude Desktop from [Anthropic's website](https://www.anthropic.com/claude)
2. Open Claude Desktop
3. Go to Settings > Developer
4. Click "Edit Config"
5. The configuration file will be created at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

#### Adding Filesystem Support

To enable filesystem operations in Claude Desktop:

1. Open your Claude Desktop configuration file
2. Add the following configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Downloads"
      ]
    }
  }
}
```

Replace `username` with your computer's username. You can add more paths as needed.

### 2. Cursor Setup

If you choose Cursor:

1. Open Cursor
2. Go to Settings (⌘/Ctrl + ,)
3. Navigate to the MCP section
4. Configure your MCP settings according to your needs
5. Save the configuration

### 3. Custom Setup

For custom configurations:

1. The tool will create a custom configuration file
2. You can modify the configuration according to your specific needs
3. Follow the MCP specification for custom implementations

## Verifying Your Setup

After configuration:

1. Restart your chosen application (Claude Desktop or Cursor)
2. Look for the hammer icon (🔨) in the bottom right corner of the input box
3. Click the hammer icon to see available MCP tools

## Troubleshooting

If you encounter issues:

1. Check the application logs:
   - macOS: `~/Library/Logs/Claude` or `~/Library/Logs/Cursor`
   - Windows: `%APPDATA%\Claude\logs` or `%APPDATA%\Cursor\logs`
2. Ensure Node.js is installed globally
3. Verify file paths in your configuration are correct
4. Restart the application

## Next Steps

- Explore available MCP servers in the [MCP Server Gallery](https://modelcontextprotocol.io/servers)
- Learn how to build your own custom MCP server
- Check out the [MCP Specification](https://modelcontextprotocol.io/specification) for detailed documentation 
