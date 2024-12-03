from typing import Optional

from pydantic import BaseModel, Field, field_validator

from .e_status_atividade_sessao import EStatusAtividadeSessao


class AtividadeSessaoParticipanteApiViewModel(BaseModel):
    """Activity Session Participant API View Model

    This model represents a participant in an activity session in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    id_member: Optional[int] = Field(default=None, alias="idMember")
    id_employee: Optional[int] = Field(default=None, alias="idEmployee")
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    id: Optional[int] = None
    slot_number: Optional[int] = Field(default=None, alias="slotNumber")
    name: Optional[str] = None
    photo: Optional[str] = None
    justified_absence: Optional[bool] = Field(default=None, alias="justifiedAbsence")
    id_sale_item: Optional[int] = Field(default=None, alias="idSaleItem")
    status: Optional[EStatusAtividadeSessao] = None
    exclusive: Optional[bool] = None
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    branch_name: Optional[str] = Field(default=None, alias="branchName")
    replacement: Optional[bool] = None
    suspended: Optional[bool] = None
    removed: Optional[bool] = None

    @field_validator("status", mode="before")
    def convert_status(cls, v):
        """Convert integer status to string format."""
        if isinstance(v, int):
            return str(v)
        return v

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True, mode="json")
