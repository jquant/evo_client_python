"""Tests for the AsyncReceivablesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncReceivablesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel
from evo_client.models.receivables_mask_received_view_model import (
    ReceivablesMaskReceivedViewModel,
)


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def receivables_api(async_client):
    """Create an AsyncReceivablesApi instance for testing."""
    return AsyncReceivablesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_receivables_basic(
    receivables_api: AsyncReceivablesApi, mock_api_client: Mock
):
    """Test getting receivables without filters."""
    expected = [ReceivablesApiViewModel()]
    mock_api_client.return_value = expected

    result = await receivables_api.get_receivables()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/receivables"


@pytest.mark.asyncio
async def test_get_receivables_with_filters(
    receivables_api: AsyncReceivablesApi, mock_api_client: Mock
):
    """Test getting receivables with various filters."""
    expected = [ReceivablesApiViewModel()]
    mock_api_client.return_value = expected

    result = await receivables_api.get_receivables(
        due_date_start=datetime(2023, 1, 1),
        due_date_end=datetime(2023, 12, 31),
        competence_date_start=datetime(2023, 1, 1),
        competence_date_end=datetime(2023, 12, 31),
        take=50,
        skip=0,
        member_id=123,
        account_status="1",
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/receivables"
    query_params = args["query_params"]
    assert query_params["take"] == 50
    assert query_params["skip"] == 0
    assert query_params["memberId"] == 123
    assert query_params["accountStatus"] == "1"


@pytest.mark.asyncio
async def test_mark_received(
    receivables_api: AsyncReceivablesApi, mock_api_client: Mock
):
    """Test marking receivables as received."""
    mock_api_client.return_value = None
    mask_data = ReceivablesMaskReceivedViewModel()

    await receivables_api.mark_received(receivables=mask_data)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/receivables/received"
    assert args["body"] == mask_data.model_dump(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_error_handling(
    receivables_api: AsyncReceivablesApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await receivables_api.get_receivables()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
