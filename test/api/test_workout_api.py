"""Tests for the SyncWorkoutApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

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
    """Mock the API client call_api method."""
    with patch.object(SyncApiClient, "call_api") as mock:
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

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/workout"


def test_get_client_workouts(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test getting client workouts."""
    expected = [{"id": 1, "name": "Test Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_client_workouts(
        client_id=123,
        inactive=False,
        deleted=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-client-workout"


def test_get_default_workouts(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test getting default workouts."""
    expected = [{"id": 1, "name": "Default Workout"}]
    mock_api_client.return_value = expected

    result = workout_api.get_default_workouts(
        employee_id=123,
        tag_id=456,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-workout"


def test_link_workout_to_client(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test linking a workout to a client."""
    expected = True
    mock_api_client.return_value = expected

    result = workout_api.link_workout_to_client(
        source_workout_id=123,
        prescription_employee_id=456,
        client_id=789,
        prescription_date=datetime(2024, 1, 1),
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/workout/link-workout-to-client"


def test_error_handling(workout_api: SyncWorkoutApi, mock_api_client: Mock):
    """Test error handling in workout API."""
    from evo_client.exceptions.api_exceptions import ApiException

    mock_api_client.side_effect = ApiException("Test error")

    with pytest.raises(ApiException):
        workout_api.get_client_workouts(client_id=123)
