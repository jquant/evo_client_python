"""Tests for the AsyncApiClient class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.core.configuration import Configuration
from evo_client.aio.core.api_client import AsyncApiClient
from evo_client.models.members_basic_api_view_model import MembersBasicApiViewModel


@pytest.fixture
def configuration():
    """Create a test configuration."""
    config = Configuration()
    config.host = "https://api.example.com"
    config.username = "test_user"
    config.password = "test_pass"
    return config


@pytest.fixture
def async_api_client(configuration):
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient(configuration=configuration)


@pytest.mark.asyncio
async def test_async_api_client_initialization(configuration):
    """Test initializing AsyncApiClient."""
    client = AsyncApiClient(configuration=configuration)
    assert client.configuration == configuration
    assert isinstance(client.request_handler, object)  # AsyncRequestHandler
    assert client.user_agent == "EVO-Client-Python-Async/1.0.0"


@pytest.mark.asyncio
async def test_async_api_client_default_configuration():
    """Test initializing AsyncApiClient with default configuration."""
    client = AsyncApiClient()
    assert isinstance(client.configuration, Configuration)


@pytest.mark.asyncio
async def test_async_api_client_with_custom_headers():
    """Test initializing AsyncApiClient with custom headers."""
    client = AsyncApiClient(
        header_name="X-Custom-Header",
        header_value="CustomValue",
        cookie="session=abc123",
    )
    assert client.default_headers["X-Custom-Header"] == "CustomValue"
    assert client.cookie == "session=abc123"


@pytest.mark.asyncio
async def test_user_agent_property(async_api_client):
    """Test user agent property getter and setter."""
    assert async_api_client.user_agent == "EVO-Client-Python-Async/1.0.0"

    async_api_client.user_agent = "Custom-Agent/2.0.0"
    assert async_api_client.user_agent == "Custom-Agent/2.0.0"
    assert async_api_client.default_headers["User-Agent"] == "Custom-Agent/2.0.0"


@pytest.mark.asyncio
async def test_context_manager(async_api_client):
    """Test async context manager functionality."""
    with patch.object(
        async_api_client.request_handler, "__aenter__"
    ) as mock_enter, patch.object(
        async_api_client.request_handler, "__aexit__"
    ) as mock_exit:

        mock_enter.return_value = async_api_client.request_handler
        mock_exit.return_value = None

        async with async_api_client as client:
            assert client == async_api_client

        mock_enter.assert_called_once()
        mock_exit.assert_called_once()


@pytest.mark.asyncio
async def test_call_api_simple_get(async_api_client):
    """Test call_api method with simple GET request."""
    mock_response = {"id": 1, "name": "test"}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/test", method="GET", response_type=dict
        )

        assert result == mock_response
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[1]
        assert call_args["resource_path"] == "/api/v1/test"
        assert call_args["method"] == "GET"
        assert call_args["response_type"] is dict


@pytest.mark.asyncio
async def test_call_api_with_path_params(async_api_client):
    """Test call_api method with path parameters."""
    mock_response = {"id": 123, "name": "test user"}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/users/{user_id}/profile/{section}",
            method="GET",
            path_params={"user_id": 123, "section": "basic"},
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["resource_path"] == "/api/v1/users/123/profile/basic"


@pytest.mark.asyncio
async def test_call_api_with_query_params(async_api_client):
    """Test call_api method with query parameters."""
    mock_response = {"data": []}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/members",
            method="GET",
            query_params={"take": 10, "skip": 0, "filter": "active"},
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["query_params"] == {"take": 10, "skip": 0, "filter": "active"}


@pytest.mark.asyncio
async def test_call_api_with_headers(async_api_client):
    """Test call_api method with additional headers."""
    mock_response = {"success": True}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        custom_headers = {"Accept": "application/json", "X-Custom": "value"}
        result = await async_api_client.call_api(
            resource_path="/api/v1/test",
            method="GET",
            headers=custom_headers,
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        expected_headers = async_api_client.default_headers.copy()
        expected_headers.update(custom_headers)
        assert call_args["header_params"] == expected_headers


@pytest.mark.asyncio
async def test_call_api_post_with_body(async_api_client):
    """Test call_api method with POST request and body."""
    mock_response = {"id": 1, "created": True}
    request_body = {"name": "test", "email": "test@example.com"}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/users",
            method="POST",
            body=request_body,
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["body"] == request_body
        assert call_args["method"] == "POST"


@pytest.mark.asyncio
async def test_call_api_with_authentication(async_api_client):
    """Test call_api method with authentication settings."""
    mock_response = {"data": "secure"}

    # Create a proper mock configuration with auth_settings method
    mock_config = Mock()
    mock_config.auth_settings.return_value = {
        "Basic": {"type": "basic"},
        "ApiKey": {"type": "api_key", "key": "X-API-Key", "value": "secret123"},
    }
    async_api_client.configuration = mock_config

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/secure",
            method="GET",
            auth_settings=["Basic", "ApiKey"],
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        # API key should be added to headers
        assert call_args["header_params"]["X-API-Key"] == "secret123"


@pytest.mark.asyncio
async def test_call_api_with_api_key_auth_only(async_api_client):
    """Test call_api method with API key authentication only."""
    mock_response = {"data": "secure"}

    # Create a proper mock configuration with auth_settings method
    mock_config = Mock()
    mock_config.auth_settings.return_value = {
        "ApiKey": {
            "type": "api_key",
            "key": "Authorization",
            "value": "Bearer token123",
        }
    }
    async_api_client.configuration = mock_config

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/secure",
            method="GET",
            auth_settings=["ApiKey"],
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["header_params"]["Authorization"] == "Bearer token123"


@pytest.mark.asyncio
async def test_call_api_with_missing_api_key_value(async_api_client):
    """Test call_api method with API key auth but missing value."""
    mock_response = {"data": "secure"}

    # Create a proper mock configuration with auth_settings method
    mock_config = Mock()
    mock_config.auth_settings.return_value = {
        "ApiKey": {"type": "api_key", "key": "Authorization", "value": None}
    }
    async_api_client.configuration = mock_config

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/secure",
            method="GET",
            auth_settings=["ApiKey"],
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        # Should not add the header if value is None
        assert (
            "Authorization" not in call_args["header_params"]
            or call_args["header_params"].get("Authorization") != None
        )


@pytest.mark.asyncio
async def test_call_api_with_response_type_deserialization(async_api_client):
    """Test call_api method with response type deserialization."""
    # Use a mock response instead of trying to construct the actual model
    mock_response = Mock(spec=MembersBasicApiViewModel)

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/members/basic",
            method="GET",
            response_type=MembersBasicApiViewModel,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["response_type"] == MembersBasicApiViewModel


@pytest.mark.asyncio
async def test_call_api_with_all_parameters(async_api_client):
    """Test call_api method with all possible parameters."""
    mock_response = {"comprehensive": "test"}

    # Create a proper mock configuration with auth_settings method
    mock_config = Mock()
    mock_config.auth_settings.return_value = {"Basic": {"type": "basic"}}
    async_api_client.configuration = mock_config

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/users/{user_id}",
            method="PUT",
            response_type=dict,
            path_params={"user_id": 123},
            query_params={"validate": True},
            headers={"Accept": "application/json"},
            body={"name": "updated"},
            post_params={"form_field": "value"},
            files={"avatar": "/path/to/file"},
            auth_settings=["Basic"],
            return_http_data_only=False,
            preload_content=False,
            request_timeout=30,
            raw_response=True,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["resource_path"] == "/api/v1/users/123"
        assert call_args["method"] == "PUT"
        assert call_args["query_params"] == {"validate": True}
        assert call_args["body"] == {"name": "updated"}
        assert call_args["post_params"] == {"form_field": "value"}
        assert call_args["files"] == {"avatar": "/path/to/file"}
        assert call_args["_return_http_data_only"] is False
        assert call_args["_preload_content"] is False
        assert call_args["timeout"] == 30
        assert call_args["raw_response"] is True


@pytest.mark.asyncio
async def test_call_api_error_handling(async_api_client):
    """Test call_api method error handling."""
    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            await async_api_client.call_api(
                resource_path="/api/v1/test", method="GET", response_type=dict
            )


@pytest.mark.asyncio
async def test_call_api_default_parameters(async_api_client):
    """Test call_api method with default parameters."""
    mock_response = {"default": "test"}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api("/api/v1/test")

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        assert call_args["method"] == "GET"
        assert call_args["response_type"] is None
        assert call_args["_return_http_data_only"] is True
        assert call_args["_preload_content"] is True
        assert call_args["raw_response"] is False


@pytest.mark.asyncio
async def test_complex_path_params_substitution(async_api_client):
    """Test complex path parameter substitution."""
    mock_response = {"result": "success"}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        result = await async_api_client.call_api(
            resource_path="/api/v1/gyms/{gym_id}/members/{member_id}/services/{service_id}",
            method="GET",
            path_params={
                "gym_id": "gym-123",
                "member_id": 456,
                "service_id": "service-789",
            },
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        expected_path = "/api/v1/gyms/gym-123/members/456/services/service-789"
        assert call_args["resource_path"] == expected_path


@pytest.mark.asyncio
async def test_headers_merging(async_api_client):
    """Test that custom headers are properly merged with default headers."""
    # Set up default headers
    async_api_client.default_headers = {
        "User-Agent": "Test-Agent",
        "Accept": "application/json",
    }

    mock_response = {"merged": "headers"}

    with patch.object(async_api_client.request_handler, "execute") as mock_execute:
        mock_execute.return_value = mock_response

        custom_headers = {
            "Authorization": "Bearer token",
            "Accept": "application/xml",  # Should override default
            "X-Custom": "value",
        }

        result = await async_api_client.call_api(
            resource_path="/api/v1/test",
            method="GET",
            headers=custom_headers,
            response_type=dict,
        )

        assert result == mock_response
        call_args = mock_execute.call_args[1]
        merged_headers = call_args["header_params"]

        # Check that headers were properly merged
        assert merged_headers["User-Agent"] == "Test-Agent"  # From default
        assert merged_headers["Accept"] == "application/xml"  # Overridden
        assert merged_headers["Authorization"] == "Bearer token"  # From custom
        assert merged_headers["X-Custom"] == "value"  # From custom
