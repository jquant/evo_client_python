"""Tests for the AsyncMembershipApi class."""

from typing import List
from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncMembershipApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
)
from evo_client.models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def membership_api(async_client):
    """Create an AsyncMembershipApi instance for testing."""
    return AsyncMembershipApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_memberships_basic(
    membership_api: AsyncMembershipApi, mock_api_client: Mock
):
    """Test getting memberships without filters using v1."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await membership_api.get_memberships()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/membership"


@pytest.mark.asyncio
async def test_get_memberships_with_filters(
    membership_api: AsyncMembershipApi, mock_api_client: Mock
):
    """Test getting memberships with various filters."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await membership_api.get_memberships(
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


@pytest.mark.asyncio
async def test_list_memberships(
    membership_api: AsyncMembershipApi, mock_api_client: Mock
):
    """Test list memberships convenience method."""
    expected = [ContratosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await membership_api.get_memberships(name="Gold", active=True, take=25)

    assert result == expected
    mock_api_client.assert_called_once()


@pytest.mark.asyncio
async def test_error_handling(
    membership_api: AsyncMembershipApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await membership_api.get_memberships()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"


@pytest.mark.asyncio
async def test_get_categories_basic(
    membership_api: AsyncMembershipApi, mock_api_client: Mock
):
    """Test getting membership categories."""
    expected = [W12UtilsCategoryMembershipViewModel()]
    mock_api_client.return_value = expected

    result = await membership_api.get_categories()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/membership/category"
    assert args["response_type"] == List[W12UtilsCategoryMembershipViewModel]
    assert args["auth_settings"] == ["Basic"]


@pytest.mark.asyncio
async def test_get_categories_error_handling(
    membership_api: AsyncMembershipApi, mock_api_client: Mock
):
    """Test error handling for get_categories."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await membership_api.get_categories()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
