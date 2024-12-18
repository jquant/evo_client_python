"""Tests for the PayablesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest



from evo_client.api.payables_api import PayablesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.cost_center_api_view_model import CostCenterApiViewModel
from evo_client.models.payables_api_view_model import PayablesApiViewModel


@pytest.fixture
def payables_api():
    """Create a PayablesApi instance for testing."""
    return PayablesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.payables_api.ApiClient.call_api") as mock:
        yield mock


def test_get_cost_centers_basic(payables_api: PayablesApi, mock_api_client: Mock):
    """Test getting cost centers list with no parameters."""
    expected = CostCenterApiViewModel()
    mock_api_client.return_value = expected

    await result = await payables_api.get_cost_centers(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/costcenter"


def test_get_cost_centers_with_pagination(
    payables_api: PayablesApi, mock_api_client: Mock
):
    """Test getting cost centers with pagination."""
    expected = CostCenterApiViewModel()
    mock_api_client.return_value = expected

    await result = await payables_api.get_cost_centers(take=10, skip=0, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {"take": 10, "skip": 0}


def test_get_payables_basic(payables_api: PayablesApi, mock_api_client: Mock):
    """Test getting payables list with no parameters."""
    expected = PayablesApiViewModel()
    mock_api_client.return_value = expected

    await result = await payables_api.get_payables(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/payables"


def test_get_payables_with_filters(payables_api: PayablesApi, mock_api_client: Mock):
    """Test getting payables with search filters."""
    expected = PayablesApiViewModel()
    mock_api_client.return_value = expected

    result = payables_api.get_payables(
        description="Test Payment",
        date_input_start=datetime(2023, 1, 1),
        date_input_end=datetime(2023, 12, 31),
        due_date_start=datetime(2023, 1, 1),
        due_date_end=datetime(2023, 12, 31),
        amount_start=100.0,
        amount_end=500.0,
        account_status="1",
        take=10,
        skip=0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "description": "Test Payment",
        "dateInputStart": datetime(2023, 1, 1),
        "dateInputEnd": datetime(2023, 12, 31),
        "dueDateStart": datetime(2023, 1, 1),
        "dueDateEnd": datetime(2023, 12, 31),
        "amountStart": 100.0,
        "amountEnd": 500.0,
        "accountStatus": "1",
        "take": 10,
        "skip": 0,
    }


def test_error_handling(payables_api: PayablesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await payables_api.get_payables(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
