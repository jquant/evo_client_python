"""Tests for the AsyncBaseApi class."""

from unittest.mock import AsyncMock, Mock

import pytest

from evo_client.aio.api.base import AsyncBaseApi
from evo_client.aio.core.api_client import AsyncApiClient


@pytest.fixture
def async_api_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.mark.asyncio
async def test_async_base_api_initialization_with_client(async_api_client):
    """Test initializing AsyncBaseApi with provided client."""
    api = AsyncBaseApi(async_api_client)
    assert api.api_client == async_api_client


@pytest.mark.asyncio
async def test_async_base_api_initialization_without_client():
    """Test initializing AsyncBaseApi without provided client."""
    api = AsyncBaseApi()
    assert api.api_client is not None
    assert isinstance(api.api_client, AsyncApiClient)


@pytest.mark.asyncio
async def test_async_base_api_context_manager_with_aenter_aexit():
    """Test async context manager when api_client has __aenter__ and __aexit__."""
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock()

    api = AsyncBaseApi(mock_client)

    async with api as context_api:
        assert context_api == api
        mock_client.__aenter__.assert_called_once()

    mock_client.__aexit__.assert_called_once()


@pytest.mark.asyncio
async def test_async_base_api_context_manager_without_aenter_aexit():
    """Test async context manager when api_client doesn't have __aenter__ and __aexit__."""
    mock_client = Mock()
    # Remove __aenter__ and __aexit__ methods
    if hasattr(mock_client, "__aenter__"):
        delattr(mock_client, "__aenter__")
    if hasattr(mock_client, "__aexit__"):
        delattr(mock_client, "__aexit__")

    api = AsyncBaseApi(mock_client)

    # Should not raise an error
    async with api as context_api:
        assert context_api == api


@pytest.mark.asyncio
async def test_async_base_api_context_manager_integration():
    """Test full async context manager integration."""
    api = AsyncBaseApi()

    # Should work without errors
    async with api as context_api:
        assert context_api == api
        assert context_api.api_client is not None
