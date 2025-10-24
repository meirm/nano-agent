# Nano CLI Usage Guide

A comprehensive guide for using the `nano-cli` command-line interface to interact with autonomous AI agents.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
5. [Commands](#commands)
6. [Provider and Model Selection](#provider-and-model-selection)
7. [Command Files](#command-files)
8. [User-defined Tools](#user-defined-tools)
9. [Session Management](#session-management)
10. [Output Formats](#output-formats)
11. [Advanced Features](#advanced-features)
12. [Troubleshooting](#troubleshooting)

## Overview

`nano-cli` is a command-line interface for executing autonomous AI agents that can perform complex tasks including file operations, code analysis, and system commands. It supports multiple LLM providers (OpenAI, Anthropic, Ollama) and provides both interactive and non-interactive modes.

## Installation

For installation instructions, please refer to the [README.md](README.md) file. Quick setup:

```bash
# Install globally
./scripts/install.sh

# Or use directly with uv
cd apps/nano_agent_mcp_server
uv run nano-cli --help
```

## Configuration

### Configuration Priority

Configuration is loaded in the following order (later sources override earlier ones):

1. Default values in code
2. Configuration file: `~/.nano-cli/config.yaml`
3. Environment variables
4. Command-line arguments

### Configuration File

Location: `~/.nano-cli/config.yaml`

Example configuration:

```yaml
# Default provider and model
default_provider: ollama
default_model: gpt-oss:20b

# Provider configurations
providers:
  openai:
    api_key_env: OPENAI_API_KEY
    known_models:
      - gpt-5-nano
      - gpt-5-mini
      - gpt-5
      - gpt-4o
    
  anthropic:
    api_key_env: ANTHROPIC_API_KEY
    api_base: https://api.anthropic.com/v1
    known_models:
      - claude-3-haiku-20240307
      - claude-opus-4-20250514
    
  ollama:
    api_base: http://localhost:11434/v1
    known_models:
      - gpt-oss:20b
      - gpt-oss:120b
      - mistral-small3.2
```

### Environment Variables

```bash
# Provider API keys
export OPENAI_API_KEY=your-key-here
export ANTHROPIC_API_KEY=your-key-here

# Default provider and model
export NANO_AGENT_DEFAULT_PROVIDER=ollama
export NANO_AGENT_DEFAULT_MODEL=gpt-oss:20b

# Ollama configuration (optional)
export OLLAMA_API_URL=http://localhost:11434
```

## Basic Usage

### Running a Simple Prompt

```bash
# Using -p/--prompt flag (recommended)
nano-cli -p "Create a Python function that calculates fibonacci numbers"
nano-cli --prompt "Create a Python function that calculates fibonacci numbers"

# Using default provider and model with 'run' command (alternative)
nano-cli run "Create a Python function that calculates fibonacci numbers"

# Specify provider and model
nano-cli -p "Analyze this codebase" --provider openai --model gpt-5-mini

# Verbose output for debugging
nano-cli -p "Fix the bug in main.py" --verbose
```

### Interactive Mode

```bash
# Start interactive session (default when called without arguments)
nano-cli

# Or explicitly with 'interactive' command
nano-cli interactive

# With specific model
nano-cli --provider anthropic --model claude-3-haiku-20240307
nano-cli interactive --provider anthropic --model claude-3-haiku-20240307
```

### Read-Only Mode

For safe exploration without file modifications:

```bash
nano-cli -p "Analyze the security of this codebase" --read-only
```

## Commands

### Core Commands

#### Direct Prompt Execution (Main Entry Point)

```bash
# Using -p/--prompt flag (recommended approach)
nano-cli -p [PROMPT] [OPTIONS]
nano-cli --prompt [PROMPT] [OPTIONS]

# Examples:
nano-cli -p "Create a README file"
nano-cli -p "Analyze all Python files" --read-only
nano-cli -p "Fix type errors" --model gpt-5 --verbose
```

Options:
- `--provider`: LLM provider (openai, anthropic, ollama)
- `--model`: Model name
- `--read-only`: Prevent file modifications
- `--verbose`: Show detailed output
- `--output-format`: Output format (simple, markdown, json, rich)
- `--session`, `-s`: Use specific session ID
- `--continue`, `-c`: Continue last session
- `--new`, `-n`: Force new session

#### `run` - Execute a single prompt (Alternative)

```bash
nano-cli run [PROMPT] [OPTIONS]

# Examples:
nano-cli run "Create a README file"
nano-cli run "Analyze all Python files" --read-only
nano-cli run "Fix type errors" --model gpt-5 --verbose
```

**Note:** The `run` command is equivalent to using `-p/--prompt`. Use whichever you prefer.

#### Interactive Mode (Default)

```bash
# Start interactive session (runs when no arguments provided)
nano-cli

# Or explicitly with 'interactive' command
nano-cli interactive [OPTIONS]

# Examples:
nano-cli --model gpt-oss:120b --provider ollama
nano-cli interactive --model gpt-oss:120b --provider ollama
```

#### `test-tools` - Test available tools

```bash
# Quick validation of tool availability
nano-cli test-tools
```

#### `list-models` - List available models

```bash
# List all models from all providers
nano-cli list-models --all

# List models from specific provider
nano-cli list-models --provider openai

# Include deprecated models
nano-cli list-models --show-deprecated

# Filter by capability
nano-cli list-models --capability vision
```

### Command File Management

#### `commands list` - List available command files

```bash
nano-cli commands list
```

#### `commands show` - Display command content

```bash
nano-cli commands show summarize
```

#### `commands create` - Create new command

```bash
nano-cli commands create my-command
```

#### `commands edit` - Edit existing command

```bash
nano-cli commands edit my-command
```

#### Running Command Files

```bash
# Run a command file using -p flag
nano-cli -p '/summarize "content to summarize"'

# Command files support parameters
nano-cli -p '/analyze --depth deep --focus security'

# Alternative: use run command
nano-cli run '/summarize "content to summarize"'
```

## Provider and Model Selection

### OpenAI Models

```bash
# GPT-5 models
nano-cli -p "task" --provider openai --model gpt-5-nano    # Fastest, cheapest
nano-cli -p "task" --provider openai --model gpt-5-mini    # Balanced
nano-cli -p "task" --provider openai --model gpt-5         # Most capable
nano-cli -p "task" --provider openai --model gpt-4o        # Legacy
```

### Anthropic Models

```bash
# Claude models
nano-cli -p "task" --provider anthropic --model claude-3-haiku-20240307
nano-cli -p "task" --provider anthropic --model claude-opus-4-20250514
```

### Ollama (Local Models)

```bash
# Local models via Ollama
nano-cli -p "task" --provider ollama --model gpt-oss:20b
nano-cli -p "task" --provider ollama --model gpt-oss:120b
nano-cli -p "task" --provider ollama --model mistral-small3.2
```

## Command Files

Command files are reusable prompts stored in the `commands/` directory.

### Creating Command Files

1. Create a file in `commands/` directory:

```markdown
# commands/review-code.md
Review the following code for:
1. Security vulnerabilities
2. Performance issues
3. Code quality
4. Best practices

Focus on: {focus}
Depth: {depth}
```

2. Use the command:

```bash
nano-cli -p '/review-code --focus security --depth detailed'
```

### Command File Features

- **Parameters**: Use `{parameter_name}` placeholders
- **Default values**: Specify in frontmatter
- **Markdown support**: Full markdown formatting
- **Reusability**: Share across projects

## User-defined Tools

Extend nano-cli with custom tools stored in `~/.nano-cli/tools/`. Supports Python modules/packages and executable scripts.

### Tool Types

**Python Module** (exports `name` and `run(args)` function):
```python
# ~/.nano-cli/tools/hello_tool.py
name = "hello"

def run(args):
    return {"result": f"Hello, {args.get('name', 'World')}!"}
```

**Executable Script** (reads JSON from stdin, writes JSON to stdout):
```bash
#!/bin/bash
# ~/.nano-cli/tools/greet.sh
read input
name=$(echo "$input" | jq -r '.name // "World"')
echo "{\"result\": \"Greetings, $name!\"}"
```
Make executable: `chmod +x ~/.nano-cli/tools/greet.sh`

### Using Tools

```bash
# List available user tools
nano-cli list-user-tools

# Run a tool with JSON input
nano-cli run-user-tool hello --input '{"name":"Alice"}'
nano-cli run-user-tool greet --input-file input.json
```

### Security & Allowlist

Optional `~/.nano-cli/allowed-tools.json` restricts exposed tools (JSON array of names):
```json
["hello", "greet"]
```
See [CONFIG.md](CONFIG.md) for configuration details.

**Security Note**: Only use trusted tools. Future enhancements may include ownership checks, permission validation, and sandboxing.

## Session Management

### Session Persistence

Sessions maintain conversation context across multiple prompts:

```bash
# Start new session
nano-cli -p "Analyze main.py" --session my-analysis

# Continue session
nano-cli -p "Now check for security issues" --session my-analysis

# Continue last session automatically
nano-cli -p "What were the main issues?" --continue
```

### Session Storage

Sessions are stored in `~/.nano-cli/sessions/` and persist across CLI invocations.

## Output Formats

### Simple (Default)

```bash
nano-cli -p "task" --output-format simple
```

Clean, minimal output suitable for terminal display.

### Markdown

```bash
nano-cli -p "task" --output-format markdown
```

Formatted markdown with headers and code blocks.

### JSON

```bash
nano-cli -p "task" --output-format json
```

Structured JSON output for programmatic use.

### Rich

```bash
nano-cli -p "task" --output-format rich
```

Enhanced terminal output with colors and formatting (requires rich library).

## Advanced Features

### Temperature Control

Adjust response randomness:

```bash
# More deterministic (0.0)
nano-cli -p "Generate code" --temperature 0.0

# More creative (2.0)
nano-cli -p "Write story" --temperature 1.5
```

### Token Limits

Control response length:

```bash
nano-cli -p "Summarize" --max-tokens 500
```

### Tool Call Limits

Control agent iteration limits:

```bash
# Limit tool calls
nano-cli -p "Complex task" --max-tool-calls 10

# Allow unlimited (use with caution)
nano-cli -p "Complex task" --unlimited-tool-calls
```

## Troubleshooting

### Common Issues

#### API Key Not Found

```bash
# Check environment variable
echo $OPENAI_API_KEY

# Set API key
export OPENAI_API_KEY=your-key-here

# Or add to config file
echo "providers:
  openai:
    api_key: your-key-here" >> ~/.nano-cli/config.yaml
```

#### Model Not Available

```bash
# List available models
nano-cli list-models --provider openai

# Check model compatibility
nano-cli test-tools
```

#### Ollama Connection Issues

```bash
# Check Ollama is running
curl http://localhost:11434/v1/models

# Start Ollama
ollama serve

# Use custom URL
export OLLAMA_API_URL=http://your-server:11434
```

### Debug Mode

Enable verbose output for debugging:

```bash
# Verbose output
nano-cli -p "task" --verbose

# With specific provider
nano-cli -p "task" --verbose --provider ollama --model gpt-oss:20b

# Development mode with detailed errors
nano-cli -p "task" --dev
```

### Log Files

Logs are stored in `~/.nano-cli/logs/` for debugging purposes.

## Examples

### Code Analysis

```bash
# Analyze codebase for issues
nano-cli -p "Analyze this Python project for code quality issues" --read-only

# Security audit
nano-cli -p "Perform a security audit on all Python files" --read-only
```

### Code Generation

```bash
# Create a new feature
nano-cli -p "Create a REST API endpoint for user authentication"

# Generate tests
nano-cli -p "Write unit tests for the auth module"
```

### File Operations

```bash
# Organize files
nano-cli -p "Organize Python files into proper module structure"

# Search and replace
nano-cli -p "Replace all TODO comments with proper documentation"
```

### System Commands

```bash
# Run system diagnostics
nano-cli -p "Check system dependencies and create a report"

# Automation
nano-cli -p "Create a bash script to automate the build process"
```

## Best Practices

1. **Use Read-Only Mode**: When analyzing or reviewing code, use `--read-only` to prevent accidental modifications

2. **Session Management**: Use session IDs for multi-step tasks to maintain context

3. **Provider Selection**: 
   - Use Ollama for local/private data
   - Use OpenAI for complex tasks
   - Use Anthropic for nuanced understanding

4. **Command Files**: Create reusable command files for common tasks

5. **Path Restrictions**: Always use path restrictions when working with sensitive directories

6. **Environment Variables**: Keep API keys in environment variables, not in config files

7. **Output Formats**: Use JSON format for automation and integration with other tools

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report bugs or request features](https://github.com/your-repo/issues)
- Documentation: Check this guide and README.md
- Command Help: Use `nano-cli --help` or `nano-cli [command] --help`