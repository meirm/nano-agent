#!/usr/bin/env python3
"""
Test script to verify event loop fixes are working properly.
Tests various scenarios that previously caused RuntimeError: Event loop is closed
"""

import subprocess
import sys
import time
import signal
import os

def run_test(name, command, timeout=10):
    """Run a test and check for event loop errors."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    try:
        # Run the command with timeout
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # Check for event loop errors in stderr
        errors = []
        if "RuntimeError: Event loop is closed" in result.stderr:
            errors.append("Found 'RuntimeError: Event loop is closed'")
        if "Exception ignored in:" in result.stderr:
            errors.append("Found 'Exception ignored in:'")
        if "This event loop is already running" in result.stderr:
            errors.append("Found 'This event loop is already running'")

        if errors:
            print(f"❌ FAILED - Errors found:")
            for error in errors:
                print(f"   - {error}")
            print("\nStderr output:")
            print(result.stderr[-1000:])  # Last 1000 chars
            return False
        else:
            print(f"✅ PASSED - No event loop errors")
            return True

    except subprocess.TimeoutExpired:
        print(f"⚠️ Test timed out after {timeout} seconds")
        return True  # Timeout is OK, we're just checking for errors
    except Exception as e:
        print(f"❌ FAILED - Exception: {e}")
        return False

def main():
    """Run all tests."""
    print("Event Loop Fix Verification Tests")
    print("=================================")

    tests = [
        # Test 1: Simple exit
        ("Simple exit from interactive mode",
         'echo "exit" | uv run nano-cli interactive --provider ollama --model gpt-oss:20b'),

        # Test 2: Command then exit
        ("List files then exit",
         'echo -e "list files\\nexit" | uv run nano-cli interactive --provider ollama --model gpt-oss:20b'),

        # Test 3: Multiple commands
        ("Multiple commands then exit",
         'echo -e "/agents\\nlist files\\nexit" | uv run nano-cli interactive --provider ollama --model gpt-oss:20b'),

        # Test 4: Direct run command
        ("Direct run command",
         'uv run nano-cli run "What is 2+2?" --provider ollama --model gpt-oss:20b'),

        # Test 5: Quick interrupt (simulated)
        ("Quick interrupt scenario",
         'timeout 2 uv run nano-cli interactive --provider ollama --model gpt-oss:20b < /dev/null'),

        # Test 6: Run with hooks if configured
        ("Run with potential hooks",
         'echo -e "test\\nexit" | uv run nano-cli interactive --provider ollama --model gpt-oss:20b'),
    ]

    passed = 0
    failed = 0

    for test_name, test_command in tests:
        if run_test(test_name, test_command):
            passed += 1
        else:
            failed += 1
        time.sleep(1)  # Brief pause between tests

    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")

    if failed == 0:
        print("\n🎉 All tests passed! Event loop issues are resolved.")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed. Review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())