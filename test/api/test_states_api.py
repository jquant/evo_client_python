"""Tests for the StatesApi class."""

from unittest.mock import Mock, patch

import pytest


from evo_client.api.states_api import StatesApi
from evo_client.exceptions.api_exceptions import ApiException


@pytest.fixture
def states_api():
    """Create a StatesApi instance for testing."""
    return StatesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.states_api.ApiClient.call_api") as mock:
        yield mock


def test_get_states_basic(states_api: StatesApi, mock_api_client: Mock):
    """Test getting states list."""
    expected = [{"id": 1, "name": "California", "abbreviation": "CA"}]
    mock_api_client.return_value = expected

    result = states_api.get_states(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/states"
    assert args["headers"] == {
        "Accept": ["text/plain", "application/json", "text/json"]
    }
    assert args["auth_settings"] == ["Basic"]


def test_error_handling(states_api: StatesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        states_api.get_states(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
