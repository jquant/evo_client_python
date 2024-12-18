"""Tests for the MembersApi class."""

from unittest.mock import Mock, patch

import pytest



from evo_client.api.members_api import MembersApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.member_authenticate_view_model import MemberAuthenticateViewModel
from evo_client.models.member_data_view_model import MemberDataViewModel
from evo_client.models.member_service_view_model import MemberServiceViewModel
from evo_client.models.member_transfer_view_model import MemberTransferViewModel
from evo_client.models.members_basic_api_view_model import MembersBasicApiViewModel


@pytest.fixture
def members_api():
    """Create a MembersApi instance for testing."""
    return MembersApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.members_api.ApiClient.call_api") as mock:
        yield mock


def test_authenticate_member(members_api: MembersApi, mock_api_client: Mock):
    """Test member authentication."""
    expected = MemberAuthenticateViewModel()
    mock_api_client.return_value = expected

    result = members_api.authenticate_member(
        email="test@example.com",
        password="password123",
        change_password=False,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/members/auth"
    assert args["query_params"] == {
        "email": "test@example.com",
        "password": "password123",
        "changePassword": False,
    }


def test_get_basic_info(members_api: MembersApi, mock_api_client: Mock):
    """Test getting basic member information."""
    expected = MembersBasicApiViewModel()
    mock_api_client.return_value = expected

    result = members_api.get_basic_info(
        email="test@example.com",
        document="12345678900",
        phone="1234567890",
        member_id=123,
        take=10,
        skip=0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/basic"


def test_get_basic_info_error(members_api: MembersApi, mock_api_client: Mock):
    with pytest.raises(ValueError) as exc:
        await members_api.get_basic_info(take=51, async_req=False)


def test_get_members(members_api: MembersApi, mock_api_client: Mock):
    """Test getting members list."""
    expected = MemberDataViewModel()
    mock_api_client.return_value = expected

    result = members_api.get_members(
        name="John",
        email="john@example.com",
        document="12345678900",
        phone="1234567890",
        status=1,
        take=10,
        skip=0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members"


def test_update_member_card(members_api: MembersApi, mock_api_client: Mock):
    """Test updating member card."""
    mock_api_client.return_value = None

    members_api.update_member_card(
        id_member=123, card_number="987654321", async_req=False
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/members/123/card"
    assert args["query_params"] == {"cardNumber": "987654321"}


def test_get_member_profile(members_api: MembersApi, mock_api_client: Mock):
    """Test getting member profile."""
    expected = MemberDataViewModel()
    mock_api_client.return_value = expected

    await result = await members_api.get_member_profile(id_member=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/123"


def test_reset_password(members_api: MembersApi, mock_api_client: Mock):
    """Test password reset."""
    expected = MemberAuthenticateViewModel()
    mock_api_client.return_value = expected

    result = members_api.reset_password(
        user="test@example.com", sign_in=True, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/resetPassword"
    assert args["query_params"] == {"user": "test@example.com", "signIn": True}


def test_get_member_services(members_api: MembersApi, mock_api_client: Mock):
    """Test getting member services."""
    expected = [MemberServiceViewModel()]
    mock_api_client.return_value = expected

    await result = await members_api.get_member_services(id_member=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/services"


def test_transfer_member(members_api: MembersApi, mock_api_client: Mock):
    """Test transferring member."""
    mock_api_client.return_value = None
    transfer_data = MemberTransferViewModel()

    await members_api.transfer_member(transfer_data=transfer_data, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/members/transfer"
    assert args["body"] == transfer_data.model_dump(exclude_unset=True)


def test_update_member_data(members_api: MembersApi, mock_api_client: Mock):
    """Test updating member data."""
    mock_api_client.return_value = True
    member_data = MemberDataViewModel()

    result = members_api.update_member_data(
        id_member=123, body=member_data, async_req=False
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PATCH"
    assert args["resource_path"] == "/api/v1/members/update-member-data/123"
    assert args["body"] == member_data


def test_error_handling(members_api: MembersApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await members_api.get_members(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
