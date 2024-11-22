import pprint
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from enum import Enum
from pydantic import BaseModel


class BandeirasBasicoViewModel(BaseModel):
    """Basic flags view model.

    This model represents basic flag information in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    value: Optional[str] = None
    text: Optional[str] = None
    logo_url: Optional[str] = Field(default=None, alias="logoUrl")

    class Config:
        """Pydantic model configuration"""

        allow_population_by_field_name = True

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
        if not isinstance(other, BandeirasBasicoViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
