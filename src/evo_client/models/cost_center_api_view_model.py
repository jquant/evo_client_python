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

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CostCenterApiViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
