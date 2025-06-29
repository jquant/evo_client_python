"""Tests for the SyncBankAccountsApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncBankAccountsApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.bank_accounts_view_model import BankAccountsViewModel


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def bank_accounts_api(sync_client):
    """Create a SyncBankAccountsApi instance for testing."""
    return SyncBankAccountsApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_accounts_basic(
    bank_accounts_api: SyncBankAccountsApi, mock_api_client: Mock
):
    """Test getting bank accounts."""
    expected = BankAccountsViewModel()
    mock_api_client.return_value = expected

    result = bank_accounts_api.get_accounts()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/bank-accounts"


def test_error_handling(bank_accounts_api: SyncBankAccountsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        bank_accounts_api.get_accounts()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
