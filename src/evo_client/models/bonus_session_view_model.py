# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from typing import Optional
import pprint
from pydantic import BaseModel, Field


class BonusSessionViewModel(BaseModel):
    """Bonus session view model.

    This model represents bonus session information in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    id_session: Optional[int] = Field(default=None, alias="idSession")
    expiration_date: Optional[datetime] = Field(default=None, alias="expirationDate")
    fl_bonus_session: Optional[bool] = Field(default=None, alias="flBonusSession")

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True)

    def to_str(self) -> str:
        """Returns the string representation of the model using pprint"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, BonusSessionViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other