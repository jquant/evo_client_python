"""Tests for the SyncPayablesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.payables_api_view_model import PayablesApiViewModel
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncPayablesApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def payables_api(sync_client):
    """Create a SyncPayablesApi instance for testing."""
    return SyncPayablesApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_payables(payables_api: SyncPayablesApi, mock_api_client: Mock):
    """Test getting payables list."""
    expected = PayablesApiViewModel()
    mock_api_client.return_value = expected

    result = payables_api.get_payables()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/payables"


def test_get_payables_with_filters(
    payables_api: SyncPayablesApi, mock_api_client: Mock
):
    """Test getting payables with date filters."""
    expected = PayablesApiViewModel()
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    result = payables_api.get_payables(
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


def test_error_handling(payables_api: SyncPayablesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        payables_api.get_payables()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
