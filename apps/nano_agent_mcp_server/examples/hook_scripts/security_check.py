#!/usr/bin/env python3
"""
Security check hook for nano-agent.

This hook validates file operations to prevent potentially dangerous actions.
It runs before write_file and edit_file operations and can block execution.

Usage:
    - Place in ~/.nano-cli/hooks/
    - Configure in hooks.json to run on pre_tool_use events
    - Returns exit code 0 to allow, non-zero to block
"""

import json
import os
import sys
from pathlib import Path


def main():
    """Main security check logic."""
    try:
        # Read event data from stdin
        input_data = sys.stdin.read()
        event_data = json.loads(input_data)

        # Extract relevant information
        tool_name = event_data.get("tool_name", "")
        tool_args = event_data.get("tool_args", {})

        # Only check file operations
        if tool_name not in ["write_file", "edit_file"]:
            return 0

        file_path = tool_args.get("file_path", "")
        if not file_path:
            return 0

        # Convert to Path object for analysis
        path = Path(file_path).resolve()

        # Security checks
        blocked_patterns = [
            # System files
            "/etc/passwd",
            "/etc/shadow",
            "/etc/sudoers",
            "/.ssh/",
            "/.gnupg/",

            # Environment and config files
            ".env",
            ".bashrc",
            ".zshrc",
            ".profile",

            # Git credentials
            ".git/config",
            ".gitconfig",
            ".git-credentials",

            # Cloud credentials
            ".aws/credentials",
            ".azure/",
            ".gcloud/",

            # API keys and tokens
            "api_key",
            "secret_key",
            "private_key",
            ".pem",
            ".key",
            ".cert",

            # Database files
            ".db",
            ".sqlite",
            ".mysql",

            # Sensitive directories
            "/System/",
            "/Library/Keychains/",
            "/private/var/",
        ]

        path_str = str(path).lower()

        # Check against blocked patterns
        for pattern in blocked_patterns:
            if pattern.lower() in path_str:
                print(f"BLOCKED: Attempt to modify potentially sensitive file: {file_path}", file=sys.stderr)
                print(f"Matched pattern: {pattern}", file=sys.stderr)
                return 1  # Block execution

        # Check for directory traversal attempts
        if "../" in file_path or "/.." in file_path:
            print(f"BLOCKED: Potential directory traversal attempt: {file_path}", file=sys.stderr)
            return 1

        # Check file size for edit operations (prevent editing huge files)
        if tool_name == "edit_file" and path.exists():
            max_size = 10 * 1024 * 1024  # 10MB
            if path.stat().st_size > max_size:
                print(f"BLOCKED: File too large to edit safely: {path.stat().st_size} bytes", file=sys.stderr)
                return 1

        # Additional checks for write_file
        if tool_name == "write_file":
            content = tool_args.get("content", "")

            # Check for potential script injection
            dangerous_patterns = [
                "eval(",
                "exec(",
                "__import__",
                "subprocess",
                "os.system",
                "shell=True",
                "; rm ",
                "&& rm ",
                "| rm ",
                "base64 -d",
                "curl | sh",
                "wget -O- |",
            ]

            content_lower = content.lower()
            for pattern in dangerous_patterns:
                if pattern.lower() in content_lower:
                    print(f"BLOCKED: Potentially dangerous content pattern detected: {pattern}", file=sys.stderr)
                    return 1

        # Log allowed operation
        print(f"ALLOWED: {tool_name} on {file_path}", file=sys.stdout)
        return 0

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON input: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Security check failed: {e}", file=sys.stderr)
        # In case of error, block by default for safety
        return 1


if __name__ == "__main__":
    sys.exit(main())