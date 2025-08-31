# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-08-30-cursor-tools-mcp/spec.md

> Created: 2025-08-30
> Version: 1.0.0

## Configuration & Command System APIs

### Configuration Loading

#### Configuration Load Order
```python
def load_configuration() -> dict:
    """Load configuration with proper precedence"""
    # 1. Load global config
    if is_nano_cli:
        global_config = load_json("~/.nano-cli/config.json")
    else:  # is_nano_agent
        global_config = load_json("~/.nano-agent/config.json")
    
    # 2. Load project config (same for both)
    project_config = load_json(".nano-agent/config.json")
    
    # 3. Merge with project overriding global
    return deep_merge(global_config, project_config)
```

### Command File System

#### Command Loading
```python
def load_commands() -> dict:
    """Load command files with override behavior"""
    commands = {}
    
    # 1. Load global commands
    for file in glob("~/.nano-cli/commands/*.md"):
        name = Path(file).stem  # filename without extension
        commands[name] = load_command_file(file)
    
    # 2. Load project commands (override global)
    for file in glob(".nano-cli/commands/*.md"):
        name = Path(file).stem
        commands[name] = load_command_file(file)  # Override if exists
    
    return commands
```

### File Reference Support

#### File Reference Expansion
```python
def expand_file_references(prompt: str) -> str:
    """Expand @filepath references in prompts"""
    pattern = r'@([^\s]+)'  # Match @filepath
    
    def replace_reference(match):
        filepath = match.group(1)
        # Resolve relative or absolute path
        path = Path(filepath).resolve()
        if path.exists():
            return path.read_text()
        else:
            raise FileNotFoundError(f"File not found: {filepath}")
    
    return re.sub(pattern, replace_reference, prompt)
```

## MCP Tool Extensions

The following new tools will be added to the nano-agent MCP server's `prompt_nano_agent` function, extending the existing tool set while maintaining backward compatibility.

### Enhanced Search Tools (Semantic Search Deferred to Phase 3)

#### grep_search  
```python
@function_tool
def grep_search(pattern: str, file_pattern: Optional[str] = None, context_lines: int = 3) -> str
```

**Purpose:** Search for exact keywords or regex patterns within files using high-performance ripgrep
**Parameters:**
- pattern (required): Regex pattern or literal string to search for
- file_pattern (optional): Glob pattern to filter files (e.g., "*.py")
- context_lines (optional): Number of surrounding lines to include (default: 3)
**Response:** Formatted text with matching lines, file paths, and line numbers
**Errors:** PatternError, RipgrepNotFound, SearchFailed

#### search_files
```python
@function_tool
def search_files(name_query: str, max_results: int = 20) -> str
```

**Purpose:** Find files by name using fuzzy matching algorithms
**Parameters:**
- name_query (required): Partial or complete filename to search for
- max_results (optional): Maximum number of results to return (default: 20)
**Response:** JSON string with file paths ranked by fuzzy matching score
**Errors:** SearchTimeout, InvalidQuery

#### web_search
```python
@function_tool
def web_search(query: str, num_results: int = 5) -> str
```

**Purpose:** Generate search queries and perform web searches with content summarization
**Parameters:**
- query (required): Search query string
- num_results (optional): Number of search results to return (default: 5)
**Response:** JSON string with search results including titles, URLs, and content snippets
**Errors:** SearchAPIError, NetworkTimeout, RateLimitExceeded

### Enhanced File Operations

#### edit_and_apply
```python
@function_tool
def edit_and_apply(file_path: str, description: str, auto_apply: bool = False) -> str
```

**Purpose:** Suggest edits to files with AI-powered context understanding and diff preview
**Parameters:**
- file_path (required): Path to file to be edited
- description (required): Natural language description of desired changes
- auto_apply (optional): Whether to automatically apply changes (default: False)
**Response:** Diff preview with option to apply changes, or success message if auto-applied
**Errors:** FileNotFound, EditGenerationFailed, ApplyFailed

#### delete_file
```python
@function_tool  
def delete_file(file_path: str, confirm: bool = True) -> str
```

**Purpose:** Delete files with safety guardrails and recovery options
**Parameters:**
- file_path (required): Path to file to be deleted
- confirm (optional): Require confirmation for deletion (default: True)
**Response:** Success message with recovery instructions
**Errors:** FileNotFound, PermissionDenied, RecoveryFailed

