from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import pprint

from enum import Enum
from pydantic import BaseModel


class BusinessHoursViewModel(BaseModel):
    id_hour: Optional[int] = Field(default=None, alias="idHour")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    week_day: Optional[str] = Field(default=None, alias="weekDay")
    hours_from: Optional[datetime] = Field(default=None, alias="hoursFrom")
    hours_to: Optional[datetime] = Field(default=None, alias="hoursTo")
    fl_deleted: Optional[bool] = Field(default=None, alias="flDeleted")
    id_tmp: Optional[int] = Field(default=None, alias="idTmp")
    creation_date: Optional[datetime] = Field(default=None, alias="creationDate")
    id_employee_creation: Optional[int] = Field(
        default=None, alias="idEmployeeCreation"
    )

    class Config:
        allow_population_by_field_name = True

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            k: v.to_dict() if hasattr(v, "to_dict") else v
            for k, v in self.model_dump(by_alias=True).items()
            if v is not None
        }

    def to_str(self) -> str:
        """Get string representation."""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """Get string representation for print."""
        return self.to_str()

    def __eq__(self, other: object) -> bool:
        """Check if two instances are equal."""
        if not isinstance(other, BusinessHoursViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other: object) -> bool:
        """Check if two instances are not equal."""
        return not self == other
