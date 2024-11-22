from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SpsRelProspectsCadastradosConvertidos(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_filial: Optional[int] = Field(default=None, alias="idFilial")
    nome_filial: Optional[str] = Field(default=None, alias="nomeFilial")
    status: Optional[str] = None
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    nome: Optional[str] = None
    dt_cadastro: Optional[datetime] = Field(default=None, alias="dtCadastro")
    primeira_visita: Optional[str] = Field(default=None, alias="primeiraVisita")
    convertido_por: Optional[str] = Field(default=None, alias="convertidoPor")
    dt_conversao: Optional[datetime] = Field(default=None, alias="dtConversao")
    id_cliente: Optional[int] = Field(default=None, alias="idCliente")
    descricao: Optional[str] = None
    primeiro_contrato: Optional[str] = Field(default=None, alias="primeiroContrato")
    apelido: Optional[str] = None
    marketing: Optional[str] = None

    class Config:
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
        if not isinstance(other, SpsRelProspectsCadastradosConvertidos):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
