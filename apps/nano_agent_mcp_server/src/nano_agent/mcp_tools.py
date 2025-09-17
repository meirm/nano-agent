"""
Additional MCP tools for session and configuration management.
"""

import logging
from typing import Any, Dict, Optional

from .modules.constants import AVAILABLE_MODELS, PROVIDER_REQUIREMENTS
from .modules.mcp_session_manager import MCPSessionManager
from .modules.model_providers import ProviderRegistry
from .modules.provider_implementations import initialize_providers

logger = logging.getLogger(__name__)


async def get_session_info(session_id: str, ctx: Any = None) -> Dict[str, Any]:
    """
    Get information about a specific session.

    Args:
        session_id: The session ID to get information for
        ctx: MCP context (automatically injected)

    Returns:
        Dictionary containing session information
    """
    if not ctx:
        return {
            "success": False,
            "error": "Session management only available in MCP context",
        }

    try:
        client_id = (
            getattr(ctx, "client_id", None)
            or getattr(ctx, "client_name", None)
            or "mcp-client"
        )
        session_manager = MCPSessionManager()

        session_info = await session_manager.get_session_info(
            client_id=client_id, session_id=session_id
        )

        if session_info:
            return {"success": True, "session_info": session_info}
        else:
            return {"success": False, "error": f"Session '{session_id}' not found"}

    except Exception as e:
        return {"success": False, "error": f"Error getting session info: {str(e)}"}


async def list_sessions(limit: int = 10, ctx: Any = None) -> Dict[str, Any]:
    """
    List all sessions for the current client.

    Args:
        limit: Maximum number of sessions to return (default: 10)
        ctx: MCP context (automatically injected)

    Returns:
        Dictionary containing list of sessions
    """
    if not ctx:
        return {
            "success": False,
            "error": "Session management only available in MCP context",
        }

    try:
        client_id = (
            getattr(ctx, "client_id", None)
            or getattr(ctx, "client_name", None)
            or "mcp-client"
        )
        session_manager = MCPSessionManager()

        sessions = await session_manager.list_client_sessions(
            client_id=client_id, limit=limit
        )

        return {"success": True, "sessions": sessions, "count": len(sessions)}

    except Exception as e:
        return {"success": False, "error": f"Error listing sessions: {str(e)}"}


async def clear_old_sessions(days: int = 30, ctx: Any = None) -> Dict[str, Any]:
    """
    Clear old sessions older than specified days.

    Args:
        days: Number of days to keep sessions (default: 30)
        ctx: MCP context (automatically injected)

    Returns:
        Dictionary containing operation result
    """
    if not ctx:
        return {
            "success": False,
            "error": "Session management only available in MCP context",
        }

    try:
        session_manager = MCPSessionManager()
        await session_manager.clear_old_sessions(days=days)

        return {"success": True, "message": f"Cleared sessions older than {days} days"}

    except Exception as e:
        return {"success": False, "error": f"Error clearing sessions: {str(e)}"}


async def get_available_models() -> Dict[str, Any]:
    """
    Get list of available models and providers (from static configuration).

    Returns:
        Dictionary containing available models by provider
    """
    try:
        models_by_provider = {}

        for provider, models in AVAILABLE_MODELS.items():
            if provider in PROVIDER_REQUIREMENTS:
                # Handle both list and dict formats
                if isinstance(models, list):
                    model_list = models
                    default_model = models[0] if models else None
                else:
                    # If it's a dict (old format)
                    model_list = list(models.keys())
                    default_model = next(iter(models.keys())) if models else None

                models_by_provider[provider] = {
                    "models": model_list,
                    "default": default_model,
                    "requirements": PROVIDER_REQUIREMENTS[provider],
                }

        return {
            "success": True,
            "providers": models_by_provider,
            "total_models": sum(
                len(info["models"]) for info in models_by_provider.values()
            ),
        }

    except Exception as e:
        return {"success": False, "error": f"Error getting available models: {str(e)}"}


