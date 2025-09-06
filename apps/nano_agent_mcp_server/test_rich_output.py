#!/usr/bin/env python
"""Test that MCP server doesn't output Rich formatting."""

import subprocess
import json
import sys

def test_no_rich_output():
    """Test that the MCP server returns clean JSON without Rich formatting."""
    
    # Start the MCP server and send a simple request
    process = subprocess.Popen(
        ["uv", "run", "nano-agent"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send initialization request
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "0.1.0",
            "capabilities": {}
        },
        "id": 1
    }
    
    # Send tool call request
    tool_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_server_capabilities",
            "arguments": {}
        },
        "id": 2
    }
    
    try:
        # Write requests
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.write(json.dumps(tool_request) + "\n")
        process.stdin.flush()
        
        # Read responses
        responses = []
        for _ in range(2):
            line = process.stdout.readline()
            if line:
                responses.append(line)
        
        # Check for Rich formatting indicators
        rich_indicators = ["Panel", "🚀", "🔧", "✅", "bold", "cyan", "style=", "───", "│", "╭", "╮", "╰", "╯"]
        
        found_in_stdout = False
        for response in responses:
            for indicator in rich_indicators:
                if indicator in response:
                    print(f"❌ Found Rich indicator '{indicator}' in stdout")
                    found_in_stdout = True
                    break
        
        # Check stderr for Rich output (shouldn't be there either in MCP mode)
        stderr_output = process.stderr.read()
        found_in_stderr = False
        for indicator in rich_indicators:
            if indicator in stderr_output:
                print(f"⚠️  Found Rich indicator '{indicator}' in stderr")
                found_in_stderr = True
                break
        
        if not found_in_stdout and not found_in_stderr:
            print("✅ No Rich formatting detected - MCP server returns clean JSON")
            print("\nSample stdout response (first 200 chars):")
            if responses:
                print(responses[0][:200])
        else:
            print("\n❌ Rich formatting detected in MCP output")
            if found_in_stdout:
                print("Stdout responses:")
                for r in responses[:2]:
                    print(r[:500])
            if found_in_stderr:
                print("Stderr output (first 500 chars):")
                print(stderr_output[:500])
        
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_no_rich_output()