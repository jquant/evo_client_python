"""Tests for the SyncServiceApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncServiceApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def service_api(sync_client):
    """Create a SyncServiceApi instance for testing."""
    return SyncServiceApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_services(service_api: SyncServiceApi, mock_api_client: Mock):
    """Test getting services list."""
    expected = [ServicosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = service_api.get_services(take=10, skip=0)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/service"
    assert args["query_params"]["take"] == 10
    assert args["query_params"]["skip"] == 0


def test_get_services_with_branch_filter(
    service_api: SyncServiceApi, mock_api_client: Mock
):
    """Test getting services with branch filter."""
    expected = [ServicosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = service_api.get_services(branch_id=123, take=5)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/service"
    assert args["query_params"]["idBranch"] == 123
    assert args["query_params"]["take"] == 5


def test_get_services_no_params(service_api: SyncServiceApi, mock_api_client: Mock):
    """Test getting services without parameters."""
    expected = [ServicosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = service_api.get_services()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/service"


def test_error_handling(service_api: SyncServiceApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        service_api.get_services()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
