"""Tests for the SyncActivitiesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.atividade_agenda_api_view_model import (
    AtividadeAgendaApiViewModel,
)
from evo_client.models.atividade_basico_api_view_model import (
    AtividadeBasicoApiViewModel,
)
from evo_client.models.atividade_list_api_view_model import AtividadeListApiViewModel
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncActivitiesApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def activities_api(sync_client):
    """Create a SyncActivitiesApi instance for testing."""
    return SyncActivitiesApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_activities_basic(activities_api: SyncActivitiesApi, mock_api_client: Mock):
    """Test getting activities without filters."""
    expected = [AtividadeListApiViewModel()]
    mock_api_client.return_value = expected

    result = activities_api.get_activities()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities"


def test_get_activities_with_filters(
    activities_api: SyncActivitiesApi, mock_api_client: Mock
):
    """Test getting activities with various filters."""
    expected = [AtividadeListApiViewModel()]
    mock_api_client.return_value = expected

    result = activities_api.get_activities(
        activity_name="Yoga",
        branch_id=1,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities"
    query_params = args["query_params"]
    assert query_params["activityName"] == "Yoga"
    assert query_params["idBranch"] == 1


def test_get_schedule_detail(activities_api: SyncActivitiesApi, mock_api_client: Mock):
    """Test getting activity schedule details."""
    expected = AtividadeBasicoApiViewModel()
    mock_api_client.return_value = expected

    result = activities_api.get_schedule_detail(
        configuration_id=123,
        date=datetime(2023, 1, 1),
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/schedule/detail"


def test_enroll_member(activities_api: SyncActivitiesApi, mock_api_client: Mock):
    """Test enrolling a member in an activity."""
    mock_api_client.return_value = None

    activities_api.enroll_in_activity(
        configuration_id=123,
        activity_date=datetime(2023, 1, 1),
        member_id=456,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/activities/schedule/enroll"


def test_get_schedule(activities_api: SyncActivitiesApi, mock_api_client: Mock):
    """Test getting activity schedule."""
    expected = [AtividadeAgendaApiViewModel()]
    mock_api_client.return_value = expected

    result = activities_api.get_schedule(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 1, 31),
        member_id=123,
        employee_id=456,
        activity_name="Yoga",
        branch_id=1,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/schedule"


def test_error_handling(activities_api: SyncActivitiesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        activities_api.get_activities()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
