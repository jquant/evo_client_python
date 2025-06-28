"""Tests for the SyncEmployeesApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncEmployeesApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.employee_api_integracao_view_model import (
    EmployeeApiIntegracaoViewModel,
)
from evo_client.models.employee_api_integracao_atualizacao_view_model import (
    EmployeeApiIntegracaoAtualizacaoViewModel,
)
from evo_client.models.funcionarios_resumo_api_view_model import (
    FuncionariosResumoApiViewModel,
)
from evo_client.models.common_models import EmployeeOperationResponse


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def employees_api(sync_client):
    """Create a SyncEmployeesApi instance for testing."""
    return SyncEmployeesApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_employees_basic(employees_api: SyncEmployeesApi, mock_api_client: Mock):
    """Test getting employees without filters."""
    expected = [FuncionariosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = employees_api.get_employees()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/employees"


def test_get_employees_with_filters(
    employees_api: SyncEmployeesApi, mock_api_client: Mock
):
    """Test getting employees with various filters."""
    expected = [FuncionariosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = employees_api.get_employees(
        employee_id=123,
        name="John",
        take=50,
        skip=0,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/employees"
    query_params = args["query_params"]
    assert query_params["idEmployee"] == 123
    assert query_params["name"] == "John"
    assert query_params["take"] == 50
    assert query_params["skip"] == 0


def test_create_employee(employees_api: SyncEmployeesApi, mock_api_client: Mock):
    """Test creating a new employee."""
    expected = {"id": 123}
    mock_api_client.return_value = expected
    employee_data = EmployeeApiIntegracaoAtualizacaoViewModel()

    result = employees_api.create_employee(employee=employee_data)

    # The API creates its own EmployeeOperationResponse, not validating the raw response
    assert isinstance(result, EmployeeOperationResponse)
    assert result.success is True
    assert result.operation_type == "create"
    assert result.message == "Employee created successfully"
    assert result.employee_id == 123  # Extracted from the mocked API response

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["body"] == employee_data.model_dump(exclude_unset=True, by_alias=True)


def test_update_employee(employees_api: SyncEmployeesApi, mock_api_client: Mock):
    """Test updating an employee."""
    expected = {"id": 123}
    mock_api_client.return_value = expected
    employee_data = EmployeeApiIntegracaoViewModel()

    result = employees_api.update_employee(employee=employee_data)

    # The API creates its own EmployeeOperationResponse, not validating the raw response
    assert isinstance(result, EmployeeOperationResponse)
    assert result.success is True
    assert result.operation_type == "update"
    assert result.message == "Employee updated successfully"

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["body"] == employee_data.model_dump(exclude_unset=True, by_alias=True)


def test_delete_employee(employees_api: SyncEmployeesApi, mock_api_client: Mock):
    """Test deleting an employee."""
    expected = {"success": True}
    mock_api_client.return_value = expected

    result = employees_api.delete_employee(employee_id=123)

    # The API creates its own EmployeeOperationResponse, not validating the raw response
    assert isinstance(result, EmployeeOperationResponse)
    assert result.success is True
    assert result.operation_type == "delete"
    assert result.message == "Employee deleted successfully"
    assert result.employee_id == 123

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["query_params"]["idEmployee"] == 123


def test_error_handling(employees_api: SyncEmployeesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        employees_api.get_employees()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
