# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.diferenciais_api_view_model import DiferenciaisApiViewModel


@pytest.fixture
def diferenciais_api_view_model():
    return DiferenciaisApiViewModel(title="Unique Feature", order=1)


def test_diferenciais_api_view_model_creation(diferenciais_api_view_model):
    """Test creating a DiferenciaisApiViewModel instance"""
    assert isinstance(diferenciais_api_view_model, DiferenciaisApiViewModel)
    assert diferenciais_api_view_model.title == "Unique Feature"
    assert diferenciais_api_view_model.order == 1


def test_diferenciais_api_view_model_to_dict(diferenciais_api_view_model):
    """Test converting DiferenciaisApiViewModel to dictionary"""
    model_dict = diferenciais_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["title"] == "Unique Feature"
    assert model_dict["order"] == 1


def test_diferenciais_api_view_model_equality(diferenciais_api_view_model):
    """Test equality comparison of DiferenciaisApiViewModel instances"""
    same_model = DiferenciaisApiViewModel(title="Unique Feature", order=1)
    different_model = DiferenciaisApiViewModel(title="Another Feature", order=2)

    assert diferenciais_api_view_model == same_model
    assert diferenciais_api_view_model != different_model
    assert diferenciais_api_view_model != 1
