"""Tests for the SyncMembershipApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
)
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncMembershipApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def membership_api(sync_client):
    """Create a SyncMembershipApi instance for testing."""
    return SyncMembershipApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_memberships_basic(
    membership_api: SyncMembershipApi, mock_api_client: Mock
):
    """Test getting memberships without filters using v1."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = membership_api.get_memberships()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/membership"


def test_get_memberships_with_filters(
    membership_api: SyncMembershipApi, mock_api_client: Mock
):
    """Test getting memberships with various filters."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = membership_api.get_memberships(
        membership_id=123,
        name="Premium",
        branch_id=1,
        take=50,
        skip=0,
        active=True,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/membership"
    query_params = args["query_params"]
    assert query_params["idMembership"] == 123
    assert query_params["name"] == "Premium"
    assert query_params["idBranch"] == 1
    assert query_params["take"] == 50
    assert query_params["skip"] == 0
    assert query_params["active"] == True


def test_list_memberships(membership_api: SyncMembershipApi, mock_api_client: Mock):
    """Test list memberships convenience method."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = membership_api.get_memberships(name="Gold", active=True, take=25)

    assert result == expected
    mock_api_client.assert_called_once()


def test_error_handling(membership_api: SyncMembershipApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        membership_api.get_memberships()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
