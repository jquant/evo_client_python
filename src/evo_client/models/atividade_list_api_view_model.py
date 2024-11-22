import pprint

from enum import IntEnum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from .periodizacao_api_view_model import PeriodizacaoApiViewModel
from .e_status_atividade import EStatusAtividade


from enum import Enum
from pydantic import BaseModel

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

    class Config:
        """Pydantic model configuration"""

        allow_population_by_field_name = True

    def to_str(self) -> str:
        """Returns the string representation of the model using pprint"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        result = self.model_dump(by_alias=True)
        # Handle nested models that might not be automatically converted
        for key, value in result.items():
            if isinstance(value, list):
                result[key] = [
                    (item.model_dump() if hasattr(item, "model_dump") else item)
                    for item in value
                ]
        return result
