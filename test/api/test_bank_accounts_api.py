"""Tests for the BankAccountsApi class."""

from unittest.mock import Mock, patch

import pytest


from evo_client.api.bank_accounts_api import BankAccountsApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.bank_accounts_view_model import BankAccountsViewModel


@pytest.fixture
def bank_accounts_api():
    """Create a BankAccountsApi instance for testing."""
    return BankAccountsApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.bank_accounts_api.ApiClient.call_api") as mock:
        yield mock


def test_get_accounts(bank_accounts_api: BankAccountsApi, mock_api_client: Mock):
    """Test getting bank accounts list."""
    expected = BankAccountsViewModel()
    mock_api_client.return_value = expected

    result = bank_accounts_api.get_accounts(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/bank-accounts"
    assert args["response_type"] == BankAccountsViewModel
    assert args["auth_settings"] == ["Basic"]
    assert args["_return_http_data_only"] is True
    assert args["_preload_content"] is True
    assert args["headers"] == {"Accept": "application/json"}


def test_error_handling(bank_accounts_api: BankAccountsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        bank_accounts_api.get_accounts(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
