"""Tests for the SyncProspectsApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.prospect_api_integracao_atualizacao_view_model import (
    ProspectApiIntegracaoAtualizacaoViewModel,
)
from evo_client.models.prospect_api_integracao_view_model import (
    ProspectApiIntegracaoViewModel,
)
from evo_client.models.prospect_id_view_model import ProspectIdViewModel
from evo_client.models.prospect_transferencia_view_model import (
    ProspectTransferenciaViewModel,
)
from evo_client.models.prospects_resumo_api_view_model import (
    ProspectsResumoApiViewModel,
)
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncProspectsApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def prospects_api(sync_client):
    """Create a SyncProspectsApi instance for testing."""
    return SyncProspectsApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_prospects_basic(prospects_api: SyncProspectsApi, mock_api_client: Mock):
    """Test getting prospects without filters."""
    expected = [ProspectsResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = prospects_api.get_prospects()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/prospects"


def test_get_prospects_with_filters(
    prospects_api: SyncProspectsApi, mock_api_client: Mock
):
    """Test getting prospects with various filters."""
    expected = [ProspectsResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = prospects_api.get_prospects(
        name="John",
        email="john@example.com",
        document="12345678900",
        phone="1234567890",
        register_date_start=datetime(2023, 1, 1),
        register_date_end=datetime(2023, 12, 31),
        take=50,
        skip=0,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/prospects"
    query_params = args["query_params"]
    assert query_params["name"] == "John"
    assert query_params["email"] == "john@example.com"
    assert query_params["document"] == "12345678900"
    assert query_params["phone"] == "1234567890"
    assert query_params["take"] == 50
    assert query_params["skip"] == 0


def test_create_prospect(prospects_api: SyncProspectsApi, mock_api_client: Mock):
    """Test creating a new prospect."""
    expected = ProspectIdViewModel()
    mock_api_client.return_value = expected
    prospect_data = ProspectApiIntegracaoViewModel()

    result = prospects_api.create_prospect(prospect=prospect_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/prospects"
    assert args["body"] == prospect_data.model_dump(exclude_unset=True, by_alias=True)


def test_update_prospect(prospects_api: SyncProspectsApi, mock_api_client: Mock):
    """Test updating a prospect."""
    expected = ProspectIdViewModel()
    mock_api_client.return_value = expected
    prospect_data = ProspectApiIntegracaoAtualizacaoViewModel()

    result = prospects_api.update_prospect(prospect=prospect_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/prospects"
    assert args["body"] == prospect_data.model_dump(exclude_unset=True, by_alias=True)


def test_transfer_prospect(prospects_api: SyncProspectsApi, mock_api_client: Mock):
    """Test transferring a prospect."""
    mock_api_client.return_value = None
    transfer_data = ProspectTransferenciaViewModel()

    prospects_api.transfer_prospect(transfer=transfer_data)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/prospects/transfer"
    assert args["body"] == transfer_data.model_dump(exclude_unset=True, by_alias=True)


def test_error_handling(prospects_api: SyncProspectsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        prospects_api.get_prospects()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
