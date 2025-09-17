#!/bin/bash
#
# Bell notification hook for nano-agent on macOS
#
# This hook plays a sound when the agent completes its task.
# It only runs in CLI mode and uses macOS native commands.
#
# Usage:
#     - Place in ~/.nano-cli/hooks/
#     - Make executable: chmod +x bell_notification.sh
#     - Configure in hooks.json for post_agent_complete event with contexts: ["cli"]

# Configuration - You can customize these
SOUND_FILE="/System/Library/Sounds/Glass.aiff"  # Options: Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink
ENABLE_NOTIFICATION=false  # Set to true to also show a macOS notification
PLAY_DIFFERENT_ON_ERROR=true  # Use different sound for errors
ERROR_SOUND="/System/Library/Sounds/Basso.aiff"

# Read JSON from stdin
JSON_INPUT=$(cat)

# Extract key fields using basic parsing
EVENT=$(echo "$JSON_INPUT" | grep -o '"event"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
CONTEXT=$(echo "$JSON_INPUT" | grep -o '"context"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
ERROR=$(echo "$JSON_INPUT" | grep -o '"error"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
PROMPT=$(echo "$JSON_INPUT" | grep -o '"prompt"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 | head -c 50)
EXECUTION_TIME=$(echo "$JSON_INPUT" | grep -o '"execution_time"[[:space:]]*:[[:space:]]*[0-9.]*' | cut -d':' -f2 | tr -d ' ')

# Only run in CLI context
if [ "$CONTEXT" != "cli" ]; then
    echo "Skipping bell notification (context: $CONTEXT)"
    exit 0
fi

# Determine which sound to play
if [ -n "$ERROR" ] && [ "$PLAY_DIFFERENT_ON_ERROR" = true ]; then
    # Error occurred - play error sound
    SOUND_TO_PLAY="$ERROR_SOUND"
    NOTIFICATION_TITLE="❌ Nano Agent Error"
    NOTIFICATION_MESSAGE="Task failed after ${EXECUTION_TIME}s"
else
    # Success - play normal sound
    SOUND_TO_PLAY="$SOUND_FILE"
    NOTIFICATION_TITLE="✅ Nano Agent Complete"
    NOTIFICATION_MESSAGE="Task completed in ${EXECUTION_TIME}s"
fi

# Play the sound using afplay (macOS command)
if [ -f "$SOUND_TO_PLAY" ]; then
    afplay "$SOUND_TO_PLAY" 2>/dev/null &
    echo "Played notification sound: $(basename "$SOUND_TO_PLAY")"
else
    # Fallback to terminal bell if sound file not found
    printf "\a"
    echo "Played terminal bell (sound file not found)"
fi

# Optionally show a macOS notification
if [ "$ENABLE_NOTIFICATION" = true ]; then
    # Truncate prompt for notification
    if [ -n "$PROMPT" ]; then
        NOTIFICATION_SUBTITLE="\"${PROMPT}...\""
    else
        NOTIFICATION_SUBTITLE="Agent task"
    fi

    # Use osascript to show notification
    osascript -e "display notification \"$NOTIFICATION_MESSAGE\" with title \"$NOTIFICATION_TITLE\" subtitle $NOTIFICATION_SUBTITLE sound name \"$(basename "$SOUND_TO_PLAY" .aiff)\"" 2>/dev/null &
fi

# Always return success (non-blocking hook)
exit 0