# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-09-03-billing-output-control/spec.md

> Created: 2025-09-03
> Version: 1.0.0

## CLI API Changes

### New Command Arguments

#### --billing Flag
```bash
# Show billing information
nano-cli run "summarize this file" --billing
nano-cli interactive --billing

# Hide billing information (default)
nano-cli run "summarize this file"
```

**Properties**:
- Type: Boolean flag
- Default: False (billing hidden)
- Scope: All commands that execute agents
- Behavior: When present, includes token usage and cost information in output

#### --output-format / -f Option
```bash
# Simple text output
nano-cli run "analyze code" --output-format simple
nano-cli run "analyze code" -f simple

# JSON output
nano-cli run "analyze code" --output-format json
nano-cli run "analyze code" -f json

# Decorated output (default)
nano-cli run "analyze code" --output-format rich
nano-cli run "analyze code"  # implicit default
```

**Properties**:
- Type: Enum (simple, json, rich)
- Default: rich
- Short form: -f
- Scope: All commands that produce output

### Updated Command Signatures

#### run Command
```python
@app.command()
def run(
    prompt: str = typer.Argument(..., help="The prompt to send to the nano agent"),
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="Model to use"),
    provider: str = typer.Option(DEFAULT_PROVIDER, "--provider", "-p", help="Provider to use"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    billing: bool = typer.Option(False, "--billing", help="Show billing and token usage information"),
    output_format: OutputFormat = typer.Option(OutputFormat.RICH, "--output-format", "-f", help="Output format")
) -> None:
```

#### interactive Command
```python
@app.command()
def interactive(
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="Model to use"),
    provider: str = typer.Option(DEFAULT_PROVIDER, "--provider", "-p", help="Provider to use"),
    billing: bool = typer.Option(False, "--billing", help="Show billing information in responses"),
    output_format: OutputFormat = typer.Option(OutputFormat.RICH, "--output-format", "-f", help="Output format")
) -> None:
```

## Output Format Specifications

### Simple Format
Plain text output suitable for command-line processing and scripting.

**Example Output**:
```
SUCCESS: Task completed successfully

The code analysis reveals 3 potential improvements:
1. Add error handling in main function
2. Optimize database query in user_service.py
3. Update deprecated API calls in auth module

Recommendations:
- Implement try-catch blocks
- Add database indexing
- Upgrade to latest API version
```

**With --billing**:
```
SUCCESS: Task completed successfully

The code analysis reveals 3 potential improvements:
1. Add error handling in main function
2. Optimize database query in user_service.py
3. Update deprecated API calls in auth module

Recommendations:
- Implement try-catch blocks
- Add database indexing
- Upgrade to latest API version

---
Tokens used: 1,250 | Estimated cost: $0.0025 | Model: gpt-5-mini | Provider: openai
```

### JSON Format
Structured JSON output for programmatic consumption.

**Schema**:
```json
{
  "success": true,
  "message": "Task completed successfully",
  "data": {
    "analysis": "The code analysis reveals 3 potential improvements...",
    "recommendations": [
      "Implement try-catch blocks",
      "Add database indexing", 
      "Upgrade to latest API version"
    ]
  },
  "metadata": {
    "execution_time": 2.45,
    "timestamp": "2025-09-03T10:30:00Z",
    "agent_turns": 3
  },
  "billing_info": {
    "tokens_used": 1250,
    "estimated_cost": 0.0025,
    "model": "gpt-5-mini",
    "provider": "openai",
    "request_timestamp": "2025-09-03T10:30:00Z"
  }
}
```

**Without --billing**:
```json
{
  "success": true,
  "message": "Task completed successfully", 
  "data": {
    "analysis": "The code analysis reveals 3 potential improvements...",
    "recommendations": [
      "Implement try-catch blocks",
      "Add database indexing",
      "Upgrade to latest API version"
    ]
  },
  "metadata": {
    "execution_time": 2.45,
    "timestamp": "2025-09-03T10:30:00Z",
    "agent_turns": 3
  }
}
```

### Decorated Format (Default)
Current Rich-based formatting with colors, panels, and enhanced visual presentation.

**Features**:
- Colored success/error indicators
- Formatted panels and sections
- Progress indicators
- Syntax highlighting for code
- Table formatting for structured data

## Backward Compatibility

### Existing Behavior Preservation
- All existing commands work without modification
- Default output format remains Rich-rich
- Billing information hidden by default (change from current behavior)
- No breaking changes to command signatures

### Migration Path
**Current users**: No action required - existing commands continue to work
**Cost monitoring users**: Add `--billing` flag to see token/cost information
**Script integration**: Use `--output-format json` or `--output-format simple`

## Error Handling

### Invalid Output Format
```bash
$ nano-cli run "test" --output-format invalid
Error: Invalid value for '--output-format' / '-f': 'invalid' is not one of 'simple', 'json', 'rich'.
```

### JSON Format Errors
- Malformed data → Include error in JSON structure
- Serialization failures → Fallback to simple format with error message

### Formatter Failures
- Rich import errors → Fallback to simple format
- Formatting exceptions → Log error, output raw data