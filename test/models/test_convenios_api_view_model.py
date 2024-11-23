# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
from typing import Optional

import pytest
from evo_client.models.convenios_api_view_model import ConveniosApiViewModel


@pytest.fixture
def convenios_api_view_model():
    return ConveniosApiViewModel(
        idPartnership=1,
        description="Partnership Description",
        isBlockedFlag=False,
        isInactiveFlag=False,
        isRecurringDiscountFlag=True,
        discount=10.0,
        discountType=1.0,
        advancedDiscount=5,
    )


def test_convenios_api_view_model_creation(convenios_api_view_model):
    """Test creating a ConveniosApiViewModel instance"""
    assert isinstance(convenios_api_view_model, ConveniosApiViewModel)
    assert convenios_api_view_model.id_partnership == 1
    assert convenios_api_view_model.description == "Partnership Description"
    assert convenios_api_view_model.is_blocked_flag is False
    assert convenios_api_view_model.is_inactive_flag is False
    assert convenios_api_view_model.is_recurring_discount_flag is True
    assert convenios_api_view_model.discount == 10.0
    assert convenios_api_view_model.discount_type == 1.0
    assert convenios_api_view_model.advanced_discount == 5


def test_convenios_api_view_model_to_dict(convenios_api_view_model):
    """Test converting ConveniosApiViewModel to dictionary"""
    model_dict = convenios_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idPartnership"] == 1
    assert model_dict["description"] == "Partnership Description"
    assert model_dict["isBlockedFlag"] is False
    assert model_dict["isInactiveFlag"] is False
    assert model_dict["isRecurringDiscountFlag"] is True
    assert model_dict["discount"] == 10.0
    assert model_dict["discountType"] == 1.0
    assert model_dict["advancedDiscount"] == 5


def test_convenios_api_view_model_equality(convenios_api_view_model):
    """Test equality comparison of ConveniosApiViewModel instances"""
    same_model = ConveniosApiViewModel(
        idPartnership=1,
        description="Partnership Description",
        isBlockedFlag=False,
        isInactiveFlag=False,
        isRecurringDiscountFlag=True,
        discount=10.0,
        discountType=1.0,
        advancedDiscount=5,
    )

    different_model = ConveniosApiViewModel(
        idPartnership=2,
        description="Different Partnership",
        isBlockedFlag=True,
        isInactiveFlag=True,
        isRecurringDiscountFlag=False,
        discount=20.0,
        discountType=2.0,
        advancedDiscount=10,
    )

    assert convenios_api_view_model == same_model
    assert convenios_api_view_model != different_model
    assert convenios_api_view_model != 1
