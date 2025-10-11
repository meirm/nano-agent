# Release Notes - Nano Agent 0.3.2

## 🚀 Version 0.3.2 - October 11, 2025

## Overview

This patch release focuses on **documentation modernization** and **user experience improvements** for the nano-cli interface. The primary change is the introduction of the `-p/--prompt` flag as the recommended way to run prompts, providing a more intuitive and consistent CLI experience across all nano-agent features.

## 🎯 Key Highlights

- **New CLI Interface**: `-p/--prompt` flag is now the primary way to run prompts
- **Documentation Overhaul**: Updated all user-facing documentation to reflect modern CLI patterns
- **Backward Compatibility**: `run` command remains fully supported as an alternative
- **Consistency**: Unified command syntax across README, guides, and examples

## 🔧 Improvements

### CLI User Experience

- **Primary Interface Change**: Introduced `-p/--prompt` as the recommended flag for running prompts
  ```bash
  # New primary pattern
  nano-cli -p "Your prompt here"

  # Alternative (equivalent)
  nano-cli run "Your prompt here"
  ```

- **Improved Discoverability**: The `-p` flag makes it immediately clear what the argument represents
- **Enhanced Consistency**: Aligns with common CLI patterns where flags indicate the nature of arguments
- **Interactive Mode Default**: Running `nano-cli` without arguments now defaults to interactive mode

### Documentation Updates

#### README.md
- **Quick Start Section**: Updated all examples to showcase `-p/--prompt` flag first
- **Core Features**: Modernized all code examples throughout the feature showcase
- **API Reference**: Added comprehensive CLI command reference with new patterns
- **Usage Examples**: Updated multi-model comparison, session management, and advanced features

#### COMMANDS.md
- **Running Commands**: Updated command invocation patterns
- **Built-in Commands**: Refreshed all `/summarize`, `/analyze`, `/explain`, `/refactor`, `/test` examples
- **Advanced Usage**: Updated examples for different models and file content passing
- **Custom Commands**: Modernized command creation and usage patterns

#### HOOKS.md
- **Quick Start**: Updated hook testing examples
- **Troubleshooting**: Refreshed debugging command examples

#### CLAUDE.md
- **Development Workflow**: Updated testing and development command patterns
- **Testing Section**: Modernized provider testing examples
- **Important Patterns**: Updated model addition testing instructions

## 📚 Documentation Structure

### Files Modified

- `README.md` - Main project documentation (93 insertions, 66 deletions)
- `apps/nano_agent_mcp_server/COMMANDS.md` - Command system guide (35 insertions, 22 deletions)
- `HOOKS.md` - Hooks system documentation (4 insertions, 4 deletions)
- `CLAUDE.md` - Developer reference (14 insertions, 7 deletions)

**Total Changes**: 4 files, 146 insertions, 99 deletions

## 🔄 Migration Guide

### For Users Upgrading from 0.3.1

**No breaking changes!** All existing scripts and workflows continue to work without modification.

#### Recommended Updates (Optional)

If you want to adopt the new recommended pattern:

**Before (still works):**
```bash
nano-cli run "Create a hello world script"
nano-cli run '/analyze "code.py"' --model gpt-5
```

**After (recommended):**
```bash
nano-cli -p "Create a hello world script"
nano-cli -p '/analyze "code.py"' --model gpt-5
```

**Why Update?**
- More explicit about what you're passing
- Shorter syntax (`-p` vs `run`)
- Consistent with modern CLI conventions
- Better IDE/shell completion support

## 🛠️ Technical Details

### CLI Argument Parsing

The `-p/--prompt` flag has been integrated into the existing argument parser:
- **Priority**: Flag-based prompt takes precedence over positional argument
- **Compatibility**: `run` command remains as alias for backward compatibility
- **Validation**: Both methods share the same validation and processing logic

### Documentation Patterns

All documentation now follows this structure:
1. Show `-p/--prompt` as the primary method
2. Note that `run` is an equivalent alternative
3. Maintain consistency across all examples
4. Include both forms in comprehensive guides

## 📦 Installation

No installation changes required. If you're already on 0.3.1:

```bash
# Update via pip (when published)
pip install --upgrade nano-agent

# Or via uv
uv tool upgrade nano-agent

# Or via git
cd nano-agent
git pull
cd apps/nano_agent_mcp_server
uv tool install -e .
```

## ✅ Quality Assurance

- ✅ All existing tests pass without modification
- ✅ Backward compatibility verified
- ✅ Documentation consistency validated across all files
- ✅ CLI argument parsing tested with both methods
- ✅ Interactive mode behavior unchanged

## 🔮 Coming Soon

Planned for future releases:
- Additional documentation for advanced CLI features
- Enhanced interactive mode features
- Expanded command templates and examples
- Web UI for session management

## 📊 Documentation Coverage

### User-Facing Documentation Updated
- ✅ README.md - Main project overview
- ✅ COMMANDS.md - Command system guide
- ✅ HOOKS.md - Hooks documentation
- ✅ CLAUDE.md - Developer reference

### Remaining Documentation (Gradual Migration)
The following files still use the older pattern and will be updated incrementally:
- Examples and tutorials
- Migration guides
- Release notes
- Advanced feature guides

This gradual approach ensures the most important user-facing documentation is updated first while maintaining stability.

## 🙏 Acknowledgments

Thank you to the nano-agent community for feedback on CLI usability and documentation clarity. This release reflects your input on making the tool more intuitive and accessible.

---

## 📦 Full Installation Guide

### Quick Install

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/meirm/nano-agent/main/apps/nano_agent_mcp_server/install.sh | bash

# Windows PowerShell
iwr https://raw.githubusercontent.com/meirm/nano-agent/main/apps/nano_agent_mcp_server/install.ps1 | iex
```

### Manual Install

```bash
git clone https://github.com/meirm/nano-agent
cd nano-agent/apps/nano_agent_mcp_server
uv tool install -e .
```

### Configuration

```bash
# Configure API keys
export OPENAI_API_KEY=your-key-here
export ANTHROPIC_API_KEY=your-key-here  # optional
export NANO_AGENT_DEFAULT_PROVIDER=ollama  # optional
export NANO_AGENT_DEFAULT_MODEL=gpt-oss:20b  # optional
```

---

## 📖 Quick Start

```bash
# Interactive mode (default)
nano-cli

# Quick prompt
nano-cli -p "Create a hello world script"

# With specific model
nano-cli -p "Analyze this code" --model gpt-5 --provider openai

# Safe read-only mode
nano-cli -p "Audit security vulnerabilities" --read-only

# Use custom commands
nano-cli -p '/summarize "long text here"'
```

---

**Full Changelog**: https://github.com/meirm/nano-agent/compare/v0.3.1...v0.3.2

**Contributors**: [@meirm](https://github.com/meirm)

**Questions or Issues?** Open an issue at https://github.com/meirm/nano-agent/issues
