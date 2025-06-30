"""Tests for the AsyncEmployeesApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncEmployeesApi
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
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def employees_api(async_client):
    """Create an AsyncEmployeesApi instance for testing."""
    return AsyncEmployeesApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_employees_basic(
    employees_api: AsyncEmployeesApi, mock_api_client: Mock
):
    """Test getting employees without filters."""
    expected = [FuncionariosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await employees_api.get_employees()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/employees"


@pytest.mark.asyncio
async def test_get_employees_with_filters(
    employees_api: AsyncEmployeesApi, mock_api_client: Mock
):
    """Test getting employees with various filters."""
    expected = [FuncionariosResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await employees_api.get_employees(
        employee_id=123,
        name="John",
        email="john@example.com",
        take=50,
        skip=0,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/employees"
    query_params = args["query_params"]
    assert query_params["idEmployee"] == 123
    assert query_params["name"] == "John"
    assert query_params["email"] == "john@example.com"
    assert query_params["take"] == 50
    assert query_params["skip"] == 0


@pytest.mark.asyncio
async def test_add_employee(employees_api: AsyncEmployeesApi, mock_api_client: Mock):
    """Test adding a new employee."""
    expected = {"id": 123}
    mock_api_client.return_value = expected
    employee_data = EmployeeApiIntegracaoAtualizacaoViewModel()

    result = await employees_api.add_employee(employee=employee_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["body"] == employee_data.model_dump(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_update_employee(employees_api: AsyncEmployeesApi, mock_api_client: Mock):
    """Test updating an employee."""
    expected = {"id": 123}
    mock_api_client.return_value = expected
    employee_data = EmployeeApiIntegracaoViewModel()

    result = await employees_api.update_employee(employee=employee_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["body"] == employee_data.model_dump(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_delete_employee(employees_api: AsyncEmployeesApi, mock_api_client: Mock):
    """Test deleting an employee."""
    expected = {"success": True}
    mock_api_client.return_value = expected

    result = await employees_api.delete_employee(employee_id=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "DELETE"
    assert args["resource_path"] == "/api/v1/employees"
    assert args["query_params"]["idEmployee"] == 123


@pytest.mark.asyncio
async def test_error_handling(employees_api: AsyncEmployeesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await employees_api.get_employees()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
