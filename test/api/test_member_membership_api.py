"""Tests for the MemberMembershipApi class."""

import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from typing import List

from evo_client.api.member_membership_api import MemberMembershipApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)
from evo_client.models.contratos_cancelados_resumo_api_view_model import (
    ContratosCanceladosResumoApiViewModel,
)


@pytest.fixture
def member_membership_api():
    """Create a MemberMembershipApi instance for testing."""
    return MemberMembershipApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.member_membership_api.ApiClient.call_api") as mock:
        yield mock


def test_cancel_membership(
    member_membership_api: MemberMembershipApi, mock_api_client: Mock
):
    """Test canceling a membership."""
    mock_api_client.return_value = None
    cancellation_date = datetime(2023, 1, 1)

    member_membership_api.cancel_membership(
        id_member_membership=123,
        id_member_branch=456,
        cancellation_date=cancellation_date,
        reason_cancellation="Test cancellation",
        notice_cancellation="Test notice",
        cancel_future_releases=True,
        cancel_future_sessions=True,
        convert_credit_days=False,
        schedule_cancellation=False,
        add_fine=False,
        async_req=False,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/membermembership/cancellation"
    assert args["query_params"]["IdMemberMembership"] == 123
    assert args["query_params"]["IdMemberBranch"] == 456
    assert args["query_params"]["CancellationDate"] == cancellation_date
    assert args["query_params"]["ReasonCancellation"] == "Test cancellation"


def test_get_membership(
    member_membership_api: MemberMembershipApi, mock_api_client: Mock
):
    """Test getting membership details."""
    expected = MemberMembershipApiViewModel()
    mock_api_client.return_value = expected

    result = member_membership_api.get_membership(
        id_member_membership=123, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/membermembership/123"
    assert args["response_type"] == MemberMembershipApiViewModel


def test_get_canceled_memberships(
    member_membership_api: MemberMembershipApi, mock_api_client: Mock
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
        async_req=False,
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


def test_get_canceled_memberships_take_limit(
    member_membership_api: MemberMembershipApi,
):
    """Test take limit validation for get_canceled_memberships."""
    with pytest.raises(ValueError) as exc:
        member_membership_api.get_canceled_memberships(take=30, async_req=False)

    assert str(exc.value) == "Maximum number of records to return is 25"


def test_error_handling(
    member_membership_api: MemberMembershipApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        member_membership_api.get_membership(id_member_membership=123, async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"