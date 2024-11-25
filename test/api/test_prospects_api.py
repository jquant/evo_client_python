"""Tests for the ProspectsApi class."""

import pytest
from datetime import datetime
from unittest.mock import patch, Mock

from evo_client.api.prospects_api import ProspectsApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.prospects_resumo_api_view_model import (
    ProspectsResumoApiViewModel,
)
from evo_client.models.prospect_api_integracao_view_model import (
    ProspectApiIntegracaoViewModel,
)
from evo_client.models.prospect_id_view_model import ProspectIdViewModel
from evo_client.models.prospect_api_integracao_atualizacao_view_model import (
    ProspectApiIntegracaoAtualizacaoViewModel,
)
from evo_client.models.member_service_view_model import MemberServiceViewModel
from evo_client.models.prospect_transferencia_view_model import (
    ProspectTransferenciaViewModel,
)


@pytest.fixture
def prospects_api():
    """Create a ProspectsApi instance for testing."""
    return ProspectsApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.prospects_api.ApiClient.call_api") as mock:
        yield mock


def test_get_prospects_basic(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test getting prospects list with no parameters."""
    expected = [ProspectsResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = prospects_api.get_prospects(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/prospects"


def test_get_prospects_with_filters(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test getting prospects with search filters."""
    expected = [ProspectsResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = prospects_api.get_prospects(
        prospect_id=123,
        name="John Doe",
        document="123456789",
        email="john@example.com",
        phone="1234567890",
        register_date_start=datetime(2023, 1, 1),
        register_date_end=datetime(2023, 12, 31),
        take=10,
        skip=0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "idProspect": 123,
        "name": "John Doe",
        "document": "123456789",
        "email": "john@example.com",
        "phone": "1234567890",
        "registerDateStart": datetime(2023, 1, 1),
        "registerDateEnd": datetime(2023, 12, 31),
        "take": 10,
        "skip": 0,
    }


def test_create_prospect(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test creating a new prospect."""
    expected = ProspectIdViewModel()
    mock_api_client.return_value = expected
    prospect_data = ProspectApiIntegracaoViewModel()

    result = prospects_api.create_prospect(prospect=prospect_data, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/prospects"
    assert args["body"] == prospect_data


def test_update_prospect(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test updating an existing prospect."""
    expected = ProspectIdViewModel()
    mock_api_client.return_value = expected
    prospect_data = ProspectApiIntegracaoAtualizacaoViewModel()

    result = prospects_api.update_prospect(prospect=prospect_data, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/prospects"
    assert args["body"] == prospect_data


def test_get_services(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test getting prospect services."""
    expected = [MemberServiceViewModel()]
    mock_api_client.return_value = expected

    result = prospects_api.get_services(prospect_id=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/prospects/services"
    assert args["query_params"] == {"idProspect": 123}


def test_transfer_prospect(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test transferring a prospect."""
    mock_api_client.return_value = None
    transfer_data = ProspectTransferenciaViewModel()

    prospects_api.transfer_prospect(transfer=transfer_data, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/prospects/transfer"
    assert args["body"] == transfer_data


def test_error_handling(prospects_api: ProspectsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        prospects_api.get_prospects(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
