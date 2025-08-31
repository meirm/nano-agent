# Nano-Agent: Cursor-Style Tools + MCP Integration

## Overview

Transform nano-agent from a basic file-operation tool into a comprehensive development assistant by:
1. **Implementing Cursor-style built-in tools** for comprehensive codebase interaction
2. **Adding MCP server integration** for extensible tool ecosystem
3. **Maintaining backward compatibility** with existing nano-agent functionality

## Current State Analysis

### Existing Tools (5)
- `read_file` - Read file contents
- `write_file` - Create/overwrite files  
- `list_directory` - List directory contents
- `get_file_info` - File metadata
- `edit_file` - Replace exact text matches

### Limitations
- No semantic search capabilities
- No codebase-wide operations
- No terminal/command execution
- No web search functionality
- No integration with external MCP servers
- Limited to basic file I/O operations

## Proposed Solution

### Phase 1: Cursor-Style Built-in Tools

#### 1. Search & Discovery Tools

**A. Codebase Semantic Search**
```python
@function_tool
def codebase_search(query: str, file_types: Optional[List[str]] = None) -> str:
    """Perform semantic searches within the indexed codebase."""
```
- Implementation: Use vector embeddings for semantic matching
- Index common file types (.py, .js, .ts, .md, etc.)
- Support filtering by file extensions
- Return ranked results with context snippets

**B. Grep Pattern Search**  
```python
@function_tool
def grep_search(pattern: str, file_pattern: Optional[str] = None, context_lines: int = 3) -> str:
    """Search for exact keywords or regex patterns within files."""
```
- Implementation: Use ripgrep (rg) for performance
- Support regex patterns and literal strings
- Include surrounding context lines
- Filter by file patterns (glob support)

**C. Fuzzy File Search**
```python
@function_tool 
def search_files(name_query: str, max_results: int = 20) -> str:
    """Find files by name using fuzzy matching."""
```
- Implementation: Use fuzzy string matching (fuzzywuzzy/rapidfuzz)
- Search across entire project structure
- Return ranked results by relevance score

**D. Web Search**
```python
@function_tool
def web_search(query: str, num_results: int = 5) -> str:
    """Generate search queries and perform web searches."""
```
- Implementation: Integration with search APIs (DuckDuckGo, Google Custom Search)
- Extract and summarize relevant content
- Include source URLs and snippets

#### 2. Enhanced File Operations

**A. Smart Edit Tool**
```python
@function_tool
def edit_and_apply(file_path: str, description: str, auto_apply: bool = False) -> str:
    """Suggest edits to files with AI-powered context understanding."""
```
- Implementation: Use LLM to understand edit intentions
- Generate precise edit suggestions with diff preview
- Optional auto-application of changes
- Support for complex multi-line edits

**B. Safe Delete Tool**
```python
@function_tool
def delete_file(file_path: str, confirm: bool = True) -> str:
    """Delete files with safety guardrails."""
```
- Implementation: Move to trash instead of permanent deletion
- Require explicit confirmation for important files
- Log all deletions for audit trail

#### 3. Execution Tools

**A. Terminal Execution**
```python
@function_tool
def run_terminal(command: str, working_dir: Optional[str] = None, timeout: int = 30) -> str:
    """Execute terminal commands and monitor output."""
```
- Implementation: subprocess with output streaming
- Working directory support
- Timeout protection
- Command history and safety checks

### Phase 2: MCP Server Integration

#### Configuration System

**A. Global Configuration (`~/.nano-agent/config.json`)**
```json
{
  "mcp_servers": {
    "context7": {
      "command": "context7-server",
      "args": ["--port", "3001"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      },
      "enabled": true,
      "tools": ["search_docs", "get_examples"]
    },
    "playwright": {
      "command": "playwright-mcp",
      "args": [],
      "env": {},
      "enabled": true,
      "tools": ["take_screenshot", "click_element", "fill_form"]
    }
  },
  "tool_settings": {
    "auto_apply_edits": false,
    "safe_mode": true,
    "max_terminal_timeout": 60
  }
}
```

**B. Project Configuration (`.nano-cli/config.json`)**
```json
{
  "project_mcp_servers": {
    "github": {
      "command": "github-mcp",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      },
      "tools": ["create_issue", "get_pr", "list_repos"]
    }
  },
  "disabled_tools": ["delete_file"],
  "restricted_paths": ["/etc", "/sys"]
}
```

#### MCP Bridge Implementation

**A. MCP Client Integration**
```python
class MCPBridge:
    def __init__(self, config_path: str):
        self.servers = {}
        self.load_config(config_path)
    
    async def start_server(self, server_name: str, config: dict):
        """Start an MCP server subprocess"""
        
    async def call_tool(self, server: str, tool: str, **kwargs):
        """Call a tool on a specific MCP server"""
        
    def get_available_tools(self) -> List[str]:
        """Get all available tools from all MCP servers"""
```

