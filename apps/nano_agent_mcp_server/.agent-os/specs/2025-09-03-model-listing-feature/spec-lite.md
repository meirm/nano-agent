# Model Listing Feature - Lite Summary

Add `nano-cli list-models` command and MCP tool to query available models across all supported providers (OpenAI, Anthropic, Ollama, LMStudio) with caching and graceful error handling.

## Key Points
- **CLI Command**: `nano-cli list-models --provider [provider]` displays models in formatted tables
- **Multi-Provider Support**: Integrates with OpenAI API, Ollama API, LMStudio API, and hardcoded Anthropic list
- **MCP Integration**: `list_available_models` tool for programmatic access via Claude Code
- **Performance**: Caching with TTL, concurrent requests, <3s response time per provider
- **User Experience**: Rich model metadata (size, context, capabilities, cost) with graceful error handling