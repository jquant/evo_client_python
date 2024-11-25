# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

from datetime import datetime

import pytest

from evo_client.models.basic_member_membership_api_view_model import (
    BasicMemberMembershipApiViewModel,
)
from evo_client.models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)
from evo_client.models.member_responsible_view_model import MemberResponsibleViewModel
from evo_client.models.telefone_api_view_model import TelefoneApiViewModel


@pytest.fixture
def cliente_detalhes_basicos_api_view_model():
    return ClienteDetalhesBasicosApiViewModel(
        idMember=123,
        firstName="John",
        lastName="Doe",
        registerDate=datetime(2023, 1, 1),
        idBranch=1,
        branchName="Main Branch",
        accessBlocked=False,
        document="12345678901",
        email="john.doe@example.com",
        contacts=[TelefoneApiViewModel(idPhone=1234567890)],
        responsibles=[MemberResponsibleViewModel(name="Jane Doe")],
        memberships=[MemberMembershipApiViewModel(idMembership=1)],
        membership=BasicMemberMembershipApiViewModel(idMembership=1),
    )


def test_cliente_detalhes_basicos_api_view_model_creation(
    cliente_detalhes_basicos_api_view_model,
):
    """Test creating a ClienteDetalhesBasicosApiViewModel instance"""
    assert isinstance(
        cliente_detalhes_basicos_api_view_model, ClienteDetalhesBasicosApiViewModel
    )
    assert cliente_detalhes_basicos_api_view_model.id_member == 123
    assert cliente_detalhes_basicos_api_view_model.first_name == "John"
    assert cliente_detalhes_basicos_api_view_model.last_name == "Doe"
    assert cliente_detalhes_basicos_api_view_model.branch_name == "Main Branch"
    assert cliente_detalhes_basicos_api_view_model.access_blocked is False
    assert cliente_detalhes_basicos_api_view_model.email == "john.doe@example.com"


def test_cliente_detalhes_basicos_api_view_model_to_dict(
    cliente_detalhes_basicos_api_view_model,
):
    """Test converting ClienteDetalhesBasicosApiViewModel to dictionary"""
    model_dict = cliente_detalhes_basicos_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idMember"] == 123
    assert model_dict["firstName"] == "John"
    assert model_dict["lastName"] == "Doe"
    assert model_dict["branchName"] == "Main Branch"
    assert model_dict["accessBlocked"] is False
    assert model_dict["email"] == "john.doe@example.com"


def test_cliente_detalhes_basicos_api_view_model_equality(
    cliente_detalhes_basicos_api_view_model,
):
    """Test equality comparison of ClienteDetalhesBasicosApiViewModel instances"""
    same_model = ClienteDetalhesBasicosApiViewModel(
        idMember=123,
        firstName="John",
        lastName="Doe",
        registerDate=datetime(2023, 1, 1),
        idBranch=1,
        branchName="Main Branch",
        accessBlocked=False,
        document="12345678901",
        email="john.doe@example.com",
        contacts=[TelefoneApiViewModel(idPhone=1234567890)],
        responsibles=[MemberResponsibleViewModel(name="Jane Doe")],
        memberships=[MemberMembershipApiViewModel(idMembership=1)],
        membership=BasicMemberMembershipApiViewModel(idMembership=1),
    )

    different_model = ClienteDetalhesBasicosApiViewModel(
        idMember=124,
        firstName="Jane",
        lastName="Smith",
        branchName="Secondary Branch",
        accessBlocked=True,
        email="jane.smith@example.com",
    )

    assert cliente_detalhes_basicos_api_view_model == same_model
    assert cliente_detalhes_basicos_api_view_model != different_model
    assert cliente_detalhes_basicos_api_view_model != 1
