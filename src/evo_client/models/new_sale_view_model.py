# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import Any, Optional, List

from pydantic import BaseModel, Field

from .card_data_view_model import CardDataViewModel
from .e_forma_pagamento_totem import EFormaPagamentoTotem
from .member_new_sale_view_model import MemberNewSaleViewModel


class NewSaleViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    id_branch_token: Optional[str] = Field(default=None, alias="idBranchToken")
    id_membership: Optional[int] = Field(default=None, alias="idMembership")
    id_service: Optional[int] = Field(default=None, alias="idService")
    service_value: Optional[float] = Field(default=None, alias="serviceValue")
    member_data: Optional[MemberNewSaleViewModel] = Field(
        default=None, alias="memberData"
    )
    card_data: Optional[CardDataViewModel] = Field(default=None, alias="cardData")
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    id_prospect_token: Optional[str] = Field(default=None, alias="idProspectToken")
    id_member: Optional[int] = Field(default=None, alias="idMember")
    id_member_token: Optional[str] = Field(default=None, alias="idMemberToken")
    voucher: Optional[str] = None
    id_card_member: Optional[int] = Field(default=None, alias="idCardMember")
    id_member_card_token: Optional[str] = Field(default=None, alias="idMemberCardToken")
    type_payment: Optional[str] = Field(default=None, alias="typePayment")
    total_installments: Optional[int] = Field(default=None, alias="totalInstallments")
    payment: Optional[EFormaPagamentoTotem] = None
    session_id: Optional[str] = Field(default=None, alias="sessionId")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NewSaleViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


class ClienteContrato(BaseModel):
    id_cliente_contrato: Optional[int] = Field(default=None, alias="idClienteContrato")
    ds_contrato: Optional[str] = Field(default=None, alias="dsContrato")
    inicio: Optional[str] = Field(default=None, alias="inicio")
    fl_familia: Optional[bool] = Field(default=None, alias="flFamilia")
    contrato_html: Optional[str] = Field(default=None, alias="contratoHtml")
    link_aceite_contrato: Optional[str] = Field(
        default=None, alias="linkAceiteContrato"
    )
    fl_recorrente_fidelidade: Optional[bool] = Field(
        default=None, alias="flRecorrenteFidelidade"
    )
    id_membership_token: Optional[str] = Field(default=None, alias="idMembershipToken")


class NewSaleResponse(BaseModel):
    id_cliente: Optional[int] = Field(default=None, alias="idCliente")
    id_cliente_token: Optional[str] = Field(default=None, alias="idClienteToken")
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    id_prospect_token: Optional[str] = Field(default=None, alias="idProspectToken")
    largura_recibo: Optional[int] = Field(default=None, alias="larguraRecibo")
    recibo: Optional[str] = Field(default=None, alias="recibo")
    transacao_online_recusada: Optional[bool] = Field(
        default=None, alias="transacaoOnlineRecusada"
    )
    mensagem_erro_transacao_online: Optional[str] = Field(
        default=None, alias="mensagemErroTransacaoOnline"
    )
    aviso_email_nao_enviado: Optional[bool] = Field(
        default=None, alias="avisoEmailNaoEnviado"
    )
    cliente_contratos: Optional[List[ClienteContrato]] = Field(
        default=None, alias="clienteContratos"
    )
    celular_envio_checkout_whatsapp: Optional[str] = Field(
        default=None, alias="celularEnvioCheckoutWhatsapp"
    )
    url_envio_checkout: Optional[str] = Field(default=None, alias="urlEnvioCheckout")
    key_cliente: Optional[str] = Field(default=None, alias="keyCliente")
    key_prospect: Optional[str] = Field(default=None, alias="keyProspect")
    link_boleto: Optional[str] = Field(default=None, alias="linkBoleto")
    qr_code: Optional[str] = Field(default=None, alias="qrCode")
    codigo_barras_boleto: Optional[str] = Field(
        default=None, alias="codigoBarrasBoleto"
    )
    codigo_retirada: Optional[str] = Field(default=None, alias="codigoRetirada")
    vencimento_boleto: Optional[str] = Field(default=None, alias="vencimentoBoleto")
    valor_boleto: Optional[str] = Field(default=None, alias="valorBoleto")
    dt_vencimento_boleto: Optional[str] = Field(
        default=None, alias="dtVencimentoBoleto"
    )
    id_recibo: Optional[int] = Field(default=None, alias="idRecibo")
    fl_boleto_enviado_email: Optional[bool] = Field(
        default=None, alias="flBoletoEnviadoEmail"
    )
    id_venda: Optional[int] = Field(default=None, alias="idVenda")
    recebimentos: Optional[Any] = Field(default=None, alias="recebimentos")
    gerou_boleto_erro: Optional[bool] = Field(default=None, alias="gerouBoletoErro")
    utiliza_qr_code: Optional[bool] = Field(default=None, alias="utilizaQrCode")
    id_externo_boleto: Optional[str] = Field(default=None, alias="idExternoBoleto")
    fl_pix_erro: Optional[bool] = Field(default=None, alias="flPixErro")
    msg_pix_erro: Optional[str] = Field(default=None, alias="msgPixErro")
    msg_retorno_whatsapp: Optional[str] = Field(
        default=None, alias="msgRetornoWhatsapp"
    )
    configuracao_payu: Optional[str] = Field(default=None, alias="configuracaoPayU")
    ids_item_venda: Optional[List[int]] = Field(default=None, alias="idsItemVenda")
    pix_detalhes: Optional[str] = Field(default=None, alias="pixDetalhes")
    link_checkout: Optional[str] = Field(default=None, alias="linkCheckout")
    fl_apresentar_modal_como_conheceu: Optional[bool] = Field(
        default=None, alias="flApresentarModalComoConheceu"
    )
    fl_erro_gerar_checkout_integrado: Optional[bool] = Field(
        default=None, alias="flErroGerarCheckoutIntegrado"
    )
