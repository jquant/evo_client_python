"""Tests for the AsyncMembersApi class."""

from datetime import datetime
from typing import List
from unittest.mock import AsyncMock, Mock, patch

import pytest

from evo_client.aio.api.members_api import AsyncMembersApi
from evo_client.models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from evo_client.models.member_authenticate_view_model import MemberAuthenticateViewModel
from evo_client.models.member_data_view_model import MemberDataViewModel
from evo_client.models.member_transfer_view_model import MemberTransferViewModel
from evo_client.models.members_api_view_model import MembersApiViewModel
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
        assert api.base_path_v2 == "/api/v2/members"
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
    assert call_args["resource_path"] == "/api/v1/members/basic"
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

    assert result == {"success": True}
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/fitcoins"
    assert call_args["method"] == "PUT"
    expected_params = {"idMember": 123, "fitcoinType": "add", "fitcoin": 100}
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

    assert result == {"success": True}
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {
        "idMember": 123,
        "fitcoinType": "add",
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

    assert result == {"success": True}
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {"idMember": 123, "fitcoinType": "add", "fitcoin": 100}
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_update_fitcoins_returns_none_on_none_response(async_members_api):
    """Test update_fitcoins with None response."""
    async_members_api.api_client.call_api.return_value = None

    result = await async_members_api.update_fitcoins(
        id_member=123, fitcoin_type="add", fitcoin=100
    )

    assert result is None


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


@pytest.mark.asyncio
async def test_get_basic_info_take_limit_validation(async_members_api):
    """Test get_basic_info raises ValueError when take > 50."""
    with pytest.raises(ValueError, match="Maximum number of records to return is 50"):
        await async_members_api.get_basic_info(take=51)


@pytest.mark.asyncio
async def test_get_members_minimal(async_members_api):
    """Test get_members with minimal parameters."""
    expected_response = [Mock(spec=MembersApiViewModel)]
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_members(name="John")

    assert result == expected_response
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v2/members"
    assert call_args["method"] == "GET"
    assert call_args["query_params"] == {
        "name": "John",
        "onlyPersonal": False,
        "showActivityData": False,
    }
    assert call_args["response_type"] == List[MembersApiViewModel]
    assert call_args["auth_settings"] == ["Basic"]


@pytest.mark.asyncio
async def test_get_members_all_params(async_members_api):
    """Test get_members with all parameters including datetime conversions."""
    expected_response = [Mock(spec=MembersApiViewModel)]
    async_members_api.api_client.call_api.return_value = expected_response

    conversion_start = datetime(2024, 1, 1, 12, 0, 0)
    conversion_end = datetime(2024, 1, 31, 12, 0, 0)
    register_start = datetime(2024, 2, 1, 12, 0, 0)
    register_end = datetime(2024, 2, 28, 12, 0, 0)
    membership_start_start = datetime(2024, 3, 1, 12, 0, 0)
    membership_start_end = datetime(2024, 3, 31, 12, 0, 0)
    membership_cancel_start = datetime(2024, 4, 1, 12, 0, 0)
    membership_cancel_end = datetime(2024, 4, 30, 12, 0, 0)

    result = await async_members_api.get_members(
        name="John",
        email="john@example.com",
        document="12345678900",
        phone="1234567890",
        conversion_date_start=conversion_start,
        conversion_date_end=conversion_end,
        register_date_start=register_start,
        register_date_end=register_end,
        membership_start_date_start=membership_start_start,
        membership_start_date_end=membership_start_end,
        membership_cancel_date_start=membership_cancel_start,
        membership_cancel_date_end=membership_cancel_end,
        status=1,
        token_gympass="token123",
        take=25,
        skip=10,
        ids_members="1,2,3",
        only_personal=True,
        personal_type=1,
        show_activity_data=True,
    )

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {
        "name": "John",
        "email": "john@example.com",
        "document": "12345678900",
        "phone": "1234567890",
        "conversionDateStart": conversion_start.isoformat(),
        "conversionDateEnd": conversion_end.isoformat(),
        "registerDateStart": register_start.isoformat(),
        "registerDateEnd": register_end.isoformat(),
        "membershipStartDateStart": membership_start_start.isoformat(),
        "membershipStartDateEnd": membership_start_end.isoformat(),
        "membershipCancelDateStart": membership_cancel_start.isoformat(),
        "membershipCancelDateEnd": membership_cancel_end.isoformat(),
        "status": 1,
        "tokenGympass": "token123",
        "take": 25,
        "skip": 10,
        "idsMembers": "1,2,3",
        "onlyPersonal": True,
        "personalType": 1,
        "showActivityData": True,
    }
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_get_members_filter_none_params(async_members_api):
    """Test get_members filters out None parameters."""
    expected_response = [Mock(spec=MembersApiViewModel)]
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_members(
        name="John",
        email=None,
        document=None,
        conversion_date_start=None,
        conversion_date_end=None,
        status=None,
    )

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["query_params"] == {
        "name": "John",
        "onlyPersonal": False,
        "showActivityData": False,
    }


@pytest.mark.asyncio
async def test_get_members_take_limit_validation(async_members_api):
    """Test get_members raises ValueError when take > 50."""
    with pytest.raises(ValueError, match="Maximum number of records to return is 50"):
        await async_members_api.get_members(take=51)


@pytest.mark.asyncio
async def test_update_member_card(async_members_api):
    """Test update_member_card method."""
    async_members_api.api_client.call_api.return_value = {"success": True}

    result = await async_members_api.update_member_card(123, "1234567890")

    assert result == {"success": True}
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/123/card"
    assert call_args["method"] == "PUT"
    expected_params = {"idMember": 123, "cardNumber": "1234567890"}
    assert call_args["query_params"] == expected_params
    assert call_args["response_type"] is None
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}


