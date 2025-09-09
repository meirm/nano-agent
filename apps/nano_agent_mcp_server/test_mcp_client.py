#!/usr/bin/env python
"""
Simple MCP client to test the nano-agent MCP server.

This client connects to the MCP server and tests various tools.
"""

import asyncio
import json
import sys
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def extract_content(result) -> Dict[str, Any]:
    """Extract the actual content from an MCP tool call result."""
    content = result.content

    # Handle list of content items
    if hasattr(content, "__iter__") and not isinstance(content, (str, dict)):
        content = content[0] if len(content) > 0 else {}

    # Handle TextContent objects
    if hasattr(content, "text"):
        try:
            content = (
                json.loads(content.text)
                if isinstance(content.text, str)
                else content.text
            )
        except json.JSONDecodeError:
            content = {"text": content.text}

    return content


async def test_mcp_server():
    """Test the nano-agent MCP server with various tool calls."""

    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="uv", args=["run", "nano-agent"], env=None
    )

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            init_result = await session.initialize()

            print("Connected to MCP server!")
            print(
                f"Server name: {init_result.server_name if hasattr(init_result, 'server_name') else 'Unknown'}"
            )
            print(
                f"Protocol version: {init_result.protocol_version if hasattr(init_result, 'protocol_version') else 'Unknown'}"
            )
            print("\n" + "=" * 60 + "\n")

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(
                    f"  - {tool.name}: {tool.description[:100] if tool.description else 'No description'}..."
                )
            print("\n" + "=" * 60 + "\n")

            # Test 1: Get server capabilities
            print("Test 1: Getting server capabilities...")
            result = await session.call_tool("get_server_capabilities", arguments={})
            content = extract_content(result)
            print(f"Result: {json.dumps(content, indent=2)[:500]}...")
            print("\n" + "=" * 60 + "\n")

            # Test 2: List available models (static)
            print("Test 2: Getting available models (static)...")
            result = await session.call_tool("get_available_models", arguments={})
            content = extract_content(result)
            print(f"Result: {json.dumps(content, indent=2)[:500]}...")
            print("\n" + "=" * 60 + "\n")

            # Test 3: List provider models (dynamic)
            print("Test 3: Listing provider models (dynamic)...")
            result = await session.call_tool(
                "list_provider_models",
                arguments={"provider": "anthropic", "include_deprecated": False},
            )
            content = extract_content(result)
            print(f"Result: {json.dumps(content, indent=2)[:500]}...")
            print("\n" + "=" * 60 + "\n")

            # Test 4: List all provider models
            print("Test 4: Listing all provider models...")
            result = await session.call_tool("list_provider_models", arguments={})
            content = extract_content(result)

            if isinstance(content, dict):
                print(f"Total models: {content.get('total_count', 'N/A')}")
                print(f"Providers: {', '.join(content.get('providers', []))}")
                print(f"Provider summary: {content.get('provider_summary', {})}")
            else:
                print(f"Result: {json.dumps(content, indent=2)[:500]}...")
            print("\n" + "=" * 60 + "\n")

            # Test 5: Test error handling
            print("Test 5: Testing error handling (unknown provider)...")
            result = await session.call_tool(
                "list_provider_models", arguments={"provider": "nonexistent"}
            )
            content = extract_content(result)
            print(f"Result: {json.dumps(content, indent=2)[:300]}...")
            print("\n" + "=" * 60 + "\n")

            print("✅ All tests completed!")


async def test_prompt_agent():
    """Test the prompt_nano_agent tool with a simple task."""

    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="uv", args=["run", "nano-agent"], env=None
    )

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            init_result = await session.initialize()

            print("Connected to MCP server for agent test!")
            print("\n" + "=" * 60 + "\n")

            # Test prompt_nano_agent
            print("Testing prompt_nano_agent tool...")
            print("Task: Create a simple test file")

            result = await session.call_tool(
                "prompt_nano_agent",
                arguments={
                    "agentic_prompt": "Create a file named 'mcp_test.txt' with the content 'Hello from MCP client test!'",
                    "model": "gpt-5-mini",
                    "provider": "openai",
                },
            )

            content = extract_content(result)
            print(f"Result: {json.dumps(content, indent=2)[:1000]}...")

            # Check if file was created
            import os

            if os.path.exists("mcp_test.txt"):
                with open("mcp_test.txt", "r") as f:
                    print(f"\n✅ File created successfully! Content: {f.read()}")
                os.remove("mcp_test.txt")
                print("🧹 Test file cleaned up")
            else:
                print("\n⚠️ File was not created")


async def main():
    """Main function to run tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Test the nano-agent MCP server")
    parser.add_argument(
        "--test",
        choices=["tools", "agent", "all"],
        default="tools",
        help="Which tests to run",
    )

    args = parser.parse_args()

    try:
        if args.test in ["tools", "all"]:
            print("🧪 Testing MCP server tools...\n")
            await test_mcp_server()

        if args.test in ["agent", "all"]:
            print("\n🤖 Testing agent execution...\n")
            await test_prompt_agent()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