async def get_server_capabilities() -> Dict[str, Any]:
    """
    Get server capabilities and limitations.

    Returns:
        Dictionary containing server capabilities
    """
    try:
        from .modules.constants import MAX_AGENT_TURNS, MAX_TOKENS, VERSION

        return {
            "success": True,
            "capabilities": {
                "version": VERSION,
                "features": {
                    "multi_provider": True,
                    "session_management": True,
                    "tool_restrictions": True,
                    "path_restrictions": True,
                    "conversation_history": True,
                    "hooks_system": True,
                    "read_only_mode": True,
                },
                "limits": {
                    "max_turns": MAX_AGENT_TURNS,
                    "max_tokens": MAX_TOKENS,
                    "session_history": 100,  # messages
                    "max_file_size": 10485760,  # 10MB
                    "timeout_seconds": 600,
                },
                "available_tools": [
                    "prompt_nano_agent",
                    "prompt_nano_agent_readonly",
                    "get_session_info",
                    "list_sessions",
                    "clear_old_sessions",
                    "get_available_models",
                    "list_provider_models",
                    "get_server_capabilities",
                ],
                "agent_internal_tools": [
                    "read_file",
                    "write_file",
                    "list_directory",
                    "get_file_info",
                    "edit_file",
                    "grep_search",
                    "search_files",
                    "bash_command",
                ],
                "available_resources": [
                    {
                        "uri": "resource://documentation",
                        "name": "Server Documentation",
                        "description": "Complete usage guide for the Nano Agent MCP server",
                    },
                    {
                        "uri": "resource://version",
                        "name": "Server version",
                        "description": "Server version",
                    },
                ],
                "hook_events": [
                    {
                        "event": "pre_agent_start",
                        "description": "Before agent initialization",
                        "blocking": True,
                        "data_available": ["prompt", "model", "provider", "temperature", "max_tokens"],
                    },
                    {
                        "event": "post_agent_complete",
                        "description": "After agent completes successfully",
                        "blocking": False,
                        "data_available": ["prompt", "agent_response", "token_usage", "execution_time"],
                    },
                    {
                        "event": "agent_error",
                        "description": "When agent encounters an error",
                        "blocking": False,
                        "data_available": ["prompt", "error", "execution_time"],
                    },
                    {
                        "event": "pre_tool_use",
                        "description": "Before any tool execution",
                        "blocking": True,
                        "data_available": ["tool_name", "tool_args"],
                    },
                    {
                        "event": "post_tool_use",
                        "description": "After successful tool execution",
                        "blocking": False,
                        "data_available": ["tool_name", "tool_args", "tool_result"],
                    },
                    {
                        "event": "tool_error",
                        "description": "When tool execution fails",
                        "blocking": False,
                        "data_available": ["tool_name", "tool_args", "error"],
                    },
                    {
                        "event": "mcp_request_received",
                        "description": "When MCP request arrives",
                        "blocking": True,
                        "data_available": ["prompt", "mcp_client", "mcp_request_id"],
                    },
                    {
                        "event": "mcp_response_ready",
                        "description": "Before sending MCP response",
                        "blocking": False,
                        "data_available": ["agent_response", "token_usage", "mcp_client", "mcp_request_id"],
                    },
                ],
                "available_prompts": [
                    {
                        "name": "code_review_prompt",
                        "description": "Generate prompt for comprehensive code review",
                        "parameters": ["file_path", "focus_areas (optional)"],
                    },
                    {
                        "name": "refactor_prompt",
                        "description": "Generate prompt for code refactoring",
                        "parameters": ["file_path", "refactor_goals (optional)"],
                    },
                    {
                        "name": "test_generation_prompt",
                        "description": "Generate prompt for creating unit tests",
                        "parameters": ["file_path", "test_framework", "coverage_target"],
                    },
                    {
                        "name": "documentation_prompt",
                        "description": "Generate prompt for creating documentation",
                        "parameters": ["directory", "doc_type", "include_examples"],
                    },
                    {
                        "name": "security_audit_prompt",
                        "description": "Generate prompt for security analysis",
                        "parameters": ["directory", "security_focus (optional)"],
                    },
                    {
                        "name": "api_design_prompt",
                        "description": "Generate prompt for API design",
                        "parameters": ["spec_type", "resource_name", "operations (optional)"],
                    },
                    {
                        "name": "bug_fix_prompt",
                        "description": "Generate prompt for debugging and fixing errors",
                        "parameters": ["error_message", "file_path (optional)", "context (optional)"],
                    },
                    {
                        "name": "code_migration_prompt",
                        "description": "Generate prompt for code migration between versions",
                        "parameters": ["source_version", "target_version", "file_or_directory"],
                    },
                    {
                        "name": "performance_optimization_prompt",
                        "description": "Generate prompt for performance optimization",
                        "parameters": ["file_path", "performance_targets (optional)"],
                    },
                    {
                        "name": "project_setup_prompt",
                        "description": "Generate prompt for setting up a new project",
                        "parameters": ["project_name", "project_type", "features (optional)"],
                    },
                ],
            },
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting server capabilities: {str(e)}",
        }


