from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from enum import Enum
from pydantic import BaseModel


class EmpresasFiliaisOcupacaoViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    name: Optional[str] = None
    occupation: Optional[int] = None
    max_occupation: Optional[int] = Field(default=None, alias="maxOccupation")
    qty_minutes_out: Optional[int] = Field(default=None, alias="qtyMinutesOut")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EmpresasFiliaisOcupacaoViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
