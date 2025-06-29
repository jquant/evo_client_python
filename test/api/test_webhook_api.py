"""Tests for the SyncWebhookApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.common_models import WebhookResponse
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncWebhookApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def webhook_api(sync_client):
    """Create a SyncWebhookApi instance for testing."""
    return SyncWebhookApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_webhooks(webhook_api: SyncWebhookApi, mock_api_client: Mock):
    """Test getting webhooks."""
    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]
    mock_api_client.return_value = expected

    result = webhook_api.get_webhooks()

    assert result == [WebhookResponse.model_validate(expected[0])]
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/webhook"


def test_create_webhook(webhook_api: SyncWebhookApi, mock_api_client: Mock):
    """Test creating a webhook."""
    mock_api_client.return_value = True

    result = webhook_api.create_webhook(
        event_type="NewSale", url_callback="https://example.com/webhook"
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/webhook"


def test_create_webhook_with_branch_id(
    webhook_api: SyncWebhookApi, mock_api_client: Mock
):
    """Test creating a webhook with branch ID."""
    mock_api_client.return_value = True

    result = webhook_api.create_webhook(
        event_type="CreateMember",
        url_callback="https://example.com/webhook",
        branch_id=123,
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/webhook"


def test_delete_webhook(webhook_api: SyncWebhookApi, mock_api_client: Mock):
    """Test deleting a webhook."""
    mock_api_client.return_value = True

    result = webhook_api.delete_webhook(webhook_id=123)

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/webhook"


def test_error_handling(webhook_api: SyncWebhookApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    # The SyncWebhookApi catches exceptions and returns empty list instead of re-raising
    result = webhook_api.get_webhooks()

    # Should return empty list when an error occurs
    assert result == []
