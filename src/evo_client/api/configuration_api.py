# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

from multiprocessing.pool import AsyncResult
from typing import Any, Dict, List, Optional, Union, overload

from evo_client.core.api_client import ApiClient

from ..models.bandeiras_basico_view_model import BandeirasBasicoViewModel
from ..models.configuracao_api_view_model import ConfiguracaoApiViewModel
from ..models.empresas_filiais_gateway_view_model import EmpresasFiliaisGatewayViewModel
from ..models.empresas_filiais_ocupacao_view_model import (
    EmpresasFiliaisOcupacaoViewModel,
)


class ConfigurationApi:
    """Configuration API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/configuration"

    @overload
    def get_gateway_config(
        self, async_req: bool = True
    ) -> Union[EmpresasFiliaisGatewayViewModel, AsyncResult[Any]]:
        ...

    @overload
    def get_gateway_config(
        self, async_req: bool = False
    ) -> EmpresasFiliaisGatewayViewModel:
        ...

    def get_gateway_config(
        self, async_req: bool = False
    ) -> Union[EmpresasFiliaisGatewayViewModel, AsyncResult[Any]]:
        """
        Get gateway configurations.

        Args:
            async_req: Execute request asynchronously

        Returns:
            Gateway configuration or AsyncResult[Any] if async
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/gateway",
            method="GET",
            response_type=EmpresasFiliaisGatewayViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_branch_config(
        self, async_req: bool = True
    ) -> Union[ConfiguracaoApiViewModel, AsyncResult[Any]]:
        ...

    @overload
    def get_branch_config(self, async_req: bool = False) -> ConfiguracaoApiViewModel:
        ...

    def get_branch_config(
        self, async_req: bool = False
    ) -> Union[ConfiguracaoApiViewModel, AsyncResult[Any]]:
        """
        Get branch configurations.

        Args:
            async_req: Execute request asynchronously

        Returns:
            Branch configuration or AsyncResult[Any] if async
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            response_type=ConfiguracaoApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_occupations(
        self, async_req: bool = True
    ) -> Union[List[EmpresasFiliaisOcupacaoViewModel], AsyncResult[Any]]:
        ...

    @overload
    def get_occupations(
        self, async_req: bool = False
    ) -> List[EmpresasFiliaisOcupacaoViewModel]:
        ...

    def get_occupations(
        self, async_req: bool = True
    ) -> Union[List[EmpresasFiliaisOcupacaoViewModel], AsyncResult[Any]]:
        """
        Get occupation configurations.

        Args:
            async_req: Execute request asynchronously

        Returns:
            List of occupation configurations or AsyncResult[Any] if async
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/occupation",
            method="GET",
            response_type=List[EmpresasFiliaisOcupacaoViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_card_flags(
        self, async_req: bool = True
    ) -> Union[List[BandeirasBasicoViewModel], AsyncResult[Any]]:
        ...

    @overload
    def get_card_flags(self, async_req: bool = False) -> List[BandeirasBasicoViewModel]:
        ...

    def get_card_flags(
        self, async_req: bool = False
    ) -> Union[List[BandeirasBasicoViewModel], AsyncResult[Any]]:
        """
        Get card flags.

        Args:
            async_req: Execute request asynchronously

        Returns:
            List of card flags or AsyncResult[Any] if async
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/card-flags",
            method="GET",
            response_type=List[BandeirasBasicoViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_translations(
        self, async_req: bool = True
    ) -> Union[Dict[str, Any], AsyncResult[Any]]:
        ...

    @overload
    def get_translations(self, async_req: bool = False) -> Dict[str, Any]:
        ...

    def get_translations(
        self, async_req: bool = False
    ) -> Union[Dict[str, Any], AsyncResult[Any]]:
        """
        Get card translations.

        Args:
            async_req: Execute request asynchronously

        Returns:
            Translation dictionary or AsyncResult[Any] if async
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/card-translation",
            method="GET",
            response_type=Dict[str, Any],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )
