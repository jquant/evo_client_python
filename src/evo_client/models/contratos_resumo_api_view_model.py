# coding: utf-8

"""
EVO API

Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

OpenAPI spec version: v1

Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from .contrato_entradas_api_view_model import ContratoEntradasApiViewModel
from .contrato_filiais_resumo_api_view_model import ContratoFiliaisResumoApiViewModel
from .contratos_resumo_pagina_venda_view_model import (
    ContratosResumoPaginaVendaViewModel,
)
from .diferenciais_api_view_model import DiferenciaisApiViewModel
from .servico_adicional_api_view_model import ServicoAdicionalApiViewModel
from .servico_anual_api_view_model import ServicoAnualApiViewModel


class ContratosResumoApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_membership: Optional[int] = Field(default=None, alias="idMembership")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    name_membership: Optional[str] = Field(default=None, alias="nameMembership")
    membership_type: Optional[str] = Field(default=None, alias="membershipType")
    duration_type: Optional[str] = Field(default=None, alias="durationType")
    duration: Optional[int] = None
    value: Optional[float] = None
    max_amount_installments: Optional[int] = Field(
        default=None, alias="maxAmountInstallments"
    )
    description: Optional[str] = None
    url_sale: Optional[str] = Field(default=None, alias="urlSale")
    online_sales_observations: Optional[str] = Field(
        default=None, alias="onlineSalesObservations"
    )
    differentials: Optional[List[DiferenciaisApiViewModel]] = None
    access_branches: Optional[List[ContratoFiliaisResumoApiViewModel]] = Field(
        default=None, alias="accessBranches"
    )
    additional_service: Optional[ServicoAdicionalApiViewModel] = Field(
        default=None, alias="additionalService"
    )
    service_yearly: Optional[ServicoAnualApiViewModel] = Field(
        default=None, alias="serviceYearly"
    )
    type_promotional_period: Optional[int] = Field(
        default=None, alias="typePromotionalPeriod"
    )
    value_promotional_period: Optional[float] = Field(
        default=None, alias="valuePromotionalPeriod"
    )
    months_promotional_period: Optional[int] = Field(
        default=None, alias="monthsPromotionalPeriod"
    )
    days_promotional_period: Optional[int] = Field(
        default=None, alias="daysPromotionalPeriod"
    )
    min_period_stay_membership: Optional[int] = Field(
        default=None, alias="minPeriodStayMembership"
    )
    installments_promotional_period: Optional[int] = Field(
        default=None, alias="installmentsPromotionalPeriod"
    )
    inactive: Optional[bool] = None
    display_name: Optional[str] = Field(default=None, alias="displayName")
    entries: Optional[ContratoEntradasApiViewModel] = None
    sales_page: Optional[List[ContratosResumoPaginaVendaViewModel]] = Field(
        default=None, alias="salesPage"
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContratosResumoApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


class ContratosResumoContainerViewModel(BaseModel):
    """Container model for the membership list API response.

    The API returns a container object with the actual membership list in the 'list' property.
    """

    qtde: Optional[int] = None
    lista: Optional[list] = None
    list: Optional[List[ContratosResumoApiViewModel]] = []
    ids: Optional[List[Any]] = None
    informacoes_indicados: Optional[dict] = Field(
        default=None, alias="informacoesIndicados"
    )
    id_ultima_conciliacao: Optional[str] = Field(
        default=None, alias="idUltimaConciliacao"
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContratosResumoContainerViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
