"""Tests for the AsyncPayablesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncPayablesApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.payables_api_view_model import PayablesApiViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def payables_api(async_client):
    """Create an AsyncPayablesApi instance for testing."""
    return AsyncPayablesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_payables(payables_api: AsyncPayablesApi, mock_api_client: Mock):
    """Test getting payables list."""
    expected = PayablesApiViewModel()
    mock_api_client.return_value = expected

    result = await payables_api.get_payables()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/payables"


@pytest.mark.asyncio
async def test_get_payables_with_filters(
    payables_api: AsyncPayablesApi, mock_api_client: Mock
):
    """Test getting payables with date filters."""
    expected = PayablesApiViewModel()
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    result = await payables_api.get_payables(
        description="Office Rent",
        due_date_start=start_date,
        due_date_end=end_date,
        account_status="1",
        take=10,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/payables"
    assert args["query_params"]["description"] == "Office Rent"
    assert args["query_params"]["accountStatus"] == "1"
    assert args["query_params"]["take"] == 10


@pytest.mark.asyncio
async def test_error_handling(payables_api: AsyncPayablesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await payables_api.get_payables()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
