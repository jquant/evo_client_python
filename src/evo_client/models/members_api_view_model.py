# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)
from evo_client.models.member_responsible_view_model import MemberResponsibleViewModel
from evo_client.models.telefone_api_view_model import TelefoneApiViewModel


class MembersApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_member: Optional[int] = Field(default=None, alias="idMember")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    register_date: Optional[datetime] = Field(default=None, alias="registerDate")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    branch_name: Optional[str] = Field(default=None, alias="branchName")
    access_blocked: Optional[bool] = Field(default=None, alias="accessBlocked")
    blocked_reason: Optional[str] = Field(default=None, alias="blockedReason")
    document: Optional[str] = None
    document_id: Optional[str] = Field(default=None, alias="documentId")
    marital_status: Optional[str] = Field(default=None, alias="maritalStatus")
    gender: Optional[str] = None
    birth_date: Optional[datetime] = Field(default=None, alias="birthDate")
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = Field(default=None, alias="zipCode")
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    access_card_number: Optional[str] = Field(default=None, alias="accessCardNumber")
    number: Optional[str] = None
    cpf: Optional[str] = None
    passport: Optional[str] = None
    membership_status: Optional[str] = Field(default=None, alias="membershipStatus")
    penalized: Optional[bool] = None
    status: Optional[str] = None
    contacts: Optional[List[TelefoneApiViewModel]] = None
    memberships: Optional[List[MemberMembershipApiViewModel]] = None
    last_access_date: Optional[datetime] = Field(default=None, alias="lastAccessDate")
    conversion_date: Optional[datetime] = Field(default=None, alias="conversionDate")
    id_employee_consultant: Optional[int] = Field(
        default=None, alias="idEmployeeConsultant"
    )
    name_employee_consultant: Optional[str] = Field(
        default=None, alias="nameEmployeeConsultant"
    )
    id_employee_instructor: Optional[int] = Field(
        default=None, alias="idEmployeeInstructor"
    )
    name_employee_instructor: Optional[str] = Field(
        default=None, alias="nameEmployeeInstructor"
    )
    id_employee_personal_trainer: Optional[int] = Field(
        default=None, alias="idEmployeePersonalTrainer"
    )
    name_employee_personal_trainer: Optional[str] = Field(
        default=None, alias="nameEmployeePersonalTrainer"
    )
    photo_url: Optional[str] = Field(default=None, alias="photoUrl")
    country: Optional[str] = None
    id_member_migration: Optional[str] = Field(default=None, alias="idMemberMigration")
    responsibles: Optional[List[MemberResponsibleViewModel]] = None
    gympass_id: Optional[str] = Field(default=None, alias="gympassId")
    personal_trainer: Optional[bool] = Field(default=None, alias="personalTrainer")
    personal_type: Optional[str] = Field(default=None, alias="personalType")
    cref: Optional[str] = None
    cref_expiration_date: Optional[datetime] = Field(
        default=None, alias="crefExpirationDate"
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, mode="json")

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MembersApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