**B. Dynamic Tool Registration**
```python
def register_mcp_tools(mcp_bridge: MCPBridge) -> List[FunctionTool]:
    """Dynamically create function_tool wrappers for MCP server tools"""
    tools = []
    
    for server_name, server_tools in mcp_bridge.get_server_tools().items():
        for tool_name, tool_schema in server_tools.items():
            
            @function_tool
            def mcp_tool_wrapper(**kwargs):
                f"""Call {tool_name} from {server_name} MCP server"""
                return run_async(mcp_bridge.call_tool(server_name, tool_name, **kwargs))
            
            # Rename function to avoid conflicts
            mcp_tool_wrapper.__name__ = f"{server_name}_{tool_name}"
            tools.append(mcp_tool_wrapper)
    
    return tools
```

#### Tool Discovery & Management

**A. Tool Registry**
```python
class ToolRegistry:
    def __init__(self):
        self.builtin_tools = []     # Core nano-agent tools
        self.mcp_tools = []         # Tools from MCP servers
        self.disabled_tools = []    # User-disabled tools
    
    def register_builtin_tools(self):
        """Register core nano-agent tools"""
        
    def register_mcp_tools(self, mcp_bridge: MCPBridge):
        """Register tools from MCP servers"""
        
    def get_available_tools(self, permissions: ToolPermissions = None):
        """Get filtered list of available tools"""
        
    def get_tool_help(self, tool_name: str) -> str:
        """Get help text for a specific tool"""
```

## Technical Implementation

### Architecture Changes

```
┌─────────────────────────────────────────────────────────────┐
│ NANO-AGENT ENHANCED ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 1. CONFIGURATION LAYER                                      │
│   • Global config (~/.nano-agent/config.json)             │  
│   • Project config (.nano-cli/config.json)                │
│   • Environment variable resolution                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. TOOL REGISTRY & MANAGEMENT                               │
│   • ToolRegistry class                                     │
│   • Built-in tool registration                            │
│   • MCP server tool discovery                             │
│   • Permission filtering                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. MCP BRIDGE LAYER                                        │
│   • MCPBridge class                                       │
│   • Server lifecycle management                           │
│   • Tool call routing                                     │
│   • Error handling & retries                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. EXECUTION LAYER                                         │
│   Built-in Tools:          External MCP Servers:          │
│   • Codebase search        • Context7 (docs)             │
│   • Grep search            • Playwright (browser)        │
│   • File operations        • GitHub (API)                │
│   • Terminal execution     • Custom servers              │
│   • Web search            • ...                          │
└─────────────────────────────────────────────────────────────┘
```

### New Module Structure

```
src/nano_agent/modules/
├── tools/                          # Tool implementations
│   ├── __init__.py
│   ├── builtin/                    # Built-in tools
│   │   ├── search_tools.py         # Codebase, grep, file search
│   │   ├── edit_tools.py           # Smart edit, delete
│   │   ├── execution_tools.py      # Terminal, web search
│   │   └── file_tools.py           # Enhanced file operations
│   └── mcp/                        # MCP integration
│       ├── bridge.py               # MCP client bridge
│       ├── registry.py             # Tool discovery & registration
│       └── config.py               # Configuration management
├── search/                         # Search implementations
│   ├── semantic.py                 # Vector-based semantic search
│   ├── fuzzy.py                    # Fuzzy file name matching
│   └── indexing.py                 # Codebase indexing
└── config/                         # Configuration system
    ├── loader.py                   # Config file loading
    ├── resolver.py                 # Environment variable resolution
    └── merger.py                   # Global + project config merging
```

## Implementation Tasks

### Phase 1: Cursor-Style Tools (2-3 weeks)

#### Week 1: Search Tools Foundation
- [ ] **Task 1.1**: Implement `grep_search` tool using ripgrep
  - Install ripgrep dependency
  - Create search_tools.py module
  - Add regex and literal pattern support
  - Include context lines functionality
  - Add file pattern filtering

- [ ] **Task 1.2**: Implement `search_files` fuzzy matching
  - Add rapidfuzz dependency
  - Implement fuzzy file name search
  - Add ranking by relevance score
  - Support for glob patterns and exclusions

- [ ] **Task 1.3**: Implement basic `web_search` tool
  - Integrate with DuckDuckGo search API
  - Add result parsing and summarization
  - Include source URL extraction
  - Add rate limiting and error handling

#### Week 2: Enhanced File Operations
- [ ] **Task 2.1**: Implement `edit_and_apply` smart editing
  - Create edit_tools.py module
  - Add LLM-powered edit suggestion
  - Implement diff preview functionality
  - Add auto-apply safety checks

- [ ] **Task 2.2**: Implement safe `delete_file` tool
  - Add file deletion with trash support
  - Implement confirmation prompts
  - Add audit logging
  - Create file recovery mechanism

- [ ] **Task 2.3**: Implement `run_terminal` execution
  - Create execution_tools.py module
  - Add subprocess execution with streaming
  - Implement timeout protection
  - Add working directory support

#### Week 3: Semantic Search & Integration
- [ ] **Task 3.1**: Implement `codebase_search` semantic search
  - Create semantic.py search module
  - Add vector embedding generation
  - Implement similarity search
  - Add file type filtering

- [ ] **Task 3.2**: Create codebase indexing system
  - Implement background indexing
  - Add incremental updates
  - Support common file types
  - Add index persistence

