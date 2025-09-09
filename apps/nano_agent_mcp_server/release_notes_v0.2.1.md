# Release Notes - v0.2.1

## Overview
Feature release adding dynamic model discovery, improved output formatting, and enhanced CLI capabilities.

## New Features

### 🔍 Dynamic Model Discovery
- Added `list-models` CLI command for querying available AI models
- New MCP tool `list_provider_models` for programmatic model discovery
- Support for OpenAI, Anthropic, Ollama, and LMStudio providers
- Real-time model availability from provider APIs
- Model capability filtering (chat, vision, function_calling, etc.)
- Deprecated model handling with replacement suggestions

### 🎯 Output Thinking Control
- Added `--output-thinking` flag to control display of agent thinking/reasoning text
- When enabled, preserves any thinking patterns in agent responses
- When disabled (default), filters out common thinking markers

### 📏 Panel Width Control  
- Added `--panel-width` flag for rich format output
- Allows custom panel widths (e.g., `--panel-width 50` for narrow displays)
- Defaults to terminal width when not specified

## Improvements

### Content Filtering
- Implemented smart filtering for agent output that removes:
  - `#### user` and `#### assistant` conversation markers
  - `<thinking>` XML-style tags
  - "Let me think/explain" phrases
  - Standalone "A" markers
- Preserves code blocks and formatting
- Normalizes excessive whitespace

### CLI Enhancements
- Better separation of concerns between output formatting and content
- Improved integration with existing formatter system
- Full backward compatibility maintained

## Technical Details

### Model Discovery Implementation
- Provider abstraction layer with `ModelProvider` base class
- Concrete implementations for each provider (OpenAI, Anthropic, Ollama, LMStudio)
- Singleton `ProviderRegistry` for managing all providers
- 5-minute caching to reduce API calls
- Parallel fetching when querying multiple providers
- Comprehensive error handling with specific exception types

### Output Formatting Implementation
- New `clean_agent_output()` function in `output_formats.py`
- Extended all formatter classes with `show_thinking` parameter
- Console width configuration for rich output
- Comprehensive test coverage for content filtering

### Usage Examples

#### Model Discovery
```bash
# List all available models
nano-cli list-models --all

# List models from specific provider
nano-cli list-models --provider anthropic

# Filter by capability with verbose output
nano-cli list-models --capability vision --verbose

# Get JSON output for programmatic use
nano-cli list-models --provider openai --format json

# Include deprecated models
nano-cli list-models --show-deprecated
```

#### Output Formatting
```bash
# Clean output (default)
nano-cli run "Explain recursion" --output-format simple

# Show thinking patterns if present
nano-cli run "Explain recursion" --output-format simple --output-thinking

# Control panel width
nano-cli run "Hello" --output-format rich --panel-width 80
```

## Important Notes

### About Thinking Text
The `--output-thinking` flag filters patterns that appear in the agent's response text. It does not expose the model's internal reasoning process, which is not accessible through the OpenAI Agent SDK. Most models don't generate thinking patterns in their output.

### Compatibility
- All changes are opt-in via flags
- Default behavior unchanged
- No breaking changes to existing API

## Dependencies Added
- `aiohttp>=3.9.0` for async HTTP requests to provider APIs

## Bug Fixes
- Fixed verbose mode panel display conditions
- Ensured billing information only appears with `--billing` flag
- Corrected error message formatting for provider not found errors
- Fixed `get_available_models` to handle list format in constants

## Testing
- Added 9 comprehensive tests for content filtering
- Added 10 tests for CLI list-models command
- Added 7 tests for MCP tool integration
- All tests passing with 100% coverage for new functionality

## Migration Guide
No migration required. All new features are opt-in and backward compatible.

## Contributors
- Implementation of output formatting improvements
- Enhanced CLI with thinking control and panel width options

---
*Version 0.2.1 - Released for improved output control and formatting flexibility*