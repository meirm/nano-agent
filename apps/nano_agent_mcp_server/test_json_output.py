#!/usr/bin/env python
"""Test that nano-agent MCP server returns pure JSON without Rich formatting."""

import asyncio
import json

from mcp_client_sdk import Client, stdio_transport


async def test_json_output():
    """Test that MCP server returns JSON without Rich formatting."""

    # Create MCP client with stdio transport
    transport = stdio_transport("uv", "run", "nano-agent")

    try:
        async with transport:
            client = Client(transport)
            await client.initialize()

            # Test a simple prompt that would normally trigger Rich output
            print("Testing prompt_nano_agent with simple task...")
            result = await client.call_tool(
                "prompt_nano_agent",
                {
                    "agentic_prompt": "Create a file called test.txt with 'Hello World' content",
                    "model": "gpt-oss:20b",
                    "provider": "ollama",
                },
            )

            # Check the result is JSON-serializable
            try:
                json_str = json.dumps(result, indent=2)
                print("✅ Result is valid JSON (no Rich formatting detected)")
                print(f"Sample output (first 500 chars):\n{json_str[:500]}...")

                # Check for any Rich-specific strings that shouldn't be there
                rich_indicators = ["Panel", "🚀", "🔧", "✅", "bold", "cyan", "style="]
                found_indicators = [ind for ind in rich_indicators if ind in json_str]

                if found_indicators:
                    print(
                        f"⚠️ Warning: Found potential Rich indicators: {found_indicators}"
                    )
                else:
                    print("✅ No Rich formatting indicators found in output")

            except (TypeError, ValueError) as e:
                print(f"❌ Result is not JSON-serializable: {e}")
                print(f"Result type: {type(result)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_json_output())
