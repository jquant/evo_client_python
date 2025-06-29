"""Tests for the AsyncBankAccountsApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncBankAccountsApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.bank_accounts_view_model import BankAccountsViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def bank_accounts_api(async_client):
    """Create an AsyncBankAccountsApi instance for testing."""
    return AsyncBankAccountsApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_accounts_basic(
    bank_accounts_api: AsyncBankAccountsApi, mock_api_client: Mock
):
    """Test getting bank accounts."""
    expected = BankAccountsViewModel()
    mock_api_client.return_value = expected

    result = await bank_accounts_api.get_accounts()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/bank-accounts"


@pytest.mark.asyncio
async def test_error_handling(
    bank_accounts_api: AsyncBankAccountsApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await bank_accounts_api.get_accounts()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
