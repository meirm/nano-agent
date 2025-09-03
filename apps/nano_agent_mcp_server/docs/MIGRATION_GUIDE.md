# Migration Guide: Flexible Model Configuration

## Overview

Nano Agent now supports flexible model configuration, allowing you to use **any model with any provider** without being restricted to a hardcoded list. This guide will help you migrate from the old system to the new configuration-based approach.

## What's Changed

### Before (Hardcoded)
- Models were restricted to predefined lists in `constants.py`
- Adding new models required code changes
- No support for custom providers
- Model validation was rigid

### After (Flexible)
- Use any model string with any provider
- Configure models through YAML/JSON files
- Add custom providers without code changes
- Model validation is configurable per provider

## Quick Start

### 1. Using Any Model (No Config Required)

The simplest way is to just use any model - the system will allow it by default:

```bash
# Use any model with LMStudio
nano-cli run "Hello" --provider lmstudio --model hermes-3-llama-3.2-3b

# Use any model with Ollama
nano-cli run "Hello" --provider ollama --model mixtral:8x7b

# Use any model with OpenAI
nano-cli run "Hello" --provider openai --model gpt-5-turbo
```

### 2. Creating a Configuration File

For more control, create a configuration file in one of these locations:

- **User config**: `~/.config/nano-agent/config.yaml`
- **Project config**: `.nano-agent.yaml` (in your project directory)
- **System config**: `/etc/nano-agent/config.yaml`

Example configuration:

```yaml
# ~/.config/nano-agent/config.yaml

# Set your defaults
default_provider: ollama
default_model: llama3.2:3b

providers:
  # Configure LMStudio
  lmstudio:
    api_base: http://localhost:1234
    allow_unknown_models: true  # Allow any model
    known_models:
      - hermes-3-llama-3.2-3b
      - qwen/qwen3-coder-30b
      - your-custom-model-here
    
  # Configure Ollama
  ollama:
    api_base: http://localhost:11434/v1
    allow_unknown_models: true
    discover_models: true  # Auto-discover installed models
    
  # Configure OpenAI
  openai:
    api_key_env: OPENAI_API_KEY
    allow_unknown_models: true
    known_models:
      - gpt-5-nano
      - gpt-5-mini
      - gpt-5
      - gpt-5-turbo  # Add new models here
      
  # Add a custom provider
  custom_provider:
    api_base: https://api.custom.com/v1
    api_key_env: CUSTOM_API_KEY
    allow_unknown_models: true
    known_models:
      - custom-model-1
      - custom-model-2

# Define convenient aliases
model_aliases:
  hermes: hermes-3-llama-3.2-3b
  llama: llama3.2:3b
  gpt5: gpt-5
```

## Configuration Options

### Provider Configuration

Each provider can have the following settings:

| Option | Description | Default |
|--------|-------------|---------|
| `api_base` | API endpoint URL | Provider-specific |
| `api_key_env` | Environment variable for API key | Provider-specific |
| `allow_unknown_models` | Allow models not in known_models list | `true` |
| `known_models` | List of known/validated models | `[]` |
| `discover_models` | Auto-discover available models | `false` |
| `discovery_endpoint` | API endpoint for model discovery | Provider-specific |
| `timeout` | Request timeout in seconds | `30` |
| `max_retries` | Maximum retry attempts | `3` |

### Model-Specific Configuration

You can configure settings per model:

```yaml
providers:
  openai:
    models:
      gpt-5:
        max_tokens: 8192
        temperature: 1.0
        description: "Most powerful model"
      gpt-5-mini:
        max_tokens: 4096
        temperature: 0.7
        description: "Balanced performance"
```

## Environment Variables

Override any configuration setting using environment variables with the `NANO_AGENT_` prefix:

```bash
# Set default provider
export NANO_AGENT_DEFAULT_PROVIDER=ollama

# Set default model
export NANO_AGENT_DEFAULT_MODEL=mixtral:8x7b

# Configure provider settings
export NANO_AGENT_PROVIDER_OLLAMA_API_BASE=http://remote-server:11434/v1
export NANO_AGENT_PROVIDER_OPENAI_ALLOW_UNKNOWN_MODELS=true
```

