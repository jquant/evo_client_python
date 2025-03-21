from typing import List, Optional

from pydantic import BaseModel, Field

from .publico_atividade_view_model import PublicoAtividadeViewModel


class AtividadeListApiViewModel(BaseModel):
    """Activity List API View Model

    This model represents an activity listing in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    id_activity: Optional[int] = Field(default=None, alias="idActivity")
    photo: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None
    activity_group: Optional[str] = Field(default=None, alias="activityGroup")
    total_records: Optional[int] = Field(default=None, alias="totalRecords")
    inactive: Optional[bool] = None
    description: Optional[str] = None
    id_activity_group: Optional[int] = Field(default=None, alias="idActivityGroup")
    show_on_mobile: Optional[bool] = Field(default=None, alias="showOnMobile")
    show_on_website: Optional[bool] = Field(default=None, alias="showOnWebsite")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    audience: Optional[List[PublicoAtividadeViewModel]] = None
    id_audience: Optional[int] = Field(default=None, alias="idAudience")
    discriminator: Optional[str] = None

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True, mode="json")
