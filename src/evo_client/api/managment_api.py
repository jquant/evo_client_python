from datetime import datetime
from io import BytesIO
from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

import pandas as pd
from loguru import logger

from ..core.api_client import ApiClient
from ..exceptions.api_exceptions import ApiException
from ..models.clientes_ativos_view_model import ClientesAtivosViewModel
from ..models.contrato_nao_renovados_view_model import ContratoNaoRenovadosViewModel
from ..models.sps_rel_prospects_cadastrados_convertidos import (
    SpsRelProspectsCadastradosConvertidos,
)
from .base import BaseApi


def convert_value(value: Any, expected_type: type) -> Any:
    """Convert a value to the expected type, handling None and empty values."""
    if pd.isna(value) or value == "":
        return None

    try:
        if expected_type is int:
            # Handle float values from Excel
            return int(float(value)) if value is not None else None
        elif expected_type is str:
            return str(value) if value is not None else None
        elif expected_type is bool:
            return bool(value) if value is not None else None
        elif expected_type is datetime:
            if value is not None:
                # Explicitly specify the date format and set dayfirst=True for Brazilian date format
                return pd.to_datetime(
                    value, format="%d/%m/%Y", dayfirst=True
                ).to_pydatetime()
            return None
        return value
    except (ValueError, TypeError):
        return None


