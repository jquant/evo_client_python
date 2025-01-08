"""Tests for the PartnershipApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest


from evo_client.api.partnership_api import PartnershipApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.convenios_api_view_model import ConveniosApiViewModel


@pytest.fixture
def partnership_api():
    """Create a PartnershipApi instance for testing."""
    return PartnershipApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.partnership_api.ApiClient.call_api") as mock:
        yield mock


def test_get_partnerships_basic(partnership_api: PartnershipApi, mock_api_client: Mock):
    """Test getting partnerships list with no parameters."""
    expected = [ConveniosApiViewModel()]
    mock_api_client.return_value = expected

    result = partnership_api.get_partnerships(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/partnership"


def test_get_partnerships_with_filters(
    partnership_api: PartnershipApi, mock_api_client: Mock
):
    """Test getting partnerships with search filters."""
    expected = [ConveniosApiViewModel()]
    mock_api_client.return_value = expected

    result = partnership_api.get_partnerships(
        status=1,
        description="Test Partnership",
        dt_created=datetime(2023, 1, 1),
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "status": 1,
        "description": "Test Partnership",
        "dtCreated": datetime(2023, 1, 1),
    }


def test_error_handling(partnership_api: PartnershipApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await partnership_api.get_partnerships(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
