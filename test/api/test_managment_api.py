"""Tests for the ManagementApi class."""

from datetime import datetime
from io import BytesIO
from typing import List
from unittest.mock import Mock, patch, MagicMock

import pytest

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


def create_mock_response(status=200, data=b"dummy data"):
    """Helper to create a mock response object with the required attributes."""
    mock_response = MagicMock()
    mock_response.status = status
    mock_response.data = data
    return mock_response


@pytest.mark.asyncio
async def test_get_active_clients_basic(
    management_api: ManagementApi, mock_api_client: Mock
):
    """Test getting active clients list."""
    expected = [ClientesAtivosViewModel()]

    # Mock the response object with required attributes
    mock_response = create_mock_response()
    mock_api_client.return_value = mock_response

    # Patch the _process_excel_response method to return our expected data
    with patch.object(management_api, "_process_excel_response", return_value=expected):
        result = management_api.get_active_clients(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/managment/activeclients"


@pytest.mark.asyncio
async def test_get_prospects(management_api: ManagementApi, mock_api_client: Mock):
    """Test getting prospects with date filters."""
    expected = [SpsRelProspectsCadastradosConvertidos()]

    # Mock the response object
    mock_response = create_mock_response()
    mock_api_client.return_value = mock_response

    # Patch the processing method
    with patch.object(
        management_api, "_process_prospects_excel_response", return_value=expected
    ):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 2)
        result = management_api.get_prospects(
            dt_start=start_date, dt_end=end_date, async_req=False
        )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/managment/prospects"
    assert args["query_params"] == {"dtStart": start_date, "dtEnd": end_date}


@pytest.mark.asyncio
async def test_get_non_renewed_clients(
    management_api: ManagementApi, mock_api_client: Mock
):
    """Test getting non-renewed clients with date filters."""
    expected = [ContratoNaoRenovadosViewModel()]

    # Mock the response object
    mock_response = create_mock_response()
    mock_api_client.return_value = mock_response

    # Patch the processing method
    with patch.object(
        management_api, "_process_non_renewed_excel_response", return_value=expected
    ):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 2)
        result = management_api.get_non_renewed_clients(
            dt_start=start_date, dt_end=end_date, async_req=False
        )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/managment/not-renewed"
    assert args["query_params"] == {"dtStart": start_date, "dtEnd": end_date}


@pytest.mark.asyncio
async def test_error_handling(management_api: ManagementApi, mock_api_client: Mock):
    """Test API error handling."""
    api_exception = ApiException(status=404, reason="Not Found")
    mock_api_client.side_effect = api_exception

    with pytest.raises(ApiException) as exc_info:
        management_api.get_active_clients(async_req=False)

    assert "404" in str(exc_info.value)
    assert "Not Found" in str(exc_info.value)
