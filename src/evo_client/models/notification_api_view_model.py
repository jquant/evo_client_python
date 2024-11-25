from pydantic import BaseModel, Field
from typing import Optional
import pprint


class NotificationApiViewModel(BaseModel):
    """
    NotificationApiViewModel - a model defined in Swagger
    """

    id_member: Optional[int] = Field(default=None, alias="idMember")
    notification_message: Optional[str] = Field(
        default=None, alias="notificationMessage"
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NotificationApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
