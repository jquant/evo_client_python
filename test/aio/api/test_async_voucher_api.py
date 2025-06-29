"""Tests for the AsyncVoucherApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncVoucherApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def voucher_api(async_client):
    """Create an AsyncVoucherApi instance for testing."""
    return AsyncVoucherApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_vouchers(voucher_api: AsyncVoucherApi, mock_api_client: Mock):
    """Test getting vouchers list."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await voucher_api.get_vouchers(take=10, skip=0)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"
    assert args["query_params"]["take"] == 10
    assert args["query_params"]["skip"] == 0


@pytest.mark.asyncio
async def test_get_vouchers_with_filters(
    voucher_api: AsyncVoucherApi, mock_api_client: Mock
):
    """Test getting vouchers with filters."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await voucher_api.get_vouchers(name="Holiday Discount", valid=True, take=5)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"
    assert args["query_params"]["name"] == "Holiday Discount"
    assert args["query_params"]["valid"] == True
    assert args["query_params"]["take"] == 5


@pytest.mark.asyncio
async def test_get_vouchers_no_params(
    voucher_api: AsyncVoucherApi, mock_api_client: Mock
):
    """Test getting vouchers without parameters."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await voucher_api.get_vouchers()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"


@pytest.mark.asyncio
async def test_error_handling(voucher_api: AsyncVoucherApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await voucher_api.get_vouchers()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
