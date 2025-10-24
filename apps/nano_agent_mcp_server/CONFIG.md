# Nano Agent Configuration Guide

This guide covers configuration for both the nano-cli and the nano-agent MCP server.

## MCP Server Configuration (nano-agent)

The nano-agent MCP server uses **environment variables ONLY** for configuration. No config files are created or used.

### Environment Variables

Set environment variables prefixed with `NANO_AGENT_`:

```bash
# Set default provider and model
export NANO_AGENT_DEFAULT_PROVIDER=openai
export NANO_AGENT_DEFAULT_MODEL=gpt-5-mini

# Or for Anthropic
export NANO_AGENT_DEFAULT_PROVIDER=anthropic
export NANO_AGENT_DEFAULT_MODEL=claude-3-haiku-20240307

# Or for local Ollama
export NANO_AGENT_DEFAULT_PROVIDER=ollama
export NANO_AGENT_DEFAULT_MODEL=gpt-oss:20b

# API Keys
export OPENAI_API_KEY=your-key-here
export ANTHROPIC_API_KEY=your-key-here
export OLLAMA_API_URL=http://localhost:11434  # optional, this is the default
```

### Claude Desktop Configuration

When using nano-agent with Claude Desktop, set environment variables in the Claude Desktop config file:

```json
{
  "mcpServers": {
    "nano-agent": {
      "command": "/path/to/nano-agent",
      "args": [],
      "env": {
        "NANO_AGENT_DEFAULT_PROVIDER": "ollama",
        "NANO_AGENT_DEFAULT_MODEL": "qwen3:4b",
        "OPENAI_API_KEY": "your-key-if-needed"
      }
    }
  }
}
```

## Nano CLI Configuration

The nano-cli supports both environment variables and a persistent configuration file at `~/.config/nano-cli/config.yaml`.

### Configuration Priority

1. **Environment variables** (highest priority)
2. **Config file** (`~/.config/nano-cli/config.yaml`)
3. **Built-in defaults** (lowest priority)

### Configuration File

Create `~/.config/nano-cli/config.yaml` with the following structure:

```yaml
# Default provider and model
default_provider: openai
default_model: gpt-5-mini

# Interactive mode settings
ps1_format: "{time} {agent}@{model} > "
default_agent: coder
show_welcome: true

# Provider-specific settings (optional)
providers:
  ollama:
    api_url: http://localhost:11434
```

## Read-Only Mode Configuration

### Using Read-Only Mode

The nano-agent provides a dedicated read-only mode through `prompt_nano_agent_readonly` that prevents any file system modifications. This doesn't require configuration - it's enforced at the function level.

**Via MCP (Claude Desktop):**
```python
# Use the dedicated read-only function
Use prompt_nano_agent_readonly to analyze the codebase

# Or use the regular function with read_only flag
Use prompt_nano_agent with read_only=true to review the code
```

**Via CLI:**
```bash
# Use the --read-only flag
uv run nano-cli run "Analyze the code" --read-only

# This automatically blocks write operations
```

### What Gets Blocked
When read-only mode is active (either via `prompt_nano_agent_readonly` or `read_only=true`):
- `write_file` - Cannot create new files
- `edit_file` - Cannot modify existing files  
- `create_directory` - Cannot create directories
- `delete_file` - Cannot delete anything

### Use Cases for Read-Only Mode
- **Security Audits**: Scan for vulnerabilities without risk
- **Code Reviews**: Analyze quality without changes
- **Documentation**: Generate reports from existing code
- **Learning**: Safely explore unfamiliar codebases
- **Analysis**: Dependency graphs, architecture reviews

## Configuration Options

### ps1_format
The prompt format string for interactive mode. See [PS1.md](PS1.md) for details.

**Default**: `"{time} {agent}@{model} > "`

### default_model
The default AI model to use when not specified via CLI flags.

**Default**: `"gpt-5-mini"`

**Available models**: 
- OpenAI: `gpt-5-mini`, `gpt-5-nano`, `gpt-5`, `gpt-4o`, `gpt-4o-mini`
- Anthropic: `claude-3-haiku-20240307`, `claude-opus-4-1-20250805`, `claude-sonnet-4-20250514`
- Ollama: `gpt-oss:20b`, `gpt-oss:120b`

### default_provider
The default provider to use when not specified via CLI flags.

**Default**: `"openai"`

**Available providers**: `openai`, `anthropic`, `ollama`, `lmstudio`

### default_agent
The default agent personality to load on startup.

**Default**: `null` (no agent loaded)

**Available agents**: Any agent file in `~/.nano-cli/agents/` (e.g., `coder`, `analyst`, `h4x0r`)

### show_welcome
Whether to display the welcome message when starting interactive mode.

**Default**: `true`

**Options**: `true` or `false`

**Toggle in interactive mode**: Use `/welcome on` or `/welcome off`

## Configuration Priority Summary

### nano-agent (MCP Server)
1. **Environment variables** - From system or Claude Desktop config
2. **Built-in defaults** - Hardcoded in the application

### nano-cli
1. **CLI flags** - Explicitly provided command-line options
2. **Environment variables** - System environment variables
3. **Config file** - Settings from `~/.config/nano-cli/config.yaml`
4. **Built-in defaults** - Hardcoded in the application

