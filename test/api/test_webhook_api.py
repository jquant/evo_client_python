"""Tests for the SyncWebhookApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.common_models import WebhookResponse
from evo_client.models.w12_utils_webhook_filter_view_model import (
    W12UtilsWebhookFilterViewModel,
)
from evo_client.models.w12_utils_webhook_header_view_model import (
    W12UtilsWebhookHeaderViewModel,
)
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


def test_webhook_api_initialization():
    """Test SyncWebhookApi initialization."""
    with patch("evo_client.sync.api.base.SyncApiClient"):
        api = SyncWebhookApi()
        assert api.base_path == "/api/v1/webhook"
        assert hasattr(api, "api_client")


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
    assert args["_return_http_data_only"] is True
    assert args["_preload_content"] is True


def test_get_webhooks_with_branch_id_from_config(webhook_api: SyncWebhookApi):
    """Test getting webhooks with branch ID extracted from configuration."""
    # Mock configuration with username containing branch ID
    mock_config = Mock()
    mock_config.username = "branch_name:456"
    webhook_api.api_client.configuration = mock_config

    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=expected
    ) as mock_call:
        result = webhook_api.get_webhooks()

        assert len(result) == 1
        assert isinstance(result[0], WebhookResponse)
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["query_params"] == {"idFilial": "456"}


def test_get_webhooks_no_branch_id_in_config(webhook_api: SyncWebhookApi):
    """Test getting webhooks when configuration has no branch ID."""
    # Mock configuration without branch ID format
    mock_config = Mock()
    mock_config.username = "simple_username"
    webhook_api.api_client.configuration = mock_config

    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=expected
    ) as mock_call:
        result = webhook_api.get_webhooks()

        assert len(result) == 1
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["query_params"] == {}


def test_get_webhooks_no_configuration(webhook_api: SyncWebhookApi):
    """Test getting webhooks when client has no configuration."""
    # Remove configuration
    if hasattr(webhook_api.api_client, "configuration"):
        delattr(webhook_api.api_client, "configuration")

    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=expected
    ) as mock_call:
        result = webhook_api.get_webhooks()

        assert len(result) == 1
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["query_params"] == {}


def test_get_webhooks_bytes_response(webhook_api: SyncWebhookApi):
    """Test getting webhooks with bytes response data."""
    json_bytes = (
        '[{"eventType": "NewSale", "urlCallback": "https://example.com"}]'.encode(
            "utf-8"
        )
    )

    mock_response = Mock()
    mock_response.data = json_bytes

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should parse the JSON from bytes and return WebhookResponse objects
        assert len(result) == 1
        assert isinstance(result[0], WebhookResponse)


def test_get_webhooks_string_response(webhook_api: SyncWebhookApi):
    """Test getting webhooks with string response data."""
    json_string = '[{"eventType": "NewSale", "urlCallback": "https://example.com"}]'

    mock_response = Mock()
    mock_response.data = json_string

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should parse the JSON from string and return WebhookResponse objects
        assert len(result) == 1
        assert isinstance(result[0], WebhookResponse)


def test_get_webhooks_invalid_json_bytes(webhook_api: SyncWebhookApi):
    """Test getting webhooks with invalid JSON in bytes."""
    invalid_json_bytes = b"invalid json content"

    mock_response = Mock()
    mock_response.data = invalid_json_bytes

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should return empty list when JSON parsing fails
        assert result == []


def test_get_webhooks_invalid_json_string(webhook_api: SyncWebhookApi):
    """Test getting webhooks with invalid JSON string."""
    invalid_json_string = "invalid json content"

    mock_response = Mock()
    mock_response.data = invalid_json_string

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should return empty list when JSON parsing fails
        assert result == []


def test_get_webhooks_decode_error(webhook_api: SyncWebhookApi):
    """Test getting webhooks when bytes decoding fails."""
    # Create bytes that will cause decode error
    bad_bytes = b"\xff\xfe"  # Invalid UTF-8

    mock_response = Mock()
    mock_response.data = bad_bytes

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should return empty list when decoding fails
        assert result == []


def test_get_webhooks_raw_data_list(webhook_api: SyncWebhookApi):
    """Test getting webhooks when response.data is a list."""
    raw_data = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    mock_response = Mock()
    mock_response.data = raw_data

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should convert list to WebhookResponse objects
        assert len(result) == 1
        assert isinstance(result[0], WebhookResponse)


def test_get_webhooks_no_data_attribute(webhook_api: SyncWebhookApi):
    """Test getting webhooks when response has no data attribute."""
    mock_response = Mock(spec=[])  # Mock without data attribute

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.get_webhooks()

        # Should return empty list
        assert result == []


def test_get_webhooks_response_processing_exception(webhook_api: SyncWebhookApi):
    """Test getting webhooks when response processing fails."""
    mock_response = []

    # Mock hasattr to raise an exception, triggering the fallback logic
    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        with patch("builtins.hasattr", side_effect=Exception("Test error")):
            result = webhook_api.get_webhooks()

            # Should return empty list in the exception handler
            assert result == []


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
    assert args["_return_http_data_only"] is True
    assert args["_preload_content"] is True


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


def test_create_webhook_with_headers_and_filters(webhook_api: SyncWebhookApi):
    """Test creating a webhook with headers and filters."""
    headers = [
        W12UtilsWebhookHeaderViewModel(nome="Authorization", valor="Bearer token123"),
        W12UtilsWebhookHeaderViewModel(nome="Content-Type", valor="application/json"),
    ]
    filters = [
        W12UtilsWebhookFilterViewModel(filterType="memberId", value="123"),
        W12UtilsWebhookFilterViewModel(filterType="amount", value="100"),
    ]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=True
    ) as mock_call:
        result = webhook_api.create_webhook(
            event_type="PaymentCompleted",
            url_callback="https://example.com/webhook",
            branch_id=456,
            headers=headers,
            filters=filters,
        )

        assert result is True
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["method"] == "POST"
        assert args["resource_path"] == "/api/v1/webhook"

        # Verify body contains the webhook data
        body = args["body"]
        assert "eventType" in body
        assert body["eventType"] == "PaymentCompleted"
        assert body["urlCallback"] == "https://example.com/webhook"


def test_create_webhook_status_code_response(webhook_api: SyncWebhookApi):
    """Test creating a webhook with status code response."""
    mock_response = Mock()
    mock_response.status = 201  # Success status

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is True


def test_create_webhook_failed_status_code(webhook_api: SyncWebhookApi):
    """Test creating a webhook with failed status code."""
    mock_response = Mock()
    mock_response.status = 400  # Bad request

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is False


def test_create_webhook_non_none_response(webhook_api: SyncWebhookApi):
    """Test creating a webhook with non-None response (success case)."""
    mock_response = {"id": 123, "created": True}

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is True


def test_create_webhook_none_response(webhook_api: SyncWebhookApi):
    """Test creating a webhook with None response (failure case)."""
    with patch.object(webhook_api.api_client, "call_api", return_value=None):
        result = webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is False


def test_create_webhook_exception(webhook_api: SyncWebhookApi):
    """Test creating a webhook when exception occurs."""
    with patch.object(
        webhook_api.api_client, "call_api", side_effect=Exception("API Error")
    ):
        result = webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is False


def test_delete_webhook(webhook_api: SyncWebhookApi, mock_api_client: Mock):
    """Test deleting a webhook."""
    mock_api_client.return_value = True

    result = webhook_api.delete_webhook(webhook_id=123)

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/webhook"
    assert args["query_params"] == {"IdWebhook": "123"}
    assert args["_return_http_data_only"] is True
    assert args["_preload_content"] is True


def test_delete_webhook_boolean_response(webhook_api: SyncWebhookApi):
    """Test deleting a webhook with boolean response."""
    with patch.object(webhook_api.api_client, "call_api", return_value=True):
        result = webhook_api.delete_webhook(webhook_id=123)
        assert result is True

    with patch.object(webhook_api.api_client, "call_api", return_value=False):
        result = webhook_api.delete_webhook(webhook_id=123)
        assert result is False


def test_delete_webhook_status_code_response(webhook_api: SyncWebhookApi):
    """Test deleting a webhook with status code response."""
    mock_response = Mock()
    mock_response.status = 200  # Success status

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.delete_webhook(webhook_id=123)
        assert result is True


def test_delete_webhook_failed_status_code(webhook_api: SyncWebhookApi):
    """Test deleting a webhook with failed status code."""
    mock_response = Mock()
    mock_response.status = 404  # Not found

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.delete_webhook(webhook_id=123)
        assert result is False


def test_delete_webhook_no_status_attribute(webhook_api: SyncWebhookApi):
    """Test deleting a webhook when response has no status attribute."""
    mock_response = Mock(spec=[])  # Mock without status attribute

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = webhook_api.delete_webhook(webhook_id=123)
        # Should return True as fallback when no status available
        assert result is True


def test_delete_webhook_exception(webhook_api: SyncWebhookApi):
    """Test deleting a webhook when exception occurs."""
    with patch.object(
        webhook_api.api_client, "call_api", side_effect=Exception("API Error")
    ):
        result = webhook_api.delete_webhook(webhook_id=123)
        assert result is False


def test_error_handling(webhook_api: SyncWebhookApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    # The SyncWebhookApi catches exceptions and returns empty list instead of re-raising
    result = webhook_api.get_webhooks()

    # Should return empty list when an error occurs
    assert result == []


def test_context_manager_delegation():
    """Test that SyncWebhookApi properly delegates context manager methods."""
    with patch("evo_client.sync.api.base.SyncApiClient") as mock_client_class:
        mock_client = Mock()
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock()
        mock_client_class.return_value = mock_client

        api = SyncWebhookApi()

        # Test context manager
        with api as context_api:
            assert context_api == api

        # Verify context manager methods were called
        mock_client.__enter__.assert_called_once()
        mock_client.__exit__.assert_called_once()
