#!/usr/bin/env python
"""Nano Agent MCP Server - Main entry point."""

import logging
import os

from mcp.server.fastmcp import FastMCP

# Apply typing fixes FIRST before any other imports that might use OpenAI SDK

# Set up logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variable to indicate we're running as MCP server
os.environ["NANO_AGENT_MCP_MODE"] = "true"

from .mcp_tools import (clear_old_sessions, get_available_models,
                        get_server_capabilities, get_session_info,
                        list_provider_models, list_sessions)
from .mcp_resources import get_documentation, get_version
from .mcp_prompts import (code_review_prompt, refactor_prompt, test_generation_prompt,
                         documentation_prompt, security_audit_prompt, api_design_prompt,
                         bug_fix_prompt, code_migration_prompt, performance_optimization_prompt,
                         project_setup_prompt)
# Import our nano agent tools and additional MCP tools
from .modules.nano_agent import prompt_nano_agent, prompt_nano_agent_readonly

# Logging already set up above

# Create the MCP server instance
mcp = FastMCP(
    name="nano-agent",
    instructions="""
    A powerful MCP server that bridges Model Context Protocol with OpenAI's Agent SDK.
    
    This server enables autonomous agent execution through natural language prompts,
    allowing clients to describe work in plain English and have it completed by
    an AI agent with access to file system tools.
    
    Features:
    - Multi-provider LLM support (OpenAI, Anthropic, Ollama)
    - Conversation persistence across sessions
    - Fine-grained tool and path permissions
    - Read-only mode for safe exploration
    - Hooks system for customization
    - Temperature and token limit control
    
    Main tools:
    - prompt_nano_agent: Execute autonomous agent with full configuration options
    - prompt_nano_agent_readonly: Execute agent in safe read-only mode (no file modifications)
    - get_session_info: Get information about a specific session
    - list_sessions: List all sessions for the client
    - clear_old_sessions: Clean up old session data
    - get_available_models: List available models and providers (static)
    - list_provider_models: Query providers for current model lists with details
    - get_server_capabilities: Get server features and limitations
    - get_documentation: Get documentation for the nano agent
    """,
)

# Register all tools
mcp.tool()(prompt_nano_agent)
mcp.tool()(prompt_nano_agent_readonly)
mcp.tool()(get_session_info)
mcp.tool()(list_sessions)
mcp.tool()(clear_old_sessions)
mcp.tool()(get_available_models)
mcp.tool()(list_provider_models)
mcp.tool()(get_server_capabilities)

# Register resources using decorator pattern
@mcp.resource("resource://documentation")
def documentation_resource() -> str:
    """Get server documentation."""
    return get_documentation()

@mcp.resource("resource://version")
def version_resource() -> str:
    """Get important server notices."""
    return get_version()

# Register prompts
mcp.prompt()(code_review_prompt)
mcp.prompt()(refactor_prompt)
mcp.prompt()(test_generation_prompt)
mcp.prompt()(documentation_prompt)
mcp.prompt()(security_audit_prompt)
mcp.prompt()(api_design_prompt)
mcp.prompt()(bug_fix_prompt)
mcp.prompt()(code_migration_prompt)
mcp.prompt()(performance_optimization_prompt)
mcp.prompt()(project_setup_prompt)

def run():
    """Entry point for the nano-agent command."""
    try:
        logger.info("Starting Nano Agent MCP Server...")
        # FastMCP.run() handles its own async context with anyio
        # Don't wrap it in asyncio.run()
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    run()