## Auto-Save Behavior

The configuration is automatically saved when you:
- Change the PS1 format with `/ps1`
- Change the model with `/model`
- Change the provider with `/provider`
- Switch agents with `@agent`

## Example Configurations (nano-cli)

### Minimalist
```yaml
ps1_format: "> "
```

### Developer Setup
```yaml
ps1_format: "{pwd} [{agent}:{model}] $ "
default_model: gpt-5
default_provider: openai
default_agent: coder
```

### Analyst Setup
```yaml
ps1_format: "[{time}] {agent}@{model} > "
default_model: gpt-4o
default_provider: openai
default_agent: analyst
```

### Local Development
```yaml
ps1_format: "{pwd} $ "
default_model: gpt-oss:20b
default_provider: ollama
default_agent: coder
```

## Manual Editing

You can manually edit the nano-cli config file with any text editor:

```bash
# Edit with your default editor
nano ~/.config/nano-cli/config.yaml

# Or with any specific editor
vim ~/.config/nano-cli/config.yaml
code ~/.config/nano-cli/config.yaml
```

## Missing Keys

If any configuration key is missing from the file, the application will use the built-in defaults. You don't need to include all keys - only the ones you want to customize.

## Usage Examples

### Run with config defaults
```bash
# Uses default_model, default_provider, and default_agent from config
nano-cli run "Hello"

# Uses config defaults for interactive mode
nano-cli interactive
```

### Override config with CLI flags
```bash
# Override the default model
nano-cli run "Hello" --model gpt-4o

# Override the default agent
nano-cli interactive --agent h4x0r
```

## Related Files

### nano-cli
- `~/.config/nano-cli/config.yaml` - Main configuration file
- `~/.nano-cli/agents/` - Agent personality files
- `~/.nano-cli/commands/` - Command template files
- `~/.nano-cli/history.txt` - Command history

### nano-agent (MCP Server)
- No configuration files - uses environment variables only

### User tools

- Location: `~/.nano-cli/tools` — drop Python modules (exporting `name` + `run`) or executable scripts here.
- Optional allowlist: `~/.nano-cli/allowed-tools.json` — a JSON array of tool names. If present, only listed tools are exposed.
- See `apps/nano_agent_mcp_server/NANO_CLI_USAGE.md` -> "User-defined tools" for CLI examples (`list-user-tools`, `run-user-tool`) and usage snippets.

## Troubleshooting

### Config not loading (nano-cli)
- Check file permissions: `ls -la ~/.config/nano-cli/config.yaml`
- Validate YAML syntax: `python -c "import yaml; yaml.safe_load(open('~/.config/nano-cli/config.yaml'))"`
- Check for typos in key names

### Environment variables not working (nano-agent)
- Check variable names start with `NANO_AGENT_`
- Verify Claude Desktop config has env vars in the `env` section
- Restart Claude Desktop after config changes

### Settings not persisting
- Ensure `~/.nano-cli/` directory is writable
- Check disk space
- Look for error messages when changing settings

### Reset to defaults

For nano-cli:
```bash
rm ~/.config/nano-cli/config.yaml
# or
mv ~/.config/nano-cli/config.yaml ~/.config/nano-cli/config.yaml.backup
```

For nano-agent (MCP Server):
- Remove environment variables from Claude Desktop config
- Or unset them in your shell: `unset NANO_AGENT_DEFAULT_PROVIDER NANO_AGENT_DEFAULT_MODEL`

## Testing Default Configuration

### Check Current Defaults

```bash
# Show environment variables
env | grep NANO_AGENT_

# Test MCP server with defaults
echo '{"prompt": "List files"}' | nano-agent

# Test CLI with defaults
nano-cli run "List files"
```

### Example: Setting Organization-Wide Defaults

For a team using OpenAI primarily:

1. Set environment variables in shell profile (`~/.bashrc` or `~/.zshrc`):
```bash
export NANO_AGENT_DEFAULT_PROVIDER=openai
export NANO_AGENT_DEFAULT_MODEL=gpt-5-mini
```

2. Now all nano-agent commands use these defaults:
```bash
# Uses gpt-5-mini automatically
nano-cli run "Create a Python script"

# Claude Code will also use gpt-5-mini when calling nano-agent
```

3. Override when needed:
```bash
# Use a different model for complex tasks
nano-cli run "Complex analysis" --model gpt-5 --provider openai

# Use local model for testing
nano-cli run "Test task" --model gpt-oss:20b --provider ollama
```


## Available Providers and Models

### OpenAI
- `gpt-5-nano` - Fastest, best for simple tasks
- `gpt-5-mini` - Efficient, good for most tasks (recommended default)
- `gpt-5` - Most powerful, best for complex reasoning
- `gpt-4o` - Previous generation

### Anthropic
- `claude-3-haiku-20240307` - Fast and efficient
- `claude-opus-4-20250514` - Powerful reasoning
- `claude-opus-4-1-20250805` - Latest flagship
- `claude-sonnet-4-20250514` - Balanced performance

### Ollama (Local)
- `gpt-oss:20b` - Local open-source model (built-in default)
- `gpt-oss:120b` - Large local model
- Any model installed in Ollama

### LMStudio (Local)
- `qwen/qwen3-coder-30b`
- Any model loaded in LMStudio