"""Tests for the SyncReceivablesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncReceivablesApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel
from evo_client.models.receivables_mask_received_view_model import (
    ReceivablesMaskReceivedViewModel,
)


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def receivables_api(sync_client):
    """Create a SyncReceivablesApi instance for testing."""
    return SyncReceivablesApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_receivables_basic(
    receivables_api: SyncReceivablesApi, mock_api_client: Mock
):
    """Test getting receivables without filters."""
    expected = [ReceivablesApiViewModel()]
    mock_api_client.return_value = expected

    result = receivables_api.get_receivables()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/receivables"


def test_get_receivables_with_filters(
    receivables_api: SyncReceivablesApi, mock_api_client: Mock
):
    """Test getting receivables with various filters."""
    expected = [ReceivablesApiViewModel()]
    mock_api_client.return_value = expected

    result = receivables_api.get_receivables(
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


def test_mark_received(receivables_api: SyncReceivablesApi, mock_api_client: Mock):
    """Test marking receivables as received."""
    mock_api_client.return_value = None
    mask_data = ReceivablesMaskReceivedViewModel()

    receivables_api.mark_received(receivables=mask_data)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/receivables/received"
    assert args["body"] == mask_data.model_dump(exclude_unset=True, by_alias=True)


def test_error_handling(receivables_api: SyncReceivablesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        receivables_api.get_receivables()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
