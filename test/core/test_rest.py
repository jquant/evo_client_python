"""Tests for the RESTClient class."""

from typing import Tuple
from unittest.mock import Mock, patch

import pytest
import requests
from requests.auth import HTTPBasicAuth

from evo_client.core.configuration import Configuration
from evo_client.core.response import RESTResponse
from evo_client.core.rest import RESTClient
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def rest_client():
    """Create a RESTClient instance for testing."""
    with patch(
        "evo_client.core.rest.requests.Session",
        return_value=Mock(),
    ) as mock:
        yield RESTClient(
            configuration=Configuration(username="test", password="test")
        ), mock


def test_rest_client_initialization(rest_client: Tuple[RESTClient, Mock]):
    """Test initializing RESTClient."""
    assert isinstance(rest_client[0].session, Mock)


def test_create_session_with_proxy():
    """Test creating a session with a proxy."""
    config = Configuration()
    config.proxy = "http://proxy.example.com"
    rest_client = RESTClient(configuration=config)
    assert rest_client.session.proxies == {
        "http": "http://proxy.example.com",
        "https": "http://proxy.example.com",
    }


def test_create_session_with_cert_file():
    """Test creating a session with a cert file."""
    config = Configuration(cert_file="cert.pem", key_file="key.pem")
    rest_client = RESTClient(configuration=config)
    assert rest_client.session.cert == ("cert.pem", "key.pem")


def test_request_get(rest_client: Tuple[RESTClient, Mock]):
    """Test making a GET request using request method."""
    mock_session = rest_client[1]()
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.content = b"{}"
    mock_response.reason = "OK"
    mock_response.headers = {"Content-Type": "application/json"}
    mock_session.request.return_value = mock_response

    response = rest_client[0].request(
        method="GET",
        url="http://example.com/api",
        preload_content=False,
    )

    assert isinstance(response, RESTResponse)
    assert response.status == 200
    mock_session.request.assert_called_once_with(
        method="GET",
        url="http://example.com/api",
        params=None,
        headers={"Content-Type": "application/json"},
        json=None,
        data=None,
        timeout=None,
        auth=HTTPBasicAuth("test", "test"),
        stream=True,
    )


def test_request_post(rest_client: Tuple[RESTClient, Mock]):
    """Test making a POST request using request method."""
    mock_session = rest_client[1]()
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.content = b"{}"
    mock_response.reason = "OK"
    mock_response.headers = {"Content-Type": "application/json"}
    mock_session.request.return_value = mock_response

    response = rest_client[0].request(
        method="POST",
        url="http://example.com/api",
        body={"data": "test"},
        preload_content=False,
    )

    assert isinstance(response, RESTResponse)
    assert response.status == 200
    mock_session.request.assert_called_once_with(
        method="POST",
        url="http://example.com/api",
        params=None,
        headers={"Content-Type": "application/json"},
        json={"data": "test"},
        data=None,
        auth=HTTPBasicAuth("test", "test"),
        timeout=None,
        stream=True,
    )


def test_request_error_handling_bad_request(rest_client: Tuple[RESTClient, Mock]):
    """Test error handling in request method."""
    mock_session = rest_client[1]()
    mock_response = Mock(
        status_code=500,
        reason="Request failed",
        headers={"Content-Type": "application/json"},
        content=b"",
    )
    mock_session.request.return_value = mock_response

    with pytest.raises(ApiException) as exc_info:
        rest_client[0].request(
            method="GET",
            url="http://example.com/api",
        )

    assert (
        str(exc_info.value)
        == "(500)\nReason: Request failed\nHTTP response headers: {'Content-Type': 'application/json'}"
    )


def test_request_error_handling_ssl_error(rest_client: Tuple[RESTClient, Mock]):
    """Test error handling in request method."""
    mock_session = rest_client[1]()
    mock_session.request.side_effect = requests.exceptions.SSLError("Error message")

    with pytest.raises(ApiException) as exc_info:
        rest_client[0].request(
            method="GET",
            url="http://example.com/api",
        )

    assert str(exc_info.value) == "(0)\nReason: SSLError: Error message"


def test_get_timeout():
    """Test converting timeout value."""
    assert RESTClient._get_timeout((5, 10)) == (5, 10)
    assert RESTClient._get_timeout(5) == 5
    assert RESTClient._get_timeout(None) is None

    with pytest.raises(ValueError):
        RESTClient._get_timeout((5, 10, 15))
