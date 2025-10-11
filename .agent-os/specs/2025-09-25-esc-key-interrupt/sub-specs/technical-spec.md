# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-25-esc-key-interrupt/spec.md

## Technical Requirements

### Key Event Handling
- Implement low-level key event capture using prompt_toolkit's key binding system
- Create custom key handler for ESC key detection with immediate response
- Implement double-tap detection with 500ms timeout window
- Ensure key events are captured at all stages of agent execution

### Interruption Mechanism
- Add cancellation token/signal to agent execution pipeline
- Implement async cancellation for OpenAI SDK agent operations
- Create interrupt handler that cleanly stops current tool execution
- Preserve partial results and conversation state in interrupted operations

### History Navigation Interface
- Build interactive history browser using prompt_toolkit's full-screen application
- Implement arrow key navigation (↑/↓) for history browsing
- Add inline editing capability for selected history items
- Create visual distinction between original and edited prompts
- Support ESC to exit history mode and return to normal prompt

### State Management
- Maintain execution state object with cancellable flag
- Store partial results from interrupted operations
- Preserve ChatMessage history during interruptions
- Implement state recovery for continuation after interrupt

### Visual Feedback
- Display brief "[Interrupted]" message on ESC press
- Show history navigation mode indicator when double-ESC activated
- Highlight currently selected history item during navigation
- Indicate edit mode when modifying historical prompts

## UI/UX Specifications

### Single ESC Behavior
- Immediate interruption without confirmation
- Brief status message: "[Interrupted by user]" in dim text
- Instant return to prompt with preserved context
- No modal dialogs or additional user interaction required

### Double ESC Behavior
- Enter history navigation mode within 500ms double-tap window
- Display last 20 commands in scrollable list
- Show timestamp and preview of each command
- Allow selection with arrow keys and editing with Enter
- Exit with ESC or execute edited command with Ctrl+Enter

## Integration Requirements

### prompt_toolkit Integration
- Utilize prompt_toolkit.key_binding for ESC key capture
- Integrate with existing CompleterProvider and history system
- Maintain compatibility with current autocomplete functionality
- Preserve existing keyboard shortcuts and navigation

### Agent Execution Integration
- Modify _execute_nano_agent to accept cancellation token
- Add interrupt checking at each tool execution boundary
- Implement graceful shutdown of OpenAI SDK agent on interrupt
- Ensure proper cleanup of resources on cancellation

### Session State Integration
- Extend InteractiveSession class with interrupt handling
- Maintain chat_history integrity during interruptions
- Update session metadata with interrupt information
- Support continuation prompts after interruption

## Performance Criteria

- ESC key response time: < 50ms from keypress to interruption
- History navigation load time: < 100ms for 1000 items
- Double-tap detection accuracy: > 99% with 500ms window
- Zero data loss during interruption of operations
- Memory overhead for interrupt handling: < 1MB