"""Tests for the AsyncInvoicesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncInvoicesApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.enotas_retorno import EnotasRetorno


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def invoices_api(async_client):
    """Create an AsyncInvoicesApi instance for testing."""
    return AsyncInvoicesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_invoices(invoices_api: AsyncInvoicesApi, mock_api_client: Mock):
    """Test getting invoices list."""
    expected = EnotasRetorno()
    mock_api_client.return_value = expected

    result = await invoices_api.get_invoices(take=10, skip=0)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/invoices/get-invoices"
    assert args["query_params"]["take"] == 10
    assert args["query_params"]["skip"] == 0


@pytest.mark.asyncio
async def test_get_invoices_with_filters(
    invoices_api: AsyncInvoicesApi, mock_api_client: Mock
):
    """Test getting invoices with date filters."""
    expected = EnotasRetorno()
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    result = await invoices_api.get_invoices(
        issue_date_start=start_date, issue_date_end=end_date, take=5
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/invoices/get-invoices"
    assert args["query_params"]["take"] == 5


@pytest.mark.asyncio
async def test_get_invoices_no_params(invoices_api: AsyncInvoicesApi, mock_api_client: Mock):
    """Test getting invoices without parameters."""
    expected = EnotasRetorno()
    mock_api_client.return_value = expected

    result = await invoices_api.get_invoices()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/invoices/get-invoices"


@pytest.mark.asyncio
async def test_error_handling(invoices_api: AsyncInvoicesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await invoices_api.get_invoices()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
