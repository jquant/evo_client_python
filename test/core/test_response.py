from typing import List
from unittest.mock import Mock

import pytest
import requests
from pydantic import BaseModel

from evo_client.core.response import RESTResponse
from evo_client.exceptions.api_exceptions import ApiException


class SomeBaseModel(BaseModel):
    key: str


@pytest.fixture
def mock_urllib3_response():
    """Create a mock requests response."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.content = b'{"key": "value"}'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"key": "value"}
    return mock_response


@pytest.fixture
def mock_urllib3_response_list():
    """Create a mock requests response with list data."""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.content = b'[{"key": "value"}, {"key": "value"}]'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = [{"key": "value"}, {"key": "value"}]
    return mock_response


def test_rest_response_initialization(mock_urllib3_response):
    """Test initializing RESTResponse."""
    response = RESTResponse(mock_urllib3_response)
    assert response.status == 200
    assert response.reason == "OK"
    assert response.data == b'{"key": "value"}'


def test_rest_response_getheaders(mock_urllib3_response):
    """Test getheaders method of RESTResponse."""
    response = RESTResponse(mock_urllib3_response)
    headers = response.getheaders()
    assert headers == {"Content-Type": "application/json"}


def test_rest_response_getheader(mock_urllib3_response):
    """Test getheader method of RESTResponse."""
    response = RESTResponse(mock_urllib3_response)
    content_type = response.getheader("Content-Type")
    assert content_type == "application/json"
    non_existent_header = response.getheader("Non-Existent-Header")
    assert non_existent_header is None


def test_rest_response_json(mock_urllib3_response):
    """Test json method of RESTResponse."""
    response = RESTResponse(mock_urllib3_response)
    data = response.json()
    assert data == {"key": "value"}


def test_rest_response_json_invalid_content_type(mock_urllib3_response):
    """Test json method of RESTResponse with invalid content type."""
    mock_urllib3_response.headers = {"Content-Type": "text/plain"}
    response = RESTResponse(mock_urllib3_response)
    with pytest.raises(ValueError) as exc_info:
        response.json()
    assert str(exc_info.value) == "Response content is not in JSON format"


def test_rest_response_deserialize(mock_urllib3_response):
    """Test deserialize method of RESTResponse."""
    response = RESTResponse(mock_urllib3_response)
    data = response.deserialize(dict)
    assert data == {"key": "value"}

    """Test deserialize method of RESTResponse with BaseModel."""
    response = RESTResponse(mock_urllib3_response)

    data = response.deserialize(SomeBaseModel)
    assert data == SomeBaseModel(key="value")


def test_rest_response_deserialize_list(mock_urllib3_response_list):
    """Test deserialize method of RESTResponse with list."""

    response = RESTResponse(mock_urllib3_response_list)
    data = response.deserialize(list[SomeBaseModel])
    assert data == [SomeBaseModel(key="value"), SomeBaseModel(key="value")]


class TestModel(BaseModel):
    id: int
    name: str


def test_deserialize_single_model():
    # Mock response with single object
    mock_response = Mock(spec=requests.Response)
    mock_response.content = b'{"id": 1, "name": "test"}'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.json.return_value = {"id": 1, "name": "test"}
    rest_response = RESTResponse(mock_response)

    # Test single model deserialization
    result = rest_response.deserialize(TestModel)
    assert isinstance(result, TestModel)
    assert result.id == 1
    assert result.name == "test"


def test_deserialize_list_of_models():
    # Mock response with list of objects
    mock_response = Mock(spec=requests.Response)
    mock_response.content = b'[{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.json.return_value = [
        {"id": 1, "name": "test1"},
        {"id": 2, "name": "test2"},
    ]
    rest_response = RESTResponse(mock_response)

    # Test list deserialization
    result = rest_response.deserialize(List[TestModel])
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, TestModel) for item in result)
    assert result[0].id == 1
    assert result[1].name == "test2"


def test_error_handling():
    mock_response = Mock(spec=requests.Response)
    mock_response.content = b'{"id": 1, "name": "test"}'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.status_code = 500
    mock_response.reason = "Some error message"
    mock_response.json.return_value = {"id": 1, "name": "test"}
    rest_response = RESTResponse(mock_response)

    exception = ApiException(http_resp=rest_response)

    with pytest.raises(ApiException) as exc_info:
        raise exception

    assert str(exc_info.value) == (
        "(500)\n"
        "Reason: Some error message\n"
        "HTTP response headers: {'Content-Type': 'application/json'}\n"
        'HTTP response body: b\'{"id": 1, "name": "test"}\''
    )
