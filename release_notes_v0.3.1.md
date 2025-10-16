# Release Notes - Nano Agent v0.3.1

## 🚀 Version 0.3.1 - December 17, 2024

### 🎭 Agent Persona System Fixes

**Fixed Agent Persona Support in Interactive Mode**
- **Issue**: The `--agent` flag was being ignored in interactive mode, and agent switching commands weren't working properly
- **Solution**: Fixed agent parameter passing and command handling in interactive sessions
- **Impact**: Agent personalities now work consistently across all modes

#### Key Improvements:
- ✅ `--agent <name>` flag now works when starting interactive sessions
- ✅ `@<agent>` command properly switches agents during sessions
- ✅ `@` command shows current agent and lists available agents
- ✅ Prompt display correctly shows current agent (e.g., `h4x0r@qwen2.5:7b`)
- ✅ Agent personalities function correctly (h4x0r uses l33t speak, etc.)

#### Usage Examples:
```bash
# Start with specific agent
nano-cli interactive --agent h4x0r --provider ollama --model qwen2.5:7b

# Switch agents during session
@h4x0r                    # Switch to h4x0r agent
@default                  # Switch back to default
@                         # Show current agent and list available
```

### 🔧 Event Loop Management Enhancements

**Resolved HTTP Client Cleanup Issues**
- **Issue**: AsyncOpenAI HTTP clients weren't being properly closed, causing "RuntimeError: Event loop is closed" exceptions on exit
- **Solution**: Implemented comprehensive HTTP client lifecycle management
- **Impact**: Clean exit from all modes without runtime errors

#### Technical Improvements:
- ✅ Added HTTP client tracking in `ProviderConfig` class
- ✅ Implemented proper async client cleanup before event loop shutdown
- ✅ Added cleanup calls in both sync and async execution paths
- ✅ Eliminated "RuntimeError: Event loop is closed" exceptions
- ✅ Eliminated "Exception ignored in" warnings

### 🛠️ Files Modified

#### Core Agent System:
- `src/nano_agent/modules/interactive_mode.py` - Fixed agent parameter passing and @ command handling
- `src/nano_agent/modules/provider_config.py` - Added HTTP client tracking and cleanup infrastructure
- `src/nano_agent/modules/nano_agent.py` - Added cleanup calls in execution finally blocks
- `src/nano_agent/modules/nano_agent_runner.py` - Enhanced cleanup sequence

#### Hook System Improvements:
- `src/nano_agent/modules/hook_executor_v2.py` - Subprocess-based execution without asyncio dependencies
- `src/nano_agent/modules/hook_manager_simplified.py` - Clean sync/async separation
- `src/nano_agent/modules/hook_types.py` - Fixed initialization parameter issues

### 🧪 Testing & Verification

**Comprehensive Testing Suite**
- ✅ All event loop management tests pass
- ✅ Agent persona switching verified across all scenarios
- ✅ HTTP client cleanup confirmed working
- ✅ Interactive mode stability validated
- ✅ Hook system functionality preserved

### 📈 Performance & Stability

- **Improved Stability**: Eliminated runtime exceptions on exit
- **Better Resource Management**: Proper HTTP client lifecycle management
- **Enhanced User Experience**: Consistent agent persona behavior
- **Cleaner Architecture**: Better separation of sync/async contexts

### 🔄 Backward Compatibility

- ✅ All existing functionality preserved
- ✅ Configuration files remain compatible
- ✅ Command-line interface unchanged
- ✅ MCP server API compatibility maintained

### 🎯 Migration Notes

No breaking changes in this release. All existing configurations, commands, and integrations will continue to work without modification.

### 🐛 Bug Fixes

1. **Agent Persona System**:
   - Fixed `--agent` flag being ignored in interactive mode
   - Fixed `@<agent>` command not switching agents properly
   - Fixed prompt display not showing current agent name

2. **Event Loop Management**:
   - Fixed "RuntimeError: Event loop is closed" on exit
   - Fixed HTTP client cleanup warnings
   - Fixed hook system subprocess cleanup issues

3. **Configuration**:
   - Fixed `HookConfig` initialization missing 'event' parameter
   - Fixed `HookResult` initialization parameter errors

---

## 📦 Installation

```bash
# Update to latest version
uv tool install -e . --force

# Or reinstall completely
./scripts/install.sh
```

## 🙏 Acknowledgments

Special thanks to the community for reporting the agent persona and event loop issues that led to these important stability improvements.

---

For detailed technical information, see:
- `EVENT_LOOP_FIX_SUMMARY.md` - Complete event loop management solution
- `AGENT_PERSONA_FIX_SUMMARY.md` - Agent persona system fixes