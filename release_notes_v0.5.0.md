# Release Notes - Nano Agent v0.5.0

## 🚀 Version 0.5.0 - November 1, 2025

## Overview
This release introduces the **Agent Skills system** – a powerful, extensible framework inspired by Anthropic's Agent Skills that enables nano-agent to discover, load, and execute specialized capabilities automatically. Skills extend nano-agent's functionality through modular, reusable instructions and resources that are loaded progressively based on context relevance.

**Key Highlights**:
- Three built-in skills included: README Generator, Code Formatting Checker, and Write Release Notes
- Progressive disclosure architecture optimizes context window usage
- Full CLI and MCP server integration for skill management
- Cascade loading system (global and project-specific skills)
- Comprehensive test coverage with 344 lines of tests

## 🎯 New Features

### 🧠 Agent Skills System

The Agent Skills system allows you to package domain-specific expertise, workflows, and best practices as reusable skills. Skills are automatically discovered and triggered based on keyword matching between user prompts and skill descriptions.

**Core Architecture**:
- **Progressive Disclosure**: Skills are loaded in stages (metadata → instructions → resources) to optimize context usage
- **SkillLoader Module**: New `SkillLoader` class (`src/nano_agent/modules/skill_loader.py`) handles discovery, parsing, caching, and matching
- **Cascade Loading**: Skills can be defined globally (`~/.nano-cli/skills/`) or per-project (`.nano-cli/skills/`), with project-level overriding global
- **Automatic Installation**: Built-in skills are automatically installed to `~/.nano-cli/skills/` on first initialization

**Skill Structure**:
- Skills are directories containing a `SKILL.md` file with YAML frontmatter (name, description)
- Optional resources: additional markdown files, scripts, templates
- Skills use keyword-based matching for automatic triggering

### 📦 Built-in Skills

Three production-ready skills are included:

1. **README Generator** (`readme-generator`)
   - Automatically generates comprehensive README.md files
   - Analyzes project structure, configuration files, and dependencies
   - Creates installation, usage, and documentation sections
   - Trigger keywords: "readme", "generate readme", "documentation"

2. **Code Formatting Checker** (`code-formatting-checker`)
   - Scans codebase for formatting inconsistencies
   - Detects style issues and inconsistencies
   - Language-agnostic checks plus language-specific formatter integration
   - Trigger keywords: "format", "check formatting", "code style", "linting"

3. **Write Release Notes** (`write-release-notes`)
   - Generates professional release notes from git history
   - Analyzes commits, version files, and project changes
   - Follows semantic versioning conventions
   - Trigger keywords: "release notes", "changelog", "version changes"

### 🖥️ CLI Enhancements

New `nano-cli skills` sub-command for managing Agent Skills:

- **`nano-cli skills list`** - Lists all available skills with metadata
  - Shows name, description, source (global/project/builtin), and trigger keywords
  - Displays in a formatted table using `rich`

- **`nano-cli skills show <name>`** - Shows detailed information about a skill
  - Displays full skill metadata and instructions
  - Shows resources and file structure

- **`nano-cli skills create <name>`** - Creates a new skill template
  - Creates skill directory structure with `SKILL.md` template
  - Supports `--global` flag for global skills
  - Supports `--overwrite` flag to replace existing skills

- **`nano-cli skills install-builtin`** - Installs or reinstalls built-in skills
  - Copies built-in skills to `~/.nano-cli/skills/`
  - `--overwrite` flag updates existing built-in skills (useful for updates)
  - `--skill <name>` flag installs a specific skill only

### 🔌 MCP Tools Integration

New MCP tools for skill management via the nano-agent MCP server:

- **`list_skills`** - Lists all available skills with metadata
  - Returns structured JSON with skill information
  - Includes name, description, source, and path

- **`get_skill_info`** - Gets detailed information about a specific skill
  - Returns full skill metadata and file structure
  - Includes resource listing

- **`load_skill_instructions`** - Loads skill instructions for a specific skill
  - Returns the full instructions content
  - Useful for programmatic skill access

### 🧩 Progressive Disclosure Implementation

Skills are integrated into nano-agent's execution pipeline using progressive disclosure:

