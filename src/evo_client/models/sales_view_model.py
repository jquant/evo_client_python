# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from .sales_items_view_model import SalesItemsViewModel
from .receivables_api_view_model import ReceivablesApiViewModel


class SalesViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_sale: Optional[int] = Field(default=None, alias="idSale")
    id_member: Optional[int] = Field(default=None, alias="idMember")
    id_employee: Optional[int] = Field(default=None, alias="idEmployee")
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    id_employee_sale: Optional[int] = Field(default=None, alias="idEmployeeSale")
    sale_date: Optional[datetime] = Field(default=None, alias="saleDate")
    sale_date_server: Optional[datetime] = Field(default=None, alias="saleDateServer")
    id_personal: Optional[int] = Field(default=None, alias="idPersonal")
    corporate_partnership_name: Optional[str] = Field(
        default=None, alias="corporatePartnershipName"
    )
    coporate_partnership_id: Optional[int] = Field(
        default=None, alias="coporatePartnershipId"
    )
    removed: Optional[bool] = None
    id_employee_removal: Optional[int] = Field(default=None, alias="idEmployeeRemoval")
    removal_date: Optional[datetime] = Field(default=None, alias="removalDate")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    observations: Optional[str] = None
    id_sale_recurrency: Optional[int] = Field(default=None, alias="idSaleRecurrency")
    sale_source: Optional[int] = Field(default=None, alias="saleSource")
    id_sale_migration: Optional[str] = Field(default=None, alias="idSaleMigration")
    sale_itens: Optional[List[SalesItemsViewModel]] = Field(
        default=None, alias="saleItens"
    )
    receivables: Optional[List[ReceivablesApiViewModel]] = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SalesViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
