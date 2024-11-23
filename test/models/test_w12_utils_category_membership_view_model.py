# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)


@pytest.fixture
def w12_utils_category_membership_view_model():
    return W12UtilsCategoryMembershipViewModel(
        idCategoryMembership=1, name="Premium Membership"
    )


def test_w12_utils_category_membership_view_model_creation(
    w12_utils_category_membership_view_model,
):
    """Test creating a W12UtilsCategoryMembershipViewModel instance"""
    assert isinstance(
        w12_utils_category_membership_view_model, W12UtilsCategoryMembershipViewModel
    )
    assert w12_utils_category_membership_view_model.id_category_membership == 1
    assert w12_utils_category_membership_view_model.name == "Premium Membership"


def test_w12_utils_category_membership_view_model_to_dict(
    w12_utils_category_membership_view_model,
):
    """Test converting W12UtilsCategoryMembershipViewModel to dictionary"""
    model_dict = w12_utils_category_membership_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idCategoryMembership"] == 1
    assert model_dict["name"] == "Premium Membership"


def test_w12_utils_category_membership_view_model_equality(
    w12_utils_category_membership_view_model,
):
    """Test equality comparison of W12UtilsCategoryMembershipViewModel instances"""
    same_model = W12UtilsCategoryMembershipViewModel(
        idCategoryMembership=1, name="Premium Membership"
    )

    different_model = W12UtilsCategoryMembershipViewModel(
        idCategoryMembership=2, name="Basic Membership"
    )

    assert w12_utils_category_membership_view_model == same_model
    assert w12_utils_category_membership_view_model != 1
    assert w12_utils_category_membership_view_model != different_model
