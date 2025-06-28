"""Clean synchronous Employees API."""

from typing import Any, List, Optional, cast

from ...models.employee_api_integracao_atualizacao_view_model import (
    EmployeeApiIntegracaoAtualizacaoViewModel,
)
from ...models.employee_api_integracao_view_model import EmployeeApiIntegracaoViewModel
from ...models.funcionarios_resumo_api_view_model import FuncionariosResumoApiViewModel
from .base import SyncBaseApi


class SyncEmployeesApi(SyncBaseApi):
    """Clean synchronous Employees API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/employees"

    def get_employees(
        self,
        employee_id: Optional[int] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> List[FuncionariosResumoApiViewModel]:
        """
        Get employees with optional filtering.

        Args:
            employee_id: Filter by employee ID
            name: Filter by name
            email: Filter by email
            take: Number of records to return
            skip: Number of records to skip

        Returns:
            List of employees matching the criteria

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     employees = api.get_employees(
            ...         name="John",
            ...         take=10
            ...     )
            ...     for employee in employees:
            ...         print(f"Employee: {employee.name} - {employee.email}")
        """
        params = {
            "idEmployee": employee_id,
            "name": name,
            "email": email,
            "take": take,
            "skip": skip,
        }

        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[FuncionariosResumoApiViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[FuncionariosResumoApiViewModel], result)

    def delete_employee(self, employee_id: int) -> Any:
        """
        Delete an employee.

        Args:
            employee_id: ID of employee to delete

        Returns:
            Deletion result

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     result = api.delete_employee(employee_id=123)
            ...     print(f"Employee deleted: {result}")
        """
        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="DELETE",
            query_params={"idEmployee": employee_id},
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return result

    def update_employee(self, employee: EmployeeApiIntegracaoViewModel) -> Any:
        """
        Update an existing employee.

        Args:
            employee: Employee data to update

        Returns:
            Update result

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     employee_data = EmployeeApiIntegracaoViewModel(
            ...         id=123,
            ...         name="John Updated",
            ...         email="john.updated@example.com"
            ...     )
            ...     result = api.update_employee(employee_data)
            ...     print(f"Employee updated: {result}")
        """
        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=employee.model_dump(exclude_unset=True, by_alias=True),
            auth_settings=["Basic"],
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        return result

    def create_employee(
        self, employee: EmployeeApiIntegracaoAtualizacaoViewModel
    ) -> Any:
        """
        Create a new employee.

        Args:
            employee: Employee data to create

        Returns:
            Created employee result

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     employee_data = EmployeeApiIntegracaoAtualizacaoViewModel(
            ...         name="Jane Doe",
            ...         email="jane.doe@example.com",
            ...         department="HR"
            ...     )
            ...     result = api.create_employee(employee_data)
            ...     print(f"Employee created: {result}")
        """
        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="PUT",
            body=employee.model_dump(exclude_unset=True, by_alias=True),
            auth_settings=["Basic"],
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        return result
