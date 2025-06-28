"""Tests for the SyncMembersApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncMembersApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.member_authenticate_view_model import MemberAuthenticateViewModel
from evo_client.models.member_data_view_model import MemberDataViewModel
from evo_client.models.member_service_view_model import MemberServiceViewModel
from evo_client.models.member_transfer_view_model import MemberTransferViewModel
from evo_client.models.members_basic_api_view_model import MembersBasicApiViewModel


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def members_api(sync_client):
    """Create a SyncMembersApi instance for testing."""
    return SyncMembersApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_authenticate_member(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test member authentication."""
    expected = MemberAuthenticateViewModel()
    mock_api_client.return_value = expected

    result = members_api.authenticate_member(
        email="test@example.com",
        password="password123",
        change_password=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["resource_path"] == "/api/v1/members/auth"
    assert args["method"] == "POST"
    assert args["query_params"]["email"] == "test@example.com"
    assert args["query_params"]["password"] == "password123"
    assert args["query_params"]["changePassword"] is False


def test_get_basic_info(members_api: SyncMembersApi, mock_api_client: Mock):
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
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/basic"


def test_get_basic_info_error(members_api: SyncMembersApi, mock_api_client: Mock):
    with pytest.raises(ValueError):
        members_api.get_basic_info(take=51)


def test_get_members(members_api: SyncMembersApi, mock_api_client: Mock):
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
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/members"


def test_update_member_card(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test updating member card."""
    mock_api_client.return_value = None

    members_api.update_member_card(id_member=123, card_number="987654321")

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/members/123/card"
    assert args["query_params"] == {"cardNumber": "987654321"}


def test_get_member_profile(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test getting member profile."""
    expected = MemberDataViewModel()
    mock_api_client.return_value = expected

    result = members_api.get_member_profile(id_member=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/members/123"


def test_reset_password(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test password reset."""
    expected = MemberAuthenticateViewModel()
    mock_api_client.return_value = expected

    result = members_api.reset_password(user="test@example.com", sign_in=True)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/resetPassword"
    assert args["query_params"] == {"user": "test@example.com", "signIn": True}


def test_get_member_services(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test getting member services."""
    # Mock raw API response that gets converted to MemberServiceResponse
    expected = [{"id": 1, "serviceName": "Test Service", "serviceType": "Monthly"}]
    mock_api_client.return_value = expected

    result = members_api.get_member_services(id_member=123)

    # Should return list of MemberServiceResponse objects
    assert len(result) == 1
    assert hasattr(result[0], "service_name")  # Check it's a MemberServiceResponse

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/members/services"


def test_transfer_member(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test transferring member."""
    mock_api_client.return_value = None
    transfer_data = MemberTransferViewModel()

    members_api.transfer_member(transfer_data=transfer_data)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/members/transfer"
    assert args["body"] == transfer_data.model_dump(exclude_unset=True, by_alias=True)


def test_update_member_data(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test updating member data."""
    mock_api_client.return_value = True
    member_data = MemberDataViewModel()

    result = members_api.update_member_data(id_member=123, body=member_data)

    # Should return ApiOperationResponse, not boolean
    assert hasattr(result, "success")
    assert result.success is True
    assert result.message == "Member data updated successfully"

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PATCH"
    assert args["resource_path"] == "/api/v1/members/update-member-data/123"
    assert args["body"] == member_data.model_dump(exclude_unset=True, by_alias=True)


def test_error_handling(members_api: SyncMembersApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        members_api.get_members()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
