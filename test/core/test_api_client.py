"""Tests for the ApiClient class."""

import pytest
from unittest.mock import patch, Mock
from evo_client.core.api_client import ApiClient
from evo_client.core.configuration import Configuration
from evo_client.exceptions.api_exceptions import ApiClientError


@pytest.fixture
def api_client():
    """Create an ApiClient instance for testing."""
    return ApiClient(configuration=Configuration(host="http://example.com"))


@pytest.fixture
def mock_request_handler():
    """Create a mock request handler."""
    with patch("evo_client.core.api_client.ApiClient._execute_request") as mock:
        yield mock


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
    with pytest.raises(ApiClientError) as exc_info:
        api_client = ApiClient(configuration=Configuration(host=""))
        api_client.validate_configuration()
    assert str(exc_info.value) == "Host URL is required"


def test_call_api_get_request(api_client: ApiClient, mock_request_handler: Mock):
    """Test making a GET request using call_api."""
    mock_request_handler.return_value = {"key": "value"}

    result = api_client.call_api(
        resource_path="/test",
        method="GET",
        async_req=False,
    )

    assert result == {"key": "value"}
    mock_request_handler.assert_called_once()
    args = mock_request_handler.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/test"


def test_call_api_post_request(api_client: ApiClient, mock_request_handler: Mock):
    """Test making a POST request using call_api."""
    mock_request_handler.return_value = {"key": "value"}

    result = api_client.call_api(
        resource_path="/test",
        method="POST",
        body={"data": "test"},
        async_req=False,
    )

    assert result == {"key": "value"}
    mock_request_handler.assert_called_once()
    args = mock_request_handler.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/test"
    assert args["body"] == {"data": "test"}


def test_call_api_error_handling(api_client: ApiClient, mock_request_handler: Mock):
    """Test error handling in call_api."""
    mock_request_handler.side_effect = Exception("API call failed")

    with pytest.raises(Exception) as exc_info:
        api_client.call_api(
            resource_path="/test",
            method="GET",
            async_req=False,
        )

    assert str(exc_info.value) == "API call failed"
    mock_request_handler.assert_called_once()


def test_cached_get_request(api_client: ApiClient, mock_request_handler: Mock):
    """Test caching of GET requests."""
    mock_request_handler.return_value = {"key": "value"}

    result1 = api_client.call_api(
        resource_path="/test",
        method="GET",
        async_req=False,
    )
    result2 = api_client.call_api(
        resource_path="/test",
        method="GET",
        async_req=False,
    )

    assert result1 == {"key": "value"}
    assert result2 == {"key": "value"}
    assert mock_request_handler.call_count == 2


def test_execute_request_async(api_client: ApiClient, mock_request_handler: Mock):
    """Test executing an asynchronous request."""
    mock_request_handler.return_value = Mock()

    result = api_client.call_api(
        resource_path="/test",
        method="GET",
        async_req=True,
    )

    assert isinstance(result, Mock)
    mock_request_handler.assert_called_once()


def test_execute_request_sync(api_client: ApiClient, mock_request_handler: Mock):
    """Test executing a synchronous request."""
    mock_request_handler.return_value = {"key": "value"}

    result = api_client.call_api(
        resource_path="/test",
        method="GET",
        async_req=False,
    )

    assert result == {"key": "value"}
    mock_request_handler.assert_called_once()
