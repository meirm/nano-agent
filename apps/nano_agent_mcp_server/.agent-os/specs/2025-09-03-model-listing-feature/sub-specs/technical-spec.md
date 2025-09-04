# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-03-model-listing-feature/spec.md

> Created: 2025-09-03
> Version: 1.0.0

## Technical Requirements

### Core Components
1. **Model Listing Module** (`modules/model_listing.py`)
2. **CLI Command Extension** (`nano_cli.py`)
3. **MCP Tool Integration** (`nano_agent_mcp_server.py`)
4. **Provider API Clients** (extension of `modules/provider_config.py`)
5. **Caching System** (new caching utilities)

### Performance Requirements
- **Response Time**: <3 seconds per provider, <10 seconds for all providers
- **Cache Hit Rate**: >80% for repeated requests
- **Memory Usage**: <50MB additional memory overhead
- **Concurrent Requests**: Support 4 concurrent provider API calls
- **Error Recovery**: <500ms timeout handling per provider

### Reliability Requirements
- **Availability**: Graceful degradation when providers are unavailable
- **Error Handling**: 100% coverage of identified failure scenarios
- **Data Consistency**: Model information accuracy >99%
- **Cache Invalidation**: Automatic cache refresh on API errors

## Approach

### Architecture Design

```python
# Core model listing architecture
class ModelLister:
    def __init__(self):
        self.providers = {
            'openai': OpenAIModelProvider(),
            'anthropic': AnthropicModelProvider(),
            'ollama': OllamaModelProvider(),
            'lmstudio': LMStudioModelProvider()
        }
        self.cache = ModelCache(ttl=300)  # 5 minute TTL
    
    async def list_models(self, provider: str = None) -> List[ModelInfo]:
        """List models from specified provider or all providers"""
        pass
    
    async def get_provider_models(self, provider_name: str) -> List[ModelInfo]:
        """Get models from a specific provider with caching"""
        pass
```

### Provider Implementation Strategy

#### 1. OpenAI Provider
```python
class OpenAIModelProvider(BaseModelProvider):
    async def fetch_models(self) -> List[ModelInfo]:
        """Fetch models from OpenAI API"""
        endpoint = "https://api.openai.com/v1/models"
        # Implementation details in approach section
```

#### 2. Anthropic Provider (Hardcoded)
```python
class AnthropicModelProvider(BaseModelProvider):
    MODELS = [
        ModelInfo(
            id="claude-3-5-sonnet-20241022",
            name="Claude 3.5 Sonnet",
            provider="anthropic",
            context_length=200000,
            capabilities=["text", "vision", "tools"],
            cost_per_1k_tokens=3.0
        ),
        # Additional models...
    ]
```

#### 3. Ollama Provider
```python
class OllamaModelProvider(BaseModelProvider):
    async def fetch_models(self) -> List[ModelInfo]:
        """Fetch models from Ollama API"""
        endpoint = f"{self.base_url}/v1/models"
        # Parse response and extract model information
```

#### 4. LMStudio Provider
```python
class LMStudioModelProvider(BaseModelProvider):
    async def fetch_models(self) -> List[ModelInfo]:
        """Fetch models from LMStudio API"""
        endpoint = f"{self.base_url}/v1/models"
        # Similar to Ollama but different response format
```

### Data Structures

#### ModelInfo Class
```python
@dataclass
class ModelInfo:
    id: str                    # Unique model identifier
    name: str                 # Human-readable name
    provider: str             # Provider name (openai, anthropic, etc.)
    context_length: Optional[int] = None  # Max context window
    capabilities: List[str] = None        # ["text", "vision", "tools", "code"]
    size: Optional[str] = None           # Model size (e.g., "7B", "13B")
    cost_per_1k_tokens: Optional[float] = None  # Cost per 1000 tokens
    created_at: Optional[datetime] = None
    owned_by: Optional[str] = None
```

#### ProviderStatus Class
```python
@dataclass
class ProviderStatus:
    name: str
    available: bool
    error_message: Optional[str] = None
    response_time: Optional[float] = None
    model_count: Optional[int] = None
```

