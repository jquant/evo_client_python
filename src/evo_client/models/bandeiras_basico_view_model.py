from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BandeirasBasicoViewModel(BaseModel):
    """Basic flags view model.

    This model represents basic flag information in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    model_config = ConfigDict(populate_by_name=True)

    value: Optional[str] = None
    text: Optional[str] = None
    logo_url: Optional[str] = Field(default=None, alias="logoUrl")

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, BandeirasBasicoViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
