#!/bin/bash
#
# Simple tool usage logging hook for nano-agent.
#
# This hook logs tool usage to a file for auditing and analysis.
# It's a lightweight shell script that demonstrates basic logging.
#
# Usage:
#     - Place in ~/.nano-cli/hooks/
#     - Make executable: chmod +x log_tool_usage.sh
#     - Configure in hooks.json to run on pre_tool_use, post_tool_use, or tool_error events
#     - Always returns 0 (non-blocking)

# Configuration
LOG_DIR="$HOME/.nano-cli/logs"
LOG_FILE="$LOG_DIR/tool_usage.log"
MAX_LOG_SIZE=10485760  # 10MB

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Read JSON from stdin
JSON_INPUT=$(cat)

# Extract key fields using basic parsing
# Note: For production use, consider using jq for proper JSON parsing
EVENT=$(echo "$JSON_INPUT" | grep -o '"event"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
TIMESTAMP=$(echo "$JSON_INPUT" | grep -o '"timestamp"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
TOOL_NAME=$(echo "$JSON_INPUT" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
CONTEXT=$(echo "$JSON_INPUT" | grep -o '"context"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
MODEL=$(echo "$JSON_INPUT" | grep -o '"model"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
PROVIDER=$(echo "$JSON_INPUT" | grep -o '"provider"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)

# Get file path if this is a file operation
if [[ "$TOOL_NAME" == "write_file" ]] || [[ "$TOOL_NAME" == "edit_file" ]] || [[ "$TOOL_NAME" == "read_file" ]]; then
    FILE_PATH=$(echo "$JSON_INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
fi

# Get command if this is bash_command
if [[ "$TOOL_NAME" == "bash_command" ]]; then
    COMMAND=$(echo "$JSON_INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 | head -c 100)
fi

# Format log entry
if [[ "$EVENT" == "pre_tool_use" ]]; then
    STATUS="STARTING"
elif [[ "$EVENT" == "post_tool_use" ]]; then
    STATUS="COMPLETED"
elif [[ "$EVENT" == "tool_error" ]]; then
    STATUS="FAILED"
    ERROR=$(echo "$JSON_INPUT" | grep -o '"error"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 | head -c 200)
else
    STATUS="UNKNOWN"
fi

# Build log message
LOG_MSG="[$TIMESTAMP] [$STATUS] Tool: $TOOL_NAME"

# Add context information
if [[ -n "$CONTEXT" ]]; then
    LOG_MSG="$LOG_MSG | Context: $CONTEXT"
fi

# Add model/provider if available
if [[ -n "$MODEL" ]] && [[ -n "$PROVIDER" ]]; then
    LOG_MSG="$LOG_MSG | Model: $PROVIDER/$MODEL"
fi

# Add file path for file operations
if [[ -n "$FILE_PATH" ]]; then
    LOG_MSG="$LOG_MSG | File: $FILE_PATH"
fi

# Add command preview for bash operations
if [[ -n "$COMMAND" ]]; then
    LOG_MSG="$LOG_MSG | Command: $COMMAND..."
fi

# Add error message if this is an error event
if [[ -n "$ERROR" ]]; then
    LOG_MSG="$LOG_MSG | Error: $ERROR"
fi

# Check log file size and rotate if needed
if [[ -f "$LOG_FILE" ]]; then
    LOG_SIZE=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
    if [[ $LOG_SIZE -gt $MAX_LOG_SIZE ]]; then
        # Rotate log file
        mv "$LOG_FILE" "$LOG_FILE.old"
        echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Log rotated (size exceeded $MAX_LOG_SIZE bytes)" > "$LOG_FILE"
    fi
fi

# Append to log file
echo "$LOG_MSG" >> "$LOG_FILE"

# Also log to stdout for debugging (optional)
echo "Logged: $LOG_MSG"

# Generate daily summary if it's a new day
CURRENT_DATE=$(date +%Y-%m-%d)
LAST_SUMMARY_FILE="$LOG_DIR/.last_summary_date"

if [[ ! -f "$LAST_SUMMARY_FILE" ]] || [[ "$(cat "$LAST_SUMMARY_FILE")" != "$CURRENT_DATE" ]]; then
    # Generate summary for previous day
    if [[ -f "$LOG_FILE" ]]; then
        SUMMARY_FILE="$LOG_DIR/summary_$(date -d yesterday +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d).txt"
        {
            echo "=== Tool Usage Summary ==="
            echo "Generated: $(date)"
            echo ""
            echo "Top Tools:"
            grep -o "Tool: [^|]*" "$LOG_FILE" | sort | uniq -c | sort -rn | head -10
            echo ""
            echo "Status Distribution:"
            grep -o "\[STARTING\]\|\[COMPLETED\]\|\[FAILED\]" "$LOG_FILE" | sort | uniq -c
            echo ""
            echo "Files Modified:"
            grep "write_file\|edit_file" "$LOG_FILE" | grep -o "File: [^|]*" | sort -u | head -20
        } > "$SUMMARY_FILE" 2>/dev/null || true

        echo "$CURRENT_DATE" > "$LAST_SUMMARY_FILE"
    fi
fi

# Always return success (non-blocking hook)
exit 0