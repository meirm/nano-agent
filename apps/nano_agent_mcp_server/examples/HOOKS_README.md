# Nano Agent Hooks System

The nano-agent hooks system allows you to intercept and modify agent behavior at various points during execution. This provides powerful customization capabilities for security, monitoring, and workflow automation.

## Overview

Hooks are user-defined scripts that run at specific events during agent execution. They can:
- **Block execution** - Prevent dangerous operations
- **Monitor performance** - Track metrics and costs
- **Log activity** - Audit tool usage and prompts
- **Filter content** - Validate or enhance prompts
- **Customize behavior** - Modify agent responses

## Quick Start

1. **Copy example hooks to your home directory:**
```bash
# Create hooks directory
mkdir -p ~/.nano-cli/hooks

# Copy example scripts
cp examples/hook_scripts/*.py ~/.nano-cli/hooks/
cp examples/hook_scripts/*.sh ~/.nano-cli/hooks/

# Make scripts executable
chmod +x ~/.nano-cli/hooks/*.py
chmod +x ~/.nano-cli/hooks/*.sh
```

2. **Copy and customize the configuration:**
```bash
# Copy example configuration
cp examples/hooks.json ~/.nano-cli/hooks.json

# Edit to enable/disable hooks as needed
nano ~/.nano-cli/hooks.json
```

3. **Test your hooks:**
```bash
# Run nano-cli to trigger hooks
nano-cli run "List files in current directory"
```

## Available Hook Events

### Agent Lifecycle Hooks

| Event | Description | Can Block | Use Cases |
|-------|-------------|-----------|-----------|
| `pre_agent_start` | Before agent initialization | Yes | Prompt validation, rate limiting |
| `post_agent_complete` | After agent completes | No | Performance monitoring, logging |
| `agent_error` | When agent encounters error | No | Error tracking, alerting |

### Tool Execution Hooks

| Event | Description | Can Block | Use Cases |
|-------|-------------|-----------|-----------|
| `pre_tool_use` | Before any tool execution | Yes | Security checks, validation |
| `post_tool_use` | After successful tool execution | No | Logging, metrics collection |
| `tool_error` | When tool execution fails | No | Error logging, recovery |

### MCP-Specific Hooks

| Event | Description | Can Block | Use Cases |
|-------|-------------|-----------|-----------|
| `mcp_request_received` | When MCP request arrives | Yes | Rate limiting, authentication |
| `mcp_response_ready` | Before sending MCP response | No | Response logging, metrics |

### Session Hooks (CLI only)

| Event | Description | Can Block | Use Cases |
|-------|-------------|-----------|-----------|
| `session_start` | When session begins/resumes | No | Session initialization |
| `session_end` | When session terminates | No | Cleanup, summary |
| `session_save` | Before saving session | No | Data validation |

### Prompt/Response Hooks

| Event | Description | Can Block | Use Cases |
|-------|-------------|-----------|-----------|
| `user_prompt_submit` | Before processing user prompt | Yes | Prompt enhancement |
| `agent_response` | After agent generates response | No | Response logging |

## Hook Configuration

Hooks are configured via JSON files. The system loads configurations from:
1. **Global**: `~/.nano-cli/hooks.json`
2. **Project**: `./.nano-cli/hooks.json` (in current directory)
3. **Custom**: Via configuration parameter

### Configuration Structure

```json
{
  "version": "1.0",
  "enabled": true,
  "timeout_seconds": 5,
  "parallel_execution": true,
  "hooks": {
    "EVENT_NAME": [
      {
        "name": "hook_name",
        "command": "path/to/script",
        "blocking": true/false,
        "timeout": 2,
        "enabled": true/false,
        "contexts": ["cli", "mcp"],
        "matcher": {
          "tool": ["write_file", "edit_file"],
          "pattern": ".*\\.py$"
        },
        "condition": "optional condition"
      }
    ]
  }
}
```

### Configuration Options

- **`enabled`**: Master switch for all hooks (true/false)
- **`timeout_seconds`**: Default timeout for hooks
- **`parallel_execution`**: Run non-blocking hooks in parallel
- **`hooks`**: Map of event names to hook configurations

### Hook Configuration

Each hook has:
- **`name`**: Unique identifier for the hook
- **`command`**: Command to execute (can use `~` for home directory)
- **`blocking`**: Whether hook can block execution
- **`timeout`**: Maximum execution time in seconds
- **`enabled`**: Whether this specific hook is active
- **`contexts`**: Where hook runs (["cli"], ["mcp"], or ["cli", "mcp"])
- **`matcher`**: Optional criteria for when hook should run
- **`condition`**: Optional additional condition

## Hook Data Format

Hooks receive event data as JSON via stdin:

