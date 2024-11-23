# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
import pytest
from evo_client.models.member_basic_responsible_view_model import (
    MemberBasicResponsibleViewModel,
)


@pytest.fixture
def member_basic_responsible_view_model():
    return MemberBasicResponsibleViewModel(
        idResponsible=1,
        idMember=2,
        name="John Doe",
        email="john.doe@example.com",
        phone="123456789",
        observation="Test observation",
        idMemberResponsible=3,
        acessFiti=True,
        financialResponsible=False,
    )


def test_member_basic_responsible_view_model_creation(
    member_basic_responsible_view_model,
):
    """Test creating a MemberBasicResponsibleViewModel instance"""
    model = member_basic_responsible_view_model
    assert isinstance(model, MemberBasicResponsibleViewModel)
    assert model.id_responsible == 1
    assert model.id_member == 2
    assert model.name == "John Doe"
    assert model.email == "john.doe@example.com"
    assert model.phone == "123456789"
    assert model.observation == "Test observation"
    assert model.id_member_responsible == 3
    assert model.acess_fiti is True
    assert model.financial_responsible is False


def test_member_basic_responsible_view_model_to_dict(
    member_basic_responsible_view_model,
):
    """Test converting MemberBasicResponsibleViewModel to dictionary"""
    model_dict = member_basic_responsible_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idResponsible"] == 1
    assert model_dict["idMember"] == 2
    assert model_dict["name"] == "John Doe"
    assert model_dict["email"] == "john.doe@example.com"
    assert model_dict["phone"] == "123456789"
    assert model_dict["observation"] == "Test observation"
    assert model_dict["idMemberResponsible"] == 3
    assert model_dict["acessFiti"] is True
    assert model_dict["financialResponsible"] is False


def test_member_basic_responsible_view_model_equality(
    member_basic_responsible_view_model,
):
    """Test equality comparison of MemberBasicResponsibleViewModel instances"""
    same_model = MemberBasicResponsibleViewModel(
        idResponsible=1,
        idMember=2,
        name="John Doe",
        email="john.doe@example.com",
        phone="123456789",
        observation="Test observation",
        idMemberResponsible=3,
        acessFiti=True,
        financialResponsible=False,
    )

    different_model = MemberBasicResponsibleViewModel(
        idResponsible=2,
        idMember=3,
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="987654321",
        observation="Different observation",
        idMemberResponsible=4,
        acessFiti=False,
        financialResponsible=True,
    )

    assert member_basic_responsible_view_model == same_model
    assert member_basic_responsible_view_model != different_model