### CLI Integration

#### Command Structure
```bash
nano-cli list-models [options]

Options:
  --provider TEXT     Filter by provider (openai|anthropic|ollama|lmstudio)
  --all              List models from all configured providers
  --format TEXT      Output format (table|json|yaml) [default: table]
  --no-cache         Skip cache and fetch fresh data
  --timeout INT      Request timeout in seconds [default: 30]
  --help             Show this message and exit
```

#### Implementation in nano_cli.py
```python
@click.command()
@click.option('--provider', type=click.Choice(['openai', 'anthropic', 'ollama', 'lmstudio', 'all']), 
              help='Filter by provider')
@click.option('--format', type=click.Choice(['table', 'json', 'yaml']), default='table',
              help='Output format')
@click.option('--no-cache', is_flag=True, help='Skip cache and fetch fresh data')
@click.option('--timeout', type=int, default=30, help='Request timeout in seconds')
def list_models(provider: str, format: str, no_cache: bool, timeout: int):
    """List available models from providers"""
    asyncio.run(list_models_async(provider, format, no_cache, timeout))
```

### MCP Tool Integration

#### Tool Definition
```python
list_available_models_tool = {
    "name": "list_available_models",
    "description": "List available models from specified providers with optional filtering and metadata",
    "inputSchema": {
        "type": "object",
        "properties": {
            "provider": {
                "type": "string",
                "enum": ["openai", "anthropic", "ollama", "lmstudio", "all"],
                "description": "Provider to query for models, or 'all' for all providers"
            },
            "include_metadata": {
                "type": "boolean",
                "default": True,
                "description": "Include detailed model metadata (size, capabilities, cost)"
            },
            "filter_capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Filter models by capabilities (text, vision, tools, code)"
            }
        },
        "required": []
    }
}
```

#### MCP Handler Implementation
```python
async def handle_list_available_models(arguments: dict) -> dict:
    """Handle MCP tool call for listing models"""
    try:
        provider = arguments.get('provider', 'all')
        include_metadata = arguments.get('include_metadata', True)
        filter_capabilities = arguments.get('filter_capabilities', [])
        
        model_lister = ModelLister()
        models = await model_lister.list_models(provider)
        
        # Filter by capabilities if specified
        if filter_capabilities:
            models = [m for m in models if any(cap in m.capabilities for cap in filter_capabilities)]
        
        # Format response
        response_data = []
        for model in models:
            model_data = {
                "id": model.id,
                "name": model.name,
                "provider": model.provider
            }
            
            if include_metadata:
                model_data.update({
                    "context_length": model.context_length,
                    "capabilities": model.capabilities,
                    "size": model.size,
                    "cost_per_1k_tokens": model.cost_per_1k_tokens
                })
            
            response_data.append(model_data)
        
        return {
            "success": True,
            "data": response_data,
            "message": f"Found {len(response_data)} models"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list models"
        }
```

### Caching Implementation

#### Cache Architecture
```python
class ModelCache:
    def __init__(self, ttl: int = 300, max_size: int = 1000):
        self.ttl = ttl  # Time to live in seconds
        self.max_size = max_size
        self.cache: Dict[str, CacheEntry] = {}
        self.access_times: Dict[str, datetime] = {}
    
    async def get(self, key: str) -> Optional[List[ModelInfo]]:
        """Get cached models if not expired"""
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry.created_at < timedelta(seconds=self.ttl):
                self.access_times[key] = datetime.now()
                return entry.models
            else:
                # Expired, remove from cache
                del self.cache[key]
                if key in self.access_times:
                    del self.access_times[key]
        return None
    
    async def set(self, key: str, models: List[ModelInfo]):
        """Cache models with automatic cleanup"""
        # Implement LRU eviction if cache is full
        if len(self.cache) >= self.max_size:
            await self._evict_oldest()
        
        self.cache[key] = CacheEntry(models=models, created_at=datetime.now())
        self.access_times[key] = datetime.now()
    
    async def _evict_oldest(self):
        """Evict least recently used entry"""
        if self.access_times:
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]

@dataclass
class CacheEntry:
    models: List[ModelInfo]
    created_at: datetime
```

