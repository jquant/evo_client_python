"""Tests for the AsyncMembersApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncMembersApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.members_basic_api_view_model import MembersBasicApiViewModel
from evo_client.models.member_authenticate_view_model import MemberAuthenticateViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def members_api(async_client):
    """Create an AsyncMembersApi instance for testing."""
    return AsyncMembersApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_basic_info(members_api: AsyncMembersApi, mock_api_client: Mock):
    """Test getting basic member info."""
    expected = MembersBasicApiViewModel()
    mock_api_client.return_value = expected

    result = await members_api.get_basic_info(email="john@example.com", take=10, skip=0)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/basic-info"
    assert args["query_params"]["email"] == "john@example.com"
    assert args["query_params"]["take"] == 10
    assert args["query_params"]["skip"] == 0


@pytest.mark.asyncio
async def test_get_basic_info_with_filters(
    members_api: AsyncMembersApi, mock_api_client: Mock
):
    """Test getting basic member info with filters."""
    expected = MembersBasicApiViewModel()
    mock_api_client.return_value = expected

    result = await members_api.get_basic_info(
        email="john@example.com",
        document="12345678900",
        phone="1234567890",
        member_id=123,
        take=5,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/basic-info"
    assert args["query_params"]["email"] == "john@example.com"
    assert args["query_params"]["document"] == "12345678900"
    assert args["query_params"]["phone"] == "1234567890"
    assert args["query_params"]["idMember"] == 123
    assert args["query_params"]["take"] == 5


@pytest.mark.asyncio
async def test_authenticate_member(members_api: AsyncMembersApi, mock_api_client: Mock):
    """Test member authentication."""
    expected = MemberAuthenticateViewModel()
    mock_api_client.return_value = expected

    result = await members_api.authenticate_member(
        email="john@example.com", password="password123", change_password=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/members/auth"
    assert args["query_params"]["email"] == "john@example.com"
    assert args["query_params"]["password"] == "password123"
    assert args["query_params"]["changePassword"] == False


@pytest.mark.asyncio
async def test_error_handling(members_api: AsyncMembersApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await members_api.get_basic_info(email="test@example.com")

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
