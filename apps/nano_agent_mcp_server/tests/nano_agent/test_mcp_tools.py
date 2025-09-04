"""Tests for MCP tools."""

import pytest
from typing import Dict, Any
import json

from nano_agent.mcp_tools import (
    get_available_models,
    list_provider_models,
    get_server_capabilities
)


class TestMCPTools:
    """Test MCP tool functions."""
    
    @pytest.mark.asyncio
    async def test_get_available_models(self):
        """Test getting available models (static)."""
        result = await get_available_models()
        
        assert result["success"] is True
        assert "providers" in result
        assert "total_models" in result
        
        # Check that we have some providers
        assert len(result["providers"]) > 0
        
        # Check provider structure
        for provider_name, provider_info in result["providers"].items():
            assert "models" in provider_info
            assert "default" in provider_info
            assert "requirements" in provider_info
            assert isinstance(provider_info["models"], list)
            assert len(provider_info["models"]) > 0
    
    @pytest.mark.asyncio
    async def test_list_provider_models_all(self):
        """Test listing models from all providers."""
        result = await list_provider_models()
        
        assert result["success"] is True
        assert "models" in result
        assert "providers" in result
        assert "total_count" in result
        assert "provider_summary" in result
        
        # Should have at least Anthropic models (hardcoded)
        assert len(result["models"]) > 0
        assert "anthropic" in result["providers"]
        
        # Check model structure
        if result["models"]:
            model = result["models"][0]
            assert "id" in model
            assert "name" in model
            assert "provider" in model
            assert "capabilities" in model
            assert "deprecated" in model
    
    @pytest.mark.asyncio
    async def test_list_provider_models_anthropic(self):
        """Test listing models from Anthropic provider."""
        result = await list_provider_models(provider="anthropic")
        
        assert result["success"] is True
        assert "models" in result
        assert len(result["models"]) > 0
        
        # All models should be from Anthropic
        for model in result["models"]:
            assert model["provider"] == "anthropic"
        
        # Check for known Anthropic models
        model_ids = [m["id"] for m in result["models"]]
        assert any("claude-3" in mid for mid in model_ids)
    
    @pytest.mark.asyncio
    async def test_list_provider_models_with_capability_filter(self):
        """Test filtering models by capability."""
        result = await list_provider_models(
            provider="anthropic",
            capability="vision"
        )
        
        if result["success"] and result["models"]:
            # All returned models should have vision capability
            for model in result["models"]:
                assert "vision" in model["capabilities"]
    
    @pytest.mark.asyncio
    async def test_list_provider_models_deprecated_filter(self):
        """Test filtering deprecated models."""
        # Without include_deprecated (default)
        result_no_deprecated = await list_provider_models(provider="anthropic")
        
        # With include_deprecated
        result_with_deprecated = await list_provider_models(
            provider="anthropic",
            include_deprecated=True
        )
        
        assert result_no_deprecated["success"] is True
        assert result_with_deprecated["success"] is True
        
        # Should have same or more models with deprecated included
        assert len(result_with_deprecated["models"]) >= len(result_no_deprecated["models"])
    
    @pytest.mark.asyncio
    async def test_list_provider_models_unknown_provider(self):
        """Test error handling for unknown provider."""
        result = await list_provider_models(provider="unknown_provider")
        
        assert result["success"] is False
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_get_server_capabilities(self):
        """Test getting server capabilities."""
        result = await get_server_capabilities()
        
        assert result["success"] is True
        assert "capabilities" in result
        
        caps = result["capabilities"]
        assert "version" in caps
        assert "features" in caps
        assert "limits" in caps
        assert "available_tools" in caps
        
        # Check features
        features = caps["features"]
        assert features["multi_provider"] is True
        assert features["session_management"] is True
        
        # Check limits
        limits = caps["limits"]
        assert "max_turns" in limits
        assert "max_tokens" in limits
        
        # Check tools
        tools = caps["available_tools"]
        assert "read_file" in tools
        assert "write_file" in tools