# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import Optional

from pydantic import BaseModel, Field


class RevenueCenterApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_revenue_center: Optional[int] = Field(default=None, alias="idRevenueCenter")
    description: Optional[str] = None
    active: Optional[bool] = None
    id_revenue_center_parent: Optional[int] = Field(
        default=None, alias="idRevenueCenterParent"
    )
    abreviation: Optional[str] = None
    id_dre_group: Optional[int] = Field(default=None, alias="idDreGroup")
    level: Optional[int] = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RevenueCenterApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
