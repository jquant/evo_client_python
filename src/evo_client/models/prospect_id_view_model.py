import pprint
from pydantic import BaseModel, Field


class ProspectIdViewModel(BaseModel):
    """
    ProspectIdViewModel - a model defined in Swagger
    """

    id_prospect: int | None = Field(
        default=None,
        alias="idProspect",
        description="The id_prospect of this ProspectIdViewModel",
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ProspectIdViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