class ManagementApi(BaseApi):
    """Management API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = (
            "/api/v1/managment"  # Note: API uses 'managment' without the 'e'
        )

    @overload
    def get_active_clients(
        self, async_req: Literal[False] = False
    ) -> List[ClientesAtivosViewModel]:
        ...

    @overload
    def get_active_clients(self, async_req: Literal[True] = True) -> AsyncResult[Any]:
        ...

    def get_active_clients(
        self, async_req: bool = False
    ) -> Union[List[ClientesAtivosViewModel], AsyncResult[Any]]:
        """Get active clients."""
        try:
            logger.debug("Calling active clients API")
            logger.debug(f"Using base path: {self.base_path}")

            # Add debug headers
            headers = {
                "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Accept Excel files only
            }
            logger.debug(f"Request headers: {headers}")

            # Make API call and get response directly
            response = self.api_client.call_api(
                resource_path=f"{self.base_path}/activeclients",
                method="GET",
                headers=headers,
            )

            # For async requests, wrap the Excel processing in a ThreadPool
            if async_req:
                return self.api_client.request_handler.pool.apply_async(
                    self._process_excel_response, args=(response,)
                )

            return self._process_excel_response(response)

        except Exception as e:
            logger.error(f"Unexpected error in get_active_clients: {str(e)}")
            raise ApiException(f"Unexpected error: {str(e)}")

    def _process_excel_response(self, response: Any) -> List[ClientesAtivosViewModel]:
        """Process Excel response for active clients."""
        try:
            if response.status != 200:
                raise ApiException(f"Request failed with status {response.status}")

            # Get raw response data
            raw_data = response.data
            if not isinstance(raw_data, bytes):
                raise ApiException("Expected bytes response")

            # Read Excel data directly from bytes
            df = pd.read_excel(BytesIO(raw_data))
            logger.debug(f"Excel columns: {df.columns.tolist()}")

            # Define expected types for each field
            field_types = {
                "IdFilial": int,
                "Filial": str,
                "IdCliente": int,
                "NomeCompleto": str,
                "Telefone": str,
                "Email": str,
                "IdClienteContratoAtivo": int,
                "ContratoAtivo": str,
                "DtInicioContratoAtivo": datetime,
                "DtFimContratoAtivo": datetime,
                "IdClienteContratoFuturo": int,
                "ContratoFuturo": str,
                "DtInicioContratoFuturo": datetime,
                "DtFimContratoFuturo": datetime,
            }

            # Convert DataFrame rows to model instances
            result = []
            for _, row in df.iterrows():
                try:
                    # Convert row to dict with proper type conversion and field name mapping
                    row_dict = {}
                    for api_field, value in row.to_dict().items():
                        # Map API field names to model field names
                        model_field = {
                            "IdFilial": "idFilial",
                            "Filial": "filial",
                            "IdCliente": "idCliente",
                            "NomeCompleto": "nomeCompleto",
                            "Telefone": "telefone",
                            "Email": "email",
                            "IdClienteContratoAtivo": "idClienteContratoAtivo",
                            "ContratoAtivo": "contratoAtivo",
                            "DtInicioContratoAtivo": "dtInicioContratoAtivo",
                            "DtFimContratoAtivo": "dtFimContratoAtivo",
                            "IdClienteContratoFuturo": "idClienteContratoFuturo",
                            "ContratoFuturo": "contratoFuturo",
                            "DtInicioContratoFuturo": "dtInicioContratoFuturo",
                            "DtFimContratoFuturo": "dtFimContratoFuturo",
                        }.get(api_field)

                        if model_field:  # Only include fields we know about
                            row_dict[model_field] = convert_value(
                                value, field_types.get(api_field, str)
                            )

                    # Create model instance
                    model = ClientesAtivosViewModel(**row_dict)
                    result.append(model)

                except Exception as e:
                    logger.warning(f"Failed to convert row to model: {str(e)}")
                    logger.warning(f"Row data: {row_dict}")
                    continue

            return result

        except Exception as e:
            logger.error(f"Failed to process Excel response: {str(e)}")
            raise ApiException(f"Failed to process Excel response: {str(e)}")

    def _process_prospects_excel_response(
        self, response: Any
    ) -> List[SpsRelProspectsCadastradosConvertidos]:
        """Process Excel response for prospects."""
        try:
            if response.status != 200:
                raise ApiException(f"Request failed with status {response.status}")

            # Get raw response data
            raw_data = response.data
            if not isinstance(raw_data, bytes):
                raise ApiException("Expected bytes response")

            # Read Excel data directly from bytes
            df = pd.read_excel(BytesIO(raw_data))
            logger.debug(f"Excel columns: {df.columns.tolist()}")

            # Convert DataFrame rows to model instances
            result = []
            for _, row in df.iterrows():
                try:
                    # Create model instance directly from row data
                    model = SpsRelProspectsCadastradosConvertidos(**row.to_dict())
                    result.append(model)
                except Exception as e:
                    logger.warning(f"Failed to convert row to model: {str(e)}")
                    continue

            return result

        except Exception as e:
            logger.error(f"Failed to process Excel response: {str(e)}")
            raise ApiException(f"Failed to process Excel response: {str(e)}")

    def _process_non_renewed_excel_response(
        self, response: Any
    ) -> List[ContratoNaoRenovadosViewModel]:
        """Process Excel response for non-renewed clients."""
        try:
            if response.status != 200:
                raise ApiException(f"Request failed with status {response.status}")

            # Get raw response data
            raw_data = response.data
            if not isinstance(raw_data, bytes):
                raise ApiException("Expected bytes response")

            # Read Excel data directly from bytes
            df = pd.read_excel(BytesIO(raw_data))
            logger.debug(f"Excel columns: {df.columns.tolist()}")

            # Convert DataFrame rows to model instances
            result = []
            for _, row in df.iterrows():
                try:
                    # Create model instance directly from row data
                    model = ContratoNaoRenovadosViewModel(**row.to_dict())
                    result.append(model)
                except Exception as e:
                    logger.warning(f"Failed to convert row to model: {str(e)}")
                    continue

            return result

        except Exception as e:
            logger.error(f"Failed to process Excel response: {str(e)}")
            raise ApiException(f"Failed to process Excel response: {str(e)}")

    @overload
    def get_prospects(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> List[SpsRelProspectsCadastradosConvertidos]:
        ...

    @overload
    def get_prospects(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    def get_prospects(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[SpsRelProspectsCadastradosConvertidos], AsyncResult[Any]]:
        """Get prospects."""
        try:
            logger.debug("Calling prospects API")

            # Add query parameters
            params = {"dtStart": dt_start, "dtEnd": dt_end}

            # Add debug headers
            headers = {
                "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Accept Excel files
            }
            logger.debug(f"Request headers: {headers}")

            # Make API call and get response directly
            response = self.api_client.call_api(
                resource_path=f"{self.base_path}/prospects",
                method="GET",
                headers=headers,
                query_params={k: v for k, v in params.items() if v is not None},
            )

            # For async requests, wrap the Excel processing in a ThreadPool
            if async_req:
                return self.api_client.request_handler.pool.apply_async(
                    self._process_prospects_excel_response, args=(response,)
                )

            return self._process_prospects_excel_response(response)

        except Exception as e:
            logger.error(f"Unexpected error in get_prospects: {str(e)}")
            raise ApiException(f"Unexpected error: {str(e)}")

    @overload
    def get_non_renewed_clients(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> List[ContratoNaoRenovadosViewModel]:
        ...

    @overload
    def get_non_renewed_clients(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    def get_non_renewed_clients(
        self,
        dt_start: Optional[datetime] = None,
        dt_end: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[ContratoNaoRenovadosViewModel], AsyncResult[Any]]:
        """Get non-renewed clients."""
        try:
            logger.debug("Calling non-renewed clients API")

            # Add query parameters
            params = {"dtStart": dt_start, "dtEnd": dt_end}

            # Add debug headers
            headers = {
                "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Accept Excel files
            }
            logger.debug(f"Request headers: {headers}")

            # Make API call and get response directly
            response = self.api_client.call_api(
                resource_path=f"{self.base_path}/not-renewed",
                method="GET",
                headers=headers,
                query_params={k: v for k, v in params.items() if v is not None},
            )

            # For async requests, wrap the Excel processing in a ThreadPool
            if async_req:
                return self.api_client.request_handler.pool.apply_async(
                    self._process_non_renewed_excel_response, args=(response,)
                )

            return self._process_non_renewed_excel_response(response)

        except Exception as e:
            logger.error(f"Unexpected error in get_non_renewed_clients: {str(e)}")
            raise ApiException(f"Unexpected error: {str(e)}")
