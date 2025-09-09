# Spec Requirements Document

> Spec: Output Formatting Fixes
> Created: 2025-09-03
> Status: Planning

## Overview

Fix output formatting issues in nano-agent CLI to provide clean, controlled output with proper thinking text management and improved panel sizing. This addresses unwanted thinking text in simple format, inconsistent content between formats, and overly wide rich format panels.

## User Stories

### Clean Simple Format Output

As a developer using nano-agent in scripts, I want simple format output to contain only the clean agent response, so that I can easily parse and process the results without filtering out thinking markers or conversation structure.

The current simple format includes unwanted "#### user" and "#### assistant" markers along with thinking text that makes it difficult to use programmatically. The improved format should provide just the clean response content.

### Optional Thinking Text Display

As a developer debugging agent behavior, I want to optionally view the agent's thinking process and reasoning, so that I can understand how the agent arrived at its conclusions.

The thinking content should be controllable via a flag (--output-thinking) and available across all output formats when requested.

### Readable Rich Format Panels

As a user viewing agent output in the terminal, I want rich format panels to be appropriately sized, so that the content is readable without excessive white space or text spanning the full terminal width.

Current panels extend to full terminal width making short responses look awkward and harder to read.

## Spec Scope

1. **Thinking Text Control** - Add --output-thinking flag to control display of agent reasoning and conversation markers
2. **Content Cleaning** - Implement content filtering to remove thinking markers from default output
3. **Simple Format Enhancement** - Ensure simple format contains only clean agent response text, matching rich format content
4. **Rich Panel Width Control** - Add configurable panel width for better readability (--panel-width option)
5. **Format Consistency** - Ensure the same clean content appears across simple and rich formats

## Out of Scope

- Changes to the underlying agent reasoning or thinking generation
- Modifications to the OpenAI Agent SDK behavior
- Complex content parsing beyond thinking marker removal
- Interactive terminal width detection and auto-adjustment

## Expected Deliverable

1. Simple format output shows only clean agent responses by default, without thinking markers or conversation structure
2. --output-thinking flag enables viewing of complete agent output including reasoning when needed  
3. Rich format panels use appropriate width (default 80 characters) with --panel-width option for customization
4. All output formats maintain backward compatibility with current behavior when using appropriate flags

## Spec Documentation

- Tasks: @.agent-os/specs/2025-09-03-output-formatting-fixes/tasks.md
- Technical Specification: @.agent-os/specs/2025-09-03-output-formatting-fixes/sub-specs/technical-spec.md