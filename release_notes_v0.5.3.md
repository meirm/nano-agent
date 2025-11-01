# Release Notes - Nano Agent v0.5.3

## 🚀 Version 0.5.3 - December 2024

## Overview
This release adds **builtin `/skills` command** to nano-cli interactive mode, making it easy to browse and inspect Agent Skills directly from the interactive shell. This enhancement improves discoverability and usability of the Skills system by providing seamless access to skill information without leaving the interactive session.

**Key Highlights**:
- New `/skills` builtin command in interactive mode
- `/skills show <name>` command to view detailed skill information
- Tab completion support for Skills commands
- Consistent user experience with `/commands` and `/agents` commands

## ✨ New Features

### Builtin `/skills` Command in Interactive Mode

The interactive mode now includes a native `/skills` command that allows users to browse and inspect Agent Skills without leaving the session.

#### `/skills` Command

**Usage**: `/skills`

**Features**:
- Displays all available Agent Skills in a formatted table
- Shows skill name, description, status (enabled/disabled), source (global/project), and resource count
- Displays summary statistics (total skills, enabled/disabled counts, global/project counts)
- Shows directory paths for global and project skill locations

**Example Output**:
```
Available Skills
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
┃ Name                  ┃ Description         ┃ Status    ┃ Source ┃ Resources ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
│ readme-generator      │ Generate README...   │ ✓ Enabled │ global │ 0         │
│ code-formatting-checker│ Check formatting... │ ✓ Enabled │ global │ 0         │
│ security-audit        │ Perform security... │ ✓ Enabled │ global │ 0         │
│ write-release-notes   │ Generate release... │ ✓ Enabled │ global │ 0         │
└───────────────────────┴─────────────────────┴───────────┴────────┴───────────┘

Total: 4 skills (4 enabled, 0 disabled, 4 global, 0 project)
```

#### `/skills show <name>` Command

**Usage**: `/skills show <skill_name>`

**Features**:
- Displays the full `SKILL.md` content in a formatted panel
- Shows skill path and enabled/disabled status
- Displays disabled reason if the skill is not enabled
- Color-coded border (green for enabled, red for disabled)

**Example**:
```bash
/skills show readme-generator
```

Shows the complete skill documentation including:
- YAML frontmatter (name, description, tools)
- Full instructions
- Examples and usage patterns
- Any additional content in the SKILL.md file

### Enhanced Command Integration

**Tab Completion**:
- `/skills` is now available in tab autocompletion
- Shows helpful description: "List all available Agent Skills"
- Consistent with other builtin commands (`/help`, `/commands`, `/agents`)

**Help Integration**:
- `/skills` and `/skills show <name>` are listed in the `/help` output
- Clear usage examples provided
- Consistent formatting with other commands

**Command Routing**:
- Properly handled as a builtin command
- Doesn't conflict with user-defined commands
- Error handling for non-existent skills

## 🔧 Technical Implementation

### New Methods

**`_display_skills_table()`**:
- Loads skills using `SkillLoader` with proper permission validation
- Formats skills in a Rich table with color-coded status
- Handles empty skill lists with helpful messages
- Shows directory paths for skill management

**`_show_skill_details(skill_name)`**:
- Loads and displays individual skill content
- Reads and formats `SKILL.md` file
- Shows permission status and disabled reasons
- Error handling for missing skills or files

### Integration Points

**`NanoAgentCompleter`**:
- Added `/skills` to `embedded_commands` list
- Added description for autocompletion
- Refreshes command list on demand

**`InteractiveSession`**:
- Added `/skills` handler in `_handle_special_command()`
- Added `/skills show` handler for detailed views
- Updated embedded command check list

## 📊 User Experience Improvements

**Discoverability**:
- Skills are now easily discoverable from within interactive mode
- No need to exit to run `nano-cli skills list`
- Quick access to skill documentation

**Consistency**:
- Matches the behavior and style of `/commands` and `/agents`
- Familiar interface for users already using these commands
- Consistent error messages and help text

**Workflow Integration**:
- Browse skills while working in interactive mode
- Check skill status before using them
- Review skill instructions without context switching

## ✅ Testing

**Verification Completed**:
- ✅ `/skills` command displays skills table correctly
- ✅ `/skills show <name>` displays skill details
- ✅ Tab completion works for `/skills`
- ✅ Help text includes Skills commands
- ✅ Error handling for missing skills
- ✅ Permission validation works correctly
- ✅ Empty skill list handled gracefully

## 📦 What's Included

**Files Modified**:
- `interactive_mode.py` - Added `/skills` command implementation
  - Added to `embedded_commands` list
  - Added `_display_skills_table()` method
  - Added `_show_skill_details()` method
  - Updated help text and command routing
- Version numbers updated to 0.5.3

**No Breaking Changes**: All changes are backward compatible. Existing functionality remains unchanged.

## 🎯 Use Cases

**Example Workflows**:

1. **Browse Available Skills**:
   ```
   nano-cli
   > /skills
   ```

2. **Check Specific Skill**:
   ```
   nano-cli
   > /skills show readme-generator
   ```

3. **Discover Skills While Working**:
   - During an interactive session, quickly check what skills are available
   - Review skill documentation without leaving the session
   - Verify skill permissions before using them

## 🔄 Migration Guide

**No migration required**. This is a feature release. All existing Skills, Commands, and configurations continue to work without modification.

## 🙏 Acknowledgments

This release focuses on improving the interactive mode experience by making Skills management more accessible and integrated into the daily workflow.

## 📝 Next Steps

- Try `/skills` in interactive mode to browse available skills
- Use `/skills show <name>` to review skill documentation
- Create custom skills and view them with the new commands

---

**Full Changelog**: See [GitHub commits](https://github.com/meirm/nano-agent/compare/v0.5.2...v0.5.3) for detailed changes.

**Previous Release**: [v0.5.2 Release Notes](release_notes_v0.5.2.md)

