"""Tests for the AsyncStatesApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncStatesApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def states_api(async_client):
    """Create an AsyncStatesApi instance for testing."""
    return AsyncStatesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_states_basic(states_api: AsyncStatesApi, mock_api_client: Mock):
    """Test getting states."""
    expected = [{"id": 1, "name": "São Paulo", "uf": "SP"}]
    mock_api_client.return_value = expected

    result = await states_api.get_states()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/states"


@pytest.mark.asyncio
async def test_error_handling(states_api: AsyncStatesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await states_api.get_states()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
