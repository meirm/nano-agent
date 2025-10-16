# Release Notes - Nano Agent v0.2.0

**Release Date**: September 3, 2025

## 🚀 Major Improvements

### Clean Output Control
- **Non-verbose mode now shows only agent responses** - Removed all extra status panels, timing information, and logging messages from default output
- **Verbose mode (`--verbose`)** provides full diagnostic information including agent lifecycle panels, metadata, and execution details
- **Proper stderr redirection** - In verbose mode, all logging messages are redirected to stderr while agent responses go to stdout

### Enhanced Billing Control
- **Billing information only shown with `--billing` flag** - Token usage and cost information is now opt-in rather than always displayed
- **Consistent across all output formats** - Billing control works uniformly with simple, JSON, and rich output formats

## 🛠️ Technical Changes

### CLI Output System Overhaul
- **RichLoggingHooks** now respect verbose mode settings
- **Output formatters** properly handle verbose and billing flags
- **Console separation** between actual output (stdout) and logging (stderr when verbose)

### Command-Line Interface
- Added verbose parameter to interactive mode (`nano-cli interactive --verbose`)
- Improved error handling for invalid provider/model combinations
- Consistent behavior across all output formats (simple, JSON, rich)

## 📊 Output Behavior Matrix

| Mode | Command Example | Output |
|------|----------------|---------|
| **Default** | `nano-cli run "hello"` | Agent response only |
| **With Billing** | `nano-cli run "hello" --billing` | Agent response + token usage table |
| **Verbose** | `nano-cli run "hello" --verbose` | Full logging panels + agent response + metadata |
| **Verbose + Billing** | `nano-cli run "hello" --verbose --billing` | All logging + agent response + billing + metadata |
| **Simple Format** | `nano-cli run "hello" -f simple` | Plain text agent response |
| **JSON Format** | `nano-cli run "hello" -f json` | Clean JSON output |

## 🔧 Migration Guide

### For Existing Users
- **No breaking changes** - All existing commands work without modification
- **Cleaner default output** - You'll see less verbose output by default, which is beneficial for scripting
- **To see previous behavior** - Add `--verbose` flag to any command

### For Script Integration
- **JSON output remains unchanged** - Scripts using `-f json` are unaffected
- **Simple format improved** - Better for command-line processing and piping
- **Billing information** - Add `--billing` flag if you need token/cost information

## 🎯 Benefits

### User Experience
- **Cleaner interface** - Focus on actual agent responses without distracting status messages
- **Better scriptability** - Simple format is now truly minimal and pipe-friendly
- **Flexible verbosity** - Choose the right level of detail for your use case

### Developer Experience  
- **Proper logging separation** - Debug information goes to stderr, results to stdout
- **Consistent behavior** - All output formats follow the same verbosity rules
- **Improved testing** - Easier to validate agent responses without parsing status messages

## 🐛 Bug Fixes

- Fixed verbose mode logging not properly redirecting to stderr
- Resolved issue where rich panels showed even in simple/JSON formats
- Corrected billing information appearing regardless of `--billing` flag setting
- Improved error messages for invalid provider/model combinations

## 🔄 Backward Compatibility

- ✅ All existing commands work without changes
- ✅ Default output format remains Rich
- ✅ Command syntax and flags unchanged
- ✅ Session management and configuration files compatible

## 🚨 Breaking Changes

**None** - This is a fully backward-compatible release.

---

**Full Changelog**: Compare changes at [GitHub Release](https://github.com/your-repo/nano-agent)