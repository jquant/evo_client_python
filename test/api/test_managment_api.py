"""Tests for the ManagementApi class."""

import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from typing import List

from evo_client.api.managment_api import ManagementApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.clientes_ativos_view_model import ClientesAtivosViewModel
from evo_client.models.contrato_nao_renovados_view_model import (
    ContratoNaoRenovadosViewModel,
)
from evo_client.models.sps_rel_prospects_cadastrados_convertidos import (
    SpsRelProspectsCadastradosConvertidos,
)


@pytest.fixture
def management_api():
    """Create a ManagementApi instance for testing."""
    return ManagementApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.managment_api.ApiClient.call_api") as mock:
        yield mock


def test_get_active_clients_basic(management_api: ManagementApi, mock_api_client: Mock):
    """Test getting active clients list."""
    expected = [ClientesAtivosViewModel()]
    mock_api_client.return_value = expected

    result = management_api.get_active_clients(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/management/activeclients"
    assert args["response_type"] == List[ClientesAtivosViewModel]


def test_get_prospects(management_api: ManagementApi, mock_api_client: Mock):
    """Test getting prospects with date filters."""
    expected = [SpsRelProspectsCadastradosConvertidos()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = management_api.get_prospects(
        dt_start=start_date, dt_end=end_date, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/management/prospects"
    assert args["query_params"] == {"dtStart": start_date, "dtEnd": end_date}


def test_get_non_renewed_clients(management_api: ManagementApi, mock_api_client: Mock):
    """Test getting non-renewed clients with date filters."""
    expected = [ContratoNaoRenovadosViewModel()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = management_api.get_non_renewed_clients(
        dt_start=start_date, dt_end=end_date, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/management/not-renewed"
    assert args["query_params"] == {"dtStart": start_date, "dtEnd": end_date}


def test_error_handling(management_api: ManagementApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        management_api.get_active_clients(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
