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


class AtividadeLugarReservaApiViewModel(BaseModel):
    """Activity spot reservation API view model.

    This model represents a spot reservation for an activity in the EVO API system.
    Auto-generated from OpenAPI/Swagger specification.
    """

    number: Optional[int] = None
    available: Optional[bool] = None
    name_spot: Optional[str] = Field(default=None, alias="nameSpot")

    def to_dict(self) -> dict:
        """Returns the model properties as a dictionary"""
        return self.model_dump(by_alias=True)

    def to_str(self) -> str:
        """Returns the string representation of the model using pprint"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()
