"""Tests for the SyncMemberMembershipApi class."""

from datetime import datetime
from typing import List
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.contratos_cancelados_resumo_api_view_model import (
    ContratosCanceladosResumoApiViewModel,
)
from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncMemberMembershipApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def member_membership_api(sync_client):
    """Create a SyncMemberMembershipApi instance for testing."""
    return SyncMemberMembershipApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_cancel_membership(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test cancelling a membership."""
    mock_api_client.return_value = True

    result = member_membership_api.cancel_membership(
        id_member_membership=123,
        id_member_branch=1,
        cancellation_date=datetime(2023, 12, 31),
        reason_cancellation="Member requested",
        notice_cancellation="End of year cancellation",
        cancel_future_releases=True,
        cancel_future_sessions=False,
        convert_credit_days=True,
        schedule_cancellation=False,
        add_fine=False,
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/membermembership/cancellation"


def test_cancel_membership_minimal(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test cancelling a membership with minimal parameters."""
    mock_api_client.return_value = True

    result = member_membership_api.cancel_membership(
        id_member_membership=123,
        id_member_branch=1,
        cancellation_date=datetime(2023, 12, 31),
        reason_cancellation="Member requested",
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/membermembership/cancellation"


def test_get_membership(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test getting membership by ID."""
    expected = MemberMembershipApiViewModel()
    mock_api_client.return_value = expected

    result = member_membership_api.get_membership(id_member_membership=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/membermembership/123"


def test_cancel_membership_with_fine(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test cancelling a membership with fine."""
    mock_api_client.return_value = True

    result = member_membership_api.cancel_membership(
        id_member_membership=123,
        id_member_branch=1,
        cancellation_date=datetime(2023, 12, 31),
        reason_cancellation="Early cancellation",
        add_fine=True,
        value_fine=50.0,
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/membermembership/cancellation"


def test_cancel_membership_scheduled(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test scheduling a membership cancellation."""
    mock_api_client.return_value = True

    result = member_membership_api.cancel_membership(
        id_member_membership=123,
        id_member_branch=1,
        cancellation_date=datetime(2023, 12, 31),
        reason_cancellation="Scheduled cancellation",
        schedule_cancellation=True,
        schedule_cancellation_date=datetime(2024, 1, 31),
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/membermembership/cancellation"


def test_error_handling(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        member_membership_api.get_membership(id_member_membership=999)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"


@pytest.mark.asyncio
async def test_get_canceled_memberships(
    member_membership_api: SyncMemberMembershipApi, mock_api_client: Mock
):
    """Test getting canceled memberships with filters."""
    expected = [ContratosCanceladosResumoApiViewModel()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = member_membership_api.get_canceled_memberships(
        id_member=123,
        id_membership=456,
        member_name="John Doe",
        register_date_start=start_date,
        register_date_end=end_date,
        cancel_date_start=start_date,
        cancel_date_end=end_date,
        show_transfers=True,
        show_aggregators=True,
        show_vips=True,
        contract_type="type1",
        take=10,
        skip=0,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/membermembership"
    assert args["response_type"] == List[ContratosCanceladosResumoApiViewModel]
    assert args["query_params"]["idMember"] == 123
    assert args["query_params"]["memberName"] == "John Doe"
    assert args["query_params"]["take"] == 10


@pytest.mark.asyncio
async def test_get_canceled_memberships_take_limit(
    member_membership_api: SyncMemberMembershipApi,
):
    """Test take limit validation for get_canceled_memberships."""
    with pytest.raises(ValueError) as exc:
        member_membership_api.get_canceled_memberships(take=30)

    assert str(exc.value) == "Maximum number of records to return is 25"
