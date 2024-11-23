# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from enum import Enum
from pydantic import BaseModel, Field


class TipoContratoEnum(str, Enum):
    """Contract type enumeration"""

    _1 = "1"
    _3 = "3"
    _4 = "4"
    _5 = "5"
    _6 = "6"
    _7 = "7"
    _8 = "8"
    _9 = "9"
    _10 = "10"


class ETipoContrato(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    tipo: TipoContratoEnum = Field(
        description="Contract type",
        examples=["1", "3", "4", "5", "6", "7", "8", "9", "10"],
    )

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
        if not isinstance(other, ETipoContrato):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other