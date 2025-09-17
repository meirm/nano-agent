#!/usr/bin/env python3
"""
Prompt filter hook for nano-agent.

This hook can filter, validate, or enhance user prompts before they are processed.
It can block inappropriate prompts or add context to improve agent responses.

Usage:
    - Place in ~/.nano-cli/hooks/
    - Configure in hooks.json to run on pre_agent_start or user_prompt_submit events
    - Returns exit code 0 to allow (with optional modifications), non-zero to block
"""

import json
import os
import re
import sys
from datetime import datetime


def main():
    """Main prompt filtering logic."""
    try:
        # Read event data from stdin
        input_data = sys.stdin.read()
        event_data = json.loads(input_data)

        # Extract prompt
        prompt = event_data.get("prompt", "")
        if not prompt:
            return 0  # No prompt to filter

        # Get context information
        model = event_data.get("model", "unknown")
        provider = event_data.get("provider", "unknown")
        context = event_data.get("context", "cli")

        # 1. Content filtering - block inappropriate requests
        blocked_keywords = [
            "hack",
            "crack",
            "exploit",
            "malware",
            "virus",
            "trojan",
            "ransomware",
            "ddos",
            "phishing",
            "steal credentials",
            "bypass security",
            "disable antivirus",
        ]

        prompt_lower = prompt.lower()
        for keyword in blocked_keywords:
            if keyword in prompt_lower:
                print(f"BLOCKED: Prompt contains inappropriate content: '{keyword}'", file=sys.stderr)
                return 1  # Block execution

        # 2. Rate limiting check (example - would need persistent storage in production)
        # This is a simple example; in production, you'd track requests per time window
        if context == "mcp":
            # MCP requests might need stricter rate limiting
            max_prompt_length = 5000
        else:
            max_prompt_length = 10000

        if len(prompt) > max_prompt_length:
            print(f"BLOCKED: Prompt exceeds maximum length ({len(prompt)} > {max_prompt_length})", file=sys.stderr)
            return 1

        # 3. Prompt enhancement (optional - uncomment to enable)
        # You could modify the prompt here to add context or instructions
        # enhanced_prompt = enhance_prompt(prompt, model, provider)

        # 4. Validation checks
        # Check for potential prompt injection attempts
        injection_patterns = [
            r"ignore (all )?previous instructions",
            r"forget (everything|all)",
            r"disregard (the )?(above|previous)",
            r"new instructions:",
            r"system: ",
            r"</system>",
            r"<system>",
        ]

        for pattern in injection_patterns:
            if re.search(pattern, prompt_lower):
                print(f"WARNING: Potential prompt injection detected: '{pattern}'", file=sys.stderr)
                # You might want to block or sanitize here
                # return 1

        # 5. Log the prompt for auditing (optional)
        log_prompt(prompt, event_data)

        # 6. Check for resource-intensive requests
        resource_intensive_keywords = [
            "analyze entire codebase",
            "process all files",
            "scan everything",
            "review all code",
            "check every file",
        ]

        for keyword in resource_intensive_keywords:
            if keyword in prompt_lower:
                print(f"WARNING: Resource-intensive request detected: '{keyword}'", file=sys.stdout)
                # You might want to add token limits or warnings
                # Could modify event_data here to reduce max_tokens

        # Allow the prompt to proceed
        print(f"ALLOWED: Prompt validated ({len(prompt)} characters)", file=sys.stdout)
        return 0

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON input: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Prompt filter failed: {e}", file=sys.stderr)
        # In case of error, block by default for safety
        return 1


def enhance_prompt(prompt, model, provider):
    """
    Enhance the prompt with additional context or instructions.

    This is optional and can be customized based on your needs.
    """
    # Example: Add model-specific instructions
    if "gpt" in model.lower():
        enhanced = f"{prompt}\n\nPlease provide clear, step-by-step explanations."
    elif "claude" in model.lower():
        enhanced = f"{prompt}\n\nBe concise and focus on accuracy."
    else:
        enhanced = prompt

    # Example: Add timestamp context
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    enhanced = f"[Timestamp: {timestamp}]\n{enhanced}"

    return enhanced


def log_prompt(prompt, event_data):
    """
    Log prompts for auditing purposes.

    In production, this would write to a proper logging system.
    """
    log_dir = os.path.expanduser("~/.nano-cli/logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "prompts.log")
    timestamp = event_data.get("timestamp", datetime.now().isoformat())

    # Create a sanitized log entry
    log_entry = {
        "timestamp": timestamp,
        "context": event_data.get("context", "unknown"),
        "model": event_data.get("model", "unknown"),
        "provider": event_data.get("provider", "unknown"),
        "prompt_length": len(prompt),
        "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
    }

    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        # Don't fail the hook if logging fails
        print(f"WARNING: Failed to log prompt: {e}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())