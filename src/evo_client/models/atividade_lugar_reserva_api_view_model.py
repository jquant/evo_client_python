from typing import Optional

from pydantic import BaseModel, Field


class AtividadeLugarReservaApiViewModel(BaseModel):
    """Activity spot reservation API view model.

    This model represents a spot reservation for an activity in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    number: Optional[int] = None
    available: Optional[bool] = None
    name_spot: Optional[str] = Field(default=None, alias="nameSpot")

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True)
