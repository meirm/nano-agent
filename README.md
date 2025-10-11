# Nano Agent - Production MCP Server for Autonomous AI Agents

**Multi-provider LLM support • Enterprise security • Session management • Task delegation**

<img src="images/nano-agent.png" alt="Nano Agent" style="max-width: 800px;">

## What is Nano Agent?

Nano Agent is a evolving MCP (Model Context Protocol) server that provides autonomous AI agents with file system capabilities, enterprise-grade security, and seamless multi-provider support. Whether you're using OpenAI's GPT-5, Anthropic's Claude, or local Ollama models, Nano Agent delivers consistent, powerful agent capabilities through a unified interface.

### Why Nano Agent?

- **🚀 Production Ready**: Battle-tested with real workloads and comprehensive testing
- **🔐 Enterprise Security**: Fine-grained permissions, path restrictions, read-only mode
- **🤖 Unlimited Models**: Use ANY model from ANY provider - no hardcoded restrictions
- **⚙️ Flexible Configuration**: Hierarchical YAML/JSON config with environment overrides
- **💬 Interactive Mode**: Rich terminal UI with session management and command completion
- **🔗 Hook System**: Customizable pre/post execution hooks for workflow automation
- **📦 5-Minute Setup**: Install scripts for all platforms with auto-configuration
- **🎯 Commands & Agents**: Extensible markdown-based commands and agent profiles
- **💰 Cost Tracking**: Token usage and cost estimation across all providers
- **📚 Comprehensive Docs**: Extensive guides for MCP, CLI, setup, and migration

## Quick Start

### Install in 5 Minutes

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/meirm/nano-agent/main/apps/nano_agent_mcp_server/install.sh | bash

# Windows PowerShell
iwr https://raw.githubusercontent.com/meirm/nano-agent/main/apps/nano_agent_mcp_server/install.ps1 | iex
```

### Try It Out

**In Claude Desktop** (look for the 🔌 icon):
```
Use nano-agent to analyze this project's architecture
Use nano-agent to create a Python web scraper with error handling
Use nano-agent in read-only mode to audit security vulnerabilities
```

**Via CLI**:
```bash
# Interactive mode with rich terminal UI (default when no arguments)
nano-cli
nano-cli interactive --provider ollama --model gpt-oss:20b

# Quick test with any model using -p/--prompt flag
nano-cli -p "Create a hello world script" --model gpt-5-mini

# Safe exploration with read-only mode
nano-cli -p "Analyze this codebase" --read-only

# Use ANY model from ANY provider
nano-cli -p "Write a function" --model llama3.2:latest --provider ollama

# List available models
nano-cli list-models --provider ollama

# Continue conversation with session persistence
nano-cli -p "Add error handling to that function" --continue

# Use custom commands and agents
nano-cli -p '/analyze "Review this code for security issues"'
nano-cli -p "Explain this code" --agent analyst

# Alternative: use 'run' command (equivalent to -p flag)
nano-cli run "Create a hello world script"
```

## Core Features

### 🤖 Flexible Multi-Provider Support

**Use ANY model from ANY provider** - no hardcoded restrictions:

| Provider | Example Models | Configuration |
|----------|---------------|---------------|
| **OpenAI** | GPT-5, GPT-4o, or any model | API key required |
| **Anthropic** | Claude models or any via API | API key required |
| **Ollama** | Any local model you've pulled | No API key needed |
| **Custom** | Your own endpoints | Fully configurable |

```bash
# Use well-known models
nano-cli -p "Analyze code" --model gpt-5 --provider openai
nano-cli -p "Analyze code" --model claude-3-haiku --provider anthropic

# Use ANY Ollama model - not limited to a predefined list
nano-cli -p "Analyze code" --model llama3.2:latest --provider ollama
nano-cli -p "Analyze code" --model mistral:7b --provider ollama
nano-cli -p "Analyze code" --model qwen2.5-coder:3b --provider ollama

