from typing import Optional
from pydantic import BaseModel, Field


class CostCenterApiViewModel(BaseModel):
    """
    CostCenterApiViewModel - a model defined in Swagger
    """

    id_cost_center: Optional[int] = Field(default=None, alias="idCostCenter")
    description: Optional[str] = Field(default=None)
    id_cost_center_father: Optional[int] = Field(
        default=None, alias="idCostCenterFather"
    )
    active: Optional[bool] = Field(default=None)
    id_dre_group: Optional[int] = Field(default=None, alias="idDreGroup")
    level: Optional[int] = Field(default=None)

    class Config:
        allow_population_by_field_name = True

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CostCenterApiViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
