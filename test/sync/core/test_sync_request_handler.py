"""Tests for the SyncRequestHandler class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.core.configuration import Configuration
from evo_client.sync.core.request_handler import SyncRequestHandler


@pytest.fixture
def configuration():
    """Create a test configuration."""
    config = Configuration()
    config.host = "https://api.example.com"
    config.username = "test_user"
    config.password = "test_pass"
    config.timeout = 30
    config.verify_ssl = True
    return config


@pytest.fixture
def sync_request_handler(configuration):
    """Create a SyncRequestHandler instance for testing."""
    return SyncRequestHandler(configuration)


def test_sync_request_handler_initialization(configuration):
    """Test initializing SyncRequestHandler."""
    handler = SyncRequestHandler(configuration)
    assert handler.configuration == configuration
    assert handler.rest_client is not None


def test_cleanup(sync_request_handler):
    """Test cleanup method."""
    # Should not raise an error - no resources to clean up in sync version
    sync_request_handler.cleanup()


def test_prepare_headers(sync_request_handler):
    """Test _prepare_headers method."""
    sync_request_handler.configuration.default_headers = {"User-Agent": "Test-Agent"}

    # Test without header_params
    headers = sync_request_handler._prepare_headers()
    assert headers == {"User-Agent": "Test-Agent"}

    # Test with header_params
    custom_headers = {"Authorization": "Bearer token"}
    headers = sync_request_handler._prepare_headers(custom_headers)
    expected = {"User-Agent": "Test-Agent", "Authorization": "Bearer token"}
    assert headers == expected


def test_prepare_params(sync_request_handler):
    """Test _prepare_params method."""
    # Test without query_params
    params = sync_request_handler._prepare_params()
    assert params == {}

    # Test with query_params including bool and None
    query_params = {"filter": "active", "limit": 10, "flag": True, "skip": None}
    params = sync_request_handler._prepare_params(query_params)
    assert params == {"filter": "active", "limit": 10, "flag": "true"}


def test_get_request_options(sync_request_handler):
    """Test _get_request_options method."""
    # Test with default values
    options = sync_request_handler._get_request_options({})
    assert options["request_timeout"] == sync_request_handler.configuration.timeout
    assert options["verify_ssl"] == sync_request_handler.configuration.verify_ssl

    # Test with custom values
    kwargs = {"timeout": 60, "verify": False}
    options = sync_request_handler._get_request_options(kwargs)
    assert options["request_timeout"] == 60
    assert not options["verify_ssl"]


def test_make_request_success(sync_request_handler):
    """Test successful HTTP request."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b'{"id": 1, "name": "test"}'
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"id": 1, "name": "test"}

    with patch.object(
        sync_request_handler.rest_client, "request", return_value=mock_response
    ):
        result = sync_request_handler._make_request(method="GET", resource_path="/test")

        assert result == {"id": 1, "name": "test"}


def test_make_request_with_all_parameters(sync_request_handler):
    """Test request with all parameters."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b'{"success": true}'
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"success": True}

    with patch.object(
        sync_request_handler.rest_client, "request", return_value=mock_response
    ):
        result = sync_request_handler._make_request(
            method="POST",
            resource_path="/test",
            header_params={"Custom-Header": "value"},
            query_params={"param": "value"},
            body={"data": "test"},
            timeout=60,
            verify=False,
        )

        assert result == {"success": True}


def test_make_request_with_raw_response(sync_request_handler):
    """Test request with raw_response=True."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b'{"id": 1}'
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}

    with patch.object(
        sync_request_handler.rest_client, "request", return_value=mock_response
    ):
        result = sync_request_handler._make_request(
            method="GET", resource_path="/test", raw_response=True
        )

        assert result == mock_response


