from typing import Optional

from pydantic import BaseModel, Field

from .e_tipo_gateway import ETipoGateway


class EmpresasFiliaisGatewayViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    tipo_gateway: Optional[ETipoGateway] = Field(default=None, alias="tipoGateway")
    dados_gateway: Optional[object] = Field(default=None, alias="dadosGateway")
    exibir_tipo_cartao: Optional[bool] = Field(default=None, alias="exibirTipoCartao")
    fl_tokeniza_backend: Optional[bool] = Field(default=None, alias="flTokenizaBackend")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EmpresasFiliaisGatewayViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
