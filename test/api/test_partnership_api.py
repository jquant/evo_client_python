"""Tests for the SyncPartnershipApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.convenios_api_view_model import ConveniosApiViewModel
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncPartnershipApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def partnership_api(sync_client):
    """Create a SyncPartnershipApi instance for testing."""
    return SyncPartnershipApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_partnerships(partnership_api: SyncPartnershipApi, mock_api_client: Mock):
    """Test getting partnerships list."""
    expected = [ConveniosApiViewModel()]
    mock_api_client.return_value = expected

    result = partnership_api.get_partnerships()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/partnership"


def test_get_partnerships_with_filters(
    partnership_api: SyncPartnershipApi, mock_api_client: Mock
):
    """Test getting partnerships with filters."""
    expected = [ConveniosApiViewModel()]
    mock_api_client.return_value = expected
    dt_created = datetime(2023, 1, 1)

    result = partnership_api.get_partnerships(
        status=1, description="Health", dt_created=dt_created
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/partnership"
    assert args["query_params"]["status"] == 1
    assert args["query_params"]["description"] == "Health"
    assert args["query_params"]["dtCreated"] == dt_created


def test_error_handling(partnership_api: SyncPartnershipApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        partnership_api.get_partnerships()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
