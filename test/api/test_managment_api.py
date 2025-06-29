"""Tests for the SyncManagementApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncManagementApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.clientes_ativos_view_model import ClientesAtivosViewModel
from evo_client.models.contrato_nao_renovados_view_model import (
    ContratoNaoRenovadosViewModel,
)
from evo_client.models.sps_rel_prospects_cadastrados_convertidos import (
    SpsRelProspectsCadastradosConvertidos,
)


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def management_api(sync_client):
    """Create a SyncManagementApi instance for testing."""
    return SyncManagementApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_active_clients(management_api: SyncManagementApi, mock_api_client: Mock):
    """Test getting active clients list."""
    expected = [ClientesAtivosViewModel()]

    # Mock the _process_excel_response method since it processes Excel data
    with patch.object(management_api, "_process_excel_response", return_value=expected):
        mock_api_client.return_value = Mock(status=200, data=b"excel_data")

        result = management_api.get_active_clients()

        assert result == expected
        mock_api_client.assert_called_once()
        args = mock_api_client.call_args[1]
        assert args["method"] == "GET"
        assert args["resource_path"] == "/api/v1/managment/activeclients"


def test_get_prospects(management_api: SyncManagementApi, mock_api_client: Mock):
    """Test getting prospects with date filters."""
    expected = [SpsRelProspectsCadastradosConvertidos()]
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Mock the _process_prospects_excel_response method
    with patch.object(
        management_api, "_process_prospects_excel_response", return_value=expected
    ):
        mock_api_client.return_value = Mock(status=200, data=b"excel_data")

        result = management_api.get_prospects(dt_start=start_date, dt_end=end_date)

        assert result == expected
        mock_api_client.assert_called_once()
        args = mock_api_client.call_args[1]
        assert args["method"] == "GET"
        assert args["resource_path"] == "/api/v1/managment/prospects"
        assert args["query_params"]["dtStart"] == start_date
        assert args["query_params"]["dtEnd"] == end_date


def test_get_non_renewed_clients(
    management_api: SyncManagementApi, mock_api_client: Mock
):
    """Test getting non-renewed clients with date filters."""
    expected = [ContratoNaoRenovadosViewModel()]
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Mock the _process_non_renewed_excel_response method
    with patch.object(
        management_api, "_process_non_renewed_excel_response", return_value=expected
    ):
        mock_api_client.return_value = Mock(status=200, data=b"excel_data")

        result = management_api.get_non_renewed_clients(
            dt_start=start_date, dt_end=end_date
        )

        assert result == expected
        mock_api_client.assert_called_once()
        args = mock_api_client.call_args[1]
        assert args["method"] == "GET"
        assert args["resource_path"] == "/api/v1/managment/not-renewed"
        assert args["query_params"]["dtStart"] == start_date
        assert args["query_params"]["dtEnd"] == end_date


def test_error_handling(management_api: SyncManagementApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        management_api.get_active_clients()

    # The management API wraps exceptions, so we check the message content
    assert "500" in str(exc.value)
    assert "Server Error" in str(exc.value)
