from typing import Optional

from pydantic import BaseModel, Field


class FuncionariosResumoApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_employee: Optional[int] = Field(default=None, alias="idEmployee")
    name: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    job_position: Optional[str] = Field(default=None, alias="jobPosition")
    status: Optional[bool] = None
    photo_url: Optional[str] = Field(default=None, alias="photoUrl")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FuncionariosResumoApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
