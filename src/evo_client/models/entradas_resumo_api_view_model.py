# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class EntradasResumoApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    date: Optional[datetime] = Field(default=None, alias="date")
    date_turn: Optional[datetime] = Field(default=None, alias="dateTurn")
    time_zone: Optional[str] = Field(default=None, alias="timeZone")
    id_member: Optional[int] = Field(default=None, alias="idMember")
    name_member: Optional[str] = Field(default=None, alias="nameMember")
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    name_prospect: Optional[str] = Field(default=None, alias="nameProspect")
    id_employee: Optional[int] = Field(default=None, alias="idEmployee")
    name_employee: Optional[str] = Field(default=None, alias="nameEmployee")
    entry_type: Optional[str] = Field(default=None, alias="entryType")
    device: Optional[str] = None
    releases_by_id: Optional[int] = Field(default=None, alias="releasesByID")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    block_reason: Optional[str] = Field(default=None, alias="blockReason")
    entry_action: Optional[str] = Field(default=None, alias="entryAction")
    id_migration: Optional[str] = Field(default=None, alias="idMigration")

    class Config:
        """Pydantic model configuration"""

        populate_by_name = True
        validate_assignment = True

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EntradasResumoApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
