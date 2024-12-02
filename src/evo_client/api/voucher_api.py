from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel


class VoucherApi:
    """Voucher API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/voucher"

    @overload
    def get_vouchers(
        self,
        voucher_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        valid: Optional[bool] = None,
        voucher_type: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> List[VouchersResumoApiViewModel]: ...

    @overload
    def get_vouchers(
        self,
        voucher_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        valid: Optional[bool] = None,
        voucher_type: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_vouchers(
        self,
        voucher_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        valid: Optional[bool] = None,
        voucher_type: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[List[VouchersResumoApiViewModel], AsyncResult[Any]]:
        """
        Get vouchers with optional filtering.

        Args:
            voucher_id: Filter by specific voucher ID
            name: Filter by voucher name
            branch_id: Filter by branch ID (only for multilocation keys)
            take: Number of records to return (max 50)
            skip: Number of records to skip
            valid: Filter by validity status
            voucher_type: Filter by voucher type
            async_req: Execute request asynchronously

        Returns:
            List of voucher objects containing details like:
            - ID, name, and type
            - Validity period
            - Usage restrictions
            - Discount information
            - Branch details (if multilocation)
        """
        params = {
            "idVoucher": voucher_id,
            "name": name,
            "idBranch": branch_id,
            "take": take,
            "skip": skip,
            "valid": valid,
            "type": voucher_type,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[VouchersResumoApiViewModel],
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_voucher_details(
        self,
        voucher_id: int,
        async_req: Literal[False] = False,
    ) -> Any: ...

    @overload
    def get_voucher_details(
        self,
        voucher_id: int,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_voucher_details(
        self,
        voucher_id: int,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Get detailed information about a specific voucher.

        Args:
            voucher_id: ID of the voucher to retrieve
            async_req: Execute request asynchronously

        Returns:
            Detailed voucher information including:
            - Basic voucher details
            - Usage history
            - Restrictions and conditions
            - Related transactions
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/{voucher_id}",
            method="GET",
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def create_voucher(
        self,
        name: str,
        discount_type: int,
        discount_value: float,
        valid_from: str,
        valid_until: str,
        branch_id: Optional[int] = None,
        usage_limit: Optional[int] = None,
        min_value: Optional[float] = None,
        async_req: Literal[False] = False,
    ) -> Any: ...

    @overload
    def create_voucher(
        self,
        name: str,
        discount_type: int,
        discount_value: float,
        valid_from: str,
        valid_until: str,
        branch_id: Optional[int] = None,
        usage_limit: Optional[int] = None,
        min_value: Optional[float] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def create_voucher(
        self,
        name: str,
        discount_type: int,
        discount_value: float,
        valid_from: str,
        valid_until: str,
        branch_id: Optional[int] = None,
        usage_limit: Optional[int] = None,
        min_value: Optional[float] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Create a new voucher.

        Args:
            name: Name/code of the voucher
            discount_type: Type of discount (1=Percentage, 2=Fixed amount)
            discount_value: Value of the discount
            valid_from: Start date of validity (format: YYYY-MM-DD)
            valid_until: End date of validity (format: YYYY-MM-DD)
            branch_id: Branch ID for voucher (multilocation only)
            usage_limit: Maximum number of times voucher can be used
            min_value: Minimum purchase value required
            async_req: Execute request asynchronously

        Returns:
            Created voucher details
        """
        voucher_data = {
            "name": name,
            "discountType": discount_type,
            "discountValue": discount_value,
            "validFrom": valid_from,
            "validUntil": valid_until,
            "branchId": branch_id,
            "usageLimit": usage_limit,
            "minValue": min_value,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body={k: v for k, v in voucher_data.items() if v is not None},
            headers={
                "Accept": ["text/plain", "application/json", "text/json"],
                "Content-Type": ["application/json"],
            },
            auth_settings=["Basic"],
            async_req=async_req,
        )