**Level 1 (Always Loaded)**:
- Skill metadata (name, description) is included in the system prompt
- Minimal token cost (~100 tokens per skill)
- Enables skill discovery without context penalty

**Level 2 (Triggered)**:
- Skill instructions (`SKILL.md` body) are loaded when user prompts match skill keywords
- Content is injected into the conversation context
- Optimized loading ensures only relevant skills consume context

**Level 3 (As Needed)**:
- Additional resources (scripts, templates, reference files) are accessed via filesystem
- Executed via `bash_command` without loading into context
- Effectively unlimited resource capacity

## 🔧 Improvements

### Core Architecture

- **SkillLoader Module** (`src/nano_agent/modules/skill_loader.py`):
  - 583 lines of comprehensive skill management logic
  - YAML frontmatter parsing with `PyYAML`
  - Intelligent keyword-based skill matching
  - Built-in skills installation and management
  - Path resolution for development and production environments
  - Caching mechanism for performance optimization

- **Agent Integration** (`src/nano_agent/modules/nano_agent.py`):
  - Skill metadata automatically added to system prompt
  - Skill instructions dynamically injected when triggered
  - Seamless integration with existing agent execution flow
  - No breaking changes to existing functionality

### Documentation

- **New Documentation** (`apps/nano_agent_mcp_server/docs/SKILLS.md`):
  - 441 lines of comprehensive skill system documentation
  - Architecture explanation with progressive disclosure details
  - Skill structure and creation guide
  - Built-in skills documentation
  - CLI and MCP usage examples

- **Updated Documentation**:
  - `CONFIG.md`: Added skills configuration section
  - `NANO_CLI_USAGE.md`: Added skills command examples
  - `ai_docs/anthropic_agent_skills.md`: Reference documentation for skill architecture

### Testing

- **Comprehensive Test Suite** (`tests/nano_agent/modules/test_skill_loader.py`):
  - 344 lines of unit and integration tests
  - Tests for skill loading, parsing, and caching
  - Built-in skills installation tests
  - Skill matching and keyword detection tests
  - Cascade loading and override behavior tests
  - Path resolution tests for different environments

## 🛠️ Files Added

### Core Implementation
- `apps/nano_agent_mcp_server/src/nano_agent/modules/skill_loader.py` (583 lines) - Core SkillLoader implementation
- `apps/nano_agent_mcp_server/src/nano_agent/data/builtin_skills/__init__.py` - Package initialization
- `apps/nano_agent_mcp_server/src/nano_agent/data/builtin_skills/readme-generator/SKILL.md` (190 lines)
- `apps/nano_agent_mcp_server/src/nano_agent/data/builtin_skills/code-formatting-checker/SKILL.md` (207 lines)
- `apps/nano_agent_mcp_server/src/nano_agent/data/builtin_skills/write-release-notes/SKILL.md` (279 lines)

### Documentation
- `apps/nano_agent_mcp_server/docs/SKILLS.md` (441 lines) - Comprehensive skills documentation
- `ai_docs/anthropic_agent_skills.md` (330 lines) - Reference documentation

### Testing
- `apps/nano_agent_mcp_server/tests/nano_agent/modules/test_skill_loader.py` (344 lines) - Test suite

### Total Impact
- **15 files changed**
- **2,895 lines added**
- **3 lines removed**

## 🛠️ Files Modified

### Core Changes
- `apps/nano_agent_mcp_server/src/nano_agent/modules/nano_agent.py` (39 lines modified)
  - Integrated SkillLoader into agent execution
  - Added skill metadata to system prompt
  - Implemented skill instruction injection on trigger

- `apps/nano_agent_mcp_server/src/nano_agent/cli.py` (336 lines added)
  - Added `skills_app` Typer sub-application
  - Implemented `list`, `show`, `create`, and `install-builtin` commands
  - Added rich table formatting for skill listing

- `apps/nano_agent_mcp_server/src/nano_agent/mcp_tools.py` (134 lines added)
  - Added `list_skills` MCP tool
  - Added `get_skill_info` MCP tool
  - Added `load_skill_instructions` MCP tool

- `apps/nano_agent_mcp_server/src/nano_agent/__main__.py` (9 lines modified)
  - Registered new skill-related MCP tools
  - Updated server instructions to document skill tools