#### run_terminal
```python
@function_tool
def run_terminal(command: str, working_dir: Optional[str] = None, timeout: int = 30) -> str
```

**Purpose:** Execute terminal commands with output monitoring and safety checks
**Parameters:**
- command (required): Shell command to execute
- working_dir (optional): Working directory for command execution
- timeout (optional): Maximum execution time in seconds (default: 30)
**Response:** Command output including stdout, stderr, and exit code
**Errors:** CommandTimeout, ExecutionFailed, UnsafeCommand, PermissionDenied

## MCP Server Integration Endpoints

### Dynamic Tool Registration

The MCP bridge will dynamically register external MCP server tools with the following naming convention:
- Format: `{server_name}_{tool_name}`
- Example: `context7_search_docs`, `github_create_issue`, `playwright_take_screenshot`

#### External Tool Wrapper Template
```python
@function_tool
def {server_name}_{tool_name}(**kwargs) -> str:
    """Call {tool_name} from {server_name} MCP server"""
    return mcp_bridge.call_tool(server_name, tool_name, **kwargs)
```

**Purpose:** Provide unified access to external MCP server tools through nano-agent
**Parameters:** Dynamic based on external MCP server tool schemas
**Response:** Forwarded response from external MCP server
**Errors:** MCPServerUnavailable, ToolNotFound, CommunicationTimeout

## Configuration API Extensions

### MCP Server Configuration

#### Global Configuration Schemas

**nano-cli Global Config (~/.nano-cli/config.json)**
```json
{
  "default_model": "string",
  "default_provider": "string",
  "temperature": number,
  "max_tokens": number,
  "commands_directory": "~/.nano-cli/commands",
  "mcp_servers": {
    "{server_name}": {
      "command": "string",
      "args": ["array", "of", "strings"],
      "env": {"ENV_VAR": "value"},
      "enabled": boolean
    }
  }
}
```

**nano-agent Global Config (~/.nano-agent/config.json)**
```json
{
  "mcp_servers": {
    "{server_name}": {
      "command": "string",
      "args": ["array", "of", "strings"],
      "env": {"ENV_VAR": "value"},
      "enabled": boolean,
      "tools": ["array", "of", "tool", "names"],
      "timeout": number,
      "retry_attempts": number
    }
  },
  "tool_settings": {
    "auto_apply_edits": boolean,
    "safe_mode": boolean,
    "max_terminal_timeout": number
  }
}
```

#### Project Configuration Schema (.nano-agent/config.json at project root)
```json
{
  "mcp_servers": {
    "{server_name}": {
      "command": "string",
      "env": {"PROJECT_SPECIFIC_ENV": "value"},
      "tools": ["allowed", "tools"],
      "enabled": boolean
    }
  },
  "disabled_tools": ["array", "of", "disabled", "tool", "names"],
  "restricted_paths": ["array", "of", "path", "patterns"],
  "commands_directory": ".nano-cli/commands",
  "search_settings": {
    "excluded_directories": [".git", "node_modules", "__pycache__"],
    "indexed_extensions": [".py", ".js", ".ts", ".md", ".json"]
  }
}
```

## Error Handling Specifications

### Standard Error Response Format
```json
{
  "success": false,
  "error": {
    "type": "ErrorType",
    "message": "Human-readable error description",
    "code": "ERROR_CODE",
    "details": {
      "context": "Additional error context",
      "suggestions": ["Possible solutions"]
    }
  }
}
```

### Error Types and Recovery
- **MCPServerUnavailable**: Fallback to built-in alternatives where possible
- **ToolNotFound**: Provide suggestions for similar available tools  
- **ConfigurationError**: Clear validation messages with fix suggestions
- **PermissionDenied**: Explain permission requirements and resolution steps
- **ResourceTimeout**: Automatic retry with exponential backoff

## Backward Compatibility Guarantees

### Existing Tool Signatures Preserved
All current nano-agent tools maintain their exact function signatures and behavior:
- `read_file(file_path: str) -> str`
- `write_file(file_path: str, content: str) -> str`
- `list_directory(directory_path: Optional[str] = None) -> str`
- `get_file_info(file_path: str) -> str`
- `edit_file(file_path: str, old_str: str, new_str: str) -> str`

### MCP Protocol Compatibility
- Existing MCP clients continue to work without modification
- `prompt_nano_agent` function maintains current parameter structure
- Response format remains consistent with existing implementations
- Tool permission system extends existing functionality without breaking changes