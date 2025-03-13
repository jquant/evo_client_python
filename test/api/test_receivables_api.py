"""Tests for the ReceivablesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.api.receivables_api import ReceivablesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel
from evo_client.models.receivables_mask_received_view_model import (
    ReceivablesMaskReceivedViewModel,
)
from evo_client.models.revenue_center_api_view_model import RevenueCenterApiViewModel


@pytest.fixture
def receivables_api():
    """Create a ReceivablesApi instance for testing."""
    return ReceivablesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.receivables_api.ApiClient.call_api") as mock:
        yield mock


def test_get_receivables_basic(receivables_api: ReceivablesApi, mock_api_client: Mock):
    """Test getting receivables list with no parameters."""
    expected = [ReceivablesApiViewModel()]
    mock_api_client.return_value = expected

    result = receivables_api.get_receivables(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/receivables"


def test_get_receivables_with_filters(
    receivables_api: ReceivablesApi, mock_api_client: Mock
):
    """Test getting receivables with search filters."""
    expected = [ReceivablesApiViewModel()]
    mock_api_client.return_value = expected

    result = receivables_api.get_receivables(
        registration_date_start=datetime(2023, 1, 1),
        registration_date_end=datetime(2023, 12, 31),
        member_id=123,
        amount_start=100.0,
        amount_end=500.0,
        payment_types="1,2,3",
        account_status="1",
        take=10,
        skip=0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "registrationDateStart": datetime(2023, 1, 1),
        "registrationDateEnd": datetime(2023, 12, 31),
        "memberId": 123,
        "ammountStart": 100.0,
        "ammountEnd": 500.0,
        "paymentTypes": "1,2,3",
        "accountStatus": "1",
        "take": 10,
        "skip": 0,
    }


def test_get_revenue_centers(receivables_api: ReceivablesApi, mock_api_client: Mock):
    """Test getting revenue centers."""
    expected = RevenueCenterApiViewModel()
    mock_api_client.return_value = expected

    result = receivables_api.get_revenue_centers(take=10, skip=0, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/revenuecenter"
    assert args["query_params"] == {"take": 10, "skip": 0}


def test_mark_received(receivables_api: ReceivablesApi, mock_api_client: Mock):
    """Test marking receivables as received."""
    mock_api_client.return_value = None
    receivables = ReceivablesMaskReceivedViewModel()

    receivables_api.mark_received(receivables=receivables, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/receivables/mark-received"
    assert args["body"] == {}


def test_error_handling(receivables_api: ReceivablesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        receivables_api.get_receivables(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
