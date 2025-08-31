# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-08-30-cursor-tools-mcp/spec.md

> Created: 2025-08-30
> Version: 1.0.0

## Technical Requirements

### Phase 1: Configuration & Command System

#### Configuration Loading System
- **Global Configuration Directories**: nano-cli loads from ~/.nano-cli/config.json, nano-agent loads from ~/.nano-agent/config.json
- **Project Configuration Override**: Both tools load .nano-agent/config.json from project root which merges with and overrides global settings
- **Configuration Merge Strategy**: Project settings override global settings at the key level with deep merge for nested objects
- **Environment Variable Resolution**: Support for ${VAR} syntax in all configuration files

#### Command File Loading System  
- **Command File Discovery**: Load *.md files from global directory (~/.nano-cli/commands/) first
- **Project Command Override**: Load *.md files from project directory (.nano-cli/commands/) second, overriding global commands with same name
- **Command Name Resolution**: Use filename without extension as command identifier (e.g., summarize.md becomes /summarize command)
- **Command Template Processing**: Support for parameter substitution and file reference expansion

#### File Reference System
- **@filepath Syntax Support**: Parse and expand @filepath references in prompts and command arguments
- **Path Resolution**: Support both relative paths (resolved from current directory) and absolute paths
- **File Content Embedding**: Replace @filepath with actual file contents before processing
- **Error Handling**: Clear error messages for missing files or permission issues

### Phase 2: Cursor-Style Built-in Tools

#### Search & Discovery Tools (Semantic Search Deferred)
- **Grep Pattern Search**: Integration with ripgrep (rg) external tool for high-performance regex and literal pattern matching with configurable context lines
- **Fuzzy File Search**: Implement fuzzy string matching using rapidfuzz library for file name search with relevance scoring  
- **Web Search Integration**: HTTP client integration with DuckDuckGo search API including result parsing and content summarization

#### Enhanced File Operations  
- **Smart Edit Tool**: LLM-powered edit suggestion system with diff preview generation and optional auto-application of changes
- **Safe Delete Tool**: File deletion with trash/recovery mechanism, confirmation prompts, and audit logging for important files
- **Terminal Execution**: Subprocess management with output streaming, timeout protection, working directory support, and command safety validation

#### Performance Requirements
- Semantic search must return results within 2 seconds for codebases up to 10,000 files
- MCP tool calls must complete within 5 seconds including network latency
- Agent startup time increase limited to 3 seconds with all MCP servers active
- Memory usage must remain under 500MB with all tools and servers active

### Phase 3: MCP Server Integration Architecture

#### MCP Bridge Implementation
- **Server Lifecycle Management**: Automated startup/shutdown of MCP server subprocesses with health monitoring and automatic restart
- **Protocol Implementation**: Full MCP (Model Context Protocol) client implementation with JSON-RPC communication over stdin/stdout
- **Connection Pooling**: Efficient connection management with retry logic and circuit breaker patterns for resilient external server communication

#### Dynamic Tool Registration
- **Schema-to-Function Conversion**: Automatic generation of @function_tool wrappers from MCP server tool schemas with parameter validation
- **Namespace Management**: Tool conflict resolution through server-prefixed naming (e.g., context7_search_docs, github_create_issue)
- **Permission Integration**: Extension of existing ToolPermissions system to support MCP server tools with path and operation restrictions

### Integration Requirements

#### Tool Registry System
- **Unified Tool Discovery**: Single registry managing both built-in and MCP server tools with consistent help and documentation access
- **Permission Filtering**: Integration with existing allowed_tools, blocked_tools, read_only, and path restriction systems
- **Runtime Tool Addition**: Support for adding/removing MCP server tools without agent restart

#### Error Handling & Recovery
- **Graceful Degradation**: Continue operation when MCP servers are unavailable with clear error messaging
- **Automatic Recovery**: Retry logic with exponential backoff for temporary MCP server failures
- **Fallback Mechanisms**: Alternative built-in implementations when external tools fail

## External Dependencies

### Required New Dependencies (Phase 1 & 2)
- **rapidfuzz>=3.0.0** - Fast fuzzy string matching for file name search
- **Justification:** Provides high-performance fuzzy matching algorithms significantly faster than alternatives

- **requests>=2.31.0** - HTTP client for web search and MCP server communication
- **Justification:** Standard library for HTTP operations, needed for web search API integration

- **beautifulsoup4>=4.12.0** - HTML parsing for web search result extraction
- **Justification:** Required for parsing and extracting content from web search results

- **jsonrpc>=2.0.0** - JSON-RPC protocol implementation for MCP communication
- **Justification:** MCP protocol is based on JSON-RPC, need proper implementation for reliable communication

- **asyncio-subprocess>=0.1.0** - Async subprocess management for MCP server lifecycle
- **Justification:** Required for managing MCP server processes with proper async handling

### Deferred Dependencies (Phase 3 - Semantic Search)
- **sentence-transformers>=2.2.0** - Semantic search vector embeddings generation
- **faiss-cpu>=1.7.0** - High-performance vector similarity search

### Optional External Tools
- **ripgrep (rg)** - High-performance text search tool
- **Installation:** Automatic detection with fallback to Python-based grep implementation if not available
- **Justification:** Provides 10-100x faster search performance compared to pure Python implementations