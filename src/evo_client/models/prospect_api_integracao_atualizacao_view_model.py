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


class ProspectApiIntegracaoAtualizacaoViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    name: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = Field(default=None, alias="lastName")
    ddi: Optional[str] = None
    cellphone: Optional[str] = None
    birthday: Optional[datetime] = None
    gender: Optional[str] = None
    notes: Optional[str] = None
    current_step: Optional[str] = Field(default=None, alias="currentStep")
    cpf: Optional[str] = None
    token_gympass: Optional[str] = Field(default=None, alias="tokenGympass")

    
        validate_assignment = True

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
        if not isinstance(other, ProspectApiIntegracaoAtualizacaoViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other