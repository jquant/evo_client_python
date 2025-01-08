"""Tests for the EmployeesApi class."""

from unittest.mock import Mock, patch

import pytest


from evo_client.api.employees_api import EmployeesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.employee_api_integracao_atualizacao_view_model import (
    EmployeeApiIntegracaoAtualizacaoViewModel,
)
from evo_client.models.employee_api_integracao_view_model import (
    EmployeeApiIntegracaoViewModel,
)
from evo_client.models.funcionarios_resumo_api_view_model import (
    FuncionariosResumoApiViewModel,
)


@pytest.fixture
def employees_api():
    """Create an EmployeesApi instance for testing."""
    return EmployeesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.employees_api.ApiClient.call_api") as mock:
        yield mock


def test_get_employees_basic(employees_api: EmployeesApi, mock_api_client: Mock):
    """Test getting employees list with no parameters."""
    expected = [FuncionariosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = employees_api.get_employees(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/employees"


def test_get_employees_with_filters(employees_api: EmployeesApi, mock_api_client: Mock):
    """Test getting employees with search filters."""
    expected = [FuncionariosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = employees_api.get_employees(
        employee_id=123,
        name="John",
        email="john@example.com",
        take=10,
        skip=0,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "idEmployee": 123,
        "name": "John",
        "email": "john@example.com",
        "take": 10,
        "skip": 0,
    }


def test_delete_employee(employees_api: EmployeesApi, mock_api_client: Mock):
    """Test deleting an employee."""
    mock_api_client.return_value = None

    await employees_api.delete_employee(employee_id=123, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["query_params"] == {"idEmployee": 123}


def test_update_employee(employees_api: EmployeesApi, mock_api_client: Mock):
    """Test updating an employee."""
    mock_api_client.return_value = None
    employee = EmployeeApiIntegracaoViewModel()

    await employees_api.update_employee(employee=employee, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["body"] == employee.model_dump(exclude_unset=True)


def test_create_employee(employees_api: EmployeesApi, mock_api_client: Mock):
    """Test creating a new employee."""
    mock_api_client.return_value = None
    employee = EmployeeApiIntegracaoAtualizacaoViewModel()

    await employees_api.create_employee(employee=employee, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["body"] == employee.model_dump(exclude_unset=True)


def test_error_handling(employees_api: EmployeesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await employees_api.get_employees(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