### Error Handling Strategy

#### Exception Hierarchy
```python
class ModelListingError(Exception):
    """Base exception for model listing operations"""
    pass

class ProviderUnavailableError(ModelListingError):
    """Provider is not available or unreachable"""
    def __init__(self, provider: str, reason: str):
        self.provider = provider
        self.reason = reason
        super().__init__(f"Provider {provider} unavailable: {reason}")

class AuthenticationError(ModelListingError):
    """Authentication failed for provider"""
    def __init__(self, provider: str):
        self.provider = provider
        super().__init__(f"Authentication failed for {provider}")

class APIRateLimitError(ModelListingError):
    """Rate limit exceeded for provider"""
    def __init__(self, provider: str, retry_after: Optional[int] = None):
        self.provider = provider
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded for {provider}")
```

#### Error Handling Implementation
```python
async def safe_fetch_models(self, provider_name: str) -> Tuple[Optional[List[ModelInfo]], Optional[str]]:
    """Safely fetch models with comprehensive error handling"""
    try:
        provider = self.providers[provider_name]
        models = await asyncio.wait_for(
            provider.fetch_models(), 
            timeout=self.timeout
        )
        return models, None
    
    except asyncio.TimeoutError:
        error_msg = f"Timeout connecting to {provider_name}"
        logger.warning(error_msg)
        return None, error_msg
    
    except AuthenticationError as e:
        error_msg = f"Authentication failed for {provider_name}: Check API key"
        logger.error(error_msg)
        return None, error_msg
    
    except ProviderUnavailableError as e:
        error_msg = f"{provider_name} unavailable: {e.reason}"
        logger.warning(error_msg)
        return None, error_msg
    
    except Exception as e:
        error_msg = f"Unexpected error with {provider_name}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None, error_msg
```

## External Dependencies

### New Dependencies
```toml
# Add to pyproject.toml
[project.dependencies]
aiohttp = "^3.9.0"      # For async HTTP requests
rich = "^13.0.0"        # For rich table formatting in CLI
tabulate = "^0.9.0"     # Alternative table formatting
pydantic = "^2.0.0"     # Data validation and serialization
```

### API Endpoints

#### OpenAI Models API
```bash
GET https://api.openai.com/v1/models
Authorization: Bearer {api_key}

Response:
{
  "object": "list",
  "data": [
    {
      "id": "gpt-5-mini",
      "object": "model",
      "created": 1677649963,
      "owned_by": "openai"
    }
  ]
}
```

#### Ollama Models API
```bash
GET http://127.0.0.1:11434/v1/models

Response:
{
  "object": "list",
  "data": [
    {
      "id": "llama3.1:8b",
      "object": "model",
      "created": 1692897427,
      "owned_by": "library",
      "details": {
        "families": ["llama"],
        "format": "gguf",
        "parameter_size": "8B",
        "quantization_level": "Q4_0"
      }
    }
  ]
}
```

#### LMStudio Models API
```bash
GET http://localhost:1234/v1/models

Response:
{
  "object": "list",
  "data": [
    {
      "id": "microsoft/DialoGPT-medium",
      "object": "model",
      "created": 1677649963,
      "owned_by": "microsoft"
    }
  ]
}
```

### Provider Configuration Extensions
```python
# Extend modules/provider_config.py
PROVIDER_MODEL_ENDPOINTS = {
    'openai': 'https://api.openai.com/v1/models',
    'ollama': '{base_url}/v1/models',
    'lmstudio': '{base_url}/v1/models',
    # Anthropic has no public models endpoint
}

PROVIDER_CAPABILITIES = {
    'openai': {
        'gpt-5-mini': ['text', 'tools'],
        'gpt-5-nano': ['text', 'tools'],
        'gpt-4o': ['text', 'vision', 'tools'],
        'gpt-4o-mini': ['text', 'vision', 'tools']
    },
    'anthropic': {
        'claude-3-5-sonnet-20241022': ['text', 'vision', 'tools'],
        'claude-3-haiku-20240307': ['text', 'vision', 'tools']
    }
}
```

