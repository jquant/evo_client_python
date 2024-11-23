from pydantic import BaseModel, Field
from typing import Optional

import pprint


class MemberNewSaleViewModel(BaseModel):
    """
    MemberNewSaleViewModel - a model defined in Swagger
    """

    id_member: Optional[int] = Field(default=None, alias="idMember")
    document: Optional[str] = None
    zip_code: Optional[str] = Field(default=None, alias="zipCode")
    address: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    id_state: Optional[int] = Field(default=None, alias="idState")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MemberNewSaleViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
