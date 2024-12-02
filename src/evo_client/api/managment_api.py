from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.clientes_ativos_view_model import ClientesAtivosViewModel
from ..models.contrato_nao_renovados_view_model import ContratoNaoRenovadosViewModel
from ..models.sps_rel_prospects_cadastrados_convertidos import (
    SpsRelProspectsCadastradosConvertidos,
)


class ManagementApi:
    """Management API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/management"

    @overload
    def get_active_clients(
        self, async_req: Literal[False] = False
    ) -> List[ClientesAtivosViewModel]: ...

    @overload
    def get_active_clients(
        self, async_req: Literal[True] = True
    ) -> AsyncResult[Any]: ...

    def get_active_clients(
        self, async_req: bool = False
    ) -> Union[List[ClientesAtivosViewModel], AsyncResult[Any]]:
        """
        Get active clients.

        Args:
            async_req: Execute request asynchronously

        Returns:
            List of active clients or AsyncResult[Any] if async
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/activeclients",
            method="GET",
            response_type=List[ClientesAtivosViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_prospects(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> List[SpsRelProspectsCadastradosConvertidos]: ...

    @overload
    def get_prospects(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_prospects(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[SpsRelProspectsCadastradosConvertidos], AsyncResult[Any]]:
        """
        Get prospects within date range.

        Args:
            dt_start: Start date filter
            dt_end: End date filter
            async_req: Execute request asynchronously

        Returns:
            List of prospects or AsyncResult[Any] if async
        """
        params = {"dtStart": dt_start, "dtEnd": dt_end}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/prospects",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[SpsRelProspectsCadastradosConvertidos],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_non_renewed_clients(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> List[ContratoNaoRenovadosViewModel]: ...

    @overload
    def get_non_renewed_clients(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_non_renewed_clients(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[ContratoNaoRenovadosViewModel], AsyncResult[Any]]:
        """
        Get non-renewed clients within date range.

        Args:
            dt_start: Start date filter
            dt_end: End date filter
            async_req: Execute request asynchronously

        Returns:
            List of non-renewed clients or AsyncResult[Any] if async
        """
        params = {"dtStart": dt_start, "dtEnd": dt_end}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/not-renewed",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ContratoNaoRenovadosViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )
