from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EmployeeApiIntegracaoAtualizacaoViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_employee: Optional[int] = Field(default=None, alias="idEmployee")
    name: Optional[str] = None
    last_name: Optional[str] = Field(default=None, alias="lastName")
    document: Optional[str] = None
    document_id: Optional[str] = Field(default=None, alias="documentId")
    cellphone: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    country: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    passport: Optional[str] = None
    zip_code: Optional[str] = Field(default=None, alias="zipCode")
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    number: Optional[str] = None
    active: Optional[bool] = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True, mode="json")

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EmployeeApiIntegracaoAtualizacaoViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
