# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.differentials_view_model import DifferentialsViewModel


@pytest.fixture
def differentials_view_model():
    return DifferentialsViewModel(title="Unique Feature", order=1)


def test_differentials_view_model_creation(differentials_view_model):
    """Test creating a DifferentialsViewModel instance"""
    assert isinstance(differentials_view_model, DifferentialsViewModel)
    assert differentials_view_model.title == "Unique Feature"
    assert differentials_view_model.order == 1


def test_differentials_view_model_to_dict(differentials_view_model):
    """Test converting DifferentialsViewModel to dictionary"""
    model_dict = differentials_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["title"] == "Unique Feature"
    assert model_dict["order"] == 1


def test_differentials_view_model_equality(differentials_view_model):
    """Test equality comparison of DifferentialsViewModel instances"""
    same_model = DifferentialsViewModel(title="Unique Feature", order=1)

    different_model = DifferentialsViewModel(title="Another Feature", order=2)

    assert differentials_view_model == same_model
    assert differentials_view_model != different_model
    assert differentials_view_model != 1
