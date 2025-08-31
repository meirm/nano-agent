# Spec Requirements Document

> Spec: Cursor-Style Tools + MCP Integration
> Created: 2025-08-30
> Status: Planning

## Overview

Transform nano-agent from basic file operations into a comprehensive development assistant by implementing Cursor-style built-in tools and adding configuration-driven MCP server integration for unlimited extensibility.

## User Stories

### Development Assistant Enhancement

As a developer using nano-agent, I want access to comprehensive development tools like semantic search, pattern matching, and terminal execution, so that I can accomplish complex engineering tasks without switching between multiple tools.

The enhanced nano-agent will provide:
- Semantic codebase search using vector embeddings
- Fast pattern matching with ripgrep integration
- Fuzzy file name search for quick navigation
- Web search capabilities for research and documentation
- Smart AI-powered file editing with diff previews
- Safe terminal command execution with timeout protection

### MCP Server Ecosystem Integration

As a power user, I want to easily integrate external MCP servers through configuration files, so that I can extend nano-agent's capabilities without modifying core code.

The configuration system will enable:
- Global configuration loading: nano-cli from ~/.nano-cli/config.json, nano-agent from ~/.nano-agent/config.json
- Project-specific configuration in .nano-agent/config.json (at project root) that merges with and overrides global settings
- Command file loading with cascade: global (~/.nano-cli/commands/*.md) then project (.nano-cli/commands/*.md) with name-based override
- Dynamic tool registration from external MCP servers
- Permission management and namespace conflict resolution

### Backward Compatibility Preservation

As an existing nano-agent user, I want all current functionality to continue working unchanged, so that my existing workflows and integrations remain stable.

All existing tools (read_file, write_file, list_directory, get_file_info, edit_file) will maintain their current API and behavior while new capabilities are added alongside.

## Spec Scope

1. **Cursor-Style Built-in Tools** - Implement 7 new tools matching Cursor's agent capabilities including pattern matching, file search, web search, smart editing, safe deletion, and terminal execution (semantic search deferred to Phase 3)
2. **Configuration Management System** - Implement layered configuration with proper loading order: global configs (nano-cli from ~/.nano-cli, nano-agent from ~/.nano-agent) merged with project config (.nano-agent/config.json at project root)
3. **Command File System** - Support command file loading cascade from global (~/.nano-cli/commands/*.md) to project (.nano-cli/commands/*.md) with name-based override capability
4. **MCP Server Integration Architecture** - Create configuration-driven system for connecting external MCP servers with dynamic tool registration and permission management

## Out of Scope

- Breaking changes to existing nano-agent API or tool signatures
- Real-time collaborative editing or multi-user functionality
- Built-in version control operations beyond basic git integration
- Cloud-based or remote execution capabilities
- Full IDE replacement features like debugging or profiling
- Authentication or authorization beyond basic API key management

## Expected Deliverable

1. **Enhanced nano-agent with 7 Cursor-style tools** - Users can perform pattern matching, fuzzy file search, web research, smart editing, safe deletion, and terminal execution through nano-agent (semantic search in Phase 3)
2. **Layered configuration system** - Proper config loading from global directories (nano-cli: ~/.nano-cli, nano-agent: ~/.nano-agent) merged with project-specific .nano-agent/config.json
3. **Command file cascade system** - Commands load from global ~/.nano-cli/commands/*.md then project .nano-cli/commands/*.md with proper override behavior
4. **MCP server integration working with 3+ external servers** - Configuration files enable seamless integration with Context7, Playwright, GitHub MCP, and other external servers

## Spec Documentation

- Tasks: @.agent-os/specs/2025-08-30-cursor-tools-mcp/tasks.md
- Technical Specification: @.agent-os/specs/2025-08-30-cursor-tools-mcp/sub-specs/technical-spec.md
- API Specification: @.agent-os/specs/2025-08-30-cursor-tools-mcp/sub-specs/api-spec.md
- Tests Specification: @.agent-os/specs/2025-08-30-cursor-tools-mcp/sub-specs/tests.md