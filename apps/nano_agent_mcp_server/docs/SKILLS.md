# Agent Skills

> Agent Skills are modular capabilities that extend nano-agent's functionality. Each Skill packages instructions, metadata, and optional resources (scripts, templates) that the agent uses automatically when relevant.

## Why use Skills

Skills are reusable, filesystem-based resources that provide nano-agent with domain-specific expertise: workflows, context, and best practices that transform general-purpose agents into specialists. Unlike prompts (conversation-level instructions for one-off tasks), Skills load on-demand and eliminate the need to repeatedly provide the same guidance across multiple conversations.

**Key benefits**:

* **Specialize nano-agent**: Tailor capabilities for domain-specific tasks
* **Reduce repetition**: Create once, use automatically
* **Compose capabilities**: Combine Skills to build complex workflows
* **Progressive disclosure**: Only relevant content consumes context tokens

## How Skills work

Skills leverage nano-agent's filesystem access to provide capabilities beyond what's possible with prompts alone. Skills exist as directories containing instructions, executable code, and reference materials, organized like an onboarding guide you'd create for a new team member.

This filesystem-based architecture enables **progressive disclosure**: nano-agent loads information in stages as needed, rather than consuming context upfront.

### Three types of Skill content, three levels of loading

Skills can contain three types of content, each loaded at different times:

### Level 1: Metadata (always loaded)

**Content type: Instructions**. The Skill's YAML frontmatter provides discovery information:

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

nano-agent loads this metadata at startup and includes it in the system prompt. This lightweight approach means you can install many Skills without context penalty; nano-agent only knows each Skill exists and when to use it.

### Level 2: Instructions (loaded when triggered)

**Content type: Instructions**. The main body of SKILL.md contains procedural knowledge: workflows, best practices, and guidance:

````markdown
# PDF Processing

## Quick start

Use pdfplumber to extract text from PDFs:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For advanced form filling, see [FORMS.md](FORMS.md).
````

When you request something that matches a Skill's description, nano-agent reads SKILL.md from the filesystem. Only then does this content enter the context window.

### Level 3: Resources and code (loaded as needed)

**Content types: Instructions, code, and resources**. Skills can bundle additional materials:

```
pdf-skill/
├── SKILL.md (main instructions)
├── FORMS.md (form-filling guide)
├── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (utility script)
```

**Instructions**: Additional markdown files (FORMS.md, REFERENCE.md) containing specialized guidance and workflows

**Code**: Executable scripts (fill_form.py, validate.py) that nano-agent runs via bash_command; scripts provide deterministic operations without consuming context

**Resources**: Reference materials like database schemas, API documentation, templates, or examples

nano-agent accesses these files only when referenced. The filesystem model means each content type has different strengths: instructions for flexible guidance, code for reliability, resources for factual lookup.

| Level                     | When Loaded             | Token Cost             | Content                                                               |
| ------------------------- | ----------------------- | ---------------------- | --------------------------------------------------------------------- |
| **Level 1: Metadata**     | Always (at startup)     | ~100 tokens per Skill  | `name` and `description` from YAML frontmatter                        |
| **Level 2: Instructions** | When Skill is triggered | Under 5k tokens        | SKILL.md body with instructions and guidance                              |
| **Level 3+: Resources**   | As needed               | Effectively unlimited  | Bundled files executed via bash_command without loading contents into context |

Progressive disclosure ensures only relevant content occupies the context window at any given time.

## Where Skills work

Skills are available across nano-agent's interfaces:

### MCP Server

The nano-agent MCP server supports Skills through the SkillLoader module. Skills are automatically discovered and used when relevant to user prompts.

**MCP Tools**:
- `list_skills`: List all available Skills with metadata
- `get_skill_info(skill_name)`: Get full skill information including instructions
- `load_skill_instructions(skill_name)`: Load full SKILL.md content

### CLI (nano-cli)

The nano-cli command-line interface provides full Skills management.

**CLI Commands**:
- `nano-cli skills list`: List all available Skills
- `nano-cli skills show <name>`: Show detailed skill information
- `nano-cli skills create <name>`: Create a new skill template

## Skill structure

Every Skill requires a directory with a `SKILL.md` file containing YAML frontmatter:

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for nano-agent to follow]

