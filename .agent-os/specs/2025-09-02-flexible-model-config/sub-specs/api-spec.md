# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-09-02-flexible-model-config/spec.md

> Created: 2025-09-02
> Version: 1.0.0

## Endpoints

### CLI Configuration API

#### Config Management Commands

**`nano-cli config set <key> <value> [--scope user|system|project]`**
- **Purpose**: Set configuration values
- **Parameters**: 
  - `key`: Configuration key (dot notation supported, e.g., "providers.openai.default_model")
  - `value`: Configuration value (string, parsed based on key type)
  - `--scope`: Configuration scope (default: user)
- **Examples**:
  ```bash
  nano-cli config set default_provider openai
  nano-cli config set providers.ollama.api_base http://localhost:11434
  nano-cli config set providers.openai.known_models '["gpt-5-nano", "gpt-5-mini"]'
  ```

**`nano-cli config get <key> [--scope merged|user|system|project]`**
- **Purpose**: Get configuration values
- **Parameters**:
  - `key`: Configuration key (dot notation supported)
  - `--scope`: Configuration scope to read from (default: merged)
- **Examples**:
  ```bash
  nano-cli config get default_provider
  nano-cli config get providers.openai.known_models
  nano-cli config get providers --scope user
  ```

**`nano-cli config list [--scope merged|user|system|project] [--format yaml|json|table]`**
- **Purpose**: List all configuration values
- **Parameters**:
  - `--scope`: Configuration scope (default: merged)
  - `--format`: Output format (default: yaml)
- **Examples**:
  ```bash
  nano-cli config list
  nano-cli config list --scope user --format json
  ```

**`nano-cli config validate [--fix] [--report]`**
- **Purpose**: Validate configuration files
- **Parameters**:
  - `--fix`: Attempt to auto-fix common issues
  - `--report`: Generate detailed validation report
- **Examples**:
  ```bash
  nano-cli config validate
  nano-cli config validate --fix --report
  ```

#### Model and Provider Discovery

**`nano-cli models list [--provider <provider>] [--available-only]`**
- **Purpose**: List available models
- **Parameters**:
  - `--provider`: Filter by specific provider
  - `--available-only`: Only show models currently accessible
- **Examples**:
  ```bash
  nano-cli models list
  nano-cli models list --provider ollama
  nano-cli models list --available-only
  ```

**`nano-cli providers list [--with-models]`**
- **Purpose**: List configured providers
- **Parameters**:
  - `--with-models`: Include model lists for each provider
- **Examples**:
  ```bash
  nano-cli providers list
  nano-cli providers list --with-models
  ```

**`nano-cli models discover --provider <provider>`**
- **Purpose**: Discover available models from provider API
- **Parameters**:
  - `--provider`: Provider to query (required)
- **Examples**:
  ```bash
  nano-cli models discover --provider ollama
  nano-cli models discover --provider openai
  ```

#### Enhanced Run Command

**`nano-cli run "<prompt>" [--model <model>] [--provider <provider>] [--save-config]`**
- **Purpose**: Enhanced run command with flexible model/provider support
- **Parameters**:
  - `--model`: Any model string (resolved via config)
  - `--provider`: Any configured provider
  - `--save-config`: Save successful combination as user default
- **Examples**:
  ```bash
  nano-cli run "test prompt" --model my-custom-model --provider ollama
  nano-cli run "test prompt" --model gpt5 --provider openai  # Uses alias
  nano-cli run "test prompt" --save-config  # Saves current combination as default
  ```

## Controllers

### ConfigManager Controller

#### Core Configuration Operations

**`load_configuration() -> NanoAgentConfig`**
```python
def load_configuration() -> NanoAgentConfig:
    """
    Load and merge configuration from all sources in priority order:
    1. Command line arguments
    2. Environment variables  
    3. Project config (.nano-agent.yaml)
    4. User config (~/.nano-agent/config.yaml)
    5. System config (/etc/nano-agent/config.yaml)
    6. Built-in defaults
    
    Returns: Merged configuration object
    Raises: ConfigurationError for invalid configurations
    """
```

