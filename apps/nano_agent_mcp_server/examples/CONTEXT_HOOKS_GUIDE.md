# Context-Specific Hooks Guide

This guide explains how to configure hooks to run only in CLI or MCP contexts, or both.

## Why Context-Specific Hooks?

CLI and MCP modes have different requirements:

### CLI Mode Characteristics
- **Interactive**: User is present and can respond to prompts
- **Single-user**: Running on user's machine with their permissions
- **Development-focused**: Often used for development and debugging
- **Session-based**: Has session state and history

### MCP Mode Characteristics
- **Automated**: No user interaction possible
- **Multi-client**: May serve multiple clients (Claude Desktop, etc.)
- **Production-focused**: Needs strict security and rate limiting
- **Stateless**: Each request is independent

## Configuration Strategies

### 1. CLI-Only Hooks

Perfect for interactive features that require user presence:

```json
{
  "name": "interactive_confirmation",
  "command": "python3 ~/.nano-cli/hooks/confirm_action.py",
  "contexts": ["cli"],  // CLI only
  "blocking": true,
  "_comment": "Ask user to confirm dangerous operations"
}
```

**Use cases for CLI-only hooks:**
- User confirmation prompts
- Interactive debugging helpers
- Session management
- Command history tracking
- Development-time checks
- Verbose progress reporting

### 2. MCP-Only Hooks

Essential for API security and automation:

```json
{
  "name": "api_rate_limiter",
  "command": "python3 ~/.nano-cli/hooks/rate_limit.py",
  "contexts": ["mcp"],  // MCP only
  "blocking": true,
  "_comment": "Prevent API abuse"
}
```

**Use cases for MCP-only hooks:**
- Rate limiting
- API authentication
- Strict security policies
- Metrics collection
- Error reporting to monitoring systems
- Client-specific filtering

### 3. Universal Hooks (Both Contexts)

For consistent policies across all interfaces:

```json
{
  "name": "security_scanner",
  "command": "python3 ~/.nano-cli/hooks/security.py",
  "contexts": ["cli", "mcp"],  // Both
  "blocking": true,
  "_comment": "Apply same security policy everywhere"
}
```

**Use cases for universal hooks:**
- Security policies
- Audit logging
- Performance monitoring
- Error tracking
- Content filtering

## Practical Examples

### Example 1: Different Security Levels

```json
{
  "pre_tool_use": [
    {
      "name": "cli_relaxed_security",
      "command": "python3 ~/.nano-cli/hooks/basic_security.py",
      "contexts": ["cli"],
      "blocking": true,
      "_comment": "Basic checks for CLI - user can override"
    },
    {
      "name": "mcp_strict_security",
      "command": "python3 ~/.nano-cli/hooks/strict_security.py",
      "contexts": ["mcp"],
      "blocking": true,
      "_comment": "Strict checks for MCP - no overrides allowed"
    }
  ]
}
```

### Example 2: Different Logging Strategies

```json
{
  "post_agent_complete": [
    {
      "name": "cli_simple_log",
      "command": "echo 'Task complete' >> ~/.nano-cli/cli.log",
      "contexts": ["cli"],
      "blocking": false,
      "_comment": "Simple logging for CLI"
    },
    {
      "name": "mcp_structured_log",
      "command": "python3 ~/.nano-cli/hooks/json_logger.py",
      "contexts": ["mcp"],
      "blocking": false,
      "_comment": "Structured JSON logs for MCP monitoring"
    }
  ]
}
```

### Example 3: Development vs Production

```json
{
  "pre_agent_start": [
    {
      "name": "cli_debug_mode",
      "command": "python3 ~/.nano-cli/hooks/enable_debug.py",
      "contexts": ["cli"],
      "blocking": false,
      "_comment": "Enable debug features for CLI development"
    },
    {
      "name": "mcp_production_mode",
      "command": "python3 ~/.nano-cli/hooks/production_checks.py",
      "contexts": ["mcp"],
      "blocking": true,
      "_comment": "Enforce production standards for MCP"
    }
  ]
}
```

## Managing Multiple Configurations

### Option 1: Single Configuration File

Use one `hooks.json` with context-specific hooks:

