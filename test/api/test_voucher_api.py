"""Tests for the VoucherApi class."""

from unittest.mock import Mock, patch

import pytest


from evo_client.api.voucher_api import VoucherApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel


@pytest.fixture
def voucher_api():
    """Create a VoucherApi instance for testing."""
    return VoucherApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.voucher_api.ApiClient.call_api") as mock:
        yield mock


def test_get_vouchers_basic(voucher_api: VoucherApi, mock_api_client: Mock):
    """Test getting vouchers list with no parameters."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = voucher_api.get_vouchers(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher"


def test_get_vouchers_with_filters(voucher_api: VoucherApi, mock_api_client: Mock):
    """Test getting vouchers with search filters."""
    expected = [VouchersResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = voucher_api.get_vouchers(
        voucher_id=123,
        name="SALE10",
        branch_id=456,
        take=10,
        skip=0,
        valid=True,
        voucher_type=1,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "idVoucher": 123,
        "name": "SALE10",
        "idBranch": 456,
        "take": 10,
        "skip": 0,
        "valid": True,
        "type": 1,
    }


def test_get_voucher_details(voucher_api: VoucherApi, mock_api_client: Mock):
    """Test getting voucher details."""
    expected = {"id": 123, "name": "SALE10"}
    mock_api_client.return_value = expected

    result = voucher_api.get_voucher_details(voucher_id=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/voucher/123"


def test_create_voucher(voucher_api: VoucherApi, mock_api_client: Mock):
    """Test creating a voucher."""
    expected = {"id": 123, "name": "SALE10"}
    mock_api_client.return_value = expected

    result = voucher_api.create_voucher(
        name="SALE10",
        discount_type=1,
        discount_value=10.0,
        valid_from="2023-01-01",
        valid_until="2023-12-31",
        branch_id=456,
        usage_limit=100,
        min_value=50.0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/voucher"
    assert args["body"] == {
        "name": "SALE10",
        "discountType": 1,
        "discountValue": 10.0,
        "validFrom": "2023-01-01",
        "validUntil": "2023-12-31",
        "branchId": 456,
        "usageLimit": 100,
        "minValue": 50.0,
    }


def test_error_handling(voucher_api: VoucherApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await voucher_api.get_vouchers(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