## Examples
[Concrete examples of using this Skill]
```

**Required fields**: `name` and `description`

**Field requirements**:

`name`:
* Maximum 64 characters
* Must contain only lowercase letters, numbers, and hyphens
* Cannot contain XML tags
* Cannot contain reserved words: "anthropic", "claude"

`description`:
* Must be non-empty
* Maximum 1024 characters
* Cannot contain XML tags
* Should include keywords that help match the skill to user prompts

The `description` should include both what the Skill does and when nano-agent should use it. Include relevant keywords to improve skill matching accuracy.

## Skill locations

Skills can be placed in two locations (with cascade system):

1. **Global Skills**: `~/.nano-cli/skills/` - Available to all projects
2. **Project Skills**: `.nano-cli/skills/` - Project-specific, override global skills

Project skills with the same name override global skills, allowing project-specific customizations.

## Creating a Skill

### Quick start

```bash
# Create a new skill template
nano-cli skills create my-skill

# Or create a global skill
nano-cli skills create my-skill --global
```

This creates a skill directory with a SKILL.md template:

```
.nano-cli/skills/my-skill/
└── SKILL.md
```

### Example: PDF Processing Skill

```markdown
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Instructions

Use pdfplumber to extract text from PDFs:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### Extracting Tables

For tables, use:

```python
with pdfplumber.open("document.pdf") as pdf:
    table = pdf.pages[0].extract_table()
```

### Form Filling

For advanced form filling, see the [FORMS.md](FORMS.md) guide in this skill directory.

## Examples

- "Extract all text from this PDF"
- "Get the table data from page 2"
- "Fill out the form in this PDF document"
```

### Adding Resources

Skills can include additional files for reference or execution:

```
my-skill/
├── SKILL.md
├── FORMS.md (form-filling guide)
├── REFERENCE.md (API reference)
└── scripts/
    ├── extract_text.py
    └── validate.py
```

The agent can access these resources using the `bash_command` tool:

```bash
# Read a resource file
cat .nano-cli/skills/my-skill/FORMS.md

# Execute a script
python .nano-cli/skills/my-skill/scripts/extract_text.py document.pdf
```

## How Skills are triggered

Skills are automatically triggered when the user's prompt matches the skill's description using keyword matching. The matching algorithm:

1. Compares words in the user prompt with words in the skill description
2. Requires at least 2 matching words or key phrases
3. Ranks skills by match relevance (more matches = higher priority)

When a skill is triggered:
1. Level 2 instructions (SKILL.md content) are loaded into the prompt context
2. The agent can access Level 3 resources on-demand using bash commands
3. Multiple skills can be triggered for a single prompt if relevant

## Security considerations

We strongly recommend using Skills only from trusted sources: those you created yourself or obtained from trusted repositories. Skills provide nano-agent with new capabilities through instructions and code, and while this makes them powerful, it also means a malicious Skill can direct nano-agent to invoke tools or execute code in ways that don't match the Skill's stated purpose.

**Key security considerations**:

* **Audit thoroughly**: Review all files bundled in the Skill: SKILL.md, scripts, images, and other resources. Look for unusual patterns like unexpected network calls, file access patterns, or operations that don't match the Skill's stated purpose
* **External sources are risky**: Skills that fetch data from external URLs pose particular risk, as fetched content may contain malicious instructions
* **Tool misuse**: Malicious Skills can invoke tools (file operations, bash commands, code execution) in harmful ways
* **Data exposure**: Skills with access to sensitive data could be designed to leak information to external systems
* **Treat like installing software**: Only use Skills from trusted sources. Be especially careful when integrating Skills into production systems with access to sensitive data or critical operations

## Best practices

### Writing effective descriptions

The skill description is crucial for matching. Include:
- What the skill does (action verbs)
- When to use it (trigger keywords)
- Relevant domain terms

**Good example**:
```
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad example**:
```
description: PDF stuff
```

### Organizing skill content

- Keep SKILL.md focused on core instructions
- Use additional files for detailed references (Level 3 resources)
- Include examples in SKILL.md to guide the agent
- Reference external resources with clear file paths

### Progressive disclosure