**`validate_configuration(config: NanoAgentConfig) -> ValidationResult`**
```python
def validate_configuration(config: NanoAgentConfig) -> ValidationResult:
    """
    Validate configuration object against schema.
    
    Checks:
    - Required fields present
    - Provider configurations valid
    - Model aliases resolve correctly
    - API endpoints reachable (optional)
    
    Returns: ValidationResult with errors/warnings
    """
```

**`save_user_configuration(updates: Dict[str, Any]) -> bool`**
```python
def save_user_configuration(updates: Dict[str, Any]) -> bool:
    """
    Save configuration updates to user config file.
    
    Merges with existing user config and validates before saving.
    Creates ~/.nano-agent/ directory if it doesn't exist.
    
    Returns: True if successful, False otherwise
    Raises: ConfigurationError for validation failures
    """
```

#### Model and Provider Resolution

**`resolve_model_provider(model: str, provider: str) -> ModelProviderPair`**
```python
def resolve_model_provider(model: str = None, provider: str = None) -> ModelProviderPair:
    """
    Resolve model and provider to concrete values using configuration.
    
    Resolution order:
    1. Use explicit arguments if provided
    2. Apply model aliases if configured
    3. Use configured defaults
    4. Fall back to built-in defaults
    
    Returns: Resolved model and provider pair
    Raises: ConfigurationError if resolution fails
    """
```

**`validate_model_provider_combination(model: str, provider: str) -> ValidationResult`**
```python
def validate_model_provider_combination(model: str, provider: str) -> ValidationResult:
    """
    Validate that model can be used with provider.
    
    Validation levels:
    1. Provider exists and is configured
    2. Model in known_models list (warning if not)
    3. Provider allows arbitrary models (allow_any_model=true)
    4. API connectivity (optional, based on preferences)
    
    Returns: ValidationResult with status and warnings
    """
```

### CLI Controller Extensions

#### Configuration Management

**`handle_config_command(action: str, **kwargs) -> None`**
```python
def handle_config_command(action: str, **kwargs) -> None:
    """
    Handle all configuration-related CLI commands.
    
    Actions: set, get, list, validate, migrate
    Delegates to specific handlers based on action.
    Provides consistent error handling and output formatting.
    """
```

**`handle_models_command(action: str, **kwargs) -> None`**
```python
def handle_models_command(action: str, **kwargs) -> None:
    """
    Handle model discovery and listing commands.
    
    Actions: list, discover
    Integrates with provider APIs for real-time discovery.
    Caches results for performance.
    """
```

#### Enhanced Run Command Handler

**`handle_run_command_with_config(prompt: str, model: str, provider: str, **kwargs) -> None`**
```python
def handle_run_command_with_config(prompt: str, model: str = None, 
                                 provider: str = None, **kwargs) -> None:
    """
    Enhanced run command with configuration support.
    
    Features:
    - Flexible model/provider resolution
    - Configuration-based defaults
    - Model alias expansion
    - Success tracking for future defaults
    - Comprehensive error handling with suggestions
    """
```

### Provider Controller Extensions

#### Dynamic Model Validation

**`create_dynamic_validator(config: NanoAgentConfig) -> Callable`**
```python
def create_dynamic_validator(config: NanoAgentConfig) -> Callable:
    """
    Create a validation function based on current configuration.
    
    Replaces hardcoded model lists with config-driven validation.
    Supports per-provider validation rules and model aliases.
    
    Returns: Validation function for use in provider_config.py
    """
```

#### Model Discovery Integration

**`discover_ollama_models(base_url: str) -> List[str]`**
```python
def discover_ollama_models(base_url: str) -> List[str]:
    """
    Discover available models from Ollama API.
    
    Calls /api/tags endpoint and extracts model names.
    Caches results for 5 minutes to avoid repeated API calls.
    
    Returns: List of available model names
    Raises: ProviderError if API is unreachable
    """
```

**`validate_openai_model(model: str, api_key: str) -> bool`**
```python
def validate_openai_model(model: str, api_key: str) -> bool:
    """
    Validate model availability with OpenAI API.
    
    Optional validation - only runs if user preferences allow.
    Caches successful validations to avoid repeated API calls.
    
    Returns: True if model is available, False otherwise
    """
```