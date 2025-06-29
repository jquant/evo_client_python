"""Tests for the AsyncEntriesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncEntriesApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.entradas_resumo_api_view_model import EntradasResumoApiViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def entries_api(async_client):
    """Create an AsyncEntriesApi instance for testing."""
    return AsyncEntriesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_entries_basic(entries_api: AsyncEntriesApi, mock_api_client: Mock):
    """Test getting entries without filters."""
    expected = [EntradasResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await entries_api.get_entries()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/entries"


@pytest.mark.asyncio
async def test_get_entries_with_filters(entries_api: AsyncEntriesApi, mock_api_client: Mock):
    """Test getting entries with various filters."""
    expected = [EntradasResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await entries_api.get_entries(
        register_date_start=datetime(2023, 1, 1),
        register_date_end=datetime(2023, 12, 31),
        take=50,
        skip=0,
        entry_id=123,
        member_id=456,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/entries"
    query_params = args["query_params"]
    assert query_params["take"] == 50
    assert query_params["skip"] == 0
    assert query_params["IdEntry"] == 123
    assert query_params["idMember"] == 456


@pytest.mark.asyncio
async def test_error_handling(entries_api: AsyncEntriesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await entries_api.get_entries()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
