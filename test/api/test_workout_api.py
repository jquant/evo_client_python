"""Tests for the SyncWorkoutApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.workout_models import WorkoutResponse, WorkoutUpdateResponse
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncWorkoutApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def workout_api(sync_client):
    """Create a SyncWorkoutApi instance for testing."""
    return SyncWorkoutApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_update_workout(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test updating a workout."""
    expected = {"success": True}
    mock_api_client.return_value = expected

    result = workout_api.update_workout(
        workout_id=123,
        workout_name="New Strength Program",
        start_date=datetime(2024, 1, 1),
        expiration_date=datetime(2024, 12, 31),
        total_weeks=12,
        weekly_frequency=3,
    )

    assert result == WorkoutUpdateResponse(
        success=True,
        message="Workout updated successfully",
        workout_id=123,
    )
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/workout"
    query_params = args["query_params"]
    assert query_params["idWorkout"] == 123
    assert query_params["workoutName"] == "New Strength Program"


def test_get_client_workouts(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test getting client workouts."""
    expected = [{"id": 1, "name": "Test Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_client_workouts(
        client_id=123,
        inactive=False,
        deleted=False,
    )

    assert result == [WorkoutResponse.model_validate(expected[0])]
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-client-workout"
    query_params = args["query_params"]
    assert query_params["idClient"] == 123
    assert query_params["inactive"] is False
    assert query_params["deleted"] is False


def test_get_default_workouts(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test getting default workouts."""
    expected = [{"id": 1, "name": "Default Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_default_workouts(
        employee_id=123,
        tag_id=456,
    )

    assert result == [WorkoutResponse.model_validate(expected[0])]
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-workout"
    query_params = args["query_params"]
    assert query_params["idEmployee"] == 123
    assert query_params["idTag"] == 456


def test_link_workout_to_client(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test linking workout to client."""
    expected = True
    mock_api_client.return_value = expected

    workout_api.link_workout_to_client(
        source_workout_id=456,
        prescription_employee_id=10,
        client_id=123,
        prescription_date=datetime(2024, 1, 1),
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/workout/link-workout-to-client"


def test_error_handling(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        workout_api.get_default_workouts()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
