"""Tests for the WebhookApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.api.webhook_api import WebhookApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.w12_utils_webhook_filter_view_model import (
    W12UtilsWebhookFilterViewModel,
)
from evo_client.models.w12_utils_webhook_header_view_model import (
    W12UtilsWebhookHeaderViewModel,
)
from evo_client.models.w12_utils_webhook_view_model import W12UtilsWebhookViewModel


@pytest.fixture
def webhook_api():
    """Create a WebhookApi instance for testing."""
    return WebhookApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.webhook_api.ApiClient.call_api") as mock:
        yield mock


def test_delete_webhook(webhook_api: WebhookApi, mock_api_client: Mock):
    """Test deleting a webhook."""
    mock_api_client.return_value = None

    webhook_api.delete_webhook(webhook_id=123, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/webhook"
    assert args["query_params"] == {"IdWebhook": 123}


def test_get_webhooks(webhook_api: WebhookApi, mock_api_client: Mock):
    """Test getting webhooks list."""
    expected = [{"id": 1, "eventType": "NewSale"}]
    mock_api_client.return_value = expected

    result = webhook_api.get_webhooks(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/webhook"


def test_create_webhook(webhook_api: WebhookApi, mock_api_client: Mock):
    """Test creating a webhook."""
    mock_api_client.return_value = None
    headers = [W12UtilsWebhookHeaderViewModel()]
    filters = [W12UtilsWebhookFilterViewModel()]

    webhook_api.create_webhook(
        event_type="NewSale",
        url_callback="https://example.com/webhook",
        branch_id=123,
        headers=headers,
        filters=filters,
        async_req=False,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/webhook"
    assert isinstance(args["body"], W12UtilsWebhookViewModel)
    assert args["body"].event_type == "NewSale"
    assert args["body"].url_callback == "https://example.com/webhook"
    assert args["body"].id_branch == 123


def test_error_handling(webhook_api: WebhookApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        webhook_api.get_webhooks(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
