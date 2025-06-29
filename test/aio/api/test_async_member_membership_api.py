"""Tests for the AsyncMemberMembershipApi class."""

from datetime import datetime
from typing import List
from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncMemberMembershipApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.contratos_cancelados_resumo_api_view_model import (
    ContratosCanceladosResumoApiViewModel,
)
from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def member_membership_api(async_client):
    """Create an AsyncMemberMembershipApi instance for testing."""
    return AsyncMemberMembershipApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_cancel_membership(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test cancelling a membership."""
    mock_api_client.return_value = True

    result = await member_membership_api.cancel_membership(
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


@pytest.mark.asyncio
async def test_cancel_membership_minimal(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test cancelling a membership with minimal parameters."""
    mock_api_client.return_value = True

    result = await member_membership_api.cancel_membership(
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


@pytest.mark.asyncio
async def test_get_membership(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test getting membership by ID."""
    expected = MemberMembershipApiViewModel()
    mock_api_client.return_value = expected

    result = await member_membership_api.get_membership(id_member_membership=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/membermembership/123"


@pytest.mark.asyncio
async def test_cancel_membership_with_fine(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test cancelling a membership with fine."""
    mock_api_client.return_value = True

    result = await member_membership_api.cancel_membership(
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


@pytest.mark.asyncio
async def test_cancel_membership_scheduled(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test scheduling a membership cancellation."""
    mock_api_client.return_value = True

    result = await member_membership_api.cancel_membership(
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


@pytest.mark.asyncio
async def test_error_handling(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await member_membership_api.get_membership(id_member_membership=999)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"


@pytest.mark.asyncio
async def test_get_canceled_memberships(
    member_membership_api: AsyncMemberMembershipApi, mock_api_client: Mock
):
    """Test getting canceled memberships with filters."""
    expected = [ContratosCanceladosResumoApiViewModel()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = await member_membership_api.get_canceled_memberships(
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
    member_membership_api: AsyncMemberMembershipApi,
):
    """Test take limit validation for get_canceled_memberships."""
    with pytest.raises(ValueError) as exc:
        await member_membership_api.get_canceled_memberships(take=30)

    assert str(exc.value) == "Maximum number of records to return is 25"
