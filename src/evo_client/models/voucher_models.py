"""Voucher-related Pydantic models based on API documentation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class VoucherDetails(BaseModel):
    """Detailed voucher information model."""

    id_voucher: Optional[int] = Field(default=None, alias="idVoucher")
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    discount_type: Optional[int] = Field(default=None, alias="discountType")
    discount_value: Optional[float] = Field(default=None, alias="discountValue")
    valid_from: Optional[datetime] = Field(default=None, alias="validFrom")
    valid_until: Optional[datetime] = Field(default=None, alias="validUntil")
    usage_limit: Optional[int] = Field(default=None, alias="usageLimit")
    times_used: Optional[int] = Field(default=None, alias="timesUsed")
    min_value: Optional[float] = Field(default=None, alias="minValue")
    branch_id: Optional[int] = Field(default=None, alias="branchId")
    branch_name: Optional[str] = Field(default=None, alias="branchName")
    active: Optional[bool] = None
    created_date: Optional[datetime] = Field(default=None, alias="createdDate")
    created_by: Optional[str] = Field(default=None, alias="createdBy")


class VoucherCreateResponse(BaseModel):
    """Response model for voucher creation."""

    success: bool
    voucher_id: Optional[int] = Field(default=None, alias="voucherId")
    message: Optional[str] = None
    errors: Optional[List[str]] = None

    model_config = ConfigDict(populate_by_name=True)


class VoucherCalculationResponse(BaseModel):
    """Response model for voucher value calculation."""

    base_value: float = Field(alias="baseValue")
    discount_percentage: Optional[float] = Field(
        default=None, alias="discountPercentage"
    )
    discount_amount: Optional[float] = Field(default=None, alias="discountAmount")
    additional_fees: Optional[float] = Field(default=None, alias="additionalFees")
    final_value: float = Field(alias="finalValue")
    breakdown: Optional[dict] = None
