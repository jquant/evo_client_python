from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.member_service_view_model import MemberServiceViewModel
from ..models.prospect_api_integracao_atualizacao_view_model import (
    ProspectApiIntegracaoAtualizacaoViewModel,
)
from ..models.prospect_api_integracao_view_model import ProspectApiIntegracaoViewModel
from ..models.prospect_id_view_model import ProspectIdViewModel
from ..models.prospect_transferencia_view_model import ProspectTransferenciaViewModel
from ..models.prospects_resumo_api_view_model import ProspectsResumoApiViewModel


class ProspectsApi:
    """Prospects API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/prospects"

    @overload
    def get_prospects(
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
        async_req: bool = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def get_prospects(
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
        async_req: bool = False,
    ) -> List[ProspectsResumoApiViewModel]:
        ...

    def get_prospects(
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
        async_req: bool = False,
    ) -> Union[List[ProspectsResumoApiViewModel], AsyncResult[Any]]:
        """
        Get prospects with optional filtering.

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
            async_req: Execute request asynchronously
        """
        params = {
            "idProspect": prospect_id,
            "name": name,
            "document": document,
            "email": email,
            "phone": phone,
            "registerDateStart": register_date_start,
            "registerDateEnd": register_date_end,
            "conversionDateStart": conversion_date_start,
            "conversionDateEnd": conversion_date_end,
            "take": take,
            "skip": skip,
            "gympassId": gympass_id,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ProspectsResumoApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def create_prospect(
        self, prospect: ProspectApiIntegracaoViewModel, async_req: bool = True
    ) -> AsyncResult[Any]:
        ...

    @overload
    def create_prospect(
        self, prospect: ProspectApiIntegracaoViewModel, async_req: bool = False
    ) -> ProspectIdViewModel:
        ...

    def create_prospect(
        self, prospect: ProspectApiIntegracaoViewModel, async_req: bool = False
    ) -> Union[ProspectIdViewModel, AsyncResult[Any]]:
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
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=prospect,
            response_type=ProspectIdViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def update_prospect(
        self,
        prospect: ProspectApiIntegracaoAtualizacaoViewModel,
        async_req: bool = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def update_prospect(
        self,
        prospect: ProspectApiIntegracaoAtualizacaoViewModel,
        async_req: bool = False,
    ) -> ProspectIdViewModel:
        ...

    def update_prospect(
        self,
        prospect: ProspectApiIntegracaoAtualizacaoViewModel,
        async_req: bool = False,
    ) -> Union[ProspectIdViewModel, AsyncResult[Any]]:
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
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="PUT",
            body=prospect,
            response_type=ProspectIdViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_services(
        self, prospect_id: Optional[int] = None, async_req: bool = True
    ) -> AsyncResult[Any]:
        ...

    @overload
    def get_services(
        self, prospect_id: Optional[int] = None, async_req: bool = False
    ) -> List[MemberServiceViewModel]:
        ...

    def get_services(
        self, prospect_id: Optional[int] = None, async_req: bool = False
    ) -> Union[List[MemberServiceViewModel], AsyncResult[Any]]:
        """
        Get prospect services.

        Args:
            prospect_id: Filter by prospect ID
            async_req: Execute request asynchronously
        """
        params = {"idProspect": prospect_id} if prospect_id else {}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/services",
            method="GET",
            query_params=params,
            response_type=List[MemberServiceViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def transfer_prospect(
        self, transfer: ProspectTransferenciaViewModel, async_req: bool = True
    ) -> AsyncResult[Any]:
        ...

    @overload
    def transfer_prospect(
        self, transfer: ProspectTransferenciaViewModel, async_req: bool = False
    ) -> Any:
        ...

    def transfer_prospect(
        self, transfer: ProspectTransferenciaViewModel, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Transfer a prospect.

        Args:
            transfer: Transfer details
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/transfer",
            method="POST",
            body=transfer,
            response_type=None,
            auth_settings=["Basic"],
            async_req=async_req,
        )