- [ ] **Task 3.3**: Integrate all tools into nano-agent
  - Update tool registry system
  - Add permission handling for new tools
  - Update CLI with new capabilities
  - Add comprehensive testing

### Phase 2: MCP Integration (2-3 weeks)

#### Week 4: MCP Bridge Foundation
- [ ] **Task 4.1**: Implement MCP client bridge
  - Create MCPBridge class
  - Add MCP protocol implementation
  - Implement server lifecycle management
  - Add connection pooling and retries

- [ ] **Task 4.2**: Create configuration system
  - Implement config file loading
  - Add environment variable resolution
  - Create global + project config merging
  - Add configuration validation

- [ ] **Task 4.3**: Implement tool discovery
  - Add MCP server tool enumeration
  - Create dynamic tool registration
  - Implement schema-to-function conversion
  - Add tool conflict resolution

#### Week 5: Dynamic Tool Registration
- [ ] **Task 5.1**: Create ToolRegistry class
  - Implement built-in tool registration
  - Add MCP tool registration
  - Create permission filtering
  - Add tool help and documentation

- [ ] **Task 5.2**: Implement dynamic function_tool creation
  - Create MCP tool wrapper generation
  - Add parameter validation and conversion
  - Implement error handling and logging
  - Add tool call routing

- [ ] **Task 5.3**: Add configuration management
  - Implement server enable/disable
  - Add tool-specific permissions
  - Create configuration validation
  - Add hot-reloading support

#### Week 6: Integration & Testing
- [ ] **Task 6.1**: Integrate MCP system with nano-agent
  - Update main execution loop
  - Add startup server initialization
  - Implement graceful shutdown
  - Add error recovery mechanisms

- [ ] **Task 6.2**: Create comprehensive testing
  - Add unit tests for all new modules
  - Create integration tests with mock MCP servers
  - Add performance benchmarks
  - Implement end-to-end testing

- [ ] **Task 6.3**: Update documentation and examples
  - Create configuration examples
  - Add MCP server integration guide
  - Update CLI documentation
  - Create video tutorials

## Success Metrics

### Functionality Metrics
- ✅ All 8+ Cursor-style tools implemented and working
- ✅ MCP server integration supporting 3+ external servers
- ✅ Configuration system supporting both global and project settings
- ✅ Backward compatibility with existing nano-agent functionality
- ✅ Tool permission system preventing unauthorized access

### Performance Metrics  
- ⚡ Semantic search returns results in <2 seconds for codebases up to 10K files
- ⚡ MCP tool calls complete in <5 seconds including network latency
- ⚡ Agent startup time increases by <3 seconds with MCP integration
- ⚡ Memory usage stays under 500MB with all tools active

### User Experience Metrics
- 📈 Reduction in task completion time by 40% compared to current nano-agent
- 📈 Support for 90% of common development workflows (search, edit, execute)
- 📈 Zero-configuration setup for built-in tools
- 📈 One-command MCP server integration

## Risk Assessment

### High Risk
- **MCP Server Compatibility**: Different MCP servers may have incompatible schemas or protocols
  - **Mitigation**: Implement robust schema validation and fallback mechanisms
  
- **Performance Impact**: Adding semantic search and MCP integration may significantly slow down agent execution
  - **Mitigation**: Implement lazy loading, caching, and async operations

### Medium Risk
- **Configuration Complexity**: Users may struggle with MCP server configuration
  - **Mitigation**: Provide sensible defaults, validation, and clear error messages

- **Tool Conflicts**: Naming conflicts between built-in and MCP tools
  - **Mitigation**: Implement namespacing and conflict resolution strategies

### Low Risk
- **Backward Compatibility**: Changes may break existing nano-agent workflows
  - **Mitigation**: Maintain existing API surface and add comprehensive testing

## Dependencies

### New Dependencies
```toml
[project.dependencies]
# Existing dependencies maintained
# Search & indexing
sentence-transformers = ">=2.2.0"  # Semantic search
faiss-cpu = ">=1.7.0"              # Vector similarity
rapidfuzz = ">=3.0.0"              # Fuzzy matching

# Terminal & web
requests = ">=2.31.0"              # Web search
beautifulsoup4 = ">=4.12.0"       # HTML parsing

# MCP integration  
jsonrpc = ">=2.0.0"               # MCP protocol
asyncio-subprocess = ">=0.1.0"    # Server management
```

### External Tools
- `ripgrep` (rg) - High-performance text search
- `git` - Repository operations and file tracking

## Conclusion

This specification transforms nano-agent from a basic file manipulation tool into a comprehensive development assistant comparable to Cursor's agent system. The phased approach ensures steady progress while maintaining system stability.

Key innovations:
1. **Cursor-parity built-in tools** provide immediate value without external dependencies
2. **MCP integration architecture** enables unlimited extensibility through the growing MCP ecosystem
3. **Layered configuration system** balances ease-of-use with power-user flexibility
4. **Tool registry pattern** enables dynamic tool management and permission control

The result will position nano-agent as a leading open-source alternative to proprietary AI coding assistants while maintaining its lightweight, hackable architecture.