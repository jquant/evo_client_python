"""Tests for the AsyncPartnershipApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncPartnershipApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.convenios_api_view_model import ConveniosApiViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def partnership_api(async_client):
    """Create an AsyncPartnershipApi instance for testing."""
    return AsyncPartnershipApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_partnerships(
    partnership_api: AsyncPartnershipApi, mock_api_client: Mock
):
    """Test getting partnerships list."""
    expected = [ConveniosApiViewModel()]
    mock_api_client.return_value = expected

    result = await partnership_api.get_partnerships()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/partnership"


@pytest.mark.asyncio
async def test_get_partnerships_with_filters(
    partnership_api: AsyncPartnershipApi, mock_api_client: Mock
):
    """Test getting partnerships with filters."""
    expected = [ConveniosApiViewModel()]
    mock_api_client.return_value = expected
    dt_created = datetime(2023, 1, 1)

    result = await partnership_api.get_partnerships(
        status=1, description="Health", dt_created=dt_created
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/partnership"
    assert args["query_params"]["status"] == 1
    assert args["query_params"]["description"] == "Health"
    assert args["query_params"]["dtCreated"] == dt_created


@pytest.mark.asyncio
async def test_error_handling(
    partnership_api: AsyncPartnershipApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await partnership_api.get_partnerships()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
