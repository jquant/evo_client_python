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

from evo_client.models.employee_api_integracao_view_model import (
    EmployeeApiIntegracaoViewModel,
)


@pytest.fixture
def employee_api_integracao_view_model():
    return EmployeeApiIntegracaoViewModel(
        name="John",
        lastName="Doe",
        document="123456789",
        documentId="ID123456",
        cellphone="(123) 456-7890",
        email="john.doe@example.com",
        gender="Male",
        birthday=datetime(1990, 1, 1),
        country="USA",
        address="123 Main St",
        state="NY",
        city="New York",
        passport="P1234567",
        zipCode="10001",
        complement="Apt 101",
        neighborhood="Manhattan",
        number="123",
        active=True,
    )


def test_employee_api_integracao_view_model_creation(
    employee_api_integracao_view_model,
):
    """Test creating an EmployeeApiIntegracaoViewModel instance"""
    model = employee_api_integracao_view_model
    assert isinstance(model, EmployeeApiIntegracaoViewModel)
    assert model.name == "John"
    assert model.last_name == "Doe"
    assert model.document == "123456789"
    assert model.document_id == "ID123456"
    assert model.cellphone == "(123) 456-7890"
    assert model.email == "john.doe@example.com"
    assert model.gender == "Male"
    assert model.birthday == datetime(1990, 1, 1)
    assert model.country == "USA"
    assert model.address == "123 Main St"
    assert model.state == "NY"
    assert model.city == "New York"
    assert model.passport == "P1234567"
    assert model.zip_code == "10001"
    assert model.complement == "Apt 101"
    assert model.neighborhood == "Manhattan"
    assert model.number == "123"
    assert model.active is True


def test_employee_api_integracao_view_model_to_dict(employee_api_integracao_view_model):
    """Test converting EmployeeApiIntegracaoViewModel to dictionary"""
    model_dict = employee_api_integracao_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["name"] == "John"
    assert model_dict["lastName"] == "Doe"
    assert model_dict["document"] == "123456789"
    assert model_dict["documentId"] == "ID123456"
    assert model_dict["cellphone"] == "(123) 456-7890"
    assert model_dict["email"] == "john.doe@example.com"
    assert model_dict["gender"] == "Male"
    assert model_dict["birthday"] == "1990-01-01T00:00:00"
    assert model_dict["country"] == "USA"
    assert model_dict["address"] == "123 Main St"
    assert model_dict["state"] == "NY"
    assert model_dict["city"] == "New York"
    assert model_dict["passport"] == "P1234567"
    assert model_dict["zipCode"] == "10001"
    assert model_dict["complement"] == "Apt 101"
    assert model_dict["neighborhood"] == "Manhattan"
    assert model_dict["number"] == "123"
    assert model_dict["active"] is True


def test_employee_api_integracao_view_model_equality(
    employee_api_integracao_view_model,
):
    """Test equality comparison of EmployeeApiIntegracaoViewModel instances"""
    same_model = EmployeeApiIntegracaoViewModel(
        name="John",
        lastName="Doe",
        document="123456789",
        documentId="ID123456",
        cellphone="(123) 456-7890",
        email="john.doe@example.com",
        gender="Male",
        birthday=datetime(1990, 1, 1),
        country="USA",
        address="123 Main St",
        state="NY",
        city="New York",
        passport="P1234567",
        zipCode="10001",
        complement="Apt 101",
        neighborhood="Manhattan",
        number="123",
        active=True,
    )

    different_model = EmployeeApiIntegracaoViewModel(
        name="Jane",
        lastName="Smith",
        document="987654321",
        documentId="ID987654",
        cellphone="(987) 654-3210",
        email="jane.smith@example.com",
        gender="Female",
        birthday=datetime(1992, 2, 2),
        country="Canada",
        address="456 Elm St",
        state="ON",
        city="Toronto",
        passport="P7654321",
        zipCode="M5H 2N2",
        complement="Suite 202",
        neighborhood="Downtown",
        number="456",
        active=False,
    )

    assert employee_api_integracao_view_model == same_model
    assert employee_api_integracao_view_model != different_model
    assert employee_api_integracao_view_model != 1
