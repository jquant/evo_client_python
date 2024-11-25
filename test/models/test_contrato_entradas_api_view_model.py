# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest
from evo_client.models.contrato_entradas_api_view_model import (
    ContratoEntradasApiViewModel,
)


@pytest.fixture
def contrato_entradas_api_view_model():
    return ContratoEntradasApiViewModel(
        entriesQuantity=5, idEntriesType=1, entriesTypeDescription="Standard Entry"
    )


def test_contrato_entradas_api_view_model_creation(contrato_entradas_api_view_model):
    """Test creating a ContratoEntradasApiViewModel instance"""
    assert isinstance(contrato_entradas_api_view_model, ContratoEntradasApiViewModel)
    assert contrato_entradas_api_view_model.entries_quantity == 5
    assert contrato_entradas_api_view_model.id_entries_type == 1
    assert contrato_entradas_api_view_model.entries_type_description == "Standard Entry"


def test_contrato_entradas_api_view_model_to_dict(contrato_entradas_api_view_model):
    """Test converting ContratoEntradasApiViewModel to dictionary"""
    model_dict = contrato_entradas_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["entriesQuantity"] == 5
    assert model_dict["idEntriesType"] == 1
    assert model_dict["entriesTypeDescription"] == "Standard Entry"


def test_contrato_entradas_api_view_model_equality(contrato_entradas_api_view_model):
    """Test equality comparison of ContratoEntradasApiViewModel instances"""
    same_model = ContratoEntradasApiViewModel(
        entriesQuantity=5, idEntriesType=1, entriesTypeDescription="Standard Entry"
    )

    different_model = ContratoEntradasApiViewModel(
        entriesQuantity=10, idEntriesType=2, entriesTypeDescription="Premium Entry"
    )

    assert contrato_entradas_api_view_model == same_model
    assert contrato_entradas_api_view_model != different_model
    assert contrato_entradas_api_view_model != 1
