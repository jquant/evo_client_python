"""Tests for the AsyncMembersApi class."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from evo_client.aio.api.members_api import AsyncMembersApi
from evo_client.models.member_authenticate_view_model import MemberAuthenticateViewModel
from evo_client.models.members_basic_api_view_model import MembersBasicApiViewModel


@pytest.fixture
def async_members_api():
    """Create an AsyncMembersApi instance for testing."""
    with patch("evo_client.aio.api.base.AsyncApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        api = AsyncMembersApi()
        api.api_client = mock_client
        return api


@pytest.mark.asyncio
async def test_async_members_api_initialization():
    """Test AsyncMembersApi initialization."""
    with patch("evo_client.aio.api.base.AsyncApiClient"):
        api = AsyncMembersApi()
        assert api.base_path == "/api/v1/members"
        assert hasattr(api, "api_client")


@pytest.mark.asyncio
async def test_get_basic_info_minimal(async_members_api):
    """Test get_basic_info with minimal parameters."""
    expected_response = Mock(spec=MembersBasicApiViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_basic_info(email="test@example.com")

    assert result == expected_response
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/basic-info"
    assert call_args["method"] == "GET"
    assert call_args["query_params"] == {"email": "test@example.com"}
    assert call_args["response_type"] == MembersBasicApiViewModel
    assert call_args["auth_settings"] == ["Basic"]


@pytest.mark.asyncio
async def test_get_basic_info_all_params(async_members_api):
    """Test get_basic_info with all parameters."""
    expected_response = Mock(spec=MembersBasicApiViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_basic_info(
        email="test@example.com",
        document="12345678900",
        phone="1234567890",
        member_id=123,
        take=10,
        skip=5,
    )

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {
        "email": "test@example.com",
        "document": "12345678900",
        "phone": "1234567890",
        "idMember": 123,
        "take": 10,
        "skip": 5,
    }
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_get_basic_info_filter_none_params(async_members_api):
    """Test get_basic_info filters out None parameters."""
    expected_response = Mock(spec=MembersBasicApiViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_basic_info(
        email="test@example.com",
        document=None,
        phone=None,
        member_id=None,
        take=None,
        skip=None,
    )

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["query_params"] == {"email": "test@example.com"}


@pytest.mark.asyncio
async def test_authenticate_member(async_members_api):
    """Test authenticate_member method."""
    expected_response = Mock(spec=MemberAuthenticateViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.authenticate_member(
        email="test@example.com", password="password123"
    )

    assert result == expected_response
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/auth"
    assert call_args["method"] == "POST"
    expected_params = {
        "email": "test@example.com",
        "password": "password123",
        "changePassword": False,
    }
    assert call_args["query_params"] == expected_params
    assert call_args["response_type"] == MemberAuthenticateViewModel
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}


@pytest.mark.asyncio
async def test_authenticate_member_with_change_password(async_members_api):
    """Test authenticate_member with change_password=True."""
    expected_response = Mock(spec=MemberAuthenticateViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.authenticate_member(
        email="test@example.com", password="password123", change_password=True
    )

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {
        "email": "test@example.com",
        "password": "password123",
        "changePassword": True,
    }
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_update_fitcoins_minimal(async_members_api):
    """Test update_fitcoins with minimal parameters."""
    async_members_api.api_client.call_api.return_value = {"success": True}

    result = await async_members_api.update_fitcoins(
        id_member=123, fitcoin_type="add", fitcoin=100
    )

    assert result is True
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/fitcoins"
    assert call_args["method"] == "PUT"
    expected_params = {"idMember": 123, "type": "add", "fitcoin": 100}
    assert call_args["query_params"] == expected_params
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}


@pytest.mark.asyncio
async def test_update_fitcoins_with_reason(async_members_api):
    """Test update_fitcoins with reason parameter."""
    async_members_api.api_client.call_api.return_value = {"success": True}

    result = await async_members_api.update_fitcoins(
        id_member=123, fitcoin_type="add", fitcoin=100, reason="Bonus reward"
    )

    assert result is True
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {
        "idMember": 123,
        "type": "add",
        "fitcoin": 100,
        "reason": "Bonus reward",
    }
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_update_fitcoins_filter_none_params(async_members_api):
    """Test update_fitcoins filters out None parameters."""
    async_members_api.api_client.call_api.return_value = {"success": True}

    result = await async_members_api.update_fitcoins(
        id_member=123, fitcoin_type="add", fitcoin=100, reason=None
    )

    assert result is True
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {"idMember": 123, "type": "add", "fitcoin": 100}
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_update_fitcoins_returns_false_on_none_response(async_members_api):
    """Test update_fitcoins returns False when response is None."""
    async_members_api.api_client.call_api.return_value = None

    result = await async_members_api.update_fitcoins(
        id_member=123, fitcoin_type="add", fitcoin=100
    )

    assert result is False


@pytest.mark.asyncio
async def test_context_manager_delegation():
    """Test that AsyncMembersApi properly delegates context manager methods."""
    with patch("evo_client.aio.api.base.AsyncApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client

        api = AsyncMembersApi()

        # Test context manager
        async with api as context_api:
            assert context_api == api

        # Verify context manager methods were called
        mock_client.__aenter__.assert_called_once()
        mock_client.__aexit__.assert_called_once()


@pytest.mark.asyncio
async def test_error_handling(async_members_api):
    """Test error handling in async methods."""
    # Simulate an API error
    async_members_api.api_client.call_api.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        await async_members_api.get_basic_info(email="test@example.com")


@pytest.mark.asyncio
async def test_concurrent_requests(async_members_api):
    """Test that multiple concurrent requests work properly."""
    import asyncio

    expected_response = Mock(spec=MembersBasicApiViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    # Make multiple concurrent requests
    tasks = [
        async_members_api.get_basic_info(email=f"user{i}@example.com") for i in range(3)
    ]

    results = await asyncio.gather(*tasks)

    # All should return the expected response
    assert all(result == expected_response for result in results)

    # API client should have been called 3 times
    assert async_members_api.api_client.call_api.call_count == 3
