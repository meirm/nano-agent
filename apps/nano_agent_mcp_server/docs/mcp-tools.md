# MCP Tools Documentation

## Overview

The Nano Agent MCP Server provides several tools for model management, session management, and server introspection. These tools are available to any MCP client (like Claude Code) that connects to the server.

## Available Tools

### 1. `prompt_nano_agent`
Execute an autonomous agent with a natural language prompt.

**Parameters:**
- `agentic_prompt` (required): Natural language description of the work to be done
- `model`: Model to use (e.g., "gpt-5-mini", "claude-3-haiku")
- `provider`: Provider to use (e.g., "openai", "anthropic", "ollama")
- Additional configuration options...

### 2. `list_provider_models`
Query AI providers to get the list of available models with detailed information.

**Parameters:**
- `provider` (optional): Provider name to filter models (e.g., 'openai', 'anthropic', 'ollama', 'lmstudio')
  - If not specified, lists models from all providers
- `include_deprecated` (optional, default: false): Whether to include deprecated models
- `capability` (optional): Filter by capability (e.g., 'chat', 'vision', 'function_calling')

**Returns:**
```json
{
  "success": true,
  "models": [
    {
      "id": "claude-3-opus-20240229",
      "name": "Claude 3 Opus",
      "provider": "anthropic",
      "context_length": 200000,
      "capabilities": ["chat", "vision"],
      "deprecated": false
    }
  ],
  "total_count": 45,
  "providers": ["openai", "anthropic", "ollama", "lmstudio"],
  "provider_summary": {
    "openai": 20,
    "anthropic": 3,
    "ollama": 12,
    "lmstudio": 10
  }
}
```

**Example Usage:**
```python
# List all models
result = await list_provider_models()

# List models from specific provider
result = await list_provider_models(provider="anthropic")

# Filter by capability
result = await list_provider_models(capability="vision")

# Include deprecated models
result = await list_provider_models(include_deprecated=True)
```

### 3. `get_available_models`
Get list of statically configured models (doesn't query providers).

**Returns:**
```json
{
  "success": true,
  "providers": {
    "openai": {
      "models": ["gpt-5-mini", "gpt-5-nano", "gpt-5"],
      "default": "gpt-5-mini",
      "requirements": "Requires OPENAI_API_KEY"
    }
  },
  "total_models": 15
}
```

### 4. `get_session_info`
Get information about a specific conversation session.

**Parameters:**
- `session_id` (required): The session ID to retrieve

### 5. `list_sessions`
List all conversation sessions for the current client.

**Parameters:**
- `limit` (optional, default: 10): Maximum number of sessions to return

### 6. `clear_old_sessions`
Clean up old conversation sessions.

**Parameters:**
- `days` (optional, default: 30): Number of days to keep sessions

### 7. `get_server_capabilities`
Get server features, limitations, and available tools.

**Returns:**
```json
{
  "success": true,
  "capabilities": {
    "version": "0.2.1",
    "features": {
      "multi_provider": true,
      "session_management": true,
      "tool_restrictions": true
    },
    "limits": {
      "max_turns": 20,
      "max_tokens": 100000
    },
    "available_tools": ["read_file", "write_file", ...]
  }
}
```

## Provider Support

The `list_provider_models` tool supports the following providers:

### OpenAI
- **Requirements**: `OPENAI_API_KEY` environment variable
- **API Endpoint**: `https://api.openai.com/v1/models`
- **Models**: GPT-4, GPT-5 series, and more

### Anthropic
- **Requirements**: None (hardcoded model list)
- **Models**: Claude 3 series (Opus, Sonnet, Haiku)
- **Note**: Returns a static list of models since Anthropic doesn't provide a models API

### Ollama
- **Requirements**: Ollama server running locally
- **Default URL**: `http://localhost:11434`
- **API Endpoints**: Native Ollama API and OpenAI-compatible endpoint
- **Models**: Depends on locally installed models

### LMStudio
- **Requirements**: LMStudio server running locally
- **Default URL**: `http://localhost:1234`
- **API Endpoint**: OpenAI-compatible `/v1/models`
- **Models**: Depends on loaded models in LMStudio

## Error Handling

All tools return a consistent error format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "models": [],  // Empty result
  "providers": []
}
```

Common error types:
- `ProviderNotFoundError`: Unknown provider name
- `ProviderConnectionError`: Cannot connect to provider API
- `ProviderAuthenticationError`: Invalid or missing API key
- `ProviderRateLimitError`: Rate limit exceeded

## CLI Integration

The model listing functionality is also available through the CLI:

```bash
# List all models
nano-cli list-models --all

# List models from specific provider
nano-cli list-models --provider anthropic

# Show verbose output with capabilities
nano-cli list-models --provider openai --verbose

# Filter by capability
nano-cli list-models --capability vision

# Output as JSON
nano-cli list-models --format json

# Include deprecated models
nano-cli list-models --show-deprecated
```

## Implementation Notes

1. **Caching**: Provider responses are cached for 5 minutes (300 seconds) to reduce API calls
2. **Parallel Fetching**: When listing from all providers, requests are made in parallel for performance
3. **Error Resilience**: When listing all providers, individual provider failures don't stop the entire operation
4. **Auto-Detection**: Providers are automatically detected based on environment variables and local server availability