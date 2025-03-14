"""Tests for the ApiClient class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.core.api_client import ApiClient
from evo_client.core.configuration import Configuration
from evo_client.exceptions import ApiException


@pytest.fixture
def mock_request_handler():
    """Create a mock request handler."""
    with patch("evo_client.core.api_client.RequestHandler") as mock_handler_class:
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        yield mock_handler


@pytest.fixture
def api_client(mock_request_handler: Mock):
    """Create an ApiClient instance for testing."""
    return ApiClient(configuration=Configuration(host="http://example.com"))


def test_api_client_initialization(api_client: ApiClient):
    """Test initializing ApiClient."""
    assert isinstance(api_client.configuration, Configuration)
    assert api_client.user_agent == "Swagger-Codegen/1.0.0/python"


def test_api_client_with_custom_headers():
    """Test initializing ApiClient with custom headers."""
    api_client = ApiClient(header_name="Custom-Header", header_value="HeaderValue")
    assert api_client.default_headers["Custom-Header"] == "HeaderValue"


def test_api_client_validate_configuration():
    """Test validating configuration in ApiClient."""
    with pytest.raises(
        ValueError, match="Value error, Invalid host URL format: Invalid host URL forma"
    ):
        ApiClient(configuration=Configuration(host=""))


@pytest.mark.asyncio
async def test_call_api_get_request_with(
    api_client: ApiClient, mock_request_handler: Mock
):
    """Test call_api method with GET request and parameters."""
    mock_request_handler.execute.return_value = {"id": 1, "name": "test"}
    result = api_client.call_api(
        resource_path="/test",
        method="GET",
        path_params={"id": 1},
        query_params={"filter": "active"},
        headers={"X-Custom": "value"},
        body=None,
        post_params={},
        files={},
        response_type=dict,
        auth_settings=["basic"],
        _return_http_data_only=True,
        _preload_content=True,
        _request_timeout=None,
        async_req=False,
    )
    assert result == {"id": 1, "name": "test"}
    mock_request_handler.execute.assert_called_once()


@pytest.mark.asyncio
async def test_call_api_get_request(api_client: ApiClient, mock_request_handler: Mock):
    """Test call_api method with simple GET request."""
    mock_request_handler.execute.return_value = {"id": 1, "name": "test"}
    result = api_client.call_api(
        resource_path="/test",
        method="GET",
        response_type=dict,
        async_req=False,
    )
    assert result == {"id": 1, "name": "test"}
    mock_request_handler.execute.assert_called_once()


@pytest.mark.asyncio
async def test_call_api_post_request(api_client: ApiClient, mock_request_handler: Mock):
    """Test call_api method with POST request."""
    mock_request_handler.execute.return_value = {"id": 1, "name": "test"}
    result = api_client.call_api(
        resource_path="/test",
        method="POST",
        body={"data": "test"},
        response_type=dict,
        async_req=False,
    )
    assert result == {"id": 1, "name": "test"}
    mock_request_handler.execute.assert_called_once()


@pytest.mark.asyncio
async def test_call_api_error_handling(
    api_client: ApiClient, mock_request_handler: Mock
):
    """Test error handling in call_api method."""
    mock_request_handler.execute.side_effect = ApiException(
        status=404, reason="Not Found"
    )
    with pytest.raises(ApiException) as exc_info:
        api_client.call_api(
            resource_path="/test",
            method="GET",
            response_type=dict,
            async_req=False,
        )
    assert exc_info.value.status == 404
    assert exc_info.value.reason == "Not Found"


@pytest.mark.asyncio
async def test_cached_get_request(api_client: ApiClient, mock_request_handler: Mock):
    """Test API client makes separate calls for identical GET requests.

    Note: If caching is implemented in the future, this test should be updated.
    """
    mock_request_handler.execute.return_value = {"id": 1, "name": "test"}

    # First request
    result1 = api_client.call_api(
        resource_path="/test",
        method="GET",
        response_type=dict,
        async_req=False,
    )

    # Second request (currently makes a new request)
    result2 = api_client.call_api(
        resource_path="/test",
        method="GET",
        response_type=dict,
        async_req=False,
    )

    # Verify both calls return the same result
    assert result1 == result2

    # Verify execution was called twice (not cached)
    assert mock_request_handler.execute.call_count == 2
