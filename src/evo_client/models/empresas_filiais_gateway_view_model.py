import pprint
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from enum import Enum
from pydantic import BaseModel

from .e_tipo_gateway import ETipoGateway


class EmpresasFiliaisGatewayViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    tipo_gateway: Optional[ETipoGateway] = Field(None, alias="tipoGateway")
    dados_gateway: Optional[object] = Field(None, alias="dadosGateway")
    exibir_tipo_cartao: Optional[bool] = Field(None, alias="exibirTipoCartao")
    fl_tokeniza_backend: Optional[bool] = Field(None, alias="flTokenizaBackend")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

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
        if not isinstance(other, EmpresasFiliaisGatewayViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
