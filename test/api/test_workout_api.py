"""Tests for the WorkoutApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.api.workout_api import WorkoutApi
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def workout_api():
    """Create a WorkoutApi instance for testing."""
    return WorkoutApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.workout_api.ApiClient.call_api") as mock:
        yield mock


def test_update_workout(workout_api: WorkoutApi, mock_api_client: Mock):
    """Test updating a workout."""
    mock_api_client.return_value = None

    workout_api.update_workout(
        workout_id=123,
        workout_name="New Workout",
        start_date=datetime(2023, 1, 1),
        expiration_date=datetime(2023, 12, 31),
        observation="Test workout",
        categories="Strength,Cardio",
        restrictions="None",
        professor_id=456,
        total_weeks=12,
        weekly_frequency=3,
        async_req=False,
    )

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/workout"
    assert args["query_params"]["idWorkout"] == 123
    assert args["query_params"]["workoutName"] == "New Workout"


def test_get_client_workouts(workout_api: WorkoutApi, mock_api_client: Mock):
    """Test getting client workouts."""
    expected = [{"id": 1, "name": "Test Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_client_workouts(
        client_id=123, inactive=False, deleted=False, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["query_params"]["idClient"] == 123


def test_get_workouts_by_month_year_professor(
    workout_api: WorkoutApi, mock_api_client: Mock
):
    """Test getting workouts by month/year/professor."""
    expected = [{"id": 1, "name": "Test Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_workouts_by_month_year_professor(
        professor_id=123, month=1, year=2023, skip=0, take=10, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/workout-monthyear-professor"


def test_get_default_workouts(workout_api: WorkoutApi, mock_api_client: Mock):
    """Test getting default workouts."""
    expected = [{"id": 1, "name": "Default Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_default_workouts(
        employee_id=123, tag_id=456, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-workout"


def test_link_workout_to_client(workout_api: WorkoutApi, mock_api_client: Mock):
    """Test linking workout to client."""
    mock_api_client.return_value = True

    result = workout_api.link_workout_to_client(
        source_workout_id=123,
        prescription_employee_id=456,
        client_id=789,
        prescription_date=datetime(2023, 1, 1),
        async_req=False,
    )

    assert result is True
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/workout/link-workout-to-client"


def test_link_workout_to_client_error(workout_api: WorkoutApi, mock_api_client: Mock):
    """Test error handling for linking workout to client."""
    mock_api_client.side_effect = ValueError("source_workout_id is required")

    with pytest.raises(ValueError):
        workout_api.link_workout_to_client(
            source_workout_id=None,  # type: ignore
            prescription_employee_id=456,
            async_req=False,
        )


def test_error_handling(workout_api: WorkoutApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        workout_api.get_default_workouts(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