```bash
~/.nano-cli/hooks.json  # Contains all hooks with context fields
```

### Option 2: Separate Configuration Files

Create different configs and switch between them:

```bash
~/.nano-cli/hooks-cli.json     # CLI-specific hooks
~/.nano-cli/hooks-mcp.json     # MCP-specific hooks
~/.nano-cli/hooks-unified.json # Combined configuration
```

Then symlink the one you want:
```bash
ln -sf ~/.nano-cli/hooks-cli.json ~/.nano-cli/hooks.json
```

### Option 3: Environment-Based Configuration

Use environment variables to control which hooks load:

```bash
# In your .bashrc or .zshrc for CLI
export NANO_HOOKS_CONFIG="~/.nano-cli/hooks-cli.json"

# In MCP server startup
export NANO_HOOKS_CONFIG="~/.nano-cli/hooks-mcp.json"
```

## Testing Context-Specific Hooks

### Test CLI Context

```bash
# Run nano-cli normally
nano-cli run "Create a test file"

# Check CLI-specific hooks ran
grep "cli_only" ~/.nano-cli/logs/*.log
```

### Test MCP Context

```bash
# Set MCP mode environment variable
export NANO_AGENT_MCP_MODE=true

# Run nano-agent as MCP server
nano-agent

# In another terminal, trigger MCP requests
# Check MCP-specific hooks ran
grep "mcp_only" ~/.nano-cli/logs/*.log
```

### Verify Context Detection

Create a debug hook that logs the context:

```python
#!/usr/bin/env python3
import json
import sys

data = json.loads(sys.stdin.read())
context = data.get("context", "unknown")
print(f"Running in {context} context", file=sys.stderr)
sys.exit(0)
```

## Best Practices

1. **Start Universal**: Begin with hooks that work in both contexts
2. **Add Context-Specific as Needed**: Only make hooks context-specific when necessary
3. **Document Intent**: Use `_comment` fields to explain why a hook is context-specific
4. **Test Both Contexts**: Always test hooks in both CLI and MCP modes
5. **Fail Safe**: If unsure, make security hooks universal
6. **Monitor Context**: Log which context hooks are running in for debugging

## Common Patterns

### Interactive CLI, Automated MCP

```json
{
  "pre_tool_use": [
    {
      "name": "cli_ask_user",
      "contexts": ["cli"],
      "command": "python3 ~/.nano-cli/hooks/ask_confirmation.py"
    },
    {
      "name": "mcp_auto_check",
      "contexts": ["mcp"],
      "command": "python3 ~/.nano-cli/hooks/auto_validate.py"
    }
  ]
}
```

### Verbose CLI, Silent MCP

```json
{
  "post_tool_use": [
    {
      "name": "cli_progress",
      "contexts": ["cli"],
      "command": "python3 ~/.nano-cli/hooks/show_progress.py"
    },
    {
      "name": "mcp_metrics",
      "contexts": ["mcp"],
      "command": "python3 ~/.nano-cli/hooks/silent_metrics.py"
    }
  ]
}
```

### Development CLI, Production MCP

```json
{
  "agent_error": [
    {
      "name": "cli_debug",
      "contexts": ["cli"],
      "command": "python3 ~/.nano-cli/hooks/debug_error.py"
    },
    {
      "name": "mcp_report",
      "contexts": ["mcp"],
      "command": "python3 ~/.nano-cli/hooks/report_error.py"
    }
  ]
}
```

## Troubleshooting

### Hook Not Running in Expected Context

1. Check the `contexts` field includes your context
2. Verify context detection with a debug hook
3. Check if hooks are enabled globally
4. Look for errors in loading hooks

### Wrong Context Detected

Check environment variables:
```bash
env | grep -E "NANO|MCP|CLAUDE"
```

### Different Behavior in Different Contexts

This is by design! Use context-specific hooks to customize behavior for each interface.

## Summary

The `contexts` field gives you complete control over where hooks run:
- `["cli"]` - CLI only
- `["mcp"]` - MCP only
- `["cli", "mcp"]` - Both contexts

This allows you to:
- Have interactive features in CLI
- Enforce strict automation in MCP
- Share common policies across both
- Customize behavior per interface