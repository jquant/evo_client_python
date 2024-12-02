from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.employee_api_integracao_atualizacao_view_model import (
    EmployeeApiIntegracaoAtualizacaoViewModel,
)
from ..models.employee_api_integracao_view_model import EmployeeApiIntegracaoViewModel
from ..models.funcionarios_resumo_api_view_model import FuncionariosResumoApiViewModel


class EmployeesApi:
    """Employees API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/employees"

    @overload
    def get_employees(
        self,
        employee_id: Optional[int] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def get_employees(
        self,
        employee_id: Optional[int] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> List[FuncionariosResumoApiViewModel]:
        ...

    def get_employees(
        self,
        employee_id: Optional[int] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[List[FuncionariosResumoApiViewModel], AsyncResult[Any]]:
        """
        Get employees with optional filtering.

        Args:
            employee_id: Filter by employee ID
            name: Filter by name
            email: Filter by email
            take: Number of records to return
            skip: Number of records to skip
            async_req: Execute request asynchronously

        Returns:
            List of employees or AsyncResult[Any] if async
        """
        params = {
            "idEmployee": employee_id,
            "name": name,
            "email": email,
            "take": take,
            "skip": skip,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[FuncionariosResumoApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def delete_employee(
        self, employee_id: int, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    @overload
    def delete_employee(
        self, employee_id: int, async_req: Literal[False] = False
    ) -> Any:
        ...

    def delete_employee(
        self, employee_id: int, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Delete an employee.

        Args:
            employee_id: ID of employee to delete
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="DELETE",
            query_params={"idEmployee": employee_id},
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def update_employee(
        self, employee: EmployeeApiIntegracaoViewModel, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    @overload
    def update_employee(
        self,
        employee: EmployeeApiIntegracaoViewModel,
        async_req: Literal[False] = False,
    ) -> Any:
        ...

    def update_employee(
        self, employee: EmployeeApiIntegracaoViewModel, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Update an existing employee.

        Args:
            employee: Employee data to update
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=employee.model_dump(exclude_unset=True),
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

    @overload
    def create_employee(
        self,
        employee: EmployeeApiIntegracaoAtualizacaoViewModel,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def create_employee(
        self,
        employee: EmployeeApiIntegracaoAtualizacaoViewModel,
        async_req: Literal[False] = False,
    ) -> Union[Any, AsyncResult[Any]]:
        ...

    def create_employee(
        self,
        employee: EmployeeApiIntegracaoAtualizacaoViewModel,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Create a new employee.

        Args:
            employee: Employee data to create
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="PUT",
            body=employee.model_dump(exclude_unset=True),
            auth_settings=["Basic"],
            async_req=async_req,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
