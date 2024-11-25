"""Tests for the ActivitiesApi class."""

import pytest
from datetime import datetime
from unittest.mock import patch, Mock

from evo_client.api.activities_api import ActivitiesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.atividade_list_api_view_model import AtividadeListApiViewModel
from evo_client.models.atividade_basico_api_view_model import (
    AtividadeBasicoApiViewModel,
)
from evo_client.models.atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from evo_client.models.e_status_atividade_sessao import EStatusAtividadeSessao
from evo_client.models.e_origem_agendamento import EOrigemAgendamento


@pytest.fixture
def activities_api():
    """Create an ActivitiesApi instance for testing."""
    return ActivitiesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.activities_api.ApiClient.call_api") as mock:
        yield mock


def test_get_activities_basic(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test getting activities list with no parameters."""
    expected = [AtividadeListApiViewModel()]
    mock_api_client.return_value = expected

    result = activities_api.get_activities(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities"


def test_get_activities_with_filters(
    activities_api: ActivitiesApi, mock_api_client: Mock
):
    """Test getting activities with search filters."""
    expected = [AtividadeListApiViewModel()]
    mock_api_client.return_value = expected

    result = activities_api.get_activities(
        search="yoga", branch_id=123, take=10, skip=0, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "search": "yoga",
        "idBranch": 123,
        "take": 10,
        "skip": 0,
    }


def test_get_schedule_detail(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test getting activity schedule details."""
    expected = AtividadeBasicoApiViewModel()
    mock_api_client.return_value = expected

    result = activities_api.get_schedule_detail(
        config_id=1, activity_date=datetime(2023, 1, 1), async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/schedule/detail"


def test_get_schedule_detail_error(
    activities_api: ActivitiesApi, mock_api_client: Mock
):
    """Test error handling when neither session_id nor both config_id and date are provided."""
    with pytest.raises(ValueError) as exc_info:
        activities_api.get_schedule_detail(async_req=False)

    assert (
        str(exc_info.value)
        == "Either provide both config_id and activity_date, or session_id"
    )
    mock_api_client.assert_not_called()


def test_enroll_member(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test enrolling a member in an activity."""
    mock_api_client.return_value = None

    activities_api.enroll(
        config_id=1, activity_date=datetime(2023, 1, 1), member_id=123, async_req=False
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/activities/schedule/enroll"
    assert args["query_params"]["idConfiguration"] == 1
    assert args["query_params"]["idMember"] == 123


def test_enroll_prospect(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test enrolling a prospect in an activity."""
    mock_api_client.return_value = None

    activities_api.enroll(
        config_id=1,
        activity_date=datetime(2023, 1, 1),
        prospect_id=456,
        slot_number=2,
        origin=EOrigemAgendamento._0,
        async_req=False,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"]["idProspect"] == 456
    assert args["query_params"]["slotNumber"] == 2
    assert args["query_params"]["origin"] == EOrigemAgendamento._0.value


def test_enroll_error(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test error handling when neither member_id nor prospect_id are provided."""
    with pytest.raises(ValueError) as exc_info:
        activities_api.enroll(
            config_id=1, activity_date=datetime(2023, 1, 1), async_req=False
        )

    assert str(exc_info.value) == "Either member_id or prospect_id must be provided"


def test_change_status(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test changing member status in activity."""
    mock_api_client.return_value = None

    activities_api.change_status(
        status=EStatusAtividadeSessao._1,
        member_id=123,
        config_id=1,
        activity_date=datetime(2023, 1, 1),
        async_req=False,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/activities/schedule/enroll/change-status"
    assert args["query_params"]["status"] == EStatusAtividadeSessao._1.value


def test_get_unavailable_spots(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test getting unavailable spots for an activity."""
    expected = [1, 3, 5]
    mock_api_client.return_value = expected

    result = activities_api.get_unavailable_spots(
        config_id=1, date=datetime(2023, 1, 1), async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/list-unavailable-spots"


def test_create_experimental_class(
    activities_api: ActivitiesApi, mock_api_client: Mock
):
    """Test creating experimental class."""
    mock_api_client.return_value = None

    activities_api.create_experimental_class(
        prospect_id=123,
        activity_date=datetime(2023, 1, 1),
        activity="Yoga",
        service="Trial Class",
        activity_exists=True,
        branch_id=1,
        async_req=False,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/activities/schedule/experimental-class"


def test_get_schedule(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test getting activity schedule."""
    expected = [AtividadeSessaoParticipanteApiViewModel()]
    mock_api_client.return_value = expected

    result = activities_api.get_schedule(
        member_id=123,
        date=datetime(2023, 1, 1),
        branch_id=1,
        activity_ids=[1, 2],
        audience_ids=[3, 4],
        take=10,
        only_availables=True,
        show_full_week=True,
        branch_token="token123",
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/activities/schedule"


def test_error_handling(activities_api: ActivitiesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        activities_api.get_activities(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
