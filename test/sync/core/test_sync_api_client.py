"""Tests for the SyncApiClient class."""

from typing import List
from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel

from evo_client.core.configuration import Configuration
from evo_client.sync.core.api_client import SyncApiClient


class TestModel(BaseModel):
    """Test model for API client tests."""

    id: int
    name: str


@pytest.fixture
def configuration():
    """Create a test configuration."""
    config = Configuration()
    config.host = "https://api.example.com"
    config.username = "test_user"
    config.password = "test_pass"
    return config


@pytest.fixture
def sync_api_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


def test_sync_api_client_initialization():
    """Test initializing SyncApiClient with default configuration."""
    client = SyncApiClient()
    assert client.configuration is not None
    assert client.request_handler is not None
    assert client.default_headers == {"User-Agent": "EVO-Client-Python/2.0.0/sync"}
    assert client.cookie is None


def test_sync_api_client_initialization_with_configuration(configuration):
    """Test initializing SyncApiClient with provided configuration."""
    client = SyncApiClient(configuration=configuration)
    assert client.configuration == configuration


def test_sync_api_client_initialization_with_headers():
    """Test initializing SyncApiClient with custom headers."""
    client = SyncApiClient(header_name="X-Custom-Header", header_value="test-value")
    assert client.default_headers["X-Custom-Header"] == "test-value"


def test_sync_api_client_initialization_with_cookie():
    """Test initializing SyncApiClient with cookie."""
    client = SyncApiClient(cookie="session=abc123")
    assert client.cookie == "session=abc123"


def test_context_manager(sync_api_client):
    """Test context manager functionality."""
    with patch.object(sync_api_client.request_handler, "cleanup") as mock_cleanup:
        with sync_api_client as client:
            assert client == sync_api_client

        mock_cleanup.assert_called_once()


def test_user_agent_property(sync_api_client):
    """Test user agent property getter."""
    assert sync_api_client.user_agent == "EVO-Client-Python/2.0.0/sync"


def test_user_agent_setter(sync_api_client):
    """Test user agent property setter."""
    new_user_agent = "Custom-Agent/1.0"
    sync_api_client.user_agent = new_user_agent
    assert sync_api_client.user_agent == new_user_agent
    assert sync_api_client.default_headers["User-Agent"] == new_user_agent


def test_call_api_without_response_type(sync_api_client):
    """Test call_api without response type."""
    with patch.object(
        sync_api_client.request_handler, "execute", return_value={"id": 1}
    ) as mock_execute:
        result = sync_api_client.call_api(resource_path="/test", method="GET")

        assert result == {"id": 1}
        mock_execute.assert_called_once()


def test_call_api_with_model_response_type(sync_api_client):
    """Test call_api with model response type."""
    expected_model = TestModel(id=1, name="test")

    with patch.object(
        sync_api_client.request_handler, "execute", return_value=expected_model
    ) as mock_execute:
        result = sync_api_client.call_api(
            resource_path="/test", method="GET", response_type=TestModel
        )

        assert result == expected_model
        mock_execute.assert_called_once()


def test_call_api_with_list_response_type(sync_api_client):
    """Test call_api with list response type."""
    expected_list = [TestModel(id=1, name="test")]

    with patch.object(
        sync_api_client.request_handler, "execute", return_value=expected_list
    ) as mock_execute:
        result = sync_api_client.call_api(
            resource_path="/test", method="GET", response_type=List[TestModel]
        )

        assert result == expected_list
        mock_execute.assert_called_once()


def test_call_api_with_all_parameters(sync_api_client):
    """Test call_api with all parameters."""
    with patch.object(
        sync_api_client.request_handler, "execute", return_value={"success": True}
    ) as mock_execute:
        result = sync_api_client.call_api(
            resource_path="/test/{id}",
            method="POST",
            path_params={"id": 123},
            query_params={"filter": "active"},
            headers={"X-Custom": "value"},
            body={"data": "test"},
            post_params={"param": "value"},
            files={"file": "path/to/file"},
            auth_settings=["basic"],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=30.0,
        )

        assert result == {"success": True}
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[1]
        assert call_args["resource_path"] == "/test/{id}"
        assert call_args["method"] == "POST"
        assert call_args["path_params"] == {"id": 123}
        assert call_args["query_params"] == {"filter": "active"}
        assert call_args["headers"] == {"X-Custom": "value"}
        assert call_args["body"] == {"data": "test"}
        assert call_args["post_params"] == {"param": "value"}
        assert call_args["files"] == {"file": "path/to/file"}
        assert call_args["auth_settings"] == ["basic"]
        assert call_args["_return_http_data_only"] is True
        assert call_args["_preload_content"] is True
        assert call_args["_request_timeout"] == 30.0


def test_call_api_with_raw_response(sync_api_client):
    """Test call_api with raw_response=True."""
    mock_response = Mock()

    with patch.object(
        sync_api_client.request_handler, "execute", return_value=mock_response
    ) as mock_execute:
        result = sync_api_client.call_api(
            resource_path="/test", method="GET", raw_response=True
        )

        assert result == mock_response
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[1]
        assert call_args["raw_response"] is True
        assert call_args["_return_http_data_only"] is False
        assert call_args["_preload_content"] is False


def test_call_api_default_parameters(sync_api_client):
    """Test call_api with default parameters."""
    with patch.object(
        sync_api_client.request_handler, "execute", return_value={}
    ) as mock_execute:
        sync_api_client.call_api(resource_path="/test", method="GET")

        call_args = mock_execute.call_args[1]
        assert call_args["response_type"] is None
        assert call_args["path_params"] is None
        assert call_args["query_params"] is None
        assert call_args["headers"] is None
        assert call_args["body"] is None
        assert call_args["post_params"] is None
        assert call_args["files"] is None
        assert call_args["auth_settings"] is None
        assert call_args["_return_http_data_only"] is True
        assert call_args["_preload_content"] is True
        assert call_args["_request_timeout"] is None
        assert call_args["raw_response"] is False
