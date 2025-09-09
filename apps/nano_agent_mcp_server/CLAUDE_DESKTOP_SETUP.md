# Claude Desktop Integration Guide for Nano Agent

This guide explains how to manually configure Claude Desktop to use the Nano Agent MCP server.

## ⚠️ Important Notice

**Never let installation scripts automatically modify your Claude Desktop configuration files.** This guide provides instructions for manual setup to ensure you maintain full control over your Claude Desktop configuration.

## Prerequisites

Before configuring Claude Desktop:

1. **Install Nano Agent** using the installation script:
   ```bash
   # macOS/Linux
   ./install.sh
   
   # Windows
   .\install.ps1
   ```

2. **Verify Installation** by checking that the command works:
   ```bash
   nano-agent --help
   ```

3. **Configure API Keys** in the `.env` file located at:
   - macOS/Linux: `~/.nano-agent/nano-agent/apps/nano_agent_mcp_server/.env`
   - Windows: `%USERPROFILE%\.nano-agent\nano-agent\apps\nano_agent_mcp_server\.env`

## Manual Configuration Steps

### Step 1: Locate Your Claude Desktop Configuration File

The configuration file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Step 2: Find the Nano Agent Command Path

The installation script should have installed `nano-agent` as a command. Find its location:

```bash
# macOS/Linux
which nano-agent

# Windows
where nano-agent
```

If the command is not found, check the uv tool directory:
- macOS/Linux: `~/.local/share/uv/tools/nano-agent/bin/nano-agent`
- Windows: `%LOCALAPPDATA%\uv\tools\nano-agent\Scripts\nano-agent.exe`

### Step 3: Edit the Configuration File

#### If the file doesn't exist:

Create it with this content (replace `<PATH_TO_NANO_AGENT>` with the actual path):

```json
{
  "mcpServers": {
    "nano-agent": {
      "command": "<PATH_TO_NANO_AGENT>",
      "args": [],
      "env": {}
    }
  }
}
```

#### If the file already exists:

Add the `nano-agent` entry to the existing `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      // ... existing configuration ...
    },
    "nano-agent": {
      "command": "<PATH_TO_NANO_AGENT>",
      "args": [],
      "env": {}
    }
  }
}
```

**⚠️ CRITICAL**: Be very careful when editing an existing configuration file. Make a backup first:

```bash
# macOS/Linux
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/claude_desktop_config.backup.json

# Windows
copy "%APPDATA%\Claude\claude_desktop_config.json" "%USERPROFILE%\claude_desktop_config.backup.json"
```

### Step 4: Restart Claude Desktop

1. Completely quit Claude Desktop (not just close the window)
2. Start Claude Desktop again

### Step 5: Verify the Connection

1. Open Claude Desktop
2. Look for the 🔌 (plug) icon in the interface
3. Click on it to see available MCP servers
4. You should see "nano-agent" in the list
5. The following tools should be available:
   - `prompt_nano_agent` - Execute autonomous agent tasks
   - `list_provider_models` - List available AI models
   - `get_session_info` - View session information
   - `list_sessions` - List conversation sessions
   - `get_available_models` - Check available AI models
   - `get_server_capabilities` - View server features

## Example Configuration

Here's a complete example for macOS with nano-agent installed via uv:

```json
{
  "mcpServers": {
    "nano-agent": {
      "command": "/Users/yourname/.local/bin/nano-agent",
      "args": [],
      "env": {}
    }
  }
}
```

## Troubleshooting

### Nano Agent doesn't appear in Claude Desktop

1. **Check the configuration file** for JSON syntax errors using:
   ```bash
   # Validate JSON syntax
   python -m json.tool < /path/to/claude_desktop_config.json
   ```

2. **Verify the command path** is correct:
   ```bash
   # Test the command directly
   /path/to/nano-agent --help
   ```

3. **Check Claude Desktop logs** for error messages

### "Server disconnected" error

This usually means nano-agent is crashing on startup. Check:

1. **API Keys**: Ensure at least one provider API key is configured in the `.env` file
2. **Python Version**: Nano-agent requires Python 3.9 or higher
3. **Dependencies**: Run `uv sync` in the nano-agent directory to ensure all dependencies are installed

### Tools don't work as expected

1. **Check API Key**: The provider you're trying to use must have a valid API key
2. **Test CLI first**: Try running `nano-cli run "test"` to ensure the basic functionality works
3. **Check file permissions**: Ensure nano-agent has permission to read/write in your working directory

## Security Considerations

1. **Never share your configuration file** as it may contain paths specific to your system
2. **Keep your API keys secure** - they should only be in the `.env` file, never in the Claude Desktop configuration
3. **Be cautious with file system access** - nano-agent has file read/write capabilities
4. **Use read-only mode** when appropriate by adding `--read-only` to the args array

## Advanced Configuration

### Adding Command Arguments

You can add default arguments to the nano-agent command:

```json
{
  "mcpServers": {
    "nano-agent": {
      "command": "nano-agent",
      "args": ["--verbose"],
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Multiple Configurations

You can have multiple nano-agent configurations with different settings:

```json
{
  "mcpServers": {
    "nano-agent-readonly": {
      "command": "nano-agent",
      "args": ["--read-only"],
      "env": {}
    },
    "nano-agent-full": {
      "command": "nano-agent",
      "args": [],
      "env": {}
    }
  }
}
```

## Getting Help

- **Documentation**: Check the README.md in the nano-agent repository
- **Issues**: Report problems at https://github.com/meirm/nano-agent/issues
- **CLI Help**: Run `nano-cli --help` for command-line usage

## Important Reminders

- ✅ **DO** manually edit your Claude Desktop configuration
- ✅ **DO** make backups before editing configuration files
- ✅ **DO** verify the nano-agent command works before adding to Claude Desktop
- ❌ **DON'T** let installation scripts automatically modify Claude Desktop files
- ❌ **DON'T** share your configuration files publicly
- ❌ **DON'T** put API keys in the Claude Desktop configuration