# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-02-flexible-model-config/spec.md

> Created: 2025-09-02
> Version: 1.0.0

## Technical Requirements

### Configuration System Architecture

#### Configuration File Hierarchy
1. **System Config**: `/etc/nano-agent/config.yaml` (system-wide defaults)
2. **User Config**: `~/.nano-agent/config.yaml` (user preferences)
3. **Project Config**: `.nano-agent.yaml` (project-specific settings)
4. **Environment Variables**: Runtime overrides
5. **Command Line**: Explicit flags (highest priority)

#### Configuration Schema
```yaml
# Example configuration file
version: "1.0"
default_provider: "openai"
default_model: "gpt-5-mini"

providers:
  openai:
    api_base: "https://api.openai.com/v1"
    known_models:
      - "gpt-5-nano"
      - "gpt-5-mini"
      - "gpt-5-standard"
    model_aliases:
      "gpt5": "gpt-5-mini"
      "latest": "gpt-5-standard"
    
  anthropic:
    api_base: "https://api.anthropic.com"
    known_models:
      - "claude-3-haiku-20240307"
      - "claude-3-5-sonnet-20241022"
    cost_per_1m_tokens:
      input: 0.25
      output: 1.25
    
  ollama:
    api_base: "http://localhost:11434"
    allow_any_model: true
    known_models: []  # Auto-populated from /api/tags

user_preferences:
  warn_unknown_models: true
  validate_providers: true
  save_successful_combinations: true
```

### Core Components

#### 1. Configuration Manager (`modules/config_manager.py`)
```python
class ConfigManager:
    def __init__(self):
        self.config_hierarchy = []
        self.merged_config = {}
    
    def load_configs(self) -> Dict[str, Any]
    def get_default_provider(self) -> str
    def get_default_model(self, provider: str = None) -> str
    def get_provider_config(self, provider: str) -> Dict[str, Any]
    def validate_model_provider_combination(self, model: str, provider: str) -> ValidationResult
    def save_user_config(self, updates: Dict[str, Any]) -> bool
```

#### 2. Enhanced Provider Configuration (`modules/provider_config.py`)
- Remove hardcoded model restrictions from `validate_model_provider_combination()`
- Add dynamic model validation based on config
- Implement provider-specific model discovery
- Add model alias resolution

#### 3. CLI Configuration Commands (`modules/cli_config.py`)
```python
def config_set(key: str, value: str, scope: str = "user") -> None
def config_get(key: str, scope: str = "merged") -> Any
def config_list(scope: str = "merged") -> Dict[str, Any]
def config_validate() -> List[ValidationError]
def models_list(provider: str = None) -> List[str]
def providers_list() -> List[str]
```

### Implementation Approach

#### Phase 1: Core Configuration System
1. Create `ConfigManager` class with hierarchical loading
2. Define configuration schema and validation
3. Implement config file discovery and parsing
4. Add environment variable override support

#### Phase 2: Provider Integration
1. Modify `provider_config.py` to use dynamic configuration
2. Remove hardcoded model lists from `constants.py` 
3. Implement model alias resolution
4. Add provider-specific model discovery (Ollama `/api/tags`)

#### Phase 3: CLI Enhancement
1. Add `nano-cli config` subcommand group
2. Enhance `--model` and `--provider` flag handling
3. Implement configuration validation and diagnostics
4. Add model/provider discovery commands

#### Phase 4: Backward Compatibility
1. Maintain existing constants.py as fallback defaults
2. Ensure existing CLI commands work unchanged
3. Provide migration utilities and documentation
4. Add deprecation warnings for hardcoded usage patterns

### Data Structures

#### Configuration Object
```python
@dataclass
class NanoAgentConfig:
    version: str
    default_provider: str
    default_model: str
    providers: Dict[str, ProviderConfig]
    user_preferences: UserPreferences
    
@dataclass 
class ProviderConfig:
    api_base: str
    known_models: List[str]
    model_aliases: Dict[str, str]
    allow_any_model: bool = False
    cost_per_1m_tokens: Optional[Dict[str, float]] = None
    
@dataclass
class UserPreferences:
    warn_unknown_models: bool = True
    validate_providers: bool = True
    save_successful_combinations: bool = True
```

#### Validation Results
```python
@dataclass
class ValidationResult:
    is_valid: bool
    warnings: List[str]
    errors: List[str]
    resolved_model: str
    provider_config: Optional[ProviderConfig]
```

### File Modifications

#### New Files
- `modules/config_manager.py` - Configuration loading and management
- `modules/cli_config.py` - CLI configuration commands
- `config/default_config.yaml` - Default configuration template
- `tests/test_config_manager.py` - Configuration system tests

#### Modified Files  
- `modules/provider_config.py` - Remove hardcoded model restrictions
- `modules/constants.py` - Mark model lists as deprecated, add config defaults
- `cli.py` - Add config subcommand group and enhanced model handling
- `modules/nano_agent.py` - Use ConfigManager for model/provider resolution

## External Dependencies

### New Dependencies
- `pyyaml>=6.0` - YAML configuration file parsing
- `pydantic>=2.0` - Configuration validation and data classes
- `click>=8.0` - Enhanced CLI functionality (already present)

### Configuration File Locations
- System: `/etc/nano-agent/` (Linux/macOS), `%PROGRAMDATA%\nano-agent\` (Windows)
- User: `~/.nano-agent/` (cross-platform)
- Project: `.nano-agent.yaml` in current/parent directories

### Environment Variable Overrides
- `NANO_AGENT_DEFAULT_PROVIDER` - Override default provider
- `NANO_AGENT_DEFAULT_MODEL` - Override default model  
- `NANO_AGENT_CONFIG_PATH` - Custom config file path
- `NANO_AGENT_DISABLE_CONFIG` - Disable config loading (use hardcoded defaults)

### Backward Compatibility Strategy
1. **Gradual Migration**: Existing constants.py values become config defaults
2. **Fallback Support**: System works without config files using hardcoded values
3. **Deprecation Path**: Add warnings for hardcoded usage, eventual removal in v2.0
4. **Migration Tool**: `nano-cli config migrate` to convert hardcoded usage to config files