### Testing Strategy

#### Unit Tests
```python
# tests/test_model_listing.py
class TestModelListing:
    @pytest.fixture
    async def model_lister(self):
        return ModelLister()
    
    @pytest.mark.asyncio
    async def test_list_openai_models(self, model_lister, mock_openai_response):
        """Test OpenAI model listing with mocked API"""
        models = await model_lister.get_provider_models('openai')
        assert len(models) > 0
        assert all(m.provider == 'openai' for m in models)
    
    @pytest.mark.asyncio
    async def test_cache_functionality(self, model_lister):
        """Test model caching works correctly"""
        # First call should hit API
        models1 = await model_lister.get_provider_models('openai')
        
        # Second call should hit cache
        models2 = await model_lister.get_provider_models('openai')
        
        assert models1 == models2
    
    @pytest.mark.asyncio
    async def test_provider_unavailable(self, model_lister):
        """Test graceful handling of unavailable provider"""
        with patch.object(model_lister.providers['ollama'], 'fetch_models', 
                         side_effect=ProviderUnavailableError('ollama', 'Connection refused')):
            models, error = await model_lister.safe_fetch_models('ollama')
            assert models is None
            assert 'unavailable' in error.lower()
```

#### Integration Tests
```python
# tests/integration/test_model_listing_integration.py
class TestModelListingIntegration:
    @pytest.mark.integration
    async def test_real_openai_api(self):
        """Test against real OpenAI API (requires API key)"""
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip('OpenAI API key not available')
        
        lister = ModelLister()
        models = await lister.get_provider_models('openai')
        assert len(models) > 0
        assert any('gpt' in m.id.lower() for m in models)
    
    @pytest.mark.integration
    async def test_real_ollama_api(self):
        """Test against real Ollama API (requires running Ollama)"""
        try:
            lister = ModelLister()
            models = await lister.get_provider_models('ollama')
            # May be empty if no models installed, but should not error
            assert isinstance(models, list)
        except ProviderUnavailableError:
            pytest.skip('Ollama not running')
```

#### CLI Tests
```python
# tests/test_cli_model_listing.py
class TestCLIModelListing:
    def test_list_models_command_exists(self):
        """Test that list-models command is available"""
        result = runner.invoke(cli, ['list-models', '--help'])
        assert result.exit_code == 0
        assert 'List available models' in result.output
    
    def test_list_models_with_provider(self, mock_openai_models):
        """Test listing models for specific provider"""
        result = runner.invoke(cli, ['list-models', '--provider', 'openai'])
        assert result.exit_code == 0
        assert 'gpt' in result.output.lower()
    
    def test_list_models_json_format(self, mock_openai_models):
        """Test JSON output format"""
        result = runner.invoke(cli, ['list-models', '--provider', 'openai', '--format', 'json'])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) > 0
```

### Performance Benchmarks
```python
# tests/benchmarks/test_model_listing_performance.py
class TestModelListingPerformance:
    @pytest.mark.benchmark
    async def test_single_provider_performance(self, benchmark):
        """Benchmark single provider listing performance"""
        lister = ModelLister()
        result = benchmark(lambda: asyncio.run(lister.get_provider_models('openai')))
        assert result is not None
    
    @pytest.mark.benchmark
    async def test_all_providers_performance(self, benchmark):
        """Benchmark all providers listing performance"""
        lister = ModelLister()
        result = benchmark(lambda: asyncio.run(lister.list_models('all')))
        assert result is not None
    
    @pytest.mark.benchmark
    async def test_cache_performance(self, benchmark):
        """Benchmark cache hit performance"""
        lister = ModelLister()
        # Warm up cache
        await lister.get_provider_models('openai')
        
        # Benchmark cached access
        result = benchmark(lambda: asyncio.run(lister.get_provider_models('openai')))
        assert result is not None
```