- Start with quick-start examples in SKILL.md
- Move advanced usage to separate resource files
- Keep SKILL.md under 5k tokens when possible
- Use scripts for deterministic operations

## Example Skills

### 1. Code Review Skill

```markdown
---
name: code-review
description: Review code for bugs, security issues, and best practices. Use when the user asks to review, audit, or analyze code quality.
---

# Code Review

## Instructions

When reviewing code, check for:

1. **Security vulnerabilities**: SQL injection, XSS, authentication issues
2. **Bugs**: Logic errors, edge cases, null pointer exceptions
3. **Best practices**: Code style, error handling, documentation
4. **Performance**: Inefficient algorithms, unnecessary loops

Provide specific, actionable feedback with line numbers and examples.
```

### 2. Documentation Generator Skill

```markdown
---
name: documentation-generator
description: Generate documentation for code, APIs, or projects. Use when the user asks to create documentation, write docs, or document code.
---

# Documentation Generator

## Instructions

Generate clear, comprehensive documentation:

1. **For code**: Include function signatures, parameters, return values, examples
2. **For APIs**: Include endpoints, request/response formats, authentication
3. **For projects**: Include setup instructions, architecture overview, usage examples

Use markdown format with proper headings, code blocks, and examples.
```

## Built-in Skills

nano-agent comes with built-in skills that are automatically installed and ready to use:

### Available Built-in Skills

#### 1. README Generator
**Purpose**: Automatically generate comprehensive README.md files for projects

**Trigger keywords**: "readme", "generate readme", "create readme", "documentation", "project readme", "write readme"

**Features**:
- Analyzes project structure to determine type (Python, Node.js, Rust, Go, etc.)
- Extracts metadata from configuration files (package.json, setup.py, Cargo.toml, etc.)
- Identifies dependencies and requirements
- Generates installation instructions based on detected package manager
- Creates usage examples from actual code patterns
- Includes relevant sections (features, configuration, contributing, license)

**Usage**:
```bash
# Via CLI
nano-cli -p "Generate a README for this project"

# Or in interactive mode
nano-agent> Generate a comprehensive README file
```

#### 2. Code Formatting Checker
**Purpose**: Detect code formatting issues and style inconsistencies

**Trigger keywords**: "format check", "code style", "formatting", "linting", "code formatting", "check formatting", "format issues"

**Features**:
- Language-agnostic checks (trailing whitespace, line endings, indentation)
- Language-specific formatting rules (Python PEP 8, JavaScript/TypeScript conventions, etc.)
- Integrates with formatters (black, prettier, cargo fmt, gofmt) if available
- Generates detailed reports with file:line:issue format
- Prioritizes issues by impact (critical, high, medium, low)

**Usage**:
```bash
# Via CLI
nano-cli -p "Check code formatting in this project"

# Check specific directory
nano-cli -p "Find formatting issues in src/"
```

### Installing Built-in Skills

Built-in skills are **automatically installed** when you first use nano-agent. They're copied to `~/.nano-cli/skills/` from the package.

You can also manually install them:

```bash
# Install all built-in skills
nano-cli skills install-builtin

# Install a specific skill
nano-cli skills install-builtin --skill readme-generator

# Overwrite existing built-in skills
nano-cli skills install-builtin --overwrite
```

### Customizing Built-in Skills

Built-in skills can be customized like any other skill:

1. Skills are installed to `~/.nano-cli/skills/`
2. Edit the SKILL.md file directly to customize instructions
3. Your customizations persist across updates (skills won't be overwritten unless you use `--overwrite`)

Example:
```bash
# Edit the README Generator skill
nano-cli skills show readme-generator
# Then manually edit: ~/.nano-cli/skills/readme-generator/SKILL.md
```

### Built-in Skills vs Custom Skills

- **Built-in Skills**: Pre-configured, professionally written, automatically available
- **Custom Skills**: Your own domain-specific expertise and workflows

Both work the same way - built-in skills are just skills that come with the package!

## Next steps

* Use `nano-cli skills list` to see available Skills
* Use `nano-cli skills install-builtin` to install built-in skills
* Use `nano-cli skills create <name>` to create your first custom Skill
* Review existing Skills with `nano-cli skills show <name>`
* Create Skills that package your organization's best practices and workflows

