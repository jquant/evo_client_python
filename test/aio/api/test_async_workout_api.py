"""Tests for the AsyncWorkoutApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncWorkoutApi
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def workout_api(async_client):
    """Create an AsyncWorkoutApi instance for testing."""
    return AsyncWorkoutApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_update_workout(workout_api: AsyncWorkoutApi, mock_api_client: Mock):
    """Test updating a workout."""
    expected = {"success": True}
    mock_api_client.return_value = expected

    result = await workout_api.update_workout(
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
    query_params = args["query_params"]
    assert query_params["idWorkout"] == 123
    assert query_params["workoutName"] == "New Strength Program"


@pytest.mark.asyncio
async def test_get_client_workouts(workout_api: AsyncWorkoutApi, mock_api_client: Mock):
    """Test getting client workouts."""
    expected = [{"id": 1, "name": "Test Workout"}]
    mock_api_client.return_value = expected

    result = await workout_api.get_client_workouts(
        client_id=123,
        inactive=False,
        deleted=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-client-workout"
    query_params = args["query_params"]
    assert query_params["idClient"] == 123
    assert query_params["inactive"] == False
    assert query_params["deleted"] == False


@pytest.mark.asyncio
async def test_get_default_workouts(
    workout_api: AsyncWorkoutApi, mock_api_client: Mock
):
    """Test getting default workouts."""
    expected = [{"id": 1, "name": "Default Workout"}]
    mock_api_client.return_value = expected

    result = await workout_api.get_default_workouts(
        employee_id=123,
        tag_id=456,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/workout/default-workout"
    query_params = args["query_params"]
    assert query_params["idEmployee"] == 123
    assert query_params["idTag"] == 456


@pytest.mark.asyncio
async def test_link_workout_to_client(
    workout_api: AsyncWorkoutApi, mock_api_client: Mock
):
    """Test linking workout to client."""
    expected = True
    mock_api_client.return_value = expected

    result = await workout_api.link_workout_to_client(
        source_workout_id=456,
        prescription_employee_id=10,
        client_id=123,
        prescription_date=datetime(2024, 1, 1),
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/workout/link-workout-to-client"


@pytest.mark.asyncio
async def test_error_handling(workout_api: AsyncWorkoutApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await workout_api.get_default_workouts()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
