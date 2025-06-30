"""Clean synchronous Voucher API."""

from typing import Any, List, Optional, cast

from ...models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel
from .base import SyncBaseApi


class SyncVoucherApi(SyncBaseApi):
    """Clean synchronous Voucher API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/voucher"

    def get_vouchers(
        self,
        voucher_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        valid: Optional[bool] = None,
        voucher_type: Optional[int] = None,
    ) -> List[VouchersResumoApiViewModel]:
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

        Returns:
            List of voucher objects containing details like:
            - ID, name, and type
            - Validity period
            - Usage restrictions
            - Discount information
            - Branch details (if multilocation)

        Example:
            >>> with SyncVoucherApi() as api:
            ...     vouchers = api.get_vouchers(
            ...         valid=True,
            ...         voucher_type=1,
            ...         take=10
            ...     )
            ...     for voucher in vouchers:
            ...         print(f"Voucher: {voucher.name} - {voucher.discount_value}")
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

        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[VouchersResumoApiViewModel],
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
        )
        return cast(List[VouchersResumoApiViewModel], result)

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
    ) -> Any:
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

        Returns:
            Created voucher details

        Example:
            >>> with SyncVoucherApi() as api:
            ...     voucher = api.create_voucher(
            ...         name="NEWUSER10",
            ...         discount_type=1,
            ...         discount_value=10.0,
            ...         valid_from="2024-01-01",
            ...         valid_until="2024-12-31",
            ...         usage_limit=100
            ...     )
            ...     print(f"Created voucher with ID: {voucher.id}")
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

        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body={k: v for k, v in voucher_data.items() if v is not None},
            headers={
                "Accept": ["text/plain", "application/json", "text/json"],
                "Content-Type": ["application/json"],
            },
            auth_settings=["Basic"],
        )
        return result
