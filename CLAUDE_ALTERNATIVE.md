# Nano-agent

## Context
"Nano-Agent" is an MCP (Model Context Protocol) server framework that enables agentic workflows by routing tasks from a unified interface (e.g., Claude Code) to any LLM provider (OpenAI, Anthropic, Ollama, custom) while tracking cost, tokens and performance.

## Tooling

- Backend:
  - Python 3.12+
  - uv (package manager - replaces pip/poetry)
  - Pydantic 2.10+ (data validation)
  - pytest 8.4+ with pytest-asyncio
  - MCP SDK 1.12+

## Key Commands
- `uv run pytest` - Run all tests
- `uv run pytest tests/test_*.py` - Run specific test
- `nano-cli` - Interactive mode CLI
- `nano-cli -p "prompt"` - Quick execution mode

## Project Structure
- `apps/nano_agent_mcp_server/src/nano_agent/` - Main source code
- `apps/nano_agent_mcp_server/tests/` - Test suite
- `apps/nano_agent_mcp_server/config/` - Configuration examples
- `ai_docs/` - Additional documentation

## Development Guidelines
1. Write tests first (TDD approach)
2. Use Pydantic models for all data structures (never Dict)
3. Follow existing naming conventions
4. Use async/await for I/O operations
5. Keep functions focused and testable

## Important Notes
- Always use `uv` over `pip` or `poetry` for package management
- Validate all inputs using Pydantic models with typed fields
- MCP server runs via `nano-agent` command, CLI via `nano-cli`
- Configuration hierarchy: CLI flags > env vars > config.yaml