# Plan: Command Evaluation with Inline Shell Execution

## Metadata
adw_id: `eval-command-syntax`
prompt: `I want to be able to eval commands prompt. That means that if the command markdown file has $\`command\`, we will run the command and replace the placeholder with the output of the command. for instance if the command has a line like this:
date: $\`date "%YMD"\`
we will run the command and replace it inline with the output of it.\
date: 20251023

task_type: enhancement
complexity: medium

## Task Description
Add shell command evaluation capability to the command loader system. This will allow command markdown files to include dynamic content by executing shell commands using the syntax `$\`command\`` and replacing the placeholder with the command's output inline.

## Objective
Enable command markdown files to dynamically include shell command output using the `$\`command\`` syntax, which will be evaluated and replaced with the actual output when the command is loaded or executed.

## Problem Statement
Currently, command markdown files are static templates that can only include `$ARGUMENTS` placeholders. There's no way to dynamically generate content within commands using shell commands, which limits flexibility for use cases like timestamps, environment information, or dynamic file listings.

## Solution Approach
1. Extend the `CommandLoader` class in `command_loader.py` to detect and evaluate `$\`command\`` patterns
2. Use the `bash_command` tool or subprocess to execute shell commands safely
3. Replace the `$\`command\`` patterns with their output inline during command execution
4. Handle errors gracefully if commands fail
5. Add security considerations for command execution

## Relevant Files
Use these files to complete the task:

- `apps/nano_agent_mcp_server/src/nano_agent/modules/command_loader.py` - Main file to modify; contains `CommandLoader` class with `execute_command()` method that needs enhancement
- `apps/nano_agent_mcp_server/src/nano_agent/modules/nano_agent_tools.py` - Contains `bash_command_raw()` function for safe shell execution
- `apps/nano_agent_mcp_server/src/nano_agent/cli.py` - Uses CommandLoader to parse and execute commands; may need updates for error handling

### New Files
- `apps/nano_agent_mcp_server/tests/nano_agent/modules/test_command_eval.py` - Test file for command evaluation functionality

## Implementation Phases

### Phase 1: Foundation
- Study existing command loading and execution flow
- Identify security considerations for shell execution
- Design the regex pattern for detecting `$\`command\`` syntax
- Plan error handling strategy

### Phase 2: Core Implementation
- Add command evaluation logic to `CommandLoader.execute_command()`
- Implement pattern detection using regex
- Integrate with `bash_command_raw()` for execution
- Handle command output and replacement
- Add error handling for failed commands

### Phase 3: Integration & Polish
- Add comprehensive tests
- Update documentation with examples
- Handle edge cases (nested backticks, escaped patterns, multiline commands)
- Add configuration option to enable/disable command evaluation for security

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Research and Design
- Read `command_loader.py` to understand current implementation
- Read `nano_agent_tools.py` to understand `bash_command_raw()`
- Design regex pattern for `$\`command\`` detection
- Document security considerations and mitigations

### 2. Implement Command Evaluation Function
- Create `_evaluate_shell_commands()` method in `CommandLoader` class
- Use regex to find all `$\`command\`` patterns
- Extract shell commands from backticks
- Execute each command using `bash_command_raw()`
- Replace patterns with command output
- Handle errors gracefully (return error message or leave placeholder)

### 3. Integrate into Command Execution
- Modify `execute_command()` method to call `_evaluate_shell_commands()`
- Ensure evaluation happens after `$ARGUMENTS` substitution
- Handle escaped patterns (e.g., `\$\`command\``)
- Test with simple command examples

### 4. Add Security and Configuration
- Add `enable_command_eval` option to CommandLoader constructor
- Add environment variable `NANO_CLI_ENABLE_COMMAND_EVAL` check
- Document security implications in docstrings
- Consider command timeout for long-running commands

### 5. Edge Cases and Error Handling
- Handle commands that return empty output
- Handle commands that fail (non-zero exit code)
- Handle nested or malformed backticks
- Handle multiline command output formatting
- Test with various command types (date, ls, env vars, etc.)

### 6. Write Comprehensive Tests
- Create test file with unit tests for `_evaluate_shell_commands()`
- Test successful command execution
- Test failed command execution
- Test escaped patterns
- Test nested and edge cases
- Test security features (disabled by default)

### 7. Update Documentation
- Add examples to `command_loader.py` docstrings
- Create example command file demonstrating the feature
- Update COMMANDS.md with usage examples
- Add security notes about command evaluation

### 8. Validation and Integration Testing
- Test with real command files
- Verify error messages are clear
- Ensure no breaking changes to existing functionality
- Test performance with multiple evaluations

## Testing Strategy
- Unit tests for regex pattern matching
- Unit tests for command execution and replacement
- Integration tests with actual command files
- Error handling tests for failed commands
- Security tests for disabled/enabled modes
- Edge case tests for malformed syntax

## Acceptance Criteria
- `$\`command\`` syntax is detected and evaluated in command files
- Shell commands execute successfully and output replaces placeholder
- Failed commands are handled gracefully with clear error messages
- Feature can be disabled for security via configuration
- Escaped patterns (e.g., `\$\`command\``) are not evaluated
- Existing command functionality remains unchanged
- Comprehensive tests pass
- Documentation includes clear examples and security notes

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run pytest apps/nano_agent_mcp_server/tests/nano_agent/modules/test_command_eval.py -v` - Run new tests for command evaluation
- `uv run pytest apps/nano_agent_mcp_server/tests/nano_agent/modules/test_command_cascade.py -v` - Ensure existing tests still pass
- `uv run nano-cli commands list` - Verify command system still works
- Create test command file with `date: $\`date "+%Y%m%d"\`` and run it to verify inline evaluation
- `uv run nano-cli -p '/test_command "test"'` - Test command evaluation with actual nano-cli execution

## Notes
**Security Considerations**:
- Command evaluation should be **disabled by default** for security
- Require explicit opt-in via environment variable or configuration
- Consider command timeout to prevent infinite loops
- Commands execute in the same environment as nano-cli process
- No input validation beyond what bash provides

**Implementation Details**:
- Use `bash_command_raw()` from `nano_agent_tools.py` for consistency
- Regex pattern should be: `\$\`([^`]+)\``
- Handle escaping: `\$\`command\`` should not be evaluated
- Preserve formatting: if command output is multiline, consider how to format
- Consider caching command results for repeated patterns

**Edge Cases to Handle**:
- Empty command output
- Multiline output
- Commands with errors
- Nested backticks in output
- Special characters in output
- Very long output (consider truncation)

**Example Use Cases**:
```markdown
# Example Command File
date: $\`date "+%Y-%m-%d %H:%M:%S"\`
hostname: $\`hostname\`
user: $\`whoami\`
directory: $\`pwd\`

Perform task: $ARGUMENTS
Current time is: $\`date "+%H:%M"\`
```
