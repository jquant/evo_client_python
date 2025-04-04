# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.prospect_id_view_model import ProspectIdViewModel


@pytest.fixture
def prospect_id_view_model():
    return ProspectIdViewModel(idProspect=1)


def test_prospect_id_view_model_creation(prospect_id_view_model):
    """Test creating a ProspectIdViewModel instance"""
    assert isinstance(prospect_id_view_model, ProspectIdViewModel)
    assert prospect_id_view_model.id_prospect == 1


def test_prospect_id_view_model_to_dict(prospect_id_view_model):
    """Test converting ProspectIdViewModel to dictionary"""
    model_dict = prospect_id_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idProspect"] == 1


def test_prospect_id_view_model_equality(prospect_id_view_model):
    """Test equality comparison of ProspectIdViewModel instances"""
    same_model = ProspectIdViewModel(idProspect=1)

    different_model = ProspectIdViewModel(idProspect=2)

    assert prospect_id_view_model == same_model
    assert prospect_id_view_model != different_model
    assert prospect_id_view_model != 1