# Configure custom providers in ~/.config/nano-cli/config.yaml
nano-cli -p "Analyze code" --model custom-model --provider my-provider
```

### 🔐 Enterprise Security

**Fine-Grained Permissions**
```python
# Control exactly what the agent can do
result = await prompt_nano_agent(
    "Work on authentication",
    allowed_tools=["read_file", "write_file"],  # No editing
    allowed_paths=["./src/auth"],              # Restricted to auth module
    blocked_paths=["./src/auth/secrets"],      # Protect sensitive files
    read_only=False                            # Allow writes in allowed paths
)
```

**Read-Only Mode for Safe Exploration**

Via MCP (Claude Desktop):
```python
# Analyze without any risk of modification
result = await prompt_nano_agent_readonly(
    "Perform a comprehensive security audit"
)
# ✅ Can read files, analyze code, generate reports
# ❌ Cannot modify, create, or delete anything
```

Via CLI:
```bash
# Safe exploration with --read-only flag
nano-cli -p "Audit the codebase for vulnerabilities" --read-only
nano-cli -p "Analyze architecture and create documentation" --read-only

# The agent will only have access to:
# ✅ read_file, list_directory, get_file_info
# ❌ write_file and edit_file are blocked
```

### 🔧 Intelligent Tool Call Management

**Control agent iterations with precision** - prevent runaway operations or extend limits for complex tasks:

**CLI Control**
```bash
# Limit tool calls for safety
nano-cli -p "Analyze project" --max-tool-calls 10

# Allow unlimited calls for complex operations
nano-cli -p "Refactor entire codebase" --unlimited-tool-calls

# Default is 20 tool calls
nano-cli -p "Normal task"  # Uses default limit
```

**Configuration**
```yaml
# ~/.config/nano-cli/config.yaml
max_tool_calls: 30  # Increase default limit
```

**Smart Error Handling**
- Clean error messages when limits are reached
- No stack traces exposed to users
- Helpful feedback: "Maximum tool calls (20) reached. The agent needs more iterations to complete the task."

**Use Cases**
- **Safety**: Limit operations when testing or exploring
- **Complex Tasks**: Remove limits for large refactoring or analysis
- **Resource Control**: Prevent excessive API calls and costs

### 💬 Session Management

**Persistent Conversations**
```bash
# Start a project
nano-cli -p "Create a Flask API" --new
# Returns: session_abc123

# Continue with context (agent remembers everything)
nano-cli -p "Add user authentication" --continue
nano-cli -p "Add input validation" --continue
nano-cli -p "Write unit tests" --continue

# Or use specific session
nano-cli -p "Add logging" --session session_abc123
```

**Session Features**
- Conversation history preservation
- Token usage tracking per session
- Model/provider settings persistence
- Multi-project management
- Cost tracking and analytics

### 🎯 HOP/LOP Task Delegation System

The HOP/LOP pattern enables sophisticated multi-agent task delegation for complex workflows:

```text
┌─────────────────────────────────────────────────────────────┐
│ HIGHER ORDER PROMPT (HOP) - Task Orchestrator               │
│   • Accepts complex multi-part tasks                        │
│   • Delegates subtasks to specialized agents                │
│   • Coordinates parallel execution                          │
│   • Aggregates and synthesizes results                      │
└─────────────────────────────────────────────────────────────┘
                            │
                    Delegates Tasks To
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ LOWER ORDER PROMPTS (LOPs) - Specialized Agents            │
│   • Code Analysis Agent (read-only, security-focused)      │
│   • Implementation Agent (write access, specific paths)    │
│   • Testing Agent (test directory access)                  │
│   • Documentation Agent (markdown generation)              │
│   • Review Agent (read-only, quality checks)               │
└─────────────────────────────────────────────────────────────┘
```

**Example: Complex Feature Implementation**
```python
# HOP orchestrates the entire feature
hop_prompt = "Implement user authentication with tests and docs"

# HOP automatically delegates to LOPs:
# 1. Analysis LOP: Reviews existing code structure
# 2. Implementation LOP: Creates auth module
# 3. Testing LOP: Writes unit tests
# 4. Documentation LOP: Generates API docs
# 5. Review LOP: Validates implementation

# All agents work in parallel where possible
# Results are synthesized into cohesive output
```

### 🛠️ Rich Development Experience

**Interactive Mode with Enhanced UI**
```bash
nano-cli interactive
# Features:
# - Rich terminal UI with colors and tables
# - Command history with arrow keys
# - Tab completion for commands
# - Welcome messages and helpful tips
# - Session persistence across runs
# - Real-time token tracking
# - Markdown rendering in terminal
```

**Command & Agent System**
```bash
# Create custom command templates
nano-cli commands create code-review
nano-cli -p '/code-review "src/auth"'

# Use specialized agents
nano-cli -p "Analyze code" --agent analyst
nano-cli -p "Write tests" --agent coder
nano-cli -p "Generate ideas" --agent creative

# List available commands and agents
nano-cli commands list
nano-cli agents list
```

**Output Formats**
```bash
nano-cli -p "Task" -f rich     # Beautiful terminal output (default)
nano-cli -p "Task" -f json     # Structured JSON for scripts
nano-cli -p "Task" -f simple   # Plain text for piping
nano-cli -p "Task" -f markdown # Formatted markdown output
```

### 🔗 Hook System for Automation

**Customize agent behavior with hooks** - Run custom scripts at specific execution points for validation, monitoring, security checks, and logging.

📖 **[Complete Hook Documentation](HOOKS.md)** - Setup, configuration, examples, and best practices

### ⚙️ Flexible Configuration System

**Hierarchical configuration** with multiple levels:
```yaml
# ~/.config/nano-cli/config.yaml
providers:
  ollama:
    base_url: "http://localhost:11434/v1"
    models:
      - gpt-oss:20b
      - mistral:latest
  custom:
    base_url: "https://your-api.com/v1"
    api_key: "${CUSTOM_API_KEY}"
    
defaults:
  provider: ollama
  model: gpt-oss:20b
  max_tool_calls: 30
  temperature: 0.7
```

**Environment variable overrides**:
```bash
export NANO_AGENT_DEFAULT_PROVIDER=ollama
export NANO_AGENT_DEFAULT_MODEL=gpt-oss:120b
export NANO_AGENT_MAX_TOOL_CALLS=50
```

### 🛠️ Enhanced Tool System

**Expanded tool suite with new capabilities**:
```python
# File Operations
- read_file       # Read any file with encoding support
- write_file      # Create/overwrite files  
- edit_file       # Precise string replacements
- list_directory  # Browse file system
- get_file_info   # Metadata, size, permissions

# Search & Analysis (NEW)
- grep_search     # Search for patterns in files using regex
- search_files    # Find files by pattern matching
- bash_command    # Execute shell commands safely
- get_current_time # Time utilities for scheduling
```

**MCP Integration Features**:
- Tool call limits for safety
- Granular permission control
- Path-based access restrictions
- Read-only mode support

## Architecture

### Nested Agent System

Nano Agent implements a sophisticated nested agent architecture:

```text
┌─────────────────────────────────────────────────────────────┐
│ OUTER AGENT (Claude Desktop, VS Code, etc.)                 │
│   • Communicates via MCP protocol                          │
│   • Sees high-level tools (prompt_nano_agent)              │
│   • Manages user interaction                               │
└─────────────────────────────────────────────────────────────┘
                            │
                        MCP Protocol
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ NANO-AGENT MCP SERVER                                       │
│   • Session management                                      │
│   • Permission enforcement                                  │
│   • Provider abstraction                                    │
│   • Token tracking                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                    Creates & Manages
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ INNER AGENT (OpenAI SDK)                                    │
│   • File system tools                                       │
│   • Autonomous execution                                    │
│   • Multi-turn reasoning                                    │
│   • Tool chaining                                           │
└─────────────────────────────────────────────────────────────┘
```

## Use Cases

### 🔍 Code Analysis & Auditing
```python
# Security audit without modification risk
await prompt_nano_agent_readonly(
    "Scan for OWASP top 10 vulnerabilities and generate report"
)

# Architecture analysis
await prompt_nano_agent_readonly(
    "Create a dependency graph and identify circular dependencies"
)
```

### 🚀 Autonomous Development
```python
# Build complete features
await prompt_nano_agent(
    "Implement REST API with authentication, validation, and tests",
    allowed_paths=["./src", "./tests"],
    session_id="feature-api"
)

# Iterative refinement
await prompt_nano_agent(
    "Add rate limiting and caching",
    session_id="feature-api"  # Continues with context
)
```

### 📊 Multi-Model Comparison
```bash
# Compare different models on the same task
for model in gpt-5-mini claude-3-haiku gpt-oss:20b; do
  nano-cli -p "Optimize this function" --model $model
done
```

### 🎓 Learning & Exploration
```python
# Safe exploration of unfamiliar codebases
await prompt_nano_agent_readonly(
    "Explain how this authentication system works",
    temperature=0.3  # Lower temperature for consistent explanations
)
```

## Advanced Features

### Model Configuration
```python
result = await prompt_nano_agent(
    "Creative writing task",
    model="gpt-5",
    temperature=1.5,      # Higher creativity
    max_tokens=2000,      # Longer responses
    session_id="writing"
)
```

### Tool Restrictions
```python
# Development with guardrails
result = await prompt_nano_agent(
    "Refactor the payment module",
    allowed_tools=["read_file", "edit_file"],  # Can't create new files
    blocked_paths=["./src/payments/stripe_keys.py"],
    allowed_paths=["./src/payments"]
)
```

### Cost Tracking
```python
# Get detailed cost breakdown
info = await get_session_info("my-session")
print(f"Total tokens: {info['total_tokens']}")
print(f"Total cost: ${info['total_cost']}")
print(f"Model: {info['model']}")
```

## Installation

### Requirements
- Python 3.9+
- 5 minutes of your time

### Supported Platforms
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, Arch)
- ✅ Windows 10/11
- ✅ WSL2

### Provider Setup

**OpenAI (GPT-5 models)**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

**Anthropic (Claude models)**
```bash
export ANTHROPIC_API_KEY=your-anthropic-key
```

**Ollama (Local models)**
```bash
# Install Ollama from ollama.ai
ollama pull gpt-oss:20b
# No API key needed!
```

## Flexible Configuration

Nano Agent uses a hierarchical configuration system that allows complete customization:

### Configuration File

Create `~/.config/nano-cli/config.yaml`:

```yaml
# Default settings
default_provider: ollama
default_model: llama3.2:latest

providers:
  # Configure Ollama with any models
  ollama:
    api_base: http://localhost:11434/v1
    allow_unknown_models: true  # Accept ANY model name
    
  # Add custom provider endpoints
  my_provider:
    api_base: https://my-llm-api.com/v1
    api_key_env: MY_PROVIDER_KEY
    allow_unknown_models: true
    known_models: ["model1", "model2"]  # Optional validation
    
  # Configure OpenAI-compatible APIs
  openrouter:
    api_base: https://openrouter.ai/api/v1
    api_key_env: OPENROUTER_API_KEY
    allow_unknown_models: true

# Model aliases for convenience
model_aliases:
  llama: llama3.2:latest
  qwen: qwen2.5-coder:3b
  gpt5: gpt-5-mini
```

### Using Custom Configurations

```bash
# Use any configured provider
nano-cli -p "Task" --provider my_provider --model custom-model

# Models not in known_models still work if allow_unknown_models: true
nano-cli -p "Task" --provider ollama --model any-model-name:tag

# Use aliases for convenience
nano-cli -p "Task" --model llama  # Resolves to llama3.2:latest
```

## API Reference

### MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `prompt_nano_agent` | Full agent with all capabilities | prompt, model, provider, temperature, session_id, permissions |
| `prompt_nano_agent_readonly` | Safe read-only agent | prompt, model, provider, temperature, session_id |
| `get_session_info` | Get session details | session_id |
| `list_sessions` | List all sessions | limit |
| `clear_old_sessions` | Clean up old sessions | days |
| `get_available_models` | List available models | - |

### CLI Commands

```bash
# Primary interface: -p/--prompt flag
nano-cli -p <prompt>           # Run agent with prompt
nano-cli -p <prompt> --read-only  # Safe exploration mode
nano-cli -p <prompt> --max-tool-calls 10  # Limit tool calls
nano-cli -p <prompt> --unlimited-tool-calls  # No limit on tool calls

# Alternative: use 'run' command (equivalent to -p)
nano-cli run <prompt>

# Other commands
nano-cli                        # Start interactive mode (default)
nano-cli interactive            # Start interactive mode (explicit)
nano-cli list-models            # List all available models
nano-cli list-models --provider <name>  # List models for provider
nano-cli sessions list          # List sessions
nano-cli sessions show <id>     # Show session details
nano-cli commands list          # List command templates
nano-cli test-tools            # Test without API
```

## Performance

### Token Efficiency
- Smart context management
- Session-based conversation pruning
- Automatic summarization for long contexts

### Speed Optimization
- Parallel tool execution where possible
- Intelligent caching
- Provider-specific optimizations

### Cost Management
- Real-time token tracking
- Per-session cost calculation
- Provider cost comparison
- Local model support for zero-cost operation

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/meirm/nano-agent
cd nano-agent/apps/nano_agent_mcp_server
uv sync --extra test
```

## Roadmap

### Coming Soon
- [ ] Streaming responses for real-time feedback
- [ ] Batch operations for multiple prompts
- [ ] Resource quotas and rate limiting
- [ ] Custom system prompts
- [ ] Webhook notifications
- [ ] Web UI for session management

### Under Consideration
- [ ] Vector database integration
- [ ] Multi-file context windows
- [ ] Agent collaboration protocols
- [ ] Visual Studio Code extension
- [ ] GitHub Copilot integration

## Documentation 📚

### Comprehensive Guides
- **[MCP Usage Guide](apps/nano_agent_mcp_server/MCP_USAGE_GUIDE.md)** - Claude Desktop integration
- **[CLI Usage Guide](apps/nano_agent_mcp_server/NANO_CLI_USAGE.md)** - Complete CLI reference
- **[Configuration Guide](apps/nano_agent_mcp_server/CONFIG.md)** - Setup and customization
- **[Hook Documentation](apps/nano_agent_mcp_server/HOOKS.md)** - Automation and customization
- **[Commands Guide](apps/nano_agent_mcp_server/COMMANDS.md)** - Custom commands and agents
- **[Migration Guide](apps/nano_agent_mcp_server/docs/MIGRATION_GUIDE.md)** - Upgrading from older versions

### Additional Resources
- **[HOP-LOP Pattern](HOP-LOP-GUIDE.md)** - Task delegation architecture
- **[Agent-OS Framework](.agent-os/)** - Product specs and standards
- **[Examples](examples/)** - Sample configurations and use cases

## Testing Infrastructure 🧪

### Comprehensive Test Coverage
- **Config system tests** - Configuration loading and validation
- **Provider tests** - All providers (OpenAI, Anthropic, Ollama, LMStudio)
- **Tool tests** - File operations, search, bash commands
- **Hook system tests** - Pre/post execution hooks
- **MCP integration tests** - Claude Desktop compatibility
- **Permission tests** - Security and access control
- **Output format tests** - Rich, JSON, markdown rendering

### Run Tests
```bash
cd apps/nano_agent_mcp_server
uv run pytest tests/ -v              # Run all tests
uv run pytest tests/ -k "provider"   # Run provider tests
uv run pytest tests/ -k "config"     # Run config tests
```

## Support

- **Documentation**: See comprehensive guides above
- **Issues**: [GitHub Issues](https://github.com/meirm/nano-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/meirm/nano-agent/discussions)
- **Examples**: [/examples](examples/) directory

## Attribution

Nano Agent was originally created by [@disler](https://github.com/disler) as [nano-agent](https://github.com/disler/nano-agent). This enhanced version builds upon that foundation with production features, security enhancements, and multi-provider support.

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Ready to supercharge your AI development?** Install Nano Agent in 5 minutes and experience the power of autonomous AI agents with enterprise-grade security and multi-provider flexibility.

```bash
# Get started now!
curl -fsSL https://raw.githubusercontent.com/meirm/nano-agent/main/apps/nano_agent_mcp_server/install.sh | bash
```