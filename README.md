# kickstart-mcp

An interactive tutorial for learning Model Context Protocol (MCP). From setting up MCP hosts to building your own servers and clients, we'll guide you through every step of your MCP journey.

![AvailableTutorial](./docs/images/available_tutorial.png)

## Features

- Interactive tutorials for MCP setup and development
- Step-by-step guides for different MCP hosts (Claude, Cursor, Custom)
- Comprehensive coverage of MCP concepts:
  - Host configuration
  - Server development
  - Client implementation
- Built-in verification for each tutorial step
- Cross-platform support (macOS, Windows)

## Dependencies

For package management, we recommend using UV:

```bash
brew install uv
```

The build tool used in the instructions is Hatch, so you'll need to install it as well:

```bash
brew install hatch
```

## Installation

### Quick Start (Recommended)

```bash
uvx kickstart-mcp -l ko
```

Since v0.1.0, you can use the `-l` option to specify your preferred language.
Currently supported languages:

| Code | Language |
| ---- | -------- |
| en   | English  |
| ko   | Korean   |
| zh   | Chinese  |
| ja   | Japanese |

### Development Installation

```bash
# Clone the repository
git clone https://github.com/nolleh/kickstart-mcp.git
cd kickstart-mcp

# Install dependencies and run
uv run kickstart-mcp
```

## Usage

1. Start the tutorial:

   ```bash
   uvx kickstart-mcp
   ```

2. Follow the interactive prompts to:
   - Choose your preferred MCP host
   - Complete each tutorial step
   - Verify your progress
   - Learn MCP concepts hands-on

> While it's recommended to follow the tutorials in order, if you want to quickly learn server development,
> you can start with FastMcp in the McpServer tutorial.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Feedback

Have feedback or suggestions? Visit our [GitHub repository](https://github.com/nolleh/kickstart-mcp) to:

- Open an issue
- Submit a pull request
- Start a discussion
