# Nano Agent Configuration Guide

This guide covers configuration for both the nano-cli and the nano-agent MCP server. Configuration can be set at multiple levels with clear precedence rules.

## MCP Server Configuration

The nano-agent MCP server supports multiple ways to configure default provider and model settings:

### Setting Default Provider and Model

#### 1. Environment Variables (Highest Priority)

Set environment variables prefixed with `NANO_AGENT_`:

```bash
# Set default provider and model
export NANO_AGENT_DEFAULT_PROVIDER=openai
export NANO_AGENT_DEFAULT_MODEL=gpt-5-mini

# Or for Anthropic
export NANO_AGENT_DEFAULT_PROVIDER=anthropic
export NANO_AGENT_DEFAULT_MODEL=claude-3-haiku-20240307

# Or for local Ollama (built-in defaults)
export NANO_AGENT_DEFAULT_PROVIDER=ollama
export NANO_AGENT_DEFAULT_MODEL=gpt-oss:20b
```

## Nano CLI Configuration

The nano-cli supports persistent configuration through a JSON file at `~/.nano-cli/config.json`.

### Configuration File

The configuration file supports the following settings:

```json
{
  "ps1_format": "{time} {agent}@{model} > ",
  "default_model": "gpt-5-mini",
  "default_provider": "openai",
  "default_agent": "coder",
  "show_welcome": true
}
```

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

## Configuration Priority

Settings are loaded in the following priority order (highest to lowest):

1. **CLI flags** - Explicitly provided command-line options
2. **Config file** - Settings from `~/.nano-cli/config.json`  
3. **Built-in defaults** - Hardcoded defaults in the application

## Auto-Save Behavior

The configuration is automatically saved when you:
- Change the PS1 format with `/ps1`
- Change the model with `/model`
- Change the provider with `/provider`
- Switch agents with `@agent`

## Example Configurations

### Minimalist
```json
{
  "ps1_format": "> "
}
```

### Developer Setup
```json
{
  "ps1_format": "{pwd} [{agent}:{model}] $ ",
  "default_model": "gpt-5",
  "default_provider": "openai",
  "default_agent": "coder"
}
```

### Analyst Setup
```json
{
  "ps1_format": "[{time}] {agent}@{model} > ",
  "default_model": "gpt-4o",
  "default_provider": "openai",
  "default_agent": "analyst"
}
```

### Local Development
```json
{
  "ps1_format": "{pwd} $ ",
  "default_model": "gpt-oss:20b",
  "default_provider": "ollama",
  "default_agent": "coder"
}
```

## Manual Editing

You can manually edit the config file with any text editor:

```bash
# Edit with your default editor
nano ~/.nano-cli/config.json

# Or with any specific editor
vim ~/.nano-cli/config.json
code ~/.nano-cli/config.json
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

- `~/.nano-cli/config.json` - Main configuration file
- `~/.nano-cli/agents/` - Agent personality files
- `~/.nano-cli/commands/` - Command template files
- `~/.nano-cli/history.txt` - Command history

## Troubleshooting

### Config not loading
- Check file permissions: `ls -la ~/.nano-cli/config.json`
- Validate JSON syntax: `python -m json.tool ~/.nano-cli/config.json`
- Check for typos in key names

### Settings not persisting
- Ensure `~/.nano-cli/` directory is writable
- Check disk space
- Look for error messages when changing settings

### Reset to defaults
Remove or rename the config file:
```bash
rm ~/.nano-cli/config.json
# or
mv ~/.nano-cli/config.json ~/.nano-cli/config.json.backup
```

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

### Example: Project-Specific Configuration

For a project that needs specific models:

1. Create `.nano-agent.yaml` in project root:
```yaml
default_provider: anthropic
default_model: claude-opus-4-1-20250805

# Project uses specific Ollama setup
providers:
  ollama:
    api_base: http://gpu-server.local:11434/v1
```

2. All commands run from this directory will use these settings:
```bash
cd /path/to/project
nano-cli run "Analyze codebase"  # Uses Claude Opus 4.1
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