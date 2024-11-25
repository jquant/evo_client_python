"""Tests for the RESTClient class."""

from typing import Tuple
from unittest.mock import Mock, PropertyMock, patch

import pytest
from urllib3 import Timeout

from evo_client.core.configuration import Configuration
from evo_client.core.response import RESTResponse
from evo_client.core.rest import RESTClient
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def rest_client():
    """Create a RESTClient instance for testing."""
    with patch(
        "evo_client.core.rest.RESTClient._create_pool_manager",
        return_value=PropertyMock(),
    ) as mock:
        yield RESTClient(configuration=Configuration()), mock


@pytest.fixture
def mock_pool_manager():
    """Create a mock pool manager."""
    with patch(
        "evo_client.core.rest.RESTClient._create_pool_manager",
        return_value=PropertyMock(),
    ) as mock:
        yield mock


def test_rest_client_initialization(rest_client: Tuple[RESTClient, Mock]):
    """Test initializing RESTClient."""

    assert isinstance(rest_client[0].pool_manager, Mock)


def test_create_pool_manager_with_proxy(mock_pool_manager: Mock):
    """Test creating a pool manager with a proxy."""
    config = Configuration()
    config.proxy = "http://proxy.example.com"
    rest_client = RESTClient(configuration=config)

    assert isinstance(rest_client.pool_manager, Mock)
    mock_pool_manager.assert_called_once()


def test_request_get(rest_client: Tuple[RESTClient, Mock]):
    """Test making a GET request using request method."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0].request(
        method="GET",
        url="http://example.com/api",
    )

    assert isinstance(response, RESTResponse)
    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, kwargs = mock_pool_manager.return_value.request.call_args
    assert args[0] == "GET"
    assert args[1] == "http://example.com/api"


def test_request_post(rest_client: Tuple[RESTClient, Mock]):
    """Test making a POST request using request method."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0].request(
        method="POST",
        url="http://example.com/api",
        body={"data": "test"},
    )

    assert isinstance(response, RESTResponse)
    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, kwargs = mock_pool_manager.return_value.request.call_args
    assert args[0] == "POST"
    assert args[1] == "http://example.com/api"
    assert kwargs["body"] == '{"data": "test"}'


def test_request_error_handling(rest_client: Tuple[RESTClient, Mock]):
    """Test error handling in request method."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.side_effect = ApiException(
        status=500, reason="Request failed"
    )

    with pytest.raises(ApiException) as exc_info:
        rest_client[0].request(
            method="GET",
            url="http://example.com/api",
        )

    assert str(exc_info.value) == "(500)\nReason: Request failed"
    mock_pool_manager.return_value.request.assert_called_once()


def test_execute_request_with_body(rest_client: Tuple[RESTClient, Mock]):
    """Test executing a request with a body."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0]._execute_request_with_body(
        method="POST",
        url="http://example.com/api",
        body={"data": "test"},
    )

    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, kwargs = mock_pool_manager.return_value.request.call_args
    assert args[0] == "POST"
    assert args[1] == "http://example.com/api"
    assert kwargs["body"] == '{"data": "test"}'


def test_execute_get_request(rest_client: Tuple[RESTClient, Mock]):
    """Test executing a GET request."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0]._execute_get_request(
        method="GET",
        url="http://example.com/api",
    )

    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, _ = mock_pool_manager.return_value.request.call_args
    assert args[0] == "GET"
    assert args[1] == "http://example.com/api"


def test_handle_json_request(rest_client: Tuple[RESTClient, Mock]):
    """Test handling a JSON request."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0]._handle_json_request(
        method="POST",
        url="http://example.com/api",
        headers={"Content-Type": "application/json"},
        body={"data": "test"},
    )

    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, kwargs = mock_pool_manager.return_value.request.call_args
    assert args[0] == "POST"
    assert args[1] == "http://example.com/api"
    assert kwargs["body"] == '{"data": "test"}'


def test_handle_form_request(rest_client: Tuple[RESTClient, Mock]):
    """Test handling a form-encoded request."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0]._handle_form_request(
        method="POST",
        url="http://example.com/api",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        fields={"field1": "value1"},
        encode_multipart=False,
    )

    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, kwargs = mock_pool_manager.return_value.request.call_args
    assert args[0] == "POST"
    assert args[1] == "http://example.com/api"
    assert kwargs["fields"] == {"field1": "value1"}


def test_get_timeout():
    """Test converting timeout value to urllib3.Timeout object."""
    timeout = RESTClient._get_timeout((5, 10))
    assert isinstance(timeout, Timeout)
    assert timeout.connect_timeout == 5
    assert timeout.read_timeout == 10

    timeout = RESTClient._get_timeout(5)
    assert isinstance(timeout, Timeout)
    assert timeout.total == 5

    timeout = RESTClient._get_timeout(None)
    assert timeout is None

    with pytest.raises(ValueError):
        RESTClient._get_timeout((5, 10, 15))
