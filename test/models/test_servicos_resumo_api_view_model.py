# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.servicos_resumo_api_view_model import ServicosResumoApiViewModel


@pytest.fixture
def servicos_resumo_api_view_model():
    return ServicosResumoApiViewModel(
        idService=1,
        idBranch=2,
        nameService="Personal Training",
        value=100.0,
        allowEntries=True,
        experimentalClass=False,
        maxAmountInstallments=12,
        urlSale="https://example.com/sale",
        inactive=False,
        onlineSalesObservations="Available online",
    )


def test_servicos_resumo_api_view_model_creation(servicos_resumo_api_view_model):
    """Test creating a ServicosResumoApiViewModel instance"""
    assert isinstance(servicos_resumo_api_view_model, ServicosResumoApiViewModel)
    assert servicos_resumo_api_view_model.id_service == 1
    assert servicos_resumo_api_view_model.id_branch == 2
    assert servicos_resumo_api_view_model.name_service == "Personal Training"
    assert servicos_resumo_api_view_model.value == 100.0
    assert servicos_resumo_api_view_model.allow_entries is True
    assert servicos_resumo_api_view_model.experimental_class is False
    assert servicos_resumo_api_view_model.max_amount_installments == 12
    assert servicos_resumo_api_view_model.url_sale == "https://example.com/sale"
    assert servicos_resumo_api_view_model.inactive is False
    assert (
        servicos_resumo_api_view_model.online_sales_observations == "Available online"
    )


def test_servicos_resumo_api_view_model_to_dict(servicos_resumo_api_view_model):
    """Test converting ServicosResumoApiViewModel to dictionary"""
    model_dict = servicos_resumo_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idService"] == 1
    assert model_dict["idBranch"] == 2
    assert model_dict["nameService"] == "Personal Training"
    assert model_dict["value"] == 100.0
    assert model_dict["allowEntries"] is True
    assert model_dict["experimentalClass"] is False
    assert model_dict["maxAmountInstallments"] == 12
    assert model_dict["urlSale"] == "https://example.com/sale"
    assert model_dict["inactive"] is False
    assert model_dict["onlineSalesObservations"] == "Available online"


def test_servicos_resumo_api_view_model_equality(servicos_resumo_api_view_model):
    """Test equality comparison of ServicosResumoApiViewModel instances"""
    same_model = ServicosResumoApiViewModel(
        idService=1,
        idBranch=2,
        nameService="Personal Training",
        value=100.0,
        allowEntries=True,
        experimentalClass=False,
        maxAmountInstallments=12,
        urlSale="https://example.com/sale",
        inactive=False,
        onlineSalesObservations="Available online",
    )

    different_model = ServicosResumoApiViewModel(
        idService=2,
        idBranch=3,
        nameService="Group Training",
        value=150.0,
        allowEntries=False,
        experimentalClass=True,
        maxAmountInstallments=6,
        urlSale="https://example.com/group-sale",
        inactive=True,
        onlineSalesObservations="Not available online",
    )

    assert servicos_resumo_api_view_model == same_model
    assert servicos_resumo_api_view_model != different_model
    assert servicos_resumo_api_view_model != 1
