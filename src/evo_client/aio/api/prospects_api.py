"""Clean asynchronous Prospects API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.member_service_view_model import MemberServiceViewModel
from ...models.prospect_api_integracao_atualizacao_view_model import (
    ProspectApiIntegracaoAtualizacaoViewModel,
)
from ...models.prospect_api_integracao_view_model import ProspectApiIntegracaoViewModel
from ...models.prospect_id_view_model import ProspectIdViewModel
from ...models.prospect_transferencia_view_model import ProspectTransferenciaViewModel
from ...models.prospects_resumo_api_view_model import ProspectsResumoApiViewModel
from .base import AsyncBaseApi


class AsyncProspectsApi(AsyncBaseApi):
    """Clean asynchronous Prospects API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/prospects"

    async def get_prospects(
        self,
        prospect_id: Optional[int] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        conversion_date_start: Optional[datetime] = None,
        conversion_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        gympass_id: Optional[str] = None,
    ) -> List[ProspectsResumoApiViewModel]:
        """
        Get prospects with comprehensive filtering options.

        Args:
            prospect_id: Filter by prospect ID
            name: Filter by name
            document: Filter by document
            email: Filter by email
            phone: Filter by phone
            register_date_start: Filter by registration start date
            register_date_end: Filter by registration end date
            conversion_date_start: Filter by conversion start date
            conversion_date_end: Filter by conversion end date
            take: Number of records to return (max 50)
            skip: Number of records to skip
            gympass_id: Filter by Gympass ID

        Returns:
            List of prospects matching the criteria

        Example:
            >>> async with AsyncProspectsApi() as api:
            ...     prospects = await api.get_prospects(
            ...         name="John",
            ...         register_date_start=datetime(2024, 1, 1),
            ...         take=20
            ...     )
            ...     for prospect in prospects:
            ...         print(f"Prospect: {prospect.name} - Email: {prospect.email}")
        """
        params = {
            "idProspect": prospect_id,
            "name": name,
            "document": document,
            "email": email,
            "phone": phone,
            "registerDateStart": (
                register_date_start.isoformat() if register_date_start else None
            ),
            "registerDateEnd": (
                register_date_end.isoformat() if register_date_end else None
            ),
            "conversionDateStart": (
                conversion_date_start.isoformat() if conversion_date_start else None
            ),
            "conversionDateEnd": (
                conversion_date_end.isoformat() if conversion_date_end else None
            ),
            "take": take,
            "skip": skip,
            "gympassId": gympass_id,
        }

        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ProspectsResumoApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[ProspectsResumoApiViewModel], result)

    async def create_prospect(
        self, prospect: ProspectApiIntegracaoViewModel
    ) -> ProspectIdViewModel:
        """
        Create a new prospect.

        Args:
            prospect: Prospect details including:
                - name (required): First name
                - email (required): Email address
                - lastName (optional): Last name
                - idBranch (optional): Branch ID
                - ddi (optional): Phone country code
                - cellphone (optional): Phone number
                - birthday (optional): Birth date
                - gender (optional): "M"=Male, "F"=Female, "P"=Other
                - visit (optional): Visit origin (1=Personal, 2=Email, 3=Telephone, 4=Other)
                - marketingType (optional): Marketing source
                - notes (optional): Additional notes
                - currentStep (optional): Current conversion step

        Returns:
            Created prospect ID and details

        Example:
            >>> async with AsyncProspectsApi() as api:
            ...     prospect_data = ProspectApiIntegracaoViewModel(
            ...         name="John",
            ...         lastName="Doe",
            ...         email="john.doe@example.com",
            ...         cellphone="5511999999999"
            ...     )
            ...     result = await api.create_prospect(prospect_data)
            ...     print(f"Created prospect with ID: {result.id}")
        """
        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=prospect.model_dump(exclude_unset=True, by_alias=True),
            response_type=ProspectIdViewModel,
            auth_settings=["Basic"],
        )
        return cast(ProspectIdViewModel, result)

    async def update_prospect(
        self, prospect: ProspectApiIntegracaoAtualizacaoViewModel
    ) -> ProspectIdViewModel:
        """
        Update an existing prospect.

        Args:
            prospect: Updated prospect details including:
                - idProspect (required): Prospect ID
                - name (required): First name
                - email (required): Email address
                - lastName (optional): Last name
                - ddi (optional): Phone country code
                - cellphone (optional): Phone number
                - birthday (optional): Birth date
                - gender (optional): "M"=Male, "F"=Female, "P"=Other
                - notes (optional): Additional notes
                - currentStep (optional): Current conversion step

        Returns:
            Updated prospect ID and details

        Example:
            >>> async with AsyncProspectsApi() as api:
            ...     prospect_data = ProspectApiIntegracaoAtualizacaoViewModel(
            ...         idProspect=12345,
            ...         name="John",
            ...         lastName="Smith",
            ...         email="john.smith@example.com"
            ...     )
            ...     result = await api.update_prospect(prospect_data)
            ...     print(f"Updated prospect ID: {result.id}")
        """
        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="PUT",
            body=prospect.model_dump(exclude_unset=True, by_alias=True),
            response_type=ProspectIdViewModel,
            auth_settings=["Basic"],
        )
        return cast(ProspectIdViewModel, result)

    async def get_services(
        self, prospect_id: Optional[int] = None
    ) -> List[MemberServiceViewModel]:
        """
        Get services available for prospects.

        Args:
            prospect_id: Optional prospect ID filter

        Returns:
            List of available services

        Example:
            >>> async with AsyncProspectsApi() as api:
            ...     services = await api.get_services(prospect_id=12345)
            ...     for service in services:
            ...         print(f"Service: {service.name} - Price: ${service.price}")
        """
        params = {
            "idProspect": prospect_id,
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/services",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[MemberServiceViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[MemberServiceViewModel], result)

    async def transfer_prospect(self, transfer: ProspectTransferenciaViewModel) -> Any:
        """
        Transfer a prospect to another branch.

        Args:
            transfer: Transfer details including prospect ID and target branch

        Returns:
            Transfer operation result

        Example:
            >>> async with AsyncProspectsApi() as api:
            ...     transfer_data = ProspectTransferenciaViewModel(
            ...         prospect_id=12345,
            ...         target_branch_id=67890
            ...     )
            ...     result = await api.transfer_prospect(transfer_data)
        """
        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/transfer",
            method="POST",
            body=transfer.model_dump(exclude_unset=True, by_alias=True),
            auth_settings=["Basic"],
        )

    async def get_prospects_latest_branch_transfer(self, prospect_id: int) -> Any:
        """
        Get the latest branch transfer for a prospect.

        Args:
            prospect_id: Prospect ID

        Returns:
            Latest branch transfer details

        Response example:
        {
            "idProspect": 0,
            "transferDate": "2025-06-30T06:12:27.418Z",
            "idBranchFrom": 0,
            "idBranchTo": 0,
            "idEmployeeTransfer": 0
        }
        """
        params = {
            "idProspect": prospect_id,
        }
        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/latest-transfer",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=None,
            auth_settings=["Basic"],
        )
