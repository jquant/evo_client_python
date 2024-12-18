from unittest.mock import Mock

import pytest
import requests
from pydantic import BaseModel

from evo_client.core.configuration import Configuration
from evo_client.core.request_handler import RequestHandler
from evo_client.core.response import RESTResponse


class SampleModel(BaseModel):
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
def mock_response():
    """Create a mock requests response."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.content = b'{"id": 1, "name": "test"}'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"id": 1, "name": "test"}
    return RESTResponse(mock_response)


@pytest.mark.asyncio
async def test_execute(request_handler: RequestHandler, mock_response: Mock):
    """Test execute method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_response)
    result = await request_handler.execute(SampleModel, method="GET", resource_path="/test")
    assert isinstance(result, SampleModel)
    assert result.id == 1
    assert result.name == "test"


@pytest.mark.asyncio
async def test_execute_none(request_handler: RequestHandler, mock_response: Mock):
    """Test execute method of RequestHandler with None model."""
    request_handler.rest_client.request = Mock(return_value=mock_response)
    result = await request_handler.execute(None, method="GET", resource_path="/test")
    assert isinstance(result, dict)
    assert result == {"id": 1, "name": "test"}


@pytest.mark.asyncio
async def test_execute_async(request_handler: RequestHandler, mock_response: Mock):
    """Test execute_async method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_response)
    async_result = await request_handler.execute_async(
        SampleModel, method="GET", resource_path="/test"
    )
    result = async_result.get()
    assert isinstance(result, SampleModel)
    assert result.id == 1
    assert result.name == "test"


def test_prepare_headers(request_handler: RequestHandler):
    """Test _prepare_headers method of RequestHandler."""
    headers = request_handler._prepare_headers({"Custom-Header": "value"})
    assert headers["Custom-Header"] == "value"


def test_prepare_params(request_handler: RequestHandler):
    """Test _prepare_params method of RequestHandler."""
    params = request_handler._prepare_params({"param1": "value1"})
    assert params["param1"] == "value1"


def test_get_request_options(request_handler: RequestHandler):
    """Test _get_request_options method of RequestHandler."""
    options = request_handler._get_request_options({"timeout": 10, "verify": False})
    assert options["request_timeout"] == 10
    assert options["verify_ssl"] == False


@pytest.mark.asyncio
async def test_make_request(request_handler: RequestHandler, mock_response: Mock):
    """Test _make_request method of RequestHandler."""
    request_handler.rest_client.request = Mock(return_value=mock_response)
    result = await request_handler._make_request(
        SampleModel, method="GET", resource_path="/test"
    )
    assert isinstance(result, SampleModel)
    assert result.id == 1
    assert result.name == "test"
