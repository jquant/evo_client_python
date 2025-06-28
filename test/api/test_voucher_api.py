"""Tests for the SyncVoucherApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncVoucherApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def voucher_api(sync_client):
    """Create a SyncVoucherApi instance for testing."""
    return SyncVoucherApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_vouchers(voucher_api: SyncVoucherApi, mock_api_client: Mock):
    """Test getting vouchers list."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = voucher_api.get_vouchers(take=10, skip=0)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"
    assert args["query_params"]["take"] == 10
    assert args["query_params"]["skip"] == 0


def test_get_vouchers_with_filters(voucher_api: SyncVoucherApi, mock_api_client: Mock):
    """Test getting vouchers with filters."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = voucher_api.get_vouchers(name="Holiday Discount", valid=True, take=5)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"
    assert args["query_params"]["name"] == "Holiday Discount"
    assert args["query_params"]["valid"] == True
    assert args["query_params"]["take"] == 5


def test_get_vouchers_no_params(voucher_api: SyncVoucherApi, mock_api_client: Mock):
    """Test getting vouchers without parameters."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = voucher_api.get_vouchers()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"


def test_error_handling(voucher_api: SyncVoucherApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        voucher_api.get_vouchers()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
