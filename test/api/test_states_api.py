"""Tests for the SyncStatesApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncStatesApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.common_models import StateResponse


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def states_api(sync_client):
    """Create a SyncStatesApi instance for testing."""
    return SyncStatesApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_states(states_api: SyncStatesApi, mock_api_client: Mock):
    """Test getting states list."""
    expected = [{"id": 1, "name": "São Paulo", "uf": "SP"}]
    mock_api_client.return_value = expected

    result = states_api.get_states()

    assert result == [StateResponse.model_validate(expected[0])]
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/states"


def test_error_handling(states_api: SyncStatesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        states_api.get_states()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
