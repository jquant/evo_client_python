"""Tests for the RESTClient class."""

from typing import Any, Tuple
from unittest.mock import Mock, PropertyMock, patch

import pytest
import urllib3
from urllib3 import Timeout, exceptions

import json

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


def test_rest_client_initialization(rest_client: Tuple[RESTClient, Mock]):
    """Test initializing RESTClient."""

    assert isinstance(rest_client[0].pool_manager, Mock)


def test_create_pool_manager_with_proxy():
    """Test creating a pool manager with a proxy."""
    config = Configuration()
    config.proxy = "http://proxy.example.com"
    rest_client = RESTClient(configuration=config)
    assert isinstance(
        rest_client.pool_manager, (urllib3.ProxyManager, urllib3.PoolManager)
    )


def test_create_pool_manager_with_cert_file():
    """Test creating a pool manager with a cert file."""
    config = Configuration(cert_file="cert.pem")
    rest_client = RESTClient(configuration=config)
    assert isinstance(
        rest_client.pool_manager, (urllib3.ProxyManager, urllib3.PoolManager)
    )


def test_create_pool_manager_with_hostname_verification():
    """Test creating a pool manager with a proxy."""
    config = Configuration(assert_hostname=True)
    config.proxy = "http://proxy.example.com"
    rest_client = RESTClient(configuration=config)
    assert isinstance(
        rest_client.pool_manager, (urllib3.ProxyManager, urllib3.PoolManager)
    )


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


def test_request_error_handling_bad_request(rest_client: Tuple[RESTClient, Mock]):
    """Test error handling in request method."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(
        status=500,
        reason="Request failed",
        headers={"Content-Type": "application/json"},
        data="",
    )

    with pytest.raises(ApiException) as exc_info:
        rest_client[0].request(
            method="GET",
            url="http://example.com/api",
        )

    assert (
        str(exc_info.value)
        == "(500)\nReason: Request failed\nHTTP response headers: {'Content-Type': 'application/json'}"
    )
    mock_pool_manager.return_value.request.assert_called_once()


def test_request_error_handling_ssl_error(rest_client: Tuple[RESTClient, Mock]):
    """Test error handling in request method."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.side_effect = exceptions.SSLError(
        "Error message"
    )

    with pytest.raises(ApiException) as exc_info:
        rest_client[0].request(
            method="GET",
            url="http://example.com/api",
        )

    assert str(exc_info.value) == "(0)\nReason: SSLError: Error message"
    mock_pool_manager.return_value.request.assert_called_once()


@pytest.mark.parametrize(
    "body, content_type, query_params, body_output",
    [
        ({"data": "test"}, "application/json", None, '{"data": "test"}'),
        (
            {"data": "test"},
            "application/json",
            {"param1": "value1"},
            '{"data": "test"}',
        ),
        (
            {"field1": "value1"},
            "application/x-www-form-urlencoded",
            None,
            None,
        ),
        (
            {"file": "test.txt"},
            "multipart/form-data",
            None,
            None,
        ),
        ("test", None, None, "test"),
        ({"data": "test"}, None, None, '{"data": "test"}'),
    ],
)
def test_execute_request_with_body(
    rest_client: Tuple[RESTClient, Mock],
    body: dict,
    content_type: str,
    query_params: dict,
    body_output: Any,
):
    """Test executing a request with a body."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.return_value = Mock(status=200, data="{}")

    response = rest_client[0]._execute_request_with_body(
        method="POST",
        url="http://example.com/api",
        body=body,
        headers={"Content-Type": content_type} if content_type else None,
        query_params=query_params,
    )

    assert response.status == 200
    mock_pool_manager.return_value.request.assert_called_once()
    args, kwargs = mock_pool_manager.return_value.request.call_args
    assert args[0] == "POST"
    assert args[1] == "http://example.com/api" + (
        "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_params
        else ""
    )
    if body_output:
        assert kwargs["body"] == body_output


@pytest.mark.parametrize(
    "body, content_type",
    [
        ([1, 2, 3], None),
    ],
)
def test_execute_request_with_body_exception(
    rest_client: Tuple[RESTClient, Mock], body: dict, content_type: str
):
    """Test executing a request with a body."""
    mock_pool_manager = rest_client[1]
    mock_pool_manager.return_value.request.side_effect = ApiException(
        status=500, reason="Request failed"
    )

    with pytest.raises(ApiException) as exc_info:
        rest_client[0]._execute_request_with_body(
            method="POST",
            url="http://example.com/api",
            body=body,
            headers={"Content-Type": content_type} if content_type else None,
        )

    assert (
        str(exc_info.value)
        == "(0)\nReason: Cannot prepare request message for provided arguments."
    )


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
