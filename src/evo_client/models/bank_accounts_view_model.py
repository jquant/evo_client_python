# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import Optional
import pprint
from pydantic import BaseModel, Field


class BankAccount(BaseModel):
    """Represents a bank account."""

    id: int
    name: str
    bank_name: str
    agency: str
    account_number: str
    is_active: bool
    branch_id: Optional[int] = None


class BankAccountsViewModel(BaseModel):
    """Bank accounts view model.

    This model represents bank account information in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    id_bank_account: Optional[int] = Field(default=None, alias="idBankAccount")
    description: Optional[str] = None
    account_type: Optional[bool] = Field(default=None, alias="accountType")
    bank_code: Optional[int] = Field(default=None, alias="bankCode")
    agency: Optional[str] = None
    account: Optional[str] = None
    observations: Optional[str] = None
    inactive: Optional[bool] = None
    bank_integration: Optional[bool] = Field(default=None, alias="bankIntegration")

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
        if not isinstance(other, BankAccountsViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
