"""Clean synchronous Configuration API."""

from typing import Any, List, cast

from ...models.bandeiras_basico_view_model import BandeirasBasicoViewModel
from ...models.configuracao_api_view_model import ConfiguracaoApiViewModel
from ...models.empresas_filiais_gateway_view_model import (
    EmpresasFiliaisGatewayViewModel,
)
from ...models.empresas_filiais_ocupacao_view_model import (
    EmpresasFiliaisOcupacaoViewModel,
)
from .base import SyncBaseApi


class SyncConfigurationApi(SyncBaseApi):
    """Clean synchronous Configuration API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/configuration"

    def get_gateway_config(self) -> EmpresasFiliaisGatewayViewModel:
        """
        Get gateway configurations.

        Returns:
            Gateway configuration data including payment settings,
            merchant information, and integration details

        Example:
            >>> with SyncConfigurationApi() as api:
            ...     gateway_config = api.get_gateway_config()
            ...     print(f"Gateway: {gateway_config.merchant_id}")
            ...     print(f"Payment methods: {gateway_config.payment_methods}")
        """
        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/gateway",
            method="GET",
            response_type=EmpresasFiliaisGatewayViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(EmpresasFiliaisGatewayViewModel, result)

    def get_branch_config(self) -> List[ConfiguracaoApiViewModel]:
        """
        Get branch configurations.

        Returns:
            List of branch configurations including:
            - Branch settings and preferences
            - Operating hours and schedules
            - Feature flags and customizations
            - Integration settings

        Example:
            >>> with SyncConfigurationApi() as api:
            ...     branch_configs = api.get_branch_config()
            ...     for config in branch_configs:
            ...         print(f"Branch: {config.branch_name}")
            ...         print(f"Settings: {config.settings}")
        """
        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            response_type=List[ConfiguracaoApiViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[ConfiguracaoApiViewModel], result)

    def get_occupations(self) -> List[EmpresasFiliaisOcupacaoViewModel]:
        """
        Get occupation configurations.

        Returns:
            List of occupation configurations including:
            - Available occupation types
            - Job categories and descriptions
            - Role-based permissions
            - Department assignments

        Example:
            >>> with SyncConfigurationApi() as api:
            ...     occupations = api.get_occupations()
            ...     for occupation in occupations:
            ...         print(f"Occupation: {occupation.name}")
            ...         print(f"Department: {occupation.department}")
        """
        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/occupation",
            method="GET",
            response_type=List[EmpresasFiliaisOcupacaoViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[EmpresasFiliaisOcupacaoViewModel], result)

    def get_card_flags(self) -> List[BandeirasBasicoViewModel]:
        """
        Get card flags.

        Returns:
            List of supported credit/debit card flags including:
            - Card brand information (Visa, MasterCard, etc.)
            - Acceptance status and settings
            - Processing fees and configurations

        Example:
            >>> with SyncConfigurationApi() as api:
            ...     card_flags = api.get_card_flags()
            ...     for flag in card_flags:
            ...         print(f"Card: {flag.name}")
            ...         print(f"Accepted: {flag.accepted}")
        """
        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/card-flags",
            method="GET",
            response_type=List[BandeirasBasicoViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[BandeirasBasicoViewModel], result)

    def get_translations(self) -> Any:
        """
        Get card translations.

        Returns:
            Translation dictionary containing localized text
            for card-related terms and messages

        Example:
            >>> with SyncConfigurationApi() as api:
            ...     translations = api.get_translations()
            ...     print(f"Available languages: {translations.keys()}")
            ...     for lang, terms in translations.items():
            ...         print(f"{lang}: {terms}")
        """
        result: Any = self.api_client.call_api(
            resource_path=f"{self.base_path}/card-translation",
            method="GET",
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return result
