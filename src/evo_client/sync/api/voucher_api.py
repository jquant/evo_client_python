"""Clean synchronous Voucher API."""

from typing import List, Optional, cast, Any
import json

from ...models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel
from ...models.voucher_models import (
    VoucherDetails,
    VoucherCreateResponse,
    VoucherCalculationResponse,
)
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
            ...         print(f"Voucher: {voucher.name_voucher} - {voucher.type_voucher}")
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

        result: Any = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[VouchersResumoApiViewModel],
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
        )
        return cast(List[VouchersResumoApiViewModel], result)

    def get_voucher_details(self, voucher_id: int) -> VoucherDetails:
        """
        Get detailed information about a specific voucher.

        Args:
            voucher_id: ID of the voucher to retrieve

        Returns:
            Detailed voucher information including:
            - Basic voucher details
            - Usage history
            - Restrictions and conditions
            - Related transactions

        Example:
            >>> with SyncVoucherApi() as api:
            ...     details = api.get_voucher_details(voucher_id=123)
            ...     print(f"Voucher: {details.name} - Value: {details.value}")
        """
        result: Any = self.api_client.call_api(
            resource_path=f"{self.base_path}/{voucher_id}",
            method="GET",
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
        )

        # Parse the raw result into VoucherDetails model
        return VoucherDetails.model_validate(result)

    def create_voucher(
        self,
        member_id: int,
        value: float,
        description: Optional[str] = None,
        expiration_date: Optional[str] = None,
    ) -> VoucherCreateResponse:
        """
        Create a new voucher for a member.

        Args:
            member_id: ID of the member to create voucher for
            value: Voucher value amount
            description: Optional voucher description
            expiration_date: Optional expiration date (YYYY-MM-DD format)

        Returns:
            Created voucher details including ID and status

        Example:
            >>> with SyncVoucherApi() as api:
            ...     response = api.create_voucher(
            ...         member_id=123,
            ...         value=50.0,
            ...         description="Bonus voucher",
            ...         expiration_date="2024-12-31"
            ...     )
            ...     if response.success:
            ...         print(f"Voucher created with ID: {response.voucher_id}")
        """
        request_data = {
            "memberId": member_id,
            "value": value,
            "description": description,
            "expirationDate": expiration_date,
        }

        # Remove None values
        request_data = {k: v for k, v in request_data.items() if v is not None}

        try:
            result: Any = self.api_client.call_api(
                resource_path=f"{self.base_path}/create-voucher",
                method="POST",
                body=json.dumps(request_data),
                headers={"Content-Type": "application/json"},
                auth_settings=["Basic"],
            )

            # Parse response or create success response
            if isinstance(result, dict):
                return VoucherCreateResponse.model_validate(result)
            else:
                # If API doesn't return structured response, create our own
                return VoucherCreateResponse(
                    success=True, message="Voucher created successfully"
                )
        except Exception as e:
            return VoucherCreateResponse(
                success=False,
                message=f"Error creating voucher: {str(e)}",
                errors=[str(e)],
            )

    def calculate_voucher_value(
        self,
        base_value: float,
        discount_percentage: Optional[float] = None,
        additional_fees: Optional[float] = None,
    ) -> VoucherCalculationResponse:
        """
        Calculate the final voucher value with discounts and fees.

        Args:
            base_value: Base voucher value
            discount_percentage: Optional discount percentage (0-100)
            additional_fees: Optional additional fees to add

        Returns:
            Calculation result with final value and breakdown

        Example:
            >>> with SyncVoucherApi() as api:
            ...     calculation = api.calculate_voucher_value(
            ...         base_value=100.0,
            ...         discount_percentage=10.0,
            ...         additional_fees=5.0
            ...     )
            ...     print(f"Final value: {calculation.final_value}")
        """
        request_data = {
            "baseValue": base_value,
            "discountPercentage": discount_percentage,
            "additionalFees": additional_fees,
        }

        # Remove None values
        request_data = {k: v for k, v in request_data.items() if v is not None}

        result: Any = self.api_client.call_api(
            resource_path=f"{self.base_path}/calculate-value",
            method="POST",
            body=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
            auth_settings=["Basic"],
        )

        # Parse the raw result into VoucherCalculationResponse model
        return VoucherCalculationResponse.model_validate(result)