### Documentation Updates
- `apps/nano_agent_mcp_server/CONFIG.md` (6 lines added) - Skills configuration section
- `apps/nano_agent_mcp_server/NANO_CLI_USAGE.md` (34 lines added) - Skills command examples

## 🧪 Testing Performed

### Unit Tests
- ✅ Skill loading and parsing from various locations
- ✅ YAML frontmatter extraction and validation
- ✅ Skill metadata summary generation
- ✅ Built-in skills installation and management
- ✅ Skill matching based on keyword detection
- ✅ Cascade loading (global vs. project-level)
- ✅ Skill caching and refresh mechanisms
- ✅ Path resolution for development and production

### Integration Tests
- ✅ Built-in skills exist and are properly structured
- ✅ Skills can be installed and accessed
- ✅ Skill instructions are correctly loaded
- ✅ Keyword matching triggers appropriate skills

### Manual Testing
- ✅ CLI commands (`list`, `show`, `create`, `install-builtin`)
- ✅ MCP tools integration
- ✅ Skill triggering in agent execution
- ✅ Progressive disclosure behavior
- ✅ Built-in skills functionality

## 📚 Documentation

### New Documentation Files
1. **`docs/SKILLS.md`** - Comprehensive Agent Skills guide
   - Architecture overview
   - Skill structure and creation
   - Progressive disclosure explanation
   - Built-in skills documentation
   - CLI and MCP usage examples
   - Customization guide

2. **`ai_docs/anthropic_agent_skills.md`** - Reference documentation
   - Anthropic's Agent Skills architecture reference
   - Design inspiration and patterns

### Updated Documentation
1. **`CONFIG.md`** - Added skills configuration section
2. **`NANO_CLI_USAGE.md`** - Added skills command examples
3. **`MCP_USAGE_GUIDE.md`** - Updated with skill management examples

## 🚀 Migration Guide

### For Users Upgrading from v0.4.x

**No breaking changes!** This is a backward-compatible release. Existing functionality remains unchanged.

#### New Capabilities Available Immediately

**Built-in Skills Auto-Installation**:
- Built-in skills are automatically installed to `~/.nano-cli/skills/` on first run
- No manual installation required
- Skills are available immediately after upgrade

**Using Skills**:
- Skills are automatically triggered based on your prompts
- No configuration needed for built-in skills
- Skills work in both nano-cli and nano-agent MCP server

#### Optional: Custom Skills

To create your own skills:

```bash
# Create a new skill (project-specific)
nano-cli skills create my-skill

# Create a global skill (available everywhere)
nano-cli skills create my-global-skill --global

# Edit the skill instructions
nano ~/.nano-cli/skills/my-global-skill/SKILL.md
# or
nano .nano-cli/skills/my-skill/SKILL.md
```

#### Skill Customization

Built-in skills can be customized after installation:

```bash
# Install built-in skills (creates editable copies)
nano-cli skills install-builtin

# Customize a built-in skill
nano ~/.nano-cli/skills/readme-generator/SKILL.md

# Reinstall updates (preserve customizations with --overwrite)
nano-cli skills install-builtin --overwrite
```

**Note**: Use `--overwrite` carefully; it replaces existing skill files with the latest built-in versions.

## 📈 Performance & Stability

### Performance Features
- **Progressive disclosure** minimizes context window usage
- **Caching mechanism** optimizes skill loading
- **Efficient keyword matching** for skill triggering
- **Lazy resource loading** (Level 3) avoids unnecessary context consumption

### Stability Enhancements
- Comprehensive error handling for missing or invalid skills
- Graceful degradation when skills fail to load
- Clear error messages for debugging
- Robust path resolution for various deployment scenarios

## 🎨 Example Use Cases

### 1. Automatic README Generation
```
User: Generate a README for this project

Agent: (readme-generator skill triggered)
- Analyzes project structure
- Reads configuration files
- Generates comprehensive README.md
```

### 2. Code Formatting Check
```
User: Check the formatting of my codebase

Agent: (code-formatting-checker skill triggered)
- Scans code files
- Identifies style inconsistencies
- Provides detailed formatting report
```

