from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .atividade_lugar_reserva_view_model import AtividadeLugarReservaViewModel
from .atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from .e_status_atividade import EStatusAtividade


class AtividadeBasicoApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    model_config = ConfigDict(populate_by_name=True)

    id_group_activity: Optional[int] = Field(default=None, alias="idGroupActivity")
    id_activity_session: Optional[int] = Field(default=None, alias="idActivitySession")
    id_configuration: Optional[int] = Field(default=None, alias="idConfiguration")
    name: Optional[str] = None
    date: Optional[datetime] = Field(default=None, alias="date")
    capacity: Optional[int] = None
    ocupation: Optional[int] = None
    instructor: Optional[str] = None
    instructor_photo: Optional[str] = Field(default=None, alias="instructorPhoto")
    area: Optional[str] = None
    status: Optional["EStatusAtividade"] = None
    selected_spot: Optional[str] = Field(default=None, alias="selectedSpot")
    exibir_participantes: Optional[bool] = Field(
        default=None, alias="exibirParticipantes"
    )
    code: Optional[str] = None
    status_name: Optional[str] = Field(default=None, alias="statusName")
    week_day: Optional[int] = Field(default=None, alias="weekDay")
    allow_choosing_spot: Optional[bool] = Field(default=None, alias="allowChoosingSpot")
    time_tick: Optional[int] = Field(default=None, alias="timeTick")
    duration_tick: Optional[int] = Field(default=None, alias="durationTick")
    start_time: Optional[str] = Field(default=None, alias="startTime")
    end_time: Optional[str] = Field(default=None, alias="endTime")
    branch_name: Optional[str] = Field(default=None, alias="branchName")
    color: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    enrollments: Optional[List["AtividadeSessaoParticipanteApiViewModel"]] = None
    spots: Optional[List["AtividadeLugarReservaViewModel"]] = None
    title: Optional[str] = None
    json_config_vaga_personalizada: Optional[str] = Field(
        default=None, alias="jsonConfigVagaPersonalizada"
    )

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True, mode="json")
