# Release Notes - Nano Agent v0.4.1

## 🚀 Version 0.4.1 - October 15, 2025

## Overview
This is a **critical bug fix release** addressing a regression in v0.4.0 where shell command evaluation was not working in **enhanced interactive mode** (nano-cli). Commands using the `$`command`` syntax were being sent to the agent unevaluated, causing unnecessary tool calls.

**Note**: This bug only affected nano-cli's enhanced interactive mode. Both the direct prompt mode (`nano-cli -p`) and simple interactive mode worked correctly. The nano-agent MCP server was not affected.

## 🐛 Bug Fixes

### Critical: Interactive Mode Command Evaluation
- **Fixed shell command evaluation in interactive mode** - Commands are now properly evaluated before being sent to the agent
  - **Issue**: Interactive mode was bypassing `_process_prompt()` method, sending raw command syntax to the agent
  - **Impact**: Agent made unnecessary tool calls (bash_command_permission_wrapper) to gather information that should have been pre-evaluated
  - **Root Cause**: The `run()` method in `interactive_mode.py` was calling `_handle_special_command()` and passing raw `user_input` directly to the agent
  - **Fix**: Modified execution flow to call `_process_prompt()` which properly loads command files, evaluates shell commands, and substitutes arguments
  - **Example**: `/system_report` now sends pre-evaluated date, user, hostname instead of causing 4 tool calls

### Documentation Syntax Confusion
- **Clarified command file syntax in COMMANDS.md** - Resolved confusion about backslash escaping
  - **Issue**: Documentation showed markdown-escaped `$\`command\`` syntax, but actual files need `$`command`` (without backslashes)
  - **Impact**: Users created command files with incorrect syntax, preventing shell evaluation
  - **Fix**: Added prominent warnings and corrected examples throughout COMMANDS.md
  - **Added**: Clear section explaining markdown escaping vs. actual file syntax

## 🔧 Improvements

### Documentation Enhancements
- **COMMANDS.md Updates**:
  - Added **IMPORTANT** warning about syntax differences between documentation and actual files
  - Updated all examples to use correct `$`command`` syntax in code blocks
  - Added note: "Write these in your command files WITHOUT backslashes"
  - Clarified order of operations for command processing
  - Updated example use cases with correct syntax

### Testing & Validation
- ✅ Verified shell commands are evaluated before reaching agent in interactive mode
- ✅ Confirmed no tool calls are made for pre-evaluated system information
- ✅ Tested both `-p` flag mode and interactive mode execution
- ✅ Validated correct syntax in example command files

## 🛠️ Files Modified

### Core Bug Fixes
- **`src/nano_agent/modules/interactive_mode.py`** (Lines 887-901)
  - Changed from: `_handle_special_command()` → pass raw `user_input` to agent
  - Changed to: `_process_prompt()` → pass evaluated `processed_prompt` to agent
  - Impact: Commands now properly processed and shell commands evaluated

### Documentation Updates
- **`COMMANDS.md`** (Multiple sections)
  - Added syntax clarification warnings
  - Updated Shell Command Evaluation section with proper examples
  - Corrected all example use cases
  - Added distinction between markdown escaping and actual file syntax

- **`~/.nano-cli/commands/system_report.md`** (Example fix)
  - Changed from: `$\`date "+%Y-%m-%d %H:%M:%S"\`` (escaped)
  - Changed to: `$`date "+%Y-%m-%d %H:%M:%S"`` (correct syntax)

## 📈 Impact

### Before Fix (v0.4.0)
```
User: /system_report show me a summary

Agent Tool Calls:
🔧 Tool Call #1: bash_command_permission_wrapper (date)
🔧 Tool Call #2: bash_command_permission_wrapper (whoami)
🔧 Tool Call #3: bash_command_permission_wrapper (hostname)
🔧 Tool Call #4: bash_command_permission_wrapper (pwd)

Result: 4 unnecessary tool calls, slower execution
```

### After Fix (v0.4.1)
```
User: /system_report show me a summary

Agent receives:
# System Report
- **Date**: 2025-10-15 23:17:43
- **User**: meirm
- **Hostname**: MacPower128.local
- **Current Directory**: /Users/meirm/git/riunx/...

Result: ✅ No tool calls, instant response, correct behavior
```

## 🚀 Migration Guide

### For Users Upgrading from v0.4.0

**No action required** if you haven't created custom command files yet.

