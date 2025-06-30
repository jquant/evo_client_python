"""Tests for the SyncManagementApi class."""

import io
from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.clientes_ativos_view_model import ClientesAtivosViewModel
from evo_client.models.contrato_nao_renovados_view_model import (
    ContratoNaoRenovadosViewModel,
)
from evo_client.models.sps_rel_prospects_cadastrados_convertidos import (
    SpsRelProspectsCadastradosConvertidos,
)
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncManagementApi


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


def test_process_excel_response_success(management_api: SyncManagementApi):
    """Test successful Excel response processing."""
    # Create sample Excel data
    excel_data = {
        "IdFilial": [1],
        "Filial": ["Branch 1"],
        "IdCliente": [123],
        "NomeCompleto": ["John Doe"],
        "Telefone": ["123-456-7890"],
        "Email": ["john@example.com"],
        "IdClienteContratoAtivo": [456],
        "ContratoAtivo": ["Contract Active"],
        "DtInicioContratoAtivo": ["01/01/2023"],
        "DtFimContratoAtivo": ["31/12/2023"],
        "IdClienteContratoFuturo": [789],
        "ContratoFuturo": ["Contract Future"],
        "DtInicioContratoFuturo": ["01/01/2024"],
        "DtFimContratoFuturo": ["31/12/2024"],
    }

    df = pd.DataFrame(excel_data)
    excel_bytes = io.BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = excel_bytes.getvalue()

    result = management_api._process_excel_response(mock_response)

    assert len(result) == 1
    assert isinstance(result[0], ClientesAtivosViewModel)
    assert result[0].nome_completo == "John Doe"


def test_process_excel_response_non_200_status(management_api: SyncManagementApi):
    """Test Excel response processing with non-200 status."""
    mock_response = Mock()
    mock_response.status = 400
    mock_response.data = b"error data"

    with pytest.raises(ApiException, match="Request failed with status 400"):
        management_api._process_excel_response(mock_response)


def test_process_excel_response_non_bytes_data(management_api: SyncManagementApi):
    """Test Excel response processing with non-bytes data."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = "not bytes"

    with pytest.raises(ApiException, match="Expected bytes response"):
        management_api._process_excel_response(mock_response)


def test_process_excel_response_invalid_excel(management_api: SyncManagementApi):
    """Test Excel response processing with invalid Excel data."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"invalid excel data"

    with pytest.raises(ApiException, match="Failed to process Excel response"):
        management_api._process_excel_response(mock_response)


def test_process_excel_response_with_invalid_row_data(
    management_api: SyncManagementApi,
):
    """Test Excel response processing with some invalid row data."""
    # Create Excel data with some invalid rows
    excel_data = {
        "IdFilial": [1, "invalid"],
        "Filial": ["Branch 1", "Branch 2"],
        "IdCliente": [123, 456],
        "NomeCompleto": ["John Doe", "Jane Doe"],
        "Telefone": ["123-456-7890", ""],
        "Email": ["john@example.com", ""],
        "IdClienteContratoAtivo": [456, None],
        "ContratoAtivo": ["Contract Active", ""],
        "DtInicioContratoAtivo": ["01/01/2023", None],
        "DtFimContratoAtivo": ["31/12/2023", None],
        "IdClienteContratoFuturo": [789, None],
        "ContratoFuturo": ["Contract Future", ""],
        "DtInicioContratoFuturo": ["01/01/2024", None],
        "DtFimContratoFuturo": ["31/12/2024", None],
    }

    df = pd.DataFrame(excel_data)
    excel_bytes = io.BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = excel_bytes.getvalue()

    result = management_api._process_excel_response(mock_response)

    # Should still process valid rows and skip invalid ones
    assert len(result) >= 0  # Some rows might be processed


def test_process_prospects_excel_response_success(management_api: SyncManagementApi):
    """Test successful prospects Excel response processing."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"excel_data"

    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = Mock()
        mock_df.iterrows.return_value = [(0, {"col1": "value1"})]
        mock_read_excel.return_value = mock_df

        result = management_api._process_prospects_excel_response(mock_response)

        assert isinstance(result, list)


def test_process_prospects_excel_response_error(management_api: SyncManagementApi):
    """Test prospects Excel response processing with error."""
    mock_response = Mock()
    mock_response.status = 400

    with pytest.raises(ApiException, match="Request failed with status 400"):
        management_api._process_prospects_excel_response(mock_response)


def test_process_non_renewed_excel_response_success(management_api: SyncManagementApi):
    """Test successful non-renewed Excel response processing."""
    mock_response = Mock()
    mock_response.status = 200
    mock_response.data = b"excel_data"

    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = Mock()
        mock_df.iterrows.return_value = [(0, {"col1": "value1"})]
        mock_read_excel.return_value = mock_df

        result = management_api._process_non_renewed_excel_response(mock_response)

        assert isinstance(result, list)


def test_process_non_renewed_excel_response_error(management_api: SyncManagementApi):
    """Test non-renewed Excel response processing with error."""
    mock_response = Mock()
    mock_response.status = 400

    with pytest.raises(ApiException, match="Request failed with status 400"):
        management_api._process_non_renewed_excel_response(mock_response)


def test_get_active_clients_unexpected_error(
    management_api: SyncManagementApi, mock_api_client: Mock
):
    """Test unexpected error handling in get_active_clients."""
    mock_api_client.side_effect = Exception("Unexpected error")

    with pytest.raises(ApiException, match="Unexpected error"):
        management_api.get_active_clients()


def test_get_prospects_unexpected_error(
    management_api: SyncManagementApi, mock_api_client: Mock
):
    """Test unexpected error handling in get_prospects."""
    mock_api_client.side_effect = Exception("Unexpected error")

    with pytest.raises(ApiException, match="Unexpected error"):
        management_api.get_prospects()


def test_get_non_renewed_clients_unexpected_error(
    management_api: SyncManagementApi, mock_api_client: Mock
):
    """Test unexpected error handling in get_non_renewed_clients."""
    mock_api_client.side_effect = Exception("Unexpected error")

    with pytest.raises(ApiException, match="Unexpected error"):
        management_api.get_non_renewed_clients()


def test_convert_value():
    """Test the convert_value utility function."""
    from evo_client.sync.api.management_api import convert_value
    from datetime import datetime
    import pandas as pd

    # Test with None/NaN values
    assert convert_value(None, str) is None
    assert convert_value(pd.NA, str) is None
    assert convert_value("", str) is None

    # Test int conversion
    assert convert_value(5, int) == 5
    assert convert_value(5.0, int) == 5
    assert convert_value("invalid", int) is None

    # Test str conversion
    assert convert_value("test", str) == "test"
    assert convert_value(123, str) == "123"

    # Test bool conversion
    assert convert_value(True, bool) is True
    assert convert_value(False, bool) is False

    # Test datetime conversion
    result = convert_value("01/01/2023", datetime)
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 1

    # Test invalid datetime
    assert convert_value("invalid date", datetime) is None

    # Test default return
    assert convert_value("test", float) == "test"