```json
{
  "event": "pre_tool_use",
  "timestamp": "2024-01-15T10:30:00Z",
  "context": "cli",
  "working_dir": "/home/user/project",
  "model": "gpt-5-mini",
  "provider": "openai",
  "temperature": 0.7,
  "max_tokens": 4000,
  "prompt": "User's prompt text",
  "tool_name": "write_file",
  "tool_args": {
    "file_path": "example.txt",
    "content": "File content"
  },
  "session_id": "session-123",
  "mcp_client": "claude-desktop",
  "mcp_request_id": "req-456"
}
```

## Environment Variables

Hooks also receive key data as environment variables:
- `NANO_CLI_EVENT` - Event name
- `NANO_CLI_CONTEXT` - Execution context (cli/mcp)
- `NANO_CLI_WORKING_DIR` - Current working directory
- `NANO_CLI_SESSION_ID` - Session identifier
- `NANO_CLI_MODEL` - Model being used
- `NANO_CLI_PROVIDER` - Provider (openai/anthropic/ollama)
- `NANO_MCP_CONTEXT` - "true" if in MCP context
- `NANO_MCP_CLIENT` - MCP client identifier
- `NANO_MCP_REQUEST_ID` - MCP request ID

## Example Hook Scripts

### 1. Security Check (`security_check.py`)

Validates file operations to prevent dangerous actions:
- Blocks writes to sensitive files
- Prevents directory traversal
- Checks for dangerous content patterns
- Limits file sizes for editing

### 2. Prompt Filter (`prompt_filter.py`)

Filters and validates prompts:
- Blocks inappropriate content
- Enforces rate limits
- Detects prompt injection attempts
- Logs prompts for auditing

### 3. Performance Monitor (`performance_monitor.py`)

Tracks execution metrics:
- Monitors execution time
- Calculates token costs
- Generates performance reports
- Warns about threshold violations

### 4. Tool Usage Logger (`log_tool_usage.sh`)

Simple logging script:
- Logs all tool usage
- Tracks file modifications
- Generates daily summaries
- Rotates logs automatically

## Writing Custom Hooks

### Python Hook Template

```python
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        # Read event data
        input_data = sys.stdin.read()
        event_data = json.loads(input_data)

        # Your logic here
        tool_name = event_data.get("tool_name", "")

        # Allow execution
        print("Hook executed successfully", file=sys.stdout)
        return 0  # Allow

        # Or block execution
        # print("Blocked: Reason", file=sys.stderr)
        # return 1  # Block

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1  # Block on error

if __name__ == "__main__":
    sys.exit(main())
```

### Shell Hook Template

```bash
#!/bin/bash

# Read JSON from stdin
JSON_INPUT=$(cat)

# Extract fields (use jq for better parsing)
EVENT=$(echo "$JSON_INPUT" | grep -o '"event"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)

# Your logic here
echo "Processing event: $EVENT"

# Always return 0 for non-blocking hooks
exit 0
```

## Best Practices

1. **Keep hooks fast**: Use short timeouts (1-5 seconds)
2. **Handle errors gracefully**: Don't crash on unexpected input
3. **Use blocking sparingly**: Only block when necessary for security
4. **Log appropriately**: Balance detail with log size
5. **Test thoroughly**: Verify hooks work in both CLI and MCP contexts
6. **Document behavior**: Comment your hooks for maintainability

## Troubleshooting

### Hooks not running
- Check if hooks are enabled in configuration
- Verify hook script is executable (`chmod +x`)
- Check hook command path is correct
- Look for errors in nano-agent logs

### Hook blocking incorrectly
- Check exit codes (0 = allow, non-zero = block)
- Verify matcher and condition logic
- Test with simplified configuration

### Performance issues
- Reduce hook timeout values
- Enable parallel execution for non-blocking hooks
- Optimize hook scripts for speed
- Consider disabling verbose logging

## Security Considerations

- **Never log sensitive data**: Avoid logging passwords, keys, or PII
- **Validate all input**: Don't trust event data blindly
- **Use minimal permissions**: Run hooks with least privilege
- **Audit hook code**: Review hooks before deployment
- **Monitor hook behavior**: Track what hooks are doing

## Advanced Features

### Matchers

Control when hooks run based on criteria:

```json
"matcher": {
  "tool": ["write_file", "edit_file"],
  "pattern": ".*\\.(py|js|ts)$"
}
```

### Conditional Execution

Add conditions for fine-grained control:

```json
"condition": "{{context:mcp}}"
```

### Context-Specific Hooks

Run hooks only in specific contexts:

```json
"contexts": ["mcp"]  // Only runs in MCP context
```

## Integration with CI/CD

Hooks can be used in CI/CD pipelines:

1. **Pre-deployment checks**: Validate code before deployment
2. **Security scanning**: Check for vulnerabilities
3. **Compliance validation**: Ensure regulatory compliance
4. **Performance testing**: Monitor resource usage

## Contributing

To contribute new hook examples:

1. Create a well-documented hook script
2. Add example configuration to `hooks.json`
3. Update this README with usage information
4. Submit a pull request

## Support

For issues or questions about hooks:
- Check the [main README](../README.md)
- Review example scripts in `examples/hook_scripts/`
- Open an issue on GitHub