"""Tests for the AsyncActivitiesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncActivitiesApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.atividade_agenda_api_view_model import (
    AtividadeAgendaApiViewModel,
)
from evo_client.models.atividade_list_api_view_model import AtividadeListApiViewModel
from evo_client.models.atividade_basico_api_view_model import (
    AtividadeBasicoApiViewModel,
)


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def activities_api(async_client):
    """Create an AsyncActivitiesApi instance for testing."""
    return AsyncActivitiesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_activities_basic(
    activities_api: AsyncActivitiesApi, mock_api_client: Mock
):
    """Test getting activities without filters."""
    expected = [AtividadeListApiViewModel()]
    mock_api_client.return_value = expected

    result = await activities_api.get_activities()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities"


@pytest.mark.asyncio
async def test_get_activities_with_filters(
    activities_api: AsyncActivitiesApi, mock_api_client: Mock
):
    """Test getting activities with various filters."""
    expected = [AtividadeListApiViewModel()]
    mock_api_client.return_value = expected

    result = await activities_api.get_activities(
        search="Yoga",
        branch_id=1,
        take=50,
        skip=0,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities"
    query_params = args["query_params"]
    assert query_params["search"] == "Yoga"
    assert query_params["idBranch"] == 1
    assert query_params["take"] == 50
    assert query_params["skip"] == 0


@pytest.mark.asyncio
async def test_get_schedule_detail(
    activities_api: AsyncActivitiesApi, mock_api_client: Mock
):
    """Test getting activity schedule details."""
    expected = AtividadeBasicoApiViewModel()
    mock_api_client.return_value = expected

    result = await activities_api.get_schedule_detail(
        config_id=123,
        activity_date=datetime(2023, 1, 1),
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/schedule/detail"


@pytest.mark.asyncio
async def test_enroll_member(activities_api: AsyncActivitiesApi, mock_api_client: Mock):
    """Test enrolling a member in an activity."""
    mock_api_client.return_value = None

    await activities_api.enroll(
        config_id=123,
        activity_date=datetime(2023, 1, 1),
        member_id=456,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/activities/schedule/enroll"


@pytest.mark.asyncio
async def test_get_schedule(activities_api: AsyncActivitiesApi, mock_api_client: Mock):
    """Test getting activity schedule."""
    expected = [AtividadeAgendaApiViewModel()]
    mock_api_client.return_value = expected

    result = await activities_api.get_schedule(
        member_id=123,
        date=datetime(2023, 1, 1),
        take=20,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/schedule"


@pytest.mark.asyncio
async def test_error_handling(
    activities_api: AsyncActivitiesApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await activities_api.get_activities()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