#### If You Have Custom Command Files with Shell Evaluation

1. **Check Your Command Files** (`~/.nano-cli/commands/*.md`):
   ```bash
   # Look for escaped backticks (INCORRECT)
   grep -r '\$\\`' ~/.nano-cli/commands/
   ```

2. **Fix Syntax** - Remove backslashes before backticks:
   ```markdown
   # BEFORE (incorrect - v0.4.0 documentation confusion)
   - **Date**: $\`date "+%Y-%m-%d"\`

   # AFTER (correct - v0.4.1 and going forward)
   - **Date**: $`date "+%Y-%m-%d"`
   ```

3. **Test Your Commands**:
   ```bash
   # Interactive mode test
   nano-cli
   > /your-command test arguments

   # Direct mode test
   nano-cli -p '/your-command test arguments'
   ```

#### Command Syntax Quick Reference

| Context | Syntax | Example |
|---------|--------|---------|
| **In command files** | `$`command`` | `$`date\`` |
| **In documentation** | `$\`command\`` | Markdown escaped for display |
| **Escape in files** | `\$`command`` | Shows literal `$`command\`` |

## 🧪 Testing Performed

### Regression Tests
- ✅ Interactive mode command evaluation works correctly
- ✅ Direct mode (`-p` flag) command evaluation works correctly
- ✅ Commands with `$ARGUMENTS` substitution work correctly
- ✅ Shell command evaluation happens before agent receives prompt
- ✅ No tool calls for pre-evaluated information
- ✅ Error handling for failed commands works correctly
- ✅ Timeout protection (10 seconds) works correctly

### Platform Testing
- ✅ macOS (primary development platform)
- ✅ Ollama provider integration tested
- ✅ Both gpt-oss:20b and other models tested

## 📚 Documentation

### Updated Files
1. **COMMANDS.md** - Complete syntax clarification overhaul
2. **Example command files** - Fixed syntax in all examples
3. **This release note** - Comprehensive migration guide

### Key Documentation Additions
- Syntax distinction between markdown documentation and actual files
- Troubleshooting section for command evaluation
- Updated examples with correct, tested syntax
- Visual before/after comparisons

## ⚠️ Known Issues

### None Currently Identified

All known issues from v0.4.0 have been resolved in this release.

## 🔮 Coming Soon

Unchanged from v0.4.0:
- Visual Studio Code extension integration
- Additional command evaluation features
- Enhanced security controls (command whitelisting)
- Performance profiling for command execution

## 🙏 Acknowledgments

Thank you to users who reported the interactive mode evaluation issue immediately after v0.4.0 release, enabling rapid identification and resolution.

---

## 📦 Installation

```bash
# Install or upgrade
cd apps/nano_agent_mcp_server
uv tool install -e .

# Or for development
uv sync --extra test

# Verify version
nano-cli --version  # Should show 0.4.1
```

---

## 📋 Quick Reference

### Enable Command Evaluation (Unchanged from v0.4.0)

| Environment | Method | Command |
|-------------|--------|---------|
| nano-cli | Config | Add `enable_command_eval: true` to `~/.nano-cli/config.yaml` |
| nano-cli | Env Var | `export NANO_CLI_ENABLE_COMMAND_EVAL=true` |
| MCP Server | Env Var | `export NANO_AGENT_ENABLE_COMMAND_EVAL=true` |

### Correct Syntax for Command Files

```markdown
# ✅ CORRECT - Use in your command files
- **Date**: $`date "+%Y-%m-%d"`
- **User**: $`whoami`
- **Branch**: $`git branch --show-current`

# ❌ INCORRECT - Don't use backslashes (this was in v0.4.0 docs by mistake)
- **Date**: $\`date "+%Y-%m-%d"\`
- **User**: $\`whoami\`
```

---

**Full Changelog**: v0.4.0...v0.4.1
**Release Date**: October 15, 2025
**Release Type**: Patch (Bug Fix)
**Contributors**: @meirm

---

## Summary

v0.4.1 is a **critical bug fix** release that resolves the interactive mode command evaluation regression introduced in v0.4.0. All users of v0.4.0 should upgrade immediately, especially those using custom command files with shell evaluation. The fix ensures shell commands are properly evaluated before prompts reach the agent, eliminating unnecessary tool calls and providing the intended user experience.

**Upgrade Priority**: 🔴 **HIGH** - Critical bug fix for core functionality