## Migration Steps

### Step 1: Update Nano Agent

Ensure you have the latest version with flexible configuration support:

```bash
# Install/update nano-agent
uv tool install -e . --force
```

### Step 2: Create Your Configuration (Optional)

Create `~/.config/nano-agent/config.yaml` with your preferred settings:

```bash
mkdir -p ~/.config/nano-agent
nano ~/.config/nano-agent/config.yaml
```

### Step 3: Test Your Models

Test that your models work:

```bash
# Test with a previously unsupported model
nano-cli run "Hello" --provider lmstudio --model your-custom-model

# Test with an alias
nano-cli run "Hello" --model hermes  # Uses hermes-3-llama-3.2-3b
```

## Common Use Cases

### Use Case 1: Local Development with Multiple Models

```yaml
default_provider: ollama
default_model: llama3.2:3b

providers:
  ollama:
    allow_unknown_models: true
    discover_models: true
    
model_aliases:
  fast: llama3.2:3b
  smart: mixtral:8x7b
  code: codellama:13b
```

### Use Case 2: Multi-Provider Setup

```yaml
# Use different providers for different tasks
providers:
  openai:
    # For production/paid API
    allow_unknown_models: false  # Strict validation
    known_models: [gpt-5, gpt-5-mini]
    
  ollama:
    # For local development
    allow_unknown_models: true  # Flexible
    
  anthropic:
    # For high-quality tasks
    allow_unknown_models: true
```

### Use Case 3: Custom Provider

```yaml
providers:
  my_company:
    api_base: https://llm.mycompany.com/v1
    api_key_env: COMPANY_LLM_KEY
    allow_unknown_models: true
    known_models:
      - company-model-v1
      - company-model-v2
```

## Troubleshooting

### Model Not Working?

1. Check if the provider allows unknown models:
   ```yaml
   providers:
     your_provider:
       allow_unknown_models: true  # Must be true for unlisted models
   ```

2. For local models (Ollama/LMStudio), ensure the model is installed:
   ```bash
   # For Ollama
   ollama pull your-model
   
   # For LMStudio
   # Download model through LMStudio UI
   ```

3. Check the logs for validation errors:
   ```bash
   nano-cli run "test" --provider your_provider --model your-model --verbose
   ```

### Configuration Not Loading?

Check configuration sources in order of precedence:
1. Command-line arguments (highest priority)
2. Environment variables (`NANO_AGENT_*`)
3. Project config (`.nano-agent.yaml`)
4. User config (`~/.config/nano-agent/config.yaml`)
5. System config (`/etc/nano-agent/config.yaml`)

### API Key Issues?

Ensure environment variables are set:
```bash
export OPENAI_API_KEY=your-key
export ANTHROPIC_API_KEY=your-key
# Or configure in the YAML file
```

## Backward Compatibility

The system maintains full backward compatibility:
- All previously supported models still work
- Existing CLI commands work unchanged
- Old configuration methods are still supported

## Advanced Features

### Model Discovery (Ollama)

Enable automatic model discovery:

```yaml
providers:
  ollama:
    discover_models: true
    discovery_endpoint: /api/tags
```

The system will automatically fetch available models from Ollama.

### Validation Modes

Control how strictly models are validated:

```yaml
providers:
  openai:
    allow_unknown_models: false  # Strict - only known models
    
  ollama:
    allow_unknown_models: true   # Flexible - any model
```

### Model Deprecation

Mark models as deprecated with helpful messages:

```yaml
providers:
  openai:
    models:
      gpt-4:
        deprecated: true
        deprecation_message: "Use gpt-5 instead for better performance"
```

## Getting Help

- Check the example configurations in `config/examples/`
- View the complete schema in `config/default_config.yaml`
- Report issues at: https://github.com/your-repo/nano-agent/issues

## Summary

The new flexible configuration system gives you complete control over model usage:
- ✅ Use any model with any provider
- ✅ Configure through YAML files
- ✅ Override with environment variables
- ✅ Add custom providers easily
- ✅ Maintain backward compatibility

Start using it today by simply running nano-cli with any model you want!