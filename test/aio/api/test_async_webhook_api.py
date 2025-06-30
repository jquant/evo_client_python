"""Tests for the AsyncWebhookApi class."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncWebhookApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.w12_utils_webhook_filter_view_model import (
    W12UtilsWebhookFilterViewModel,
)
from evo_client.models.w12_utils_webhook_header_view_model import (
    W12UtilsWebhookHeaderViewModel,
)


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
async def test_webhook_api_initialization():
    """Test AsyncWebhookApi initialization."""
    with patch("evo_client.aio.api.base.AsyncApiClient"):
        api = AsyncWebhookApi()
        assert api.base_path == "/api/v1/webhook"
        assert hasattr(api, "api_client")


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
async def test_get_webhooks_with_branch_id_from_config(webhook_api: AsyncWebhookApi):
    """Test getting webhooks with branch ID extracted from configuration."""
    # Mock configuration with username containing branch ID
    mock_config = Mock()
    mock_config.username = "branch_name:456"
    webhook_api.api_client.configuration = mock_config

    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=expected
    ) as mock_call:
        result = await webhook_api.get_webhooks()

        assert result == expected
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["query_params"] == {"idFilial": "456"}


@pytest.mark.asyncio
async def test_get_webhooks_no_branch_id_in_config(webhook_api: AsyncWebhookApi):
    """Test getting webhooks when configuration has no branch ID."""
    # Mock configuration without branch ID format
    mock_config = Mock()
    mock_config.username = "simple_username"
    webhook_api.api_client.configuration = mock_config

    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=expected
    ) as mock_call:
        result = await webhook_api.get_webhooks()

        assert result == expected
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["query_params"] == {}


@pytest.mark.asyncio
async def test_get_webhooks_no_configuration(webhook_api: AsyncWebhookApi):
    """Test getting webhooks when client has no configuration."""
    # Remove configuration
    if hasattr(webhook_api.api_client, "configuration"):
        delattr(webhook_api.api_client, "configuration")

    expected = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]

    with patch.object(
        webhook_api.api_client, "call_api", return_value=expected
    ) as mock_call:
        result = await webhook_api.get_webhooks()

        assert result == expected
        mock_call.assert_called_once()
        args = mock_call.call_args[1]
        assert args["query_params"] == {}


@pytest.mark.asyncio
async def test_get_webhooks_bytes_response(webhook_api: AsyncWebhookApi):
    """Test getting webhooks with bytes response data."""
    json_data = [{"eventType": "NewSale", "urlCallback": "https://example.com"}]
    json_bytes = '{"data": [{"eventType": "NewSale", "urlCallback": "https://example.com"}]}'.encode(
        "utf-8"
    )

    mock_response = Mock()
    mock_response.data = json_bytes

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.get_webhooks()

        # Should parse the JSON from bytes
        assert result == {
            "data": [{"eventType": "NewSale", "urlCallback": "https://example.com"}]
        }


@pytest.mark.asyncio
async def test_get_webhooks_string_response(webhook_api: AsyncWebhookApi):
    """Test getting webhooks with string response data."""
    json_string = (
        '{"data": [{"eventType": "NewSale", "urlCallback": "https://example.com"}]}'
    )

    mock_response = Mock()
    mock_response.data = json_string

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.get_webhooks()

        # Should parse the JSON from string
        assert result == {
            "data": [{"eventType": "NewSale", "urlCallback": "https://example.com"}]
        }


@pytest.mark.asyncio
async def test_get_webhooks_invalid_json_bytes(webhook_api: AsyncWebhookApi):
    """Test getting webhooks with invalid JSON in bytes."""
    invalid_json_bytes = b"invalid json content"

    mock_response = Mock()
    mock_response.data = invalid_json_bytes

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.get_webhooks()

        # Should return empty list when JSON parsing fails
        assert result == []


@pytest.mark.asyncio
async def test_get_webhooks_invalid_json_string(webhook_api: AsyncWebhookApi):
    """Test getting webhooks with invalid JSON string."""
    invalid_json_string = "invalid json content"

    mock_response = Mock()
    mock_response.data = invalid_json_string

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.get_webhooks()

        # Should return empty list when JSON parsing fails
        assert result == []


@pytest.mark.asyncio
async def test_get_webhooks_decode_error(webhook_api: AsyncWebhookApi):
    """Test getting webhooks when bytes decoding fails."""
    # Create bytes that will cause decode error
    bad_bytes = b"\xff\xfe"  # Invalid UTF-8

    mock_response = Mock()
    mock_response.data = bad_bytes

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.get_webhooks()

        # Should return empty list when decoding fails
        assert result == []


@pytest.mark.asyncio
async def test_get_webhooks_no_data_attribute(webhook_api: AsyncWebhookApi):
    """Test getting webhooks when response has no data attribute."""
    mock_response = Mock(spec=[])  # Mock without data attribute

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.get_webhooks()

        # Should return the response object itself
        assert result == mock_response


@pytest.mark.asyncio
async def test_get_webhooks_list_response_fallback(webhook_api: AsyncWebhookApi):
    """Test getting webhooks when response processing fails but response is a list."""
    mock_response = []

    # Mock the hasattr to raise an exception, triggering the fallback logic
    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        with patch("builtins.hasattr", side_effect=Exception("Test error")):
            result = await webhook_api.get_webhooks()

            # Should return empty list in the exception handler
            assert result == []


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
async def test_create_webhook_with_headers_and_filters(webhook_api: AsyncWebhookApi):
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
        result = await webhook_api.create_webhook(
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


@pytest.mark.asyncio
async def test_create_webhook_status_code_response(webhook_api: AsyncWebhookApi):
    """Test creating a webhook with status code response."""
    mock_response = Mock()
    mock_response.status = 201  # Success status

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is True


@pytest.mark.asyncio
async def test_create_webhook_failed_status_code(webhook_api: AsyncWebhookApi):
    """Test creating a webhook with failed status code."""
    mock_response = Mock()
    mock_response.status = 400  # Bad request

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is False


@pytest.mark.asyncio
async def test_create_webhook_non_none_response(webhook_api: AsyncWebhookApi):
    """Test creating a webhook with non-None response (success case)."""
    mock_response = {"id": 123, "created": True}

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is True


@pytest.mark.asyncio
async def test_create_webhook_none_response(webhook_api: AsyncWebhookApi):
    """Test creating a webhook with None response (failure case)."""
    with patch.object(webhook_api.api_client, "call_api", return_value=None):
        result = await webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is False


@pytest.mark.asyncio
async def test_create_webhook_exception(webhook_api: AsyncWebhookApi):
    """Test creating a webhook when exception occurs."""
    with patch.object(
        webhook_api.api_client, "call_api", side_effect=Exception("API Error")
    ):
        result = await webhook_api.create_webhook(
            event_type="NewSale", url_callback="https://example.com/webhook"
        )

        assert result is False


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
    assert args["query_params"] == {"IdWebhook": "123"}


@pytest.mark.asyncio
async def test_delete_webhook_boolean_response(webhook_api: AsyncWebhookApi):
    """Test deleting a webhook with boolean response."""
    with patch.object(webhook_api.api_client, "call_api", return_value=True):
        result = await webhook_api.delete_webhook(webhook_id=123)
        assert result is True

    with patch.object(webhook_api.api_client, "call_api", return_value=False):
        result = await webhook_api.delete_webhook(webhook_id=123)
        assert result is False


@pytest.mark.asyncio
async def test_delete_webhook_status_code_response(webhook_api: AsyncWebhookApi):
    """Test deleting a webhook with status code response."""
    mock_response = Mock()
    mock_response.status = 200  # Success status

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.delete_webhook(webhook_id=123)
        assert result is True


@pytest.mark.asyncio
async def test_delete_webhook_failed_status_code(webhook_api: AsyncWebhookApi):
    """Test deleting a webhook with failed status code."""
    mock_response = Mock()
    mock_response.status = 404  # Not found

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.delete_webhook(webhook_id=123)
        assert result is False


@pytest.mark.asyncio
async def test_delete_webhook_no_status_attribute(webhook_api: AsyncWebhookApi):
    """Test deleting a webhook when response has no status attribute."""
    mock_response = Mock(spec=[])  # Mock without status attribute

    with patch.object(webhook_api.api_client, "call_api", return_value=mock_response):
        result = await webhook_api.delete_webhook(webhook_id=123)
        # Should return True as fallback when no status available
        assert result is True


@pytest.mark.asyncio
async def test_delete_webhook_exception(webhook_api: AsyncWebhookApi):
    """Test deleting a webhook when exception occurs."""
    with patch.object(
        webhook_api.api_client, "call_api", side_effect=Exception("API Error")
    ):
        result = await webhook_api.delete_webhook(webhook_id=123)
        assert result is False


@pytest.mark.asyncio
async def test_error_handling(webhook_api: AsyncWebhookApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    # The AsyncWebhookApi catches exceptions and returns empty list instead of re-raising
    result = await webhook_api.get_webhooks()

    # Should return empty list when an error occurs
    assert result == []


@pytest.mark.asyncio
async def test_context_manager_delegation():
    """Test that AsyncWebhookApi properly delegates context manager methods."""
    with patch("evo_client.aio.api.base.AsyncApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client

        api = AsyncWebhookApi()

        # Test context manager
        async with api as context_api:
            assert context_api == api

        # Verify context manager methods were called
        mock_client.__aenter__.assert_called_once()
        mock_client.__aexit__.assert_called_once()
