# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-03-output-formatting-fixes/spec.md

> Created: 2025-09-03
> Version: 1.0.0

## Technical Requirements

### CLI Flag Extensions
- Add `--output-thinking` / `--show-thinking` flag to run and interactive commands
- Add `--panel-width` option with values: `<number>`, `auto`, `full` (default: 80)
- Integrate with existing Typer-based CLI infrastructure
- Maintain existing command signatures and behavior

### Content Filtering System
- **Thinking Marker Detection**: Regex patterns to identify thinking text sections
- **Content Cleaning Function**: `clean_agent_output()` in output_formats.py
- **Pattern Matching**: Remove `#### user`, `#### assistant`, conversation structure
- **Whitespace Normalization**: Clean extra newlines and formatting artifacts

### Output Format Enhancements
- **SimpleFormatter**: Apply content cleaning by default, respect thinking flag
- **JSONFormatter**: Include thinking control in data structure
- **RichFormatter**: Add panel width control, maintain visual consistency

### Data Structure Updates
```python
@dataclass
class AgentResponse:
    success: bool
    message: str
    data: Any
    raw_data: Optional[str] = None  # Preserve original output with thinking
    metadata: Dict[str, Any] = field(default_factory=dict)
    billing_info: Optional[BillingInfo] = None
```

### Component Integration Points
- **modules/output_formats.py**: Core formatting system with content filtering
- **cli.py**: CLI argument parsing and formatter creation
- **modules/nano_agent.py**: Response data structure population

## Implementation Approach

### Phase 1: Content Filtering Infrastructure
1. **Content Cleaning Function**: Pattern-based thinking marker removal
2. **Response Data Enhancement**: Preserve raw output alongside cleaned version
3. **Formatter Parameter Extension**: Add thinking and width control parameters

### Phase 2: CLI Integration
1. **Argument Parser Extension**: Add new CLI flags to Typer commands  
2. **Formatter Configuration**: Wire new parameters into formatter creation
3. **Backward Compatibility**: Ensure existing behavior with default settings

### Phase 3: Rich Format Panel Control
1. **Panel Width Configuration**: Configurable Panel width in RichFormatter
2. **Width Detection Logic**: Auto-sizing based on content and terminal
3. **Responsive Design**: Adapt to different content lengths appropriately

### Content Cleaning Algorithm
```python
def clean_agent_output(raw_output: str, show_thinking: bool = False) -> str:
    if show_thinking:
        return raw_output
    
    # Thinking marker patterns
    thinking_patterns = [
        r'####\s+(user|assistant|system)',
        r'<thinking>.*?</thinking>',
        r'Let me think.*?(?=\n\n|\n[A-Z])',
        r'\n\s*A\s*\n####',  # Pattern from user examples
    ]
    
    cleaned = raw_output
    for pattern in thinking_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    # Normalize whitespace
    cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
    return cleaned.strip()
```

### Rich Panel Width Logic
```python
class RichFormatter(OutputFormatter):
    def __init__(self, panel_width: Union[int, str] = 80):
        self.panel_width = self._resolve_width(panel_width)
    
    def _resolve_width(self, width_spec):
        if width_spec == "auto":
            return min(len(content) + 10, 100)
        elif width_spec == "full":
            return None  # Let Rich use full width
        else:
            return int(width_spec)
```

### Backward Compatibility Strategy
- Default values maintain current behavior
- New flags are opt-in additions
- Content cleaning disabled when thinking flag is used
- Panel width defaults to reasonable readable size (80 chars)

## Testing Requirements

### Unit Tests
- Content cleaning function with various thinking patterns
- Formatter behavior with different flag combinations
- Panel width calculation and rendering
- CLI argument parsing and validation

### Integration Tests
- End-to-end output formatting with real agent responses
- Cross-format consistency between simple and rich formats
- Flag interaction testing (verbose, billing, thinking, width)
- Backward compatibility with existing command usage