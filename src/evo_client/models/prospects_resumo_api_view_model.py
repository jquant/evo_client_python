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

from .prospect_responsavel_resumo_api_view_model import (
    ProspectResponsavelResumoApiViewModel,
)


class ProspectsResumoApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    branch_name: Optional[str] = Field(default=None, alias="branchName")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    document: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[str] = None
    gympass_id: Optional[str] = Field(default=None, alias="gympassId")
    register_date: Optional[datetime] = Field(default=None, alias="registerDate")
    gender: Optional[str] = None
    birth_date: Optional[datetime] = Field(default=None, alias="birthDate")
    signup_type: Optional[str] = Field(default=None, alias="signupType")
    mkt_channel: Optional[str] = Field(default=None, alias="mktChannel")
    conversion_date: Optional[datetime] = Field(default=None, alias="conversionDate")
    id_member: Optional[int] = Field(default=None, alias="idMember")
    current_step: Optional[str] = Field(default=None, alias="currentStep")
    address: Optional[str] = None
    city: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = Field(default=None, alias="zipCode")
    number: Optional[str] = None
    responsible: Optional[ProspectResponsavelResumoApiViewModel] = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.model_dump())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ProspectsResumoApiViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
