# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-03-billing-output-control/spec.md

> Created: 2025-09-03
> Version: 1.0.0

## Technical Requirements

### CLI Argument Extensions
- Add `--billing` flag to all relevant commands (run, interactive, etc.)
- Add `--output-format` / `-f` option with enum values: simple, json, rich
- Integrate with existing Typer-based CLI infrastructure
- Maintain existing command signatures and behavior

### Output Format System Architecture
- **Simple Format**: Plain text without ANSI codes or Rich formatting
- **JSON Format**: Structured output with standardized schema
- **Decorated Format**: Current Rich-based formatting (default)

### Data Structure Standardization
```python
@dataclass
class AgentResponse:
    success: bool
    message: str
    data: Any
    metadata: Dict[str, Any]
    billing_info: Optional[BillingInfo] = None
    
@dataclass
class BillingInfo:
    tokens_used: int
    estimated_cost: float
    provider: str
    model: str
    request_timestamp: datetime
```

### Component Integration Points
- **modules/nano_agent.py**: Core agent execution with response formatting
- **modules/token_tracking.py**: Billing information collection and calculation
- **CLI entry points**: Argument parsing and format selection
- **Output formatters**: New formatting system implementation

## Approach

### Phase 1: Core Infrastructure
1. **Argument Parser Extension**: Add new CLI flags to Typer commands
2. **Response Standardization**: Implement unified response data structure
3. **Formatter Framework**: Create pluggable output formatter system

### Phase 2: Format Implementation
1. **Simple Formatter**: Plain text output without Rich formatting
2. **JSON Formatter**: Structured output with complete data serialization
3. **Decorated Formatter**: Refactor existing Rich-based output

### Phase 3: Integration & Testing
1. **CLI Integration**: Wire formatters into command execution flow
2. **Billing Control**: Implement conditional billing information display
3. **Comprehensive Testing**: Unit tests for all format combinations

### Implementation Strategy

#### Formatter Pattern
```python
class OutputFormatter(ABC):
    @abstractmethod
    def format_response(self, response: AgentResponse, show_billing: bool) -> str:
        pass

class SimpleFormatter(OutputFormatter):
    def format_response(self, response: AgentResponse, show_billing: bool) -> str:
        # Plain text implementation
        pass

class JSONFormatter(OutputFormatter):
    def format_response(self, response: AgentResponse, show_billing: bool) -> str:
        # JSON serialization implementation
        pass

class DecoratedFormatter(OutputFormatter):
    def format_response(self, response: AgentResponse, show_billing: bool) -> str:
        # Rich formatting implementation (current behavior)
        pass
```

#### CLI Integration
```python
def run_command(
    prompt: str,
    billing: bool = False,
    output_format: OutputFormat = OutputFormat.RICH
):
    response = execute_agent(prompt)
    formatter = get_formatter(output_format)
    output = formatter.format_response(response, billing)
    console.print(output)
```

### Backward Compatibility Strategy
- Default values maintain current behavior
- Existing command signatures unchanged
- Rich formatting remains default
- No breaking changes to existing functionality

## External Dependencies

### Existing Dependencies
- **Typer**: CLI framework (already in use)
- **Rich**: Console formatting (already in use)
- **Pydantic**: Data validation (already in use for some components)

### New Dependencies (Optional)
- Consider **click-help-colors** for enhanced CLI help formatting
- Potential **jsonschema** for JSON output validation

### Development Dependencies
- **pytest**: Unit testing framework
- **pytest-mock**: Mocking for output format testing
- **typer[test]**: CLI testing utilities

### Version Constraints
- Maintain compatibility with existing dependency versions
- No major version upgrades required
- Typer >= 0.9.0 (current requirement)
- Rich >= 13.0.0 (current requirement)