# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SaleItensViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_sale_item: Optional[int] = Field(default=None, alias="idSaleItem")
    description: Optional[str] = None
    item: Optional[str] = None
    item_value: Optional[float] = Field(default=None, alias="itemValue")
    sale_value: Optional[float] = Field(default=None, alias="saleValue")
    sale_value_without_credit_value: Optional[float] = Field(
        default=None, alias="saleValueWithoutCreditValue"
    )
    quantity: Optional[int] = None
    id_membership: Optional[int] = Field(default=None, alias="idMembership")
    id_membership_renewed: Optional[int] = Field(
        default=None, alias="idMembershipRenewed"
    )
    num_members: Optional[int] = Field(default=None, alias="numMembers")
    id_product: Optional[int] = Field(default=None, alias="idProduct")
    id_service: Optional[int] = Field(default=None, alias="idService")
    corporate_partnership_name: Optional[str] = Field(
        default=None, alias="corporatePartnershipName"
    )
    coporate_partnership_id: Optional[int] = Field(
        default=None, alias="coporatePartnershipId"
    )
    membership_start_date: Optional[datetime] = Field(
        default=None, alias="membershipStartDate"
    )
    discount: Optional[float] = None
    corporate_discount: Optional[float] = Field(default=None, alias="corporateDiscount")
    tax: Optional[float] = None
    voucher: Optional[str] = None
    accounting_code: Optional[str] = Field(default=None, alias="accountingCode")
    municipal_service_code: Optional[str] = Field(
        default=None, alias="municipalServiceCode"
    )
    fl_receipt_only: Optional[bool] = Field(default=None, alias="flReceiptOnly")
    id_sale_item_migration: Optional[str] = Field(
        default=None, alias="idSaleItemMigration"
    )
    fl_swimming: Optional[bool] = Field(default=None, alias="flSwimming")
    fl_allow_locker: Optional[bool] = Field(default=None, alias="flAllowLocker")
    id_member_membership: Optional[int] = Field(
        default=None, alias="idMemberMembership"
    )
    value_next_month: Optional[float] = Field(default=None, alias="valueNextMonth")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SaleItensViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
