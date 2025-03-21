# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.funcionarios_resumo_api_view_model import (
    FuncionariosResumoApiViewModel,
)


@pytest.fixture
def funcionarios_resumo_api_view_model():
    return FuncionariosResumoApiViewModel(
        idEmployee=1,
        name="Jane Doe",
        email="jane.doe@example.com",
        telephone="123456789",
        jobPosition="Manager",
        status=True,
        photoUrl="https://example.com/photo.jpg",
    )


def test_funcionarios_resumo_api_view_model_creation(
    funcionarios_resumo_api_view_model,
):
    """Test creating a FuncionariosResumoApiViewModel instance"""
    model = funcionarios_resumo_api_view_model
    assert isinstance(model, FuncionariosResumoApiViewModel)
    assert model.id_employee == 1
    assert model.name == "Jane Doe"
    assert model.email == "jane.doe@example.com"
    assert model.telephone == "123456789"
    assert model.job_position == "Manager"
    assert model.status is True
    assert model.photo_url == "https://example.com/photo.jpg"


def test_funcionarios_resumo_api_view_model_to_dict(funcionarios_resumo_api_view_model):
    """Test converting FuncionariosResumoApiViewModel to dictionary"""
    model_dict = funcionarios_resumo_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idEmployee"] == 1
    assert model_dict["name"] == "Jane Doe"
    assert model_dict["email"] == "jane.doe@example.com"
    assert model_dict["telephone"] == "123456789"
    assert model_dict["jobPosition"] == "Manager"
    assert model_dict["status"] is True
    assert model_dict["photoUrl"] == "https://example.com/photo.jpg"


def test_funcionarios_resumo_api_view_model_equality(
    funcionarios_resumo_api_view_model,
):
    """Test equality comparison of FuncionariosResumoApiViewModel instances"""
    same_model = FuncionariosResumoApiViewModel(
        idEmployee=1,
        name="Jane Doe",
        email="jane.doe@example.com",
        telephone="123456789",
        jobPosition="Manager",
        status=True,
        photoUrl="https://example.com/photo.jpg",
    )

    different_model = FuncionariosResumoApiViewModel(
        idEmployee=2,
        name="John Smith",
        email="john.smith@example.com",
        telephone="987654321",
        jobPosition="Assistant",
        status=False,
        photoUrl="https://example.com/photo2.jpg",
    )

    assert funcionarios_resumo_api_view_model == same_model
    assert funcionarios_resumo_api_view_model != different_model
    assert funcionarios_resumo_api_view_model != 1
