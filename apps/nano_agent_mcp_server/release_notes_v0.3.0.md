# Release Notes - v0.3.0

## Overview
Major feature release introducing enhanced search capabilities, improved CLI functionality, better error handling, and development tools for debugging.

## 🎯 New Features

### 🔍 Advanced Search Tools
- **`grep_file`** - Perform regex pattern searches within specific files
  - Full regex support with proper escaping
  - Detailed match results with line numbers and context
  - Comprehensive error handling for invalid patterns
- **`search_files`** - Find files by name pattern using fuzzy matching
  - Glob pattern support (e.g., `*.py`, `**/*.md`)
  - Case-insensitive search options
  - Returns sorted results by modification time
- **`bash_command`** - Execute shell commands with full I/O control
  - Safe command execution with timeout support
  - Captures stdout, stderr, and exit codes
  - Proper error handling and security measures

### 🎮 Tool Call Limits & Control
- **`--max-tool-calls`** flag to limit agent iterations (default: 20)
  - Prevents runaway operations
  - Customizable per execution
  - Clear error messages when limits are reached
- **`--unlimited-tool-calls`** flag for complex operations
  - Use with caution for large refactoring tasks
  - Removes iteration limits when needed
- **Configuration support** for default tool call limits
  - Set in `~/.config/nano-cli/config.yaml`
  - Environment variable override: `NANO_AGENT_MAX_TOOL_CALLS`

### 🚀 `init` Command for Easy Setup
- **`nano-cli init`** - Initialize or regenerate configuration
  - Interactive setup for default provider and model
  - Displays current configuration if it exists
  - `--force` flag to overwrite existing config
  - Creates necessary directories automatically
- **Guided configuration** with sensible defaults
  - Auto-detects available providers
  - Validates API keys when provided
  - Suggests popular models for each provider

### 🐛 Development Mode
- **`--dev`** flag for enhanced debugging
  - Detailed error messages with stack traces
  - Tool execution logging
  - Token usage breakdown per tool call
  - Performance profiling information
- **Development-specific error handling**
  - Shows exact tool names that failed
  - Lists available tools when tool not found
  - Provides suggestions for common issues
  - Includes request/response payloads for debugging

### 📋 Default Output Format Change
- **`nano-cli run` now defaults to "simple" output**
  - Clean, scriptable output for automation
  - No formatting or panels by default
  - Use `--output-format rich` or `-f rich` for formatted output
- **Interactive mode maintains rich output**
  - Beautiful panels and formatting in interactive sessions
  - Consistent user experience for interactive use

## 🔧 Improvements

### Enhanced Error Handling
- **ModelBehaviorError** exceptions with specific handling
  - Clear messages for tool not found errors
  - Lists available tools when appropriate
  - Suggests corrections for common mistakes
- **Improved terminal state management**
  - Proper cleanup on exit (Ctrl+C, Ctrl+D)
  - Fixes display issues in interactive mode
  - Ensures terminal attributes are reset correctly
- **Better error messages** throughout the system
  - User-friendly explanations without stack traces
  - Actionable suggestions for resolution
  - Development mode for detailed debugging info

### CLI Enhancements
- **Refined interactive session messages**
  - Clearer exit instructions (Ctrl+D or 'exit')
  - Better handling of keyboard interrupts
  - Improved prompt display and formatting
- **Configuration validation** on startup
  - Checks for required API keys
  - Validates provider/model combinations
  - Suggests fixes for common configuration issues

### Installation & Setup
- **Enhanced install scripts** for all platforms
  - Better error detection and recovery
  - Automatic dependency resolution
  - Progress indicators during installation
  - Validation of successful installation
- **PowerShell installer improvements** (Windows)
  - Admin privilege detection
  - Path management fixes
  - Better error messages
- **Bash installer enhancements** (Unix/Linux/macOS)
  - Improved Python detection
  - UV package manager auto-installation
  - Claude Desktop integration fixes

## 🧪 Testing

### New Test Coverage
- **Bash command execution tests** (`test_nano_agent_tools_bash.py`)
  - 25+ test cases for command execution
  - Security validation tests
  - Timeout and error handling tests
  - Output capture and formatting tests
- **Search tools tests**
  - Grep pattern matching validation
  - File search functionality tests
  - Error handling for invalid inputs

## 📚 Documentation

### New Documentation
- **`NANO_CLI_USAGE.md`** - Comprehensive CLI usage guide
  - Complete command reference
  - Examples for all features
  - Configuration guide
  - Troubleshooting section
- **`config/sample_config.yaml`** - Example configuration file
  - All available options documented
  - Provider-specific configurations
  - Environment variable mappings

### Updated Documentation
- **README.md** improvements
  - Added new tool descriptions
  - Updated examples with new features
  - Installation troubleshooting section
- **Removed outdated documentation**
  - Consolidated README_ALT.md into main README
  - Removed duplicate specification files

## 🔄 Breaking Changes

### Output Format Default
- `nano-cli run` now defaults to "simple" output format instead of "rich"
- To restore previous behavior, use `--output-format rich` or set in config:
  ```yaml
  defaults:
    output_format: rich
  ```

## 🐛 Bug Fixes

- Fixed terminal state corruption in interactive mode after errors
- Resolved display issues with Ctrl+C handling in interactive sessions
- Fixed error detail display when development mode is enabled
- Corrected tool registration for new search capabilities
- Fixed configuration file creation on first run

## 📦 Dependencies

### Removed
- `python-dotenv` - No longer needed with improved config system

### Updated
- Minor version bumps for security and compatibility

## 🚀 Migration Guide

### For Users Upgrading from v0.2.1

1. **Update your configuration** if you prefer rich output by default:
   ```bash
   nano-cli init
   # Or manually edit ~/.config/nano-cli/config.yaml
   ```

2. **New tool names** - Update any scripts using the old tool names:
   - `grep_search` → `grep_file`
   - `file_search` → `search_files`

3. **Tool call limits** - Consider setting defaults in your config:
   ```yaml
   defaults:
     max_tool_calls: 30  # Adjust based on your needs
   ```

4. **Development mode** - Use `--dev` flag when debugging issues:
   ```bash
   nano-cli run "task" --dev  # Shows detailed error information
   ```

## 📈 Performance

- Search operations optimized with compiled regex patterns
- Bash command execution with proper resource cleanup
- Improved error handling reduces unnecessary retries
- Configuration caching reduces file I/O

## 🔮 Coming Soon

- Streaming responses for real-time feedback
- Web UI for session management
- Plugin system for custom tools
- Advanced caching strategies

---

**Full Changelog**: [v0.2.1...v0.3.0](https://github.com/meirm/nano-agent/compare/ca697a4...HEAD)

**Contributors**: Thank you to everyone who reported issues and suggested improvements!