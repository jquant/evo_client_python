# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.contrato_filiais_resumo_api_view_model import (
    ContratoFiliaisResumoApiViewModel,
)


@pytest.fixture
def contrato_filiais_resumo_api_view_model():
    return ContratoFiliaisResumoApiViewModel(idBranch=1, name="Main Branch")


def test_contrato_filiais_resumo_api_view_model_creation(
    contrato_filiais_resumo_api_view_model,
):
    """Test creating a ContratoFiliaisResumoApiViewModel instance"""
    assert isinstance(
        contrato_filiais_resumo_api_view_model, ContratoFiliaisResumoApiViewModel
    )
    assert contrato_filiais_resumo_api_view_model.id_branch == 1
    assert contrato_filiais_resumo_api_view_model.name == "Main Branch"


def test_contrato_filiais_resumo_api_view_model_to_dict(
    contrato_filiais_resumo_api_view_model,
):
    """Test converting ContratoFiliaisResumoApiViewModel to dictionary"""
    model_dict = contrato_filiais_resumo_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idBranch"] == 1
    assert model_dict["name"] == "Main Branch"


def test_contrato_filiais_resumo_api_view_model_equality(
    contrato_filiais_resumo_api_view_model,
):
    """Test equality comparison of ContratoFiliaisResumoApiViewModel instances"""
    same_model = ContratoFiliaisResumoApiViewModel(idBranch=1, name="Main Branch")

    different_model = ContratoFiliaisResumoApiViewModel(
        idBranch=2, name="Secondary Branch"
    )

    assert contrato_filiais_resumo_api_view_model == same_model
    assert contrato_filiais_resumo_api_view_model != different_model
    assert contrato_filiais_resumo_api_view_model != 1
