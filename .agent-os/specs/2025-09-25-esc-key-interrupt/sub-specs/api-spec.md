# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-09-25-esc-key-interrupt/spec.md

## Key Binding API

### Escape Key Handler
```python
@kb.add('escape')
def handle_escape(event):
    """
    Handle single ESC keypress for immediate interruption.

    Purpose: Instantly interrupt current agent operation
    Parameters: event - Key event from prompt_toolkit
    Response: None (triggers interruption signal)
    Errors: None (silent operation)
    """
```

### Double Escape Handler
```python
@kb.add('escape', 'escape')
def handle_double_escape(event):
    """
    Handle double ESC keypress for history navigation.

    Purpose: Enter history navigation mode
    Parameters: event - Key event from prompt_toolkit
    Response: Opens history navigation interface
    Errors: None (fallback to single ESC if timing exceeds 500ms)
    """
```

## Interruption API

### POST /internal/interrupt
```python
def interrupt_agent_execution(session_id: str) -> dict:
    """
    Purpose: Signal interruption to running agent
    Parameters:
        - session_id: Current interactive session identifier
    Response:
        {
            "interrupted": true,
            "partial_results": "...",
            "context_preserved": true
        }
    Errors:
        - 404: No active execution found
        - 500: Interruption failed
    """
```

### GET /internal/execution-state
```python
def get_execution_state(session_id: str) -> dict:
    """
    Purpose: Check if agent execution can be interrupted
    Parameters:
        - session_id: Current interactive session identifier
    Response:
        {
            "is_running": true,
            "interruptible": true,
            "current_tool": "read_file",
            "progress": "3/5 tools completed"
        }
    Errors:
        - 404: Session not found
    """
```

## History Navigation API

### GET /internal/history
```python
def get_command_history(limit: int = 20, offset: int = 0) -> list:
    """
    Purpose: Retrieve command history for navigation
    Parameters:
        - limit: Maximum number of history items
        - offset: Starting position in history
    Response:
        [
            {
                "index": 0,
                "command": "analyze this code",
                "timestamp": "2025-09-25T10:30:00Z",
                "session_id": "abc123",
                "result_preview": "Analysis complete..."
            }
        ]
    Errors:
        - 500: History retrieval failed
    """
```

### POST /internal/history/replay
```python
def replay_history_item(index: int, edited_command: str = None) -> dict:
    """
    Purpose: Re-execute a history item, optionally with edits
    Parameters:
        - index: History item index to replay
        - edited_command: Modified command text (optional)
    Response:
        {
            "success": true,
            "original_command": "...",
            "executed_command": "...",
            "branch_created": true
        }
    Errors:
        - 404: History item not found
        - 400: Invalid command edit
    """
```

## State Management API

### InterruptibleExecution Class
```python
class InterruptibleExecution:
    """
    Wrapper for agent execution with interruption support.

    Methods:
        - start(): Begin execution with interrupt monitoring
        - interrupt(): Signal interruption
        - get_partial_results(): Retrieve results before interruption
        - resume(): Continue from interruption point
        - is_interrupted(): Check interruption status
    """
```

### ExecutionContext Class
```python
class ExecutionContext:
    """
    Maintains execution state across interruptions.

    Properties:
        - chat_history: List[ChatMessage] - Conversation history
        - partial_results: dict - Results completed before interrupt
        - interrupt_point: str - Stage where interruption occurred
        - can_resume: bool - Whether execution can be continued
    """
```

## Event System

### Interruption Events
```python
class InterruptionEvent:
    """
    Event fired when ESC interruption occurs.

    Properties:
        - timestamp: When interruption occurred
        - execution_stage: Current stage of execution
        - partial_data: Any partial results available
    """

class HistoryNavigationEvent:
    """
    Event fired when entering/exiting history mode.

    Properties:
        - action: 'enter' | 'exit' | 'select' | 'edit'
        - selected_index: Currently selected history item
        - edited_content: Modified command if edited
    """
```