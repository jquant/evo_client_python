# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .telefone_api_view_model import TelefoneApiViewModel


class MemberDataViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    cellphone: Optional[TelefoneApiViewModel] = Field(default=None)
    email: Optional[TelefoneApiViewModel] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    document: Optional[str] = Field(default=None)
    zip_code: Optional[str] = Field(alias="zipCode", default=None)
    address: Optional[str] = Field(default=None)
    number: Optional[str] = Field(default=None)
    complement: Optional[str] = Field(default=None)
    neighborhood: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    id_state: Optional[int] = Field(alias="idState", default=None)
    birth_day: Optional[datetime] = Field(alias="birthDay", default=None)

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, mode="json")

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MemberDataViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
