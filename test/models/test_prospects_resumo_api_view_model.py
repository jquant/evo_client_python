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

from evo_client.models.prospect_responsavel_resumo_api_view_model import (
    ProspectResponsavelResumoApiViewModel,
)
from evo_client.models.prospects_resumo_api_view_model import (
    ProspectsResumoApiViewModel,
)


@pytest.fixture
def prospects_resumo_api_view_model():
    return ProspectsResumoApiViewModel(
        idProspect=1,
        idBranch=2,
        branchName="Main Branch",
        firstName="John",
        lastName="Doe",
        document="123456789",
        cellphone="+1234567890",
        email="john.doe@example.com",
        gympassId="G123",
        registerDate=datetime(2023, 1, 1),
        gender="Male",
        birthDate=datetime(1990, 1, 1),
        signupType="Online",
        mktChannel="Social Media",
        conversionDate=datetime(2023, 2, 1),
        idMember=10,
        currentStep="Contacted",
        address="123 Main St",
        city="Anytown",
        complement="Apt 4",
        neighborhood="Downtown",
        state="State",
        country="Country",
        zipCode="12345",
        number="123",
        responsible=ProspectResponsavelResumoApiViewModel(
            document="123456789", name="Jane Doe", financialResponsible=True
        ),
    )


def test_prospects_resumo_api_view_model_creation(prospects_resumo_api_view_model):
    """Test creating a ProspectsResumoApiViewModel instance"""
    assert isinstance(prospects_resumo_api_view_model, ProspectsResumoApiViewModel)
    assert prospects_resumo_api_view_model.id_prospect == 1
    assert prospects_resumo_api_view_model.first_name == "John"
    assert prospects_resumo_api_view_model.last_name == "Doe"
    assert prospects_resumo_api_view_model.email == "john.doe@example.com"
    assert prospects_resumo_api_view_model.gender == "Male"


def test_prospects_resumo_api_view_model_to_dict(prospects_resumo_api_view_model):
    """Test converting ProspectsResumoApiViewModel to dictionary"""
    model_dict = prospects_resumo_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idProspect"] == 1
    assert model_dict["firstName"] == "John"
    assert model_dict["lastName"] == "Doe"
    assert model_dict["email"] == "john.doe@example.com"
    assert model_dict["gender"] == "Male"


def test_prospects_resumo_api_view_model_equality(prospects_resumo_api_view_model):
    """Test equality comparison of ProspectsResumoApiViewModel instances"""
    same_model = ProspectsResumoApiViewModel(
        idProspect=1,
        idBranch=2,
        branchName="Main Branch",
        firstName="John",
        lastName="Doe",
        document="123456789",
        cellphone="+1234567890",
        email="john.doe@example.com",
        gympassId="G123",
        registerDate=datetime(2023, 1, 1),
        gender="Male",
        birthDate=datetime(1990, 1, 1),
        signupType="Online",
        mktChannel="Social Media",
        conversionDate=datetime(2023, 2, 1),
        idMember=10,
        currentStep="Contacted",
        address="123 Main St",
        city="Anytown",
        complement="Apt 4",
        neighborhood="Downtown",
        state="State",
        country="Country",
        zipCode="12345",
        number="123",
        responsible=ProspectResponsavelResumoApiViewModel(
            document="123456789", name="Jane Doe", financialResponsible=True
        ),
    )

    different_model = ProspectsResumoApiViewModel(
        idProspect=2,
        firstName="Jane",
        lastName="Smith",
        email="jane.smith@example.com",
        gender="Female",
    )

    assert prospects_resumo_api_view_model == same_model
    assert prospects_resumo_api_view_model != different_model
    assert prospects_resumo_api_view_model != 1