### 3. Release Notes Generation
```
User: Write release notes for version 0.5.0

Agent: (write-release-notes skill triggered)
- Analyzes git history
- Reads version files
- Generates professional release notes
```

### 4. Custom Skill Creation
```bash
# Create a custom skill for your workflow
nano-cli skills create database-migration

# Edit the skill with your specific instructions
nano ~/.nano-cli/skills/database-migration/SKILL.md

# Skill is automatically available in future sessions
```

## ⚙️ Technical Details

### Skill Matching Algorithm

Skills are matched to user prompts using keyword extraction:
1. Extract keywords from skill descriptions (defined in YAML frontmatter)
2. Compare user prompt with skill keywords
3. Trigger skills with matching keywords
4. Load skill instructions into context

### Skill Directory Structure

```
~/.nano-cli/skills/
├── readme-generator/
│   └── SKILL.md
├── code-formatting-checker/
│   └── SKILL.md
└── my-custom-skill/
    ├── SKILL.md
    ├── templates/
    │   └── template.txt
    └── scripts/
        └── helper.sh
```

### Built-in Skills Location

Built-in skills are packaged with the application:
```
src/nano_agent/data/builtin_skills/
├── __init__.py
├── readme-generator/
│   └── SKILL.md
├── code-formatting-checker/
│   └── SKILL.md
└── write-release-notes/
    └── SKILL.md
```

## 🔮 Coming Soon

Future enhancements to the Skills system:
- Skill marketplace and sharing
- Skill versioning and updates
- Skill dependencies and composition
- Enhanced keyword matching with ML
- Skill performance metrics
- Visual skill builder interface

## 🙏 Acknowledgments

This release implements the Agent Skills architecture inspired by Anthropic's groundbreaking work on agent capabilities. Special recognition to the Anthropic team for their innovative approach to modular agent functionality.

---

## 📦 Installation

```bash
# Install or upgrade
cd apps/nano_agent_mcp_server
uv tool install -e .

# Or for development
uv sync --extra test

# Verify version
nano-cli --version  # Should show 0.5.0

# List available skills
nano-cli skills list
```

---

## 📋 Quick Reference

### CLI Commands

| Command | Description |
|---------|-------------|
| `nano-cli skills list` | List all available skills |
| `nano-cli skills show <name>` | Show skill details |
| `nano-cli skills create <name>` | Create a new skill |
| `nano-cli skills install-builtin` | Install built-in skills |

### MCP Tools

| Tool | Description |
|------|-------------|
| `list_skills` | List all skills with metadata |
| `get_skill_info(skill_name)` | Get detailed skill information |
| `load_skill_instructions(skill_name)` | Load skill instructions |

### Built-in Skills

| Skill | Trigger Keywords | Description |
|-------|------------------|-------------|
| `readme-generator` | "readme", "generate readme" | Generates README.md files |
| `code-formatting-checker` | "format", "check formatting" | Checks code formatting |
| `write-release-notes` | "release notes", "changelog" | Generates release notes |

### Skill Locations

| Location | Scope | Purpose |
|----------|-------|---------|
| `~/.nano-cli/skills/` | Global | Available for all projects |
| `.nano-cli/skills/` | Project | Project-specific skills |
| `src/nano_agent/data/builtin_skills/` | Built-in | Packaged with nano-agent |

---

**Full Changelog**: v0.4.1...v0.5.0  
**Release Date**: November 1, 2025  
**Release Type**: Minor (New Feature)  
**Contributors**: @meirm

---

## Summary

v0.5.0 introduces the **Agent Skills system**, a powerful framework for extending nano-agent's capabilities through modular, reusable skills. With three built-in skills, comprehensive CLI and MCP integration, and progressive disclosure architecture, this release transforms nano-agent into a more capable and extensible platform.

**Key Achievements**:
- ✅ Complete Agent Skills system implementation
- ✅ Three production-ready built-in skills
- ✅ Full CLI and MCP server integration
- ✅ Progressive disclosure for optimal context usage
- ✅ Comprehensive test coverage
- ✅ Extensive documentation

**Upgrade Priority**: 🟢 **Recommended** - Major new feature with no breaking changes

