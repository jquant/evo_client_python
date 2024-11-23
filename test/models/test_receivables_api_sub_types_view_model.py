# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.receivables_api_sub_types_view_model import (
    ReceivablesApiSubTypesViewModel,
)


@pytest.fixture
def receivables_api_sub_types_view_model():
    return ReceivablesApiSubTypesViewModel(
        id=1,
        name="Sample SubType",
    )


def test_receivables_api_sub_types_view_model_creation(
    receivables_api_sub_types_view_model,
):
    """Test creating a ReceivablesApiSubTypesViewModel instance"""
    assert isinstance(
        receivables_api_sub_types_view_model, ReceivablesApiSubTypesViewModel
    )
    assert receivables_api_sub_types_view_model.id == 1
    assert receivables_api_sub_types_view_model.name == "Sample SubType"


def test_receivables_api_sub_types_view_model_to_dict(
    receivables_api_sub_types_view_model,
):
    """Test converting ReceivablesApiSubTypesViewModel to dictionary"""
    model_dict = receivables_api_sub_types_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["id"] == 1
    assert model_dict["name"] == "Sample SubType"


def test_receivables_api_sub_types_view_model_equality(
    receivables_api_sub_types_view_model,
):
    """Test equality comparison of ReceivablesApiSubTypesViewModel instances"""
    same_model = ReceivablesApiSubTypesViewModel(
        id=1,
        name="Sample SubType",
    )

    different_model = ReceivablesApiSubTypesViewModel(
        id=2,
        name="Different SubType",
    )

    assert receivables_api_sub_types_view_model == same_model
    assert receivables_api_sub_types_view_model != different_model
