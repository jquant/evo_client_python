"""Tests for the AsyncWebhookApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncWebhookApi
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def webhook_api(async_client):
    """Create an AsyncWebhookApi instance for testing."""
    return AsyncWebhookApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_webhooks(webhook_api: AsyncWebhookApi, mock_api_client: Mock):
    """Test getting webhooks."""
    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]
    mock_api_client.return_value = expected

    result = await webhook_api.get_webhooks()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/webhook"


@pytest.mark.asyncio
async def test_create_webhook(webhook_api: AsyncWebhookApi, mock_api_client: Mock):
    """Test creating a webhook."""
    mock_api_client.return_value = True

    result = await webhook_api.create_webhook(
        event_type="NewSale", url_callback="https://example.com/webhook"
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/webhook"


@pytest.mark.asyncio
async def test_create_webhook_with_branch_id(
    webhook_api: AsyncWebhookApi, mock_api_client: Mock
):
    """Test creating a webhook with branch ID."""
    mock_api_client.return_value = True

    result = await webhook_api.create_webhook(
        event_type="CreateMember",
        url_callback="https://example.com/webhook",
        branch_id=123,
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/webhook"


@pytest.mark.asyncio
async def test_delete_webhook(webhook_api: AsyncWebhookApi, mock_api_client: Mock):
    """Test deleting a webhook."""
    mock_api_client.return_value = True

    result = await webhook_api.delete_webhook(webhook_id=123)

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/webhook"


@pytest.mark.asyncio
async def test_error_handling(webhook_api: AsyncWebhookApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    # The SyncWebhookApi catches exceptions and returns empty list instead of re-raising
    result = await webhook_api.get_webhooks()

    # Should return empty list when an error occurs
    assert result == []
