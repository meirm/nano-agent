# Release Notes - Nano Agent v0.5.1

## 🚀 Version 0.5.1 - November 1, 2025

## Overview
This release adds **permission-based control for Skills and Commands**, a new **Security Audit builtin skill**, and comprehensive **examples directory** with documentation. The permission system enables fine-grained control over which tools Skills and Commands can access, enhancing security and compliance.

**Key Highlights**:
- Permission validation system for Skills and Commands based on `allowed_tools`
- New Security Audit builtin skill for auditing Skills
- Comprehensive examples directory with agents, commands, and skills
- All builtin skills and user commands updated with tools metadata
- Enhanced test coverage with 67 tests (18 new permission tests)

## 🎯 New Features

### 🔒 Permission System for Skills and Commands

Skills and Commands now support permission validation based on `allowed_tools` configuration, enabling fine-grained access control.

#### Skills Permission System

**Activation**: Skills system is enabled when `"skill"` (lowercase) is in `allowed_tools`.

**Behavior**:
- Skills without `tools:` metadata are always allowed (when Skills system is enabled)
- Skills with `tools:` metadata require all listed tools to be in `allowed_tools`
- Skills with missing tools are disabled with clear reason messages
- Disabled skills are filtered from system prompts and matching results

**CLI Integration**:
- `nano-cli skills list` shows enabled/disabled status with reasons
- `nano-cli skills show` displays permission status and required tools
- Commands read `allowed_tools` from `~/.nano-cli/allowed-tools.json`

**Example Skill Metadata**:
```yaml
---
name: readme-generator
description: Generate comprehensive README files...
tools: ["read_file", "write_file", "list_directory"]
---
```

#### Commands Permission System

**Behavior**:
- Commands without `tools:` metadata are always allowed
- Commands with `tools:` metadata validate permissions at execution time
- Commands fail with `[Error: ...]` message if validation fails
- Clear error messages indicate which tools are missing

**Error Format**:
```
[Error: Command requires tools not allowed: write_file]
```

**CLI Integration**:
- All command execution paths validate permissions
- Error messages displayed before agent execution
- Commands read `allowed_tools` from configuration

**Example Command Metadata**:
```yaml
---
name: code-review
description: Perform a thorough code review...
tools: ["read_file", "grep_search"]
---
```

### 🔍 Security Audit Builtin Skill

New builtin skill for auditing Agent Skills for security vulnerabilities.

**Name**: `security-audit`

**Capabilities**:
- Comprehensive file-by-file review of Skill directories
- Detection of suspicious patterns (network calls, unauthorized file access)
- External dependency risk assessment
- Tool misuse detection
- Data exposure analysis
- Trust and provenance evaluation

**Tools**: `["read_file", "list_directory", "grep_search", "get_file_info"]`

**Trigger Keywords**: "audit", "security review", "check security", "verify skill"

**Output**: Structured security audit reports with:
- Executive summary with risk level
- File inventory
- Detailed findings by severity
- Pattern analysis
- Recommendations

### 📚 Examples Directory

New comprehensive examples directory demonstrating best practices:

**Structure**:
```
examples/
├── agents/          # Example agent personalities
├── commands/        # Example command templates  
├── skills/          # Example skill directories
└── README.md        # Main examples guide
```

**Content**:
- **Agents**: Example coder and analyst agents with full personality definitions
- **Commands**: Example code-review, test-generator, and documentation commands
- **Skills**: Example API testing, data analysis, and security audit skills
- **Documentation**: README files in each subdirectory explaining concepts

All examples include:
- Proper YAML frontmatter with metadata
- Tools specification for permission validation
- Usage examples and best practices
- Installation instructions

### 🔧 Metadata Updates

**Builtin Skills Updated**:
- All three builtin skills now include `tools:` metadata:
  - `readme-generator`: `["read_file", "write_file", "list_directory"]`
  - `code-formatting-checker`: `["read_file", "grep_search"]`
  - `write-release-notes`: `["read_file", "write_file"]`
  - `security-audit`: `["read_file", "list_directory", "grep_search", "get_file_info"]`

**User Commands Updated**:
- All 11 commands in `~/.nano-cli/commands/` updated with YAML frontmatter
- Appropriate `tools:` metadata added based on functionality
- Commands now compatible with permission validation system

## 🧪 Testing

### New Test Coverage

**Skills Permission Tests** (9 tests):
- `test_skill_without_tools_allowed_when_skills_enabled`
- `test_skill_with_tools_all_allowed`
- `test_skill_with_tools_some_missing_disabled`
- `test_skills_disabled_when_skill_not_in_allowed_tools`
- `test_blocked_skill_disabled`
- `test_match_skills_filters_disabled_skills`
- `test_get_skill_metadata_summary_filters_disabled`
- `test_skills_backward_compatible_no_permissions`
- `test_builtin_skills_have_tools_metadata`

**Commands Permission Tests** (9 tests):
- `test_command_without_tools_allowed`
- `test_command_with_tools_all_allowed`
- `test_command_with_tools_some_missing_fails`
- `test_command_blocked_fails`
- `test_command_backward_compatible_no_permissions`
- `test_command_tools_extracted_from_yaml_frontmatter`
- `test_command_tools_extracted_from_metadata_section`
- `test_command_loader_wrapper_preserves_shell_eval`
- `test_command_error_string_format`

