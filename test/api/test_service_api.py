"""Tests for the ServiceApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.api.service_api import ServiceApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.servicos_resumo_api_view_model import ServicosResumoApiViewModel


@pytest.fixture
def service_api():
    """Create a ServiceApi instance for testing."""
    return ServiceApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.service_api.ApiClient.call_api") as mock:
        yield mock


def test_get_services_basic(service_api: ServiceApi, mock_api_client: Mock):
    """Test getting services list with no parameters."""
    expected = [ServicosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = service_api.get_services(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/service"


def test_get_services_with_filters(service_api: ServiceApi, mock_api_client: Mock):
    """Test getting services with search filters."""
    expected = [ServicosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = service_api.get_services(
        service_id=123,
        name="Test Service",
        branch_id=456,
        take=10,
        skip=0,
        active=True,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "idService": 123,
        "name": "Test Service",
        "idBranch": 456,
        "take": 10,
        "skip": 0,
        "active": True,
    }


def test_error_handling(service_api: ServiceApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        service_api.get_services(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
