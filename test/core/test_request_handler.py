from unittest.mock import Mock
import pytest
from evo_client.core.request_handler import RequestHandler
from evo_client.core.configuration import Configuration
from evo_client.core.response import RESTResponse
from urllib3.response import BaseHTTPResponse
from pydantic import BaseModel
from typing import List
import multiprocessing.pool


class TestModel(BaseModel):
    id: int
    name: str


@pytest.fixture(autouse=True)
def cleanup_pools(request_handler):
    """Fixture to cleanup multiprocessing pools after tests."""
    yield
    request_handler.cleanup()


@pytest.fixture
def mock_configuration():
    """Create a mock configuration."""
    mock_config = Mock(spec=Configuration)
    mock_config.configure_mock(
        **{
            "host": "http://testserver",
            "get_basic_auth_token.return_value": "dGVzdDp0ZXN0",
            "timeout": 30,
            "verify_ssl": True,
            "ssl_ca_cert": None,
            "cert_file": None,
            "key_file": None,
            "connection_pool_maxsize": 4,
            "assert_hostname": None,
            "proxy": None,
            "retries": None,
        }
    )
    return mock_config


@pytest.fixture
def request_handler(mock_configuration):
    """Create a RequestHandler instance."""
    return RequestHandler(mock_configuration)


@pytest.fixture
def mock_urllib3_response():
    """Create a mock urllib3 response."""
    mock_response = Mock(spec=BaseHTTPResponse)
    mock_response.status = 200
    mock_response.reason = "OK"
    mock_response.data = b'{"id": 1, "name": "test"}'
    mock_response.headers = {"Content-Type": "application/json"}
    return RESTResponse(mock_response)


def test_execute(request_handler: RequestHandler, mock_urllib3_response: Mock):
    """Test execute method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_urllib3_response)
    result = request_handler.execute(TestModel, method="GET", resource_path="/test")
    assert isinstance(result, TestModel)
    assert result.id == 1
    assert result.name == "test"


def test_execute_none(request_handler: RequestHandler, mock_urllib3_response: Mock):
    """Test execute method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_urllib3_response)
    result = request_handler.execute(None, method="GET", resource_path="/test")
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "test"


def test_execute_async(request_handler, mock_urllib3_response):
    """Test execute_async method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_urllib3_response)
    async_result = request_handler.execute_async(
        TestModel, method="GET", resource_path="/test"
    )
    result = async_result.get()
    assert isinstance(result, TestModel)
    assert result.id == 1
    assert result.name == "test"


def test_prepare_headers(request_handler):
    """Test _prepare_headers method of RequestHandler."""
    headers = request_handler._prepare_headers({"Custom-Header": "value"})
    assert headers["Authorization"] == "Basic dGVzdDp0ZXN0"
    assert headers["Custom-Header"] == "value"


def test_prepare_params(request_handler):
    """Test _prepare_params method of RequestHandler."""
    params = request_handler._prepare_params({"param1": "value1"})
    assert params["param1"] == "value1"


def test_get_request_options(request_handler):
    """Test _get_request_options method of RequestHandler."""
    options = request_handler._get_request_options({"timeout": 10, "verify": False})
    assert options["request_timeout"] == 10
    assert options["verify_ssl"] == False


def test_make_request(request_handler, mock_urllib3_response):
    """Test _make_request method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_urllib3_response)
    result = request_handler._make_request(
        TestModel, method="GET", resource_path="/test"
    )
    assert isinstance(result, TestModel)
    assert result.id == 1
    assert result.name == "test"
