# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from .month_discount_view_model import MonthDiscountViewModel
from .year_discount_view_model import YearDiscountViewModel
from .service_discount_view_model import ServiceDiscountViewModel


class VouchersResumoApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_voucher: Optional[int] = Field(default=None, alias="idVoucher")
    name_voucher: Optional[str] = Field(default=None, alias="nameVoucher")
    type_voucher: Optional[str] = Field(default=None, alias="typeVoucher")
    limited: Optional[bool] = None
    available: Optional[int] = None
    used: Optional[int] = None
    site_available: Optional[bool] = Field(default=None, alias="siteAvailable")
    id_memberships: Optional[List[int]] = Field(default=None, alias="idMemberships")
    monthy_discount: Optional[MonthDiscountViewModel] = Field(
        default=None, alias="monthyDiscount"
    )
    yearly_discount: Optional[YearDiscountViewModel] = Field(
        default=None, alias="yearlyDiscount"
    )
    service_discount: Optional[ServiceDiscountViewModel] = Field(
        default=None, alias="serviceDiscount"
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, VouchersResumoApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
