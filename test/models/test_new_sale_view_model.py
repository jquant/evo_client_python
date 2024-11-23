# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest
from evo_client.models.new_sale_view_model import NewSaleViewModel
from evo_client.models.member_new_sale_view_model import MemberNewSaleViewModel
from evo_client.models.card_data_view_model import CardDataViewModel
from evo_client.models.e_forma_pagamento_totem import EFormaPagamentoTotem


@pytest.fixture
def new_sale_view_model():
    return NewSaleViewModel(
        idBranch=1,
        idBranchToken="branch-token",
        idMembership=101,
        idService=202,
        serviceValue=299.99,
        memberData=MemberNewSaleViewModel(idMember=1),
        cardData=CardDataViewModel(token="1234567890123456"),
        idProspect=303,
        idProspectToken="prospect-token",
        idMember=404,
        idMemberToken="member-token",
        voucher="DISCOUNT10",
        idCardMember=505,
        idMemberCardToken="member-card-token",
        typePayment="CreditCard",
        totalInstallments=12,
        payment=EFormaPagamentoTotem._1,
        sessionId="session-123",
    )


def test_new_sale_view_model_creation(new_sale_view_model):
    """Test creating a NewSaleViewModel instance"""
    model = new_sale_view_model
    assert isinstance(model, NewSaleViewModel)
    assert model.id_branch == 1
    assert model.id_branch_token == "branch-token"
    assert model.id_membership == 101
    assert model.id_service == 202
    assert model.service_value == 299.99
    assert model.member_data is not None
    assert model.member_data.id_member == 1
    assert model.card_data is not None
    assert model.card_data.token == "1234567890123456"
    assert model.id_prospect == 303
    assert model.id_prospect_token == "prospect-token"
    assert model.id_member == 404
    assert model.id_member_token == "member-token"
    assert model.voucher == "DISCOUNT10"
    assert model.id_card_member == 505
    assert model.id_member_card_token == "member-card-token"
    assert model.type_payment == "CreditCard"
    assert model.total_installments == 12
    assert model.payment == EFormaPagamentoTotem._1
    assert model.session_id == "session-123"


def test_new_sale_view_model_to_dict(new_sale_view_model):
    """Test converting NewSaleViewModel to dictionary"""
    model_dict = new_sale_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idBranch"] == 1
    assert model_dict["idBranchToken"] == "branch-token"
    assert model_dict["idMembership"] == 101
    assert model_dict["idService"] == 202
    assert model_dict["serviceValue"] == 299.99
    assert model_dict["memberData"]["idMember"] == 1
    assert model_dict["cardData"]["token"] == "1234567890123456"
    assert model_dict["idProspect"] == 303
    assert model_dict["idProspectToken"] == "prospect-token"
    assert model_dict["idMember"] == 404
    assert model_dict["idMemberToken"] == "member-token"
    assert model_dict["voucher"] == "DISCOUNT10"
    assert model_dict["idCardMember"] == 505
    assert model_dict["idMemberCardToken"] == "member-card-token"
    assert model_dict["typePayment"] == "CreditCard"
    assert model_dict["totalInstallments"] == 12
    assert model_dict["payment"] == EFormaPagamentoTotem._1
    assert model_dict["sessionId"] == "session-123"


def test_new_sale_view_model_equality(new_sale_view_model):
    """Test equality comparison of NewSaleViewModel instances"""
    same_model = NewSaleViewModel(
        idBranch=1,
        idBranchToken="branch-token",
        idMembership=101,
        idService=202,
        serviceValue=299.99,
        memberData=MemberNewSaleViewModel(idMember=1),
        cardData=CardDataViewModel(token="1234567890123456"),
        idProspect=303,
        idProspectToken="prospect-token",
        idMember=404,
        idMemberToken="member-token",
        voucher="DISCOUNT10",
        idCardMember=505,
        idMemberCardToken="member-card-token",
        typePayment="CreditCard",
        totalInstallments=12,
        payment=EFormaPagamentoTotem._1,
        sessionId="session-123",
    )

    different_model = NewSaleViewModel(
        idBranch=2,
        idBranchToken="different-branch-token",
        idMembership=102,
        idService=203,
        serviceValue=399.99,
        memberData=MemberNewSaleViewModel(idMember=2),
        cardData=CardDataViewModel(token="6543210987654321"),
        idProspect=304,
        idProspectToken="different-prospect-token",
        idMember=405,
        idMemberToken="different-member-token",
        voucher="DISCOUNT20",
        idCardMember=506,
        idMemberCardToken="different-member-card-token",
        typePayment="DebitCard",
        totalInstallments=6,
        payment=EFormaPagamentoTotem._2,
        sessionId="session-456",
    )

    assert new_sale_view_model == same_model
    assert new_sale_view_model != different_model
