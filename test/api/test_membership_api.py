"""Tests for the MembershipApi class."""

from unittest.mock import Mock, patch

import pytest


from evo_client.api.membership_api import MembershipApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
)
from evo_client.models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)


@pytest.fixture
def membership_api():
    """Create a MembershipApi instance for testing."""
    return MembershipApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.membership_api.ApiClient.call_api") as mock:
        yield mock


def test_get_categories(membership_api: MembershipApi, mock_api_client: Mock):
    """Test getting membership categories."""
    expected = [W12UtilsCategoryMembershipViewModel()]
    mock_api_client.return_value = expected

    result = membership_api.get_categories(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/membership/category"


def test_get_memberships_basic(membership_api: MembershipApi, mock_api_client: Mock):
    """Test getting memberships list with no parameters."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = membership_api.get_memberships(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/membership"


def test_get_memberships_with_filters(
    membership_api: MembershipApi, mock_api_client: Mock
):
    """Test getting memberships with search filters."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = membership_api.get_memberships(
        membership_id=123,
        name="Gold",
        branch_id=456,
        take=10,
        skip=0,
        active=True,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "idMembership": 123,
        "name": "Gold",
        "idBranch": 456,
        "take": 10,
        "skip": 0,
        "active": True,
    }


def test_error_handling(membership_api: MembershipApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        membership_api.get_memberships(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
