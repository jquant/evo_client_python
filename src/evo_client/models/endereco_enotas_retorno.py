# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from pydantic import BaseModel, Field
from typing import Optional


class EnderecoEnotasRetorno(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    pais: Optional[str] = Field(default=None)
    uf: Optional[str] = Field(default=None)
    cidade: Optional[str] = Field(default=None)
    logradouro: Optional[str] = Field(default=None)
    numero: Optional[str] = Field(default=None)
    complemento: Optional[str] = Field(default=None)
    bairro: Optional[str] = Field(default=None)
    cep: Optional[str] = Field(default=None)

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump()

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.model_dump())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EnderecoEnotasRetorno):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