def test_make_request_with_non_json_content_type(sync_request_handler):
    """Test request with non-JSON content type."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"plain text"
    mock_response.getheaders.return_value = {"Content-Type": "text/plain"}

    with patch.object(
        sync_request_handler.rest_client, "request", return_value=mock_response
    ):
        result = sync_request_handler._make_request(method="GET", resource_path="/test")

        assert result == mock_response


def test_make_request_with_return_http_data_only_false(sync_request_handler):
    """Test request with _return_http_data_only=False."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b'{"id": 1}'
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}

    with patch.object(
        sync_request_handler.rest_client, "request", return_value=mock_response
    ):
        result = sync_request_handler._make_request(
            method="GET", resource_path="/test", _return_http_data_only=False
        )

        assert result == mock_response


def test_process_response_with_response_type(sync_request_handler):
    """Test processing response with specific response type."""
    from pydantic import BaseModel

    class TestModel(BaseModel):
        id: int
        name: str

    mock_response = Mock()
    mock_response.status = 200
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.deserialize.return_value = TestModel(id=1, name="test")

    result = sync_request_handler._process_response(
        mock_response, TestModel, False, True
    )

    assert isinstance(result, TestModel)
    assert result.id == 1
    assert result.name == "test"


def test_process_response_deserialization_error_success_status(sync_request_handler):
    """Test processing response with deserialization error but success status."""
    from pydantic import BaseModel

    class TestModel(BaseModel):
        id: int

    mock_response = Mock()
    mock_response.status = 200
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.deserialize.side_effect = ValueError("Deserialization failed")

    result = sync_request_handler._process_response(
        mock_response, TestModel, False, True
    )

    assert result == mock_response


def test_process_response_deserialization_error_failure_status(sync_request_handler):
    """Test processing response with deserialization error and failure status."""
    from pydantic import BaseModel

    class TestModel(BaseModel):
        id: int

    mock_response = Mock()
    mock_response.status = 400
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.deserialize.side_effect = ValueError("Deserialization failed")

    with pytest.raises(ValueError, match="Failed to deserialize response"):
        sync_request_handler._process_response(mock_response, TestModel, False, True)


def test_process_response_with_bytes_data(sync_request_handler):
    """Test processing response with bytes data."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b'{"id": 1}'
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"id": 1}

    result = sync_request_handler._process_response(mock_response, None, False, True)

    assert result == {"id": 1}


def test_process_response_decode_error(sync_request_handler):
    """Test processing response with decode error."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"\xff\xfe"  # Invalid UTF-8
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"id": 1}

    result = sync_request_handler._process_response(mock_response, None, False, True)

    assert result == {"id": 1}


def test_process_response_json_decode_error_from_decoded_data(sync_request_handler):
    """Test JSON decode error from decoded data."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"invalid json {"
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"fallback": True}

    result = sync_request_handler._process_response(mock_response, None, False, True)

    # Should fall back to response.json()
    assert result == {"fallback": True}


def test_process_response_json_error_success_status(sync_request_handler):
    """Test JSON parsing error with success status."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"invalid json"
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.side_effect = Exception("JSON parse error")

    result = sync_request_handler._process_response(mock_response, None, False, True)

    # Should return response object for success status despite parsing failure
    assert result == mock_response


def test_process_response_json_error_failure_status(sync_request_handler):
    """Test JSON parsing error with failure status."""
    mock_response = Mock()
    mock_response.status = 400
    mock_response.data = b"invalid json"
    mock_response.getheaders.return_value = {"Content-Type": "application/json"}
    mock_response.json.side_effect = Exception("JSON parse error")

    with pytest.raises(ValueError, match="Failed to parse response"):
        sync_request_handler._process_response(mock_response, None, False, True)


def test_make_request_exception_handling(sync_request_handler):
    """Test exception handling in _make_request."""
    with patch.object(
        sync_request_handler.rest_client,
        "request",
        side_effect=Exception("Network error"),
    ):
        with pytest.raises(Exception, match="Network error"):
            sync_request_handler._make_request(method="GET", resource_path="/test")


def test_execute_delegates_to_make_request(sync_request_handler):
    """Test that execute method delegates to _make_request."""
    with patch.object(
        sync_request_handler, "_make_request", return_value={"success": True}
    ) as mock_make_request:
        result = sync_request_handler.execute(method="GET", resource_path="/test")

        assert result == {"success": True}
        mock_make_request.assert_called_once()
