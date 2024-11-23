import pprint

from enum import IntEnum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from .periodizacao_api_view_model import PeriodizacaoApiViewModel
from .e_status_atividade_sessao import EStatusAtividadeSessao


from enum import Enum
from pydantic import BaseModel

from .publico_atividade_view_model import PublicoAtividadeViewModel


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

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True, mode="json")
