# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

from datetime import datetime

import pytest

from evo_client.models.member_data_view_model import MemberDataViewModel


@pytest.fixture
def member_data_view_model():
    return MemberDataViewModel(
        cellphone=None,
        email=None,
        gender="Male",
        document="123456789",
        zipCode="12345",
        address="123 Main St",
        number="10A",
        complement="Apt 1",
        neighborhood="Downtown",
        city="Metropolis",
        idState=5,
        birthDay=datetime(1990, 1, 1),
    )


def test_member_data_view_model_creation(member_data_view_model):
    """Test creating a MemberDataViewModel instance"""
    model = member_data_view_model
    assert isinstance(model, MemberDataViewModel)
    assert model.gender == "Male"
    assert model.document == "123456789"
    assert model.zip_code == "12345"
    assert model.address == "123 Main St"
    assert model.number == "10A"
    assert model.complement == "Apt 1"
    assert model.neighborhood == "Downtown"
    assert model.city == "Metropolis"
    assert model.id_state == 5
    assert model.birth_day == datetime(1990, 1, 1)


def test_member_data_view_model_to_dict(member_data_view_model):
    """Test converting MemberDataViewModel to dictionary"""
    model_dict = member_data_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["gender"] == "Male"
    assert model_dict["document"] == "123456789"
    assert model_dict["zipCode"] == "12345"
    assert model_dict["address"] == "123 Main St"
    assert model_dict["number"] == "10A"
    assert model_dict["complement"] == "Apt 1"
    assert model_dict["neighborhood"] == "Downtown"
    assert model_dict["city"] == "Metropolis"
    assert model_dict["idState"] == 5
    assert model_dict["birthDay"] == "1990-01-01T00:00:00"


def test_member_data_view_model_equality(member_data_view_model):
    """Test equality comparison of MemberDataViewModel instances"""
    same_model = MemberDataViewModel(
        cellphone=None,
        email=None,
        gender="Male",
        document="123456789",
        zipCode="12345",
        address="123 Main St",
        number="10A",
        complement="Apt 1",
        neighborhood="Downtown",
        city="Metropolis",
        idState=5,
        birthDay=datetime(1990, 1, 1),
    )

    different_model = MemberDataViewModel(
        cellphone=None,
        email=None,
        gender="Female",
        document="987654321",
        zipCode="54321",
        address="456 Elm St",
        number="20B",
        complement="Apt 2",
        neighborhood="Uptown",
        city="Gotham",
        idState=10,
        birthDay=datetime(1995, 5, 5),
    )

    assert member_data_view_model == same_model
    assert member_data_view_model != different_model
    assert member_data_view_model != 1
