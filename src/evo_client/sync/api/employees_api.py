"""Clean synchronous Employees API."""

from typing import Any, List, Optional, cast

from ...models.common_models import EmployeeOperationResponse
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
        self.base_path_v2 = "/api/v2/employees"

    def get_employees(
        self,
        name: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        employee_id: Optional[int] = None,
        email: Optional[str] = None,
    ) -> List[FuncionariosResumoApiViewModel]:
        """
        Get employees with filtering options.

        Args:
            name: Filter by employee name
            take: Number of records to return (max 50)
            skip: Number of records to skip
            active: Filter by active status
            employee_id: Filter by specific employee ID
            email: Filter by employee email

        Returns:
            List of employee objects

        Example:
            >>> api = SyncEmployeesApi()
            >>> employees = api.get_employees(active=True, take=10)
            >>> for emp in employees:
            ...     print(f"{emp.name} - {emp.function}")
        """
        params = {
            "name": name,
            "take": take,
            "skip": skip,
            "active": active,
            "idEmployee": employee_id,
            "email": email,
        }

        result: Any = self.api_client.call_api(
            resource_path=self.base_path_v2,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[FuncionariosResumoApiViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[FuncionariosResumoApiViewModel], result)

    def delete_employee(self, employee_id: int) -> EmployeeOperationResponse:
        """
        Delete an employee.

        Args:
            employee_id: ID of employee to delete

        Returns:
            Deletion result with success status

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     result = api.delete_employee(employee_id=123)
            ...     if result.success:
            ...         print("Employee deleted successfully")
        """
        try:
            self.api_client.call_api(
                resource_path=self.base_path,
                method="DELETE",
                query_params={"idEmployee": employee_id},
                auth_settings=["Basic"],
                headers={"Accept": "application/json"},
            )

            return EmployeeOperationResponse(
                success=True,
                employeeId=employee_id,
                message="Employee deleted successfully",
                operationType="delete",
            )
        except Exception as e:
            return EmployeeOperationResponse(
                success=False,
                employeeId=employee_id,
                message=f"Error deleting employee: {str(e)}",
                operationType="delete",
                errors=[str(e)],
            )

    def update_employee(
        self, employee: EmployeeApiIntegracaoViewModel
    ) -> EmployeeOperationResponse:
        """
        Update an existing employee.

        Args:
            employee: Employee data to update

        Returns:
            Update result with success status

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     employee_data = EmployeeApiIntegracaoViewModel(
            ...         id=123,
            ...         name="John Updated",
            ...         email="john.updated@example.com"
            ...     )
            ...     result = api.update_employee(employee_data)
            ...     if result.success:
            ...         print("Employee updated successfully")
        """
        try:
            self.api_client.call_api(
                resource_path=self.base_path,
                method="POST",
                body=employee.model_dump(exclude_unset=True, by_alias=True),
                headers={
                    "Accept": ["text/plain", "application/json", "text/json"],
                    "Content-Type": ["application/json"],
                },
                auth_settings=["Basic"],
            )

            # Extract employee ID from the input model
            employee_id = getattr(employee, "id", None) or getattr(
                employee, "idEmployee", None
            )

            return EmployeeOperationResponse(
                success=True,
                employeeId=employee_id,
                message="Employee updated successfully",
                operationType="update",
            )
        except Exception as e:
            employee_id = getattr(employee, "id", None) or getattr(
                employee, "idEmployee", None
            )
            return EmployeeOperationResponse(
                success=False,
                employeeId=employee_id,
                message=f"Error updating employee: {str(e)}",
                operationType="update",
                errors=[str(e)],
            )

    def add_employee(
        self, employee: EmployeeApiIntegracaoAtualizacaoViewModel
    ) -> EmployeeOperationResponse:
        """
        Add a new employee.

        Args:
            employee: Employee data to add

        Returns:
            Created employee result with success status

        Example:
            >>> with SyncEmployeesApi() as api:
            ...     employee_data = EmployeeApiIntegracaoAtualizacaoViewModel(
            ...         name="Jane Doe",
            ...         email="jane.doe@example.com",
            ...         department="HR"
            ...     )
            ...     result = api.add_employee(employee_data)
            ...     if result.success:
            ...         print("Employee created successfully")
        """
        try:
            result: Any = self.api_client.call_api(
                resource_path=self.base_path,
                method="PUT",
                body=employee.model_dump(exclude_unset=True, by_alias=True),
                headers={
                    "Accept": ["text/plain", "application/json", "text/json"],
                    "Content-Type": ["application/json"],
                },
                auth_settings=["Basic"],
            )

            # Extract employee ID from result if available
            employee_id = None
            if isinstance(result, dict):
                employee_id = (
                    result.get("id")
                    or result.get("idEmployee")
                    or result.get("employeeId")
                )

            return EmployeeOperationResponse(
                success=True,
                employeeId=employee_id,
                message="Employee created successfully",
                operationType="create",
            )
        except Exception as e:
            return EmployeeOperationResponse(
                success=False,
                message=f"Error creating employee: {str(e)}",
                operationType="create",
                errors=[str(e)],
            )