**Total Test Count**: 67 tests (all passing)

## 🔄 Changes and Improvements

### Skills System
- **Permission Integration**: `SkillLoader` now accepts `allowed_tools` and `blocked_tools` parameters
- **Validation Logic**: `_validate_skill_permissions()` method checks tool availability
- **Filtering**: Disabled skills automatically filtered from matching and metadata summaries
- **CLI Display**: Enhanced `skills list` and `skills show` commands show permission status

### Commands System
- **YAML Frontmatter Support**: Commands now support YAML frontmatter for metadata
- **Permission Validation**: `_validate_command_permissions()` method validates at execution time
- **Error Handling**: Clear error messages when commands cannot execute due to permissions
- **All Call Sites Updated**: CLI, interactive mode, and coordinator updated to handle permissions

### Code Quality
- **Backward Compatibility**: All changes maintain backward compatibility when `allowed_tools` is `None`
- **Clear Error Messages**: Permission failures include specific reasons
- **Comprehensive Tests**: Full test coverage for permission scenarios
- **Documentation**: Examples and README files explain new features

## 📝 Documentation

### New Documentation Files
- `examples/README.md`: Comprehensive guide to examples
- `examples/agents/README.md`: Agent concepts and usage
- `examples/commands/README.md`: Command format and examples
- `examples/skills/README.md`: Skill architecture and best practices

### Updated Documentation
- All builtin skills include tools metadata
- All example files demonstrate proper metadata format
- Security audit skill includes comprehensive audit guidelines

## 🔧 Technical Details

### Permission Validation Logic

**Skills**:
1. If `allowed_tools` is `None`: enable all (backward compatible)
2. If `"skill"` not in `allowed_tools`: disable all skills
3. If skill has no `tools:` metadata: always allow (when Skills system enabled)
4. If skill has `tools:` metadata: all tools must be in `allowed_tools`

**Commands**:
1. If `allowed_tools` is `None`: allow all (backward compatible)
2. If command has no `tools:` metadata: always allow
3. If command has `tools:` metadata: validate at execution time
4. Return `[Error: ...]` if validation fails

### Files Modified
- `src/nano_agent/modules/skill_loader.py`: Permission validation and filtering
- `src/nano_agent/modules/cascade_command_loader.py`: YAML parsing and permission validation
- `src/nano_agent/modules/nano_agent.py`: Pass permissions to SkillLoader
- `src/nano_agent/cli.py`: Display permission status in commands
- `src/nano_agent/modules/interactive_mode.py`: Permission handling in interactive mode
- `src/nano_agent/modules/coordinator.py`: Permission handling in coordinator
- All builtin skills: Added `tools:` metadata
- All user commands: Added YAML frontmatter with tools

## 🐛 Bug Fixes

- Fixed command execution when permissions are restricted
- Improved error messages for permission failures
- Enhanced skill filtering to exclude disabled skills from matching

## ⚙️ Configuration

### Permission Configuration

Permissions are configured via `~/.nano-cli/allowed-tools.json`:

```json
{
  "allowed_tools": ["skill", "read_file", "write_file", "list_directory"]
}
```

The `"skill"` entry enables the Skills system. Individual tool names enable specific capabilities.

## 🔄 Migration Guide

### For Users

**No action required** if you don't use `allowed_tools`. The system remains backward compatible.

**If using `allowed_tools`**:
1. Add `"skill"` to `allowed_tools` to enable Skills system
2. Ensure required tools are listed for Skills/Commands you use
3. Check disabled skills with `nano-cli skills list`

### For Skill/Command Authors

**Update your Skills**:
- Add `tools:` to YAML frontmatter if skill uses specific tools
- Leave `tools:` empty `[]` if skill doesn't need specific tools

**Update your Commands**:
- Add YAML frontmatter with `name`, `description`, and `tools:`
- Specify all tools the command requires

## 📊 Statistics

- **New Builtin Skill**: 1 (security-audit)
- **New Tests**: 18 permission validation tests
- **Examples Added**: 8 example files (2 agents, 3 commands, 3 skills)
- **Documentation Files**: 4 README files
- **Total Test Count**: 67 tests (all passing)
- **Code Changes**: ~500 lines added/modified

## 🙏 Acknowledgments

This release focuses on security and permission control, inspired by Anthropic's Agent Skills security considerations. The permission system enables organizations to safely deploy nano-agent with restricted tool access while maintaining full functionality for authorized operations.

## 🔜 What's Next

Future releases may include:
- Additional builtin skills for common workflows
- Skill sharing and distribution mechanisms
- Enhanced permission models
- More comprehensive examples

## 📦 Installation

Update to v0.5.1:

```bash
# Using uv
uv tool install --force nano-agent

# Or reinstall from source
pip install --upgrade nano-agent
```

After updating, builtin skills will be automatically updated with new metadata.

## 🔗 Related Documentation

- **Skills Documentation**: `apps/nano_agent_mcp_server/docs/SKILLS.md`
- **Commands Documentation**: `apps/nano_agent_mcp_server/COMMANDS.md`
- **Examples**: `examples/README.md`
- **Security Audit Skill**: `apps/nano_agent_mcp_server/src/nano_agent/data/builtin_skills/security-audit/SKILL.md`

---

**Full Changelog**: See git history for detailed commit messages.