@pytest.mark.asyncio
async def test_get_member_profile(async_members_api):
    """Test get_member_profile method."""
    expected_response = Mock(spec=ClienteDetalhesBasicosApiViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_member_profile(123)

    assert result == expected_response
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v2/members/123"
    assert call_args["method"] == "GET"
    assert call_args["response_type"] == ClienteDetalhesBasicosApiViewModel
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}


@pytest.mark.asyncio
async def test_reset_password_minimal(async_members_api):
    """Test reset_password with minimal parameters."""
    expected_response = Mock(spec=MemberAuthenticateViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.reset_password("user@example.com")

    assert result == expected_response
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/resetPassword"
    assert call_args["method"] == "POST"
    expected_params = {"user": "user@example.com", "signIn": False}
    assert call_args["query_params"] == expected_params
    assert call_args["response_type"] == MemberAuthenticateViewModel
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}


@pytest.mark.asyncio
async def test_reset_password_with_sign_in(async_members_api):
    """Test reset_password with sign_in=True."""
    expected_response = Mock(spec=MemberAuthenticateViewModel)
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.reset_password("user@example.com", sign_in=True)

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    expected_params = {"user": "user@example.com", "signIn": True}
    assert call_args["query_params"] == expected_params


@pytest.mark.asyncio
async def test_get_member_services_with_member_id(async_members_api):
    """Test get_member_services with member ID."""
    expected_response = ["service1", "service2"]
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_member_services(123)

    assert result == expected_response
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/services"
    assert call_args["method"] == "GET"
    assert call_args["query_params"] == {"idMember": 123}
    assert call_args["response_type"] == list
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}


@pytest.mark.asyncio
async def test_get_member_services_without_member_id(async_members_api):
    """Test get_member_services without member ID."""
    expected_response = ["service1", "service2"]
    async_members_api.api_client.call_api.return_value = expected_response

    result = await async_members_api.get_member_services()

    assert result == expected_response
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["query_params"] is None


@pytest.mark.asyncio
async def test_transfer_member(async_members_api):
    """Test transfer_member method."""
    async_members_api.api_client.call_api.return_value = {"success": True}

    # Create a mock transfer data
    transfer_data = Mock(spec=MemberTransferViewModel)
    transfer_data.model_dump.return_value = {
        "memberId": 123,
        "targetBranchId": 456,
        "reason": "Member requested transfer",
    }

    result = await async_members_api.transfer_member(transfer_data)

    assert result == {"success": True}
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/transfer"
    assert call_args["method"] == "POST"
    assert call_args["body"] == {
        "memberId": 123,
        "targetBranchId": 456,
        "reason": "Member requested transfer",
    }
    assert call_args["response_type"] is None
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}

    # Verify model_dump was called with correct parameters
    transfer_data.model_dump.assert_called_once_with(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_update_member_data(async_members_api):
    """Test update_member_data method."""
    async_members_api.api_client.call_api.return_value = {"success": True}

    # Create a mock member data
    member_data = Mock(spec=MemberDataViewModel)
    member_data.model_dump.return_value = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
    }

    result = await async_members_api.update_member_data(123, member_data)

    assert result == {"success": True}
    async_members_api.api_client.call_api.assert_called_once()
    call_args = async_members_api.api_client.call_api.call_args[1]
    assert call_args["resource_path"] == "/api/v1/members/update-member-data/123"
    assert call_args["method"] == "PUT"
    assert call_args["body"] == {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
    }
    assert call_args["response_type"] is None
    assert call_args["auth_settings"] == ["Basic"]
    assert call_args["headers"] == {"Accept": "application/json"}

    # Verify model_dump was called with correct parameters
    member_data.model_dump.assert_called_once_with(exclude_unset=True, by_alias=True)
