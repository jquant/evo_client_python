# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
)


@pytest.fixture
def contratos_resumo_api_view_model():
    return ContratosResumoApiViewModel(
        idMembership=1,
        idBranch=2,
        nameMembership="Premium Membership",
        membershipType="Annual",
        durationType="Months",
        duration=12,
        value=499.99,
        maxAmountInstallments=12,
        description="Access to all facilities",
        urlSale="https://example.com/sale",
        onlineSalesObservations="Limited time offer",
        inactive=False,
        displayName="Premium",
    )


def test_contratos_resumo_api_view_model_creation(contratos_resumo_api_view_model):
    """Test creating a ContratosResumoApiViewModel instance"""
    assert isinstance(contratos_resumo_api_view_model, ContratosResumoApiViewModel)
    assert contratos_resumo_api_view_model.id_membership == 1
    assert contratos_resumo_api_view_model.id_branch == 2
    assert contratos_resumo_api_view_model.name_membership == "Premium Membership"
    assert contratos_resumo_api_view_model.membership_type == "Annual"
    assert contratos_resumo_api_view_model.duration == 12
    assert contratos_resumo_api_view_model.value == 499.99
    assert contratos_resumo_api_view_model.inactive is False


def test_contratos_resumo_api_view_model_to_dict(contratos_resumo_api_view_model):
    """Test converting ContratosResumoApiViewModel to dictionary"""
    model_dict = contratos_resumo_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idMembership"] == 1
    assert model_dict["idBranch"] == 2
    assert model_dict["nameMembership"] == "Premium Membership"
    assert model_dict["membershipType"] == "Annual"
    assert model_dict["duration"] == 12
    assert model_dict["value"] == 499.99
    assert model_dict["inactive"] is False


def test_contratos_resumo_api_view_model_equality(contratos_resumo_api_view_model):
    """Test equality comparison of ContratosResumoApiViewModel instances"""
    same_model = ContratosResumoApiViewModel(
        idMembership=1,
        idBranch=2,
        nameMembership="Premium Membership",
        membershipType="Annual",
        durationType="Months",
        duration=12,
        value=499.99,
        maxAmountInstallments=12,
        description="Access to all facilities",
        urlSale="https://example.com/sale",
        onlineSalesObservations="Limited time offer",
        inactive=False,
        displayName="Premium",
    )

    different_model = ContratosResumoApiViewModel(
        idMembership=2,
        idBranch=3,
        nameMembership="Basic Membership",
        membershipType="Monthly",
        duration=1,
        value=49.99,
        inactive=True,
    )

    assert contratos_resumo_api_view_model == same_model
    assert contratos_resumo_api_view_model != different_model
    assert contratos_resumo_api_view_model != 1