async def list_provider_models(
    provider: Optional[str] = None,
    include_deprecated: bool = False,
    capability: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List available models from AI providers with detailed information.

    This tool queries AI providers to get the list of available models
    with their capabilities, context lengths, and other metadata.

    Args:
        provider: Optional provider name to filter models (e.g., 'openai', 'anthropic', 'ollama', 'lmstudio')
        include_deprecated: Whether to include deprecated models (default: False)
        capability: Optional capability to filter by (e.g., 'chat', 'vision', 'function_calling')

    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - models: List of model information dictionaries
        - providers: List of available providers
        - error: Error message if operation failed
    """
    try:
        # Initialize providers
        initialize_providers()

        # Get registry instance
        registry = ProviderRegistry()

        # Fetch models based on provider parameter
        if provider:
            # List models from specific provider
            models = await registry.list_provider_models(provider)
        else:
            # List models from all providers
            models = await registry.list_all_models()

        # Filter by capability if specified
        if capability:
            models = [m for m in models if capability in m.capabilities]

        # Filter out deprecated models unless requested
        if not include_deprecated:
            models = [m for m in models if not m.deprecated]

        # Convert models to dictionaries
        model_dicts = []
        for model in models:
            model_dict = {
                "id": model.id,
                "name": model.name,
                "provider": model.provider,
                "context_length": model.context_length,
                "max_output_tokens": model.max_output_tokens,
                "capabilities": model.capabilities,
                "deprecated": model.deprecated,
            }

            # Add optional fields if present
            if model.input_cost_per_1k is not None:
                model_dict["input_cost_per_1k"] = model.input_cost_per_1k
            if model.output_cost_per_1k is not None:
                model_dict["output_cost_per_1k"] = model.output_cost_per_1k
            if model.replacement_model:
                model_dict["replacement_model"] = model.replacement_model
            if model.description:
                model_dict["description"] = model.description

            model_dicts.append(model_dict)

        # Get list of available providers
        available_providers = registry.list_provider_names()

        # Create summary by provider
        provider_summary = {}
        for m in models:
            if m.provider not in provider_summary:
                provider_summary[m.provider] = 0
            provider_summary[m.provider] += 1

        return {
            "success": True,
            "models": model_dicts,
            "total_count": len(model_dicts),
            "providers": available_providers,
            "provider_summary": provider_summary,
        }

    except Exception as e:
        logger.error(f"Error listing provider models: {str(e)}")

        # Handle specific error types
        from .modules.model_providers import (ProviderAuthenticationError,
                                              ProviderConnectionError,
                                              ProviderNotFoundError)

        if isinstance(e, ProviderNotFoundError):
            error_msg = f"Provider '{e.provider_name}' not found. Available providers: openai, anthropic, ollama, lmstudio"
        elif isinstance(e, ProviderConnectionError):
            error_msg = f"Could not connect to provider: {str(e)}"
        elif isinstance(e, ProviderAuthenticationError):
            error_msg = f"Authentication failed: {str(e)}"
        else:
            error_msg = str(e)

        return {"success": False, "error": error_msg, "models": [], "providers": []}
