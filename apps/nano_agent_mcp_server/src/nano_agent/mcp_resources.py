"""
MCP Resources for Nano Agent Server.

These resources are exposed via the MCP protocol and can be accessed
by MCP clients to get information about the server.
"""
import logging

logger = logging.getLogger(__name__)

# Define functions that will be decorated as resources in __main__.py
from .modules.constants import VERSION
def get_version() -> str:
    """Get important server notices."""
    return f"Nano Agent MCP Server version {VERSION}"

def get_documentation() -> str:
    """Get server documentation."""
    return """# Nano Agent MCP Server - Complete Usage Guide

The enhanced Nano Agent MCP server provides powerful autonomous AI agents with fine-grained control, session persistence, and security features.

## 🚀 Quick Start

### Basic Usage
```python
# Simple agent execution
result = await prompt_nano_agent(
    "Create a Python function to calculate fibonacci numbers"
)
```

### With Configuration
```python
# Agent with specific model and safety settings
result = await prompt_nano_agent(
    "Analyze the security of this codebase",
    model="gpt-5",
    temperature=0.2,
    read_only=True,
    allowed_paths=["./src"]
)
```

### Session-Based Conversation
```python
# First call - creates session
result1 = await prompt_nano_agent(
    "Create a TODO app in Python",
    session_id="my-project-session"
)

# Follow-up call - continues conversation
result2 = await prompt_nano_agent(
    "Add user authentication to the app",
    session_id="my-project-session"
)
```

## 📋 Available MCP Tools

The following tools are exposed via the MCP protocol:

1. **prompt_nano_agent** - Execute autonomous agent with full configuration
2. **prompt_nano_agent_readonly** - Execute agent in read-only mode
3. **get_session_info** - Get information about a specific session
4. **list_sessions** - List all sessions for the client
5. **clear_old_sessions** - Clean up old session data
6. **get_available_models** - List available models and providers
7. **list_provider_models** - Query providers for current model lists
8. **get_server_capabilities** - Get server features and limitations

## Agent Internal Tools

When you execute `prompt_nano_agent`, the internal agent has access to:

- **read_file** - Read file contents
- **write_file** - Write content to files
- **list_directory** - List directory contents
- **get_file_info** - Get file metadata
- **edit_file** - Edit files by replacing text
- **grep_search** - Search for patterns using regex
- **search_files** - Find files by name
- **bash_command** - Execute shell commands

## Model Configuration

**Supported Providers:**
- `openai` - GPT-5 models (nano, mini, standard)
- `anthropic` - Claude models via OpenAI-compatible endpoint
- `ollama` - Local models via OpenAI-compatible API

**Parameters:**
- `model` (str): Model to use (default: "gpt-5-mini")
- `provider` (str): Provider ("openai", "anthropic", "ollama")
- `temperature` (float): Model creativity (0.0-2.0)
- `max_tokens` (int): Maximum response tokens
"""