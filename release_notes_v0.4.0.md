# Release Notes - Nano Agent v0.4.0

## 🚀 Version 0.4.0 - October 15, 2025

## Overview
This release introduces **dynamic shell command evaluation** in command files, enabling powerful runtime automation and context-aware prompts. Commands can now execute shell scripts inline using a secure, opt-in backtick syntax.

## 🎯 New Features

### 💻 Inline Shell Command Evaluation
- **Dynamic Command Execution** - Execute shell commands inline within command markdown files
  - Use `$\`command\`` syntax to embed shell commands
  - Commands are evaluated at runtime before being sent to the agent
  - Results are seamlessly integrated into the prompt
  - **Example**:
    ```markdown
    # System Report
    - **Date**: $\`date "+%Y-%m-%d %H:%M:%S"\`
    - **User**: $\`whoami\`
    - **Hostname**: $\`hostname\`
    - **Git Branch**: $\`git branch --show-current\`
    ```

### 🔒 Security-First Design
- **Disabled by Default** - Command evaluation requires explicit opt-in for security
- **Multiple Configuration Options**:
  - **nano-cli**: Config file (`~/.nano-cli/config.yaml`) or environment variable
  - **nano-agent MCP**: Environment variable only
- **Timeout Protection** - All commands execute with a 10-second timeout
- **Error Handling** - Failed commands show clear error messages instead of breaking

### ⚙️ Configuration Support

#### For nano-cli
**Option 1: Configuration File (Recommended)**
```yaml
# ~/.nano-cli/config.yaml
enable_command_eval: true
```

**Option 2: Environment Variable**
```bash
export NANO_CLI_ENABLE_COMMAND_EVAL=true
```

#### For nano-agent (MCP Server)
```bash
# Environment variable only (no config file for MCP)
export NANO_AGENT_ENABLE_COMMAND_EVAL=true
uv run nano-agent
```

## 🔧 Improvements

### Command Processing
- Enhanced `CommandLoader` to support shell command evaluation
- Added `_evaluate_shell_commands()` method with regex pattern matching
- Improved error handling for command execution failures
- Better integration with existing argument substitution system

### Configuration Management
- Extended `NanoAgentConfig` dataclass with `enable_command_eval` field
- Updated all `CommandLoader` instantiations across the codebase (9 locations)
- Consistent configuration loading in CLI, interactive mode, and coordinator

### Documentation
- Comprehensive COMMANDS.md updates with examples and use cases
- Security notes and best practices
- Clear differentiation between nano-cli and nano-agent configuration
- Example command files demonstrating the feature

## 🛠️ Files Modified

### Core Changes
- `src/nano_agent/modules/command_loader.py` - Added shell evaluation engine (+115 lines)
  - New `_evaluate_shell_commands()` method
  - Regex pattern: `(?<!\\)\$\`([^`]*)\``
  - Security checks and timeout handling

- `src/nano_agent/modules/config_manager.py` - Configuration support (+4 lines)
  - Added `enable_command_eval` to `NanoAgentConfig`
  - Updated default configuration dictionary

### Integration Updates
- `src/nano_agent/cli.py` - Updated 6 CommandLoader instantiations (+27 lines)
  - Passes config setting to all CommandLoader instances
  - Fixed Python boolean in init command

- `src/nano_agent/modules/interactive_mode.py` - Interactive mode support (+8 lines)
  - Updated `NanoAgentCompleter` and `InteractiveSession`
  - Loads config and passes to CommandLoader

- `src/nano_agent/modules/coordinator.py` - Coordinator integration (+4 lines)
  - Updated `CoordinatorAgent` to use config

### Documentation
- `COMMANDS.md` - Comprehensive documentation (+81 lines)
  - Shell command evaluation section
  - Configuration instructions for both nano-cli and nano-agent
  - Security notes and examples

## 🧪 Testing

### Test Coverage
- ✅ 22 comprehensive tests in `tests/nano_agent/modules/test_command_eval.py`
- ✅ Security tests (disabled by default, environment variable override)
- ✅ Evaluation tests (simple commands, complex commands, error handling)
- ✅ Edge case tests (empty output, multiline, timeouts, escaping)
- ✅ Integration tests (with argument substitution, nested evaluation)

### Manual Testing
- ✅ Config file support validated (`~/.nano-cli/config.yaml`)
- ✅ Environment variable override tested
- ✅ MCP server environment variable support verified
- ✅ Command execution with real shell commands
- ✅ Error handling and timeout behavior

## 📚 Documentation

### New Documentation
- **Shell Command Evaluation** section in COMMANDS.md
- **Configuration options** for nano-cli and nano-agent
- **Security notes** and best practices
- **Example use cases** with real-world scenarios

### Updated Documentation
- Enhanced command file format documentation
- Added order of operations for command processing
- Improved troubleshooting section

## 📈 Performance & Stability

### Performance Features
- **10-second timeout** prevents hanging commands
- **Efficient regex** pattern matching for command detection
- **Minimal overhead** when evaluation is disabled
- **Subprocess isolation** for command execution

### Stability Enhancements
- Comprehensive error handling for failed commands
- Graceful degradation when commands fail
- Clear error messages: `[Error: command not found]`
- Empty output handling: `[Empty output]`

## 🎨 Example Use Cases

### 1. Dynamic System Reports
```markdown
# System Status Report

Current system status as of $\`date\`:

- **Uptime**: $\`uptime\`
- **Disk Usage**: $\`df -h / | tail -1 | awk '{print $5}'\`
- **Memory**: $\`free -h | grep Mem | awk '{print $3 "/" $2}'\`
```

### 2. Git Context Injection
```markdown
# Code Review Request

Repository: $\`basename $(git rev-parse --show-toplevel)\`
Branch: $\`git branch --show-current\`
Last Commit: $\`git log -1 --oneline\`
Modified Files: $\`git diff --name-only | wc -l\`

Please review the changes: $ARGUMENTS
```

### 3. Development Environment Info
```markdown
# Environment Debug

- **Python**: $\`python --version\`
- **Node**: $\`node --version\`
- **Working Directory**: $\`pwd\`
- **Virtual Env**: $\`echo $VIRTUAL_ENV\`
```

## ⚙️ Technical Details

### Command Evaluation Pipeline
1. Load command markdown file
2. Substitute `$ARGUMENTS` placeholder
3. **NEW**: Evaluate `$\`command\`` if enabled
4. Process escaped dollars (`\$` → `$`)
5. Send final prompt to agent

### Regex Pattern
```python
pattern = r'(?<!\\)\$\`([^`]*)\`'
# Matches: $`command` but not \$`command`
```

### Security Features
- ✅ Disabled by default
- ✅ Explicit opt-in required
- ✅ 10-second timeout per command
- ✅ Subprocess isolation
- ✅ No shell injection vulnerabilities
- ✅ Clear error reporting

## 🚀 Migration Guide

### For Users Upgrading from v0.3.x

**No breaking changes!** This is a backward-compatible release.

#### To Enable Command Evaluation (Optional)

**For nano-cli users:**
1. Edit `~/.nano-cli/config.yaml`
2. Add: `enable_command_eval: true`
3. Save and restart nano-cli

**For MCP server users:**
1. Set environment variable: `export NANO_AGENT_ENABLE_COMMAND_EVAL=true`
2. Restart the MCP server

**Existing command files will continue to work without any changes.**

## 🔮 Coming Soon

- Visual Studio Code extension integration
- Additional command evaluation features
- Enhanced security controls (command whitelisting)
- Performance profiling for command execution

## 🙏 Acknowledgments

Thank you to the community for feedback on command system enhancements. Special recognition for security-conscious design discussions that shaped this feature.

---

## 📦 Installation

```bash
# Install or upgrade
uv tool install -e .

# Or for development
cd apps/nano_agent_mcp_server
uv sync --extra test
```

---

**Full Changelog**: v0.3.2...v0.4.0
**Release Date**: October 15, 2025
**Contributors**: @meirm and the Nano Agent community

---

## 📋 Quick Reference

### Enable Command Evaluation

| Environment | Method | Command |
|-------------|--------|---------|
| nano-cli | Config | Add `enable_command_eval: true` to `~/.nano-cli/config.yaml` |
| nano-cli | Env Var | `export NANO_CLI_ENABLE_COMMAND_EVAL=true` |
| MCP Server | Env Var | `export NANO_AGENT_ENABLE_COMMAND_EVAL=true` |

### Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `$\`cmd\`` | Execute shell command | `$\`date\`` |
| `\$\`cmd\`` | Escape (literal text) | Shows `$\`date\`` literally |
| `$ARGUMENTS` | User arguments | Replaced with command args |

---

**Security Notice**: Always review command files from untrusted sources before enabling command evaluation.
