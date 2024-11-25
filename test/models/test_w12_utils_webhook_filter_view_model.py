# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.w12_utils_webhook_filter_view_model import (
    W12UtilsWebhookFilterViewModel,
)


@pytest.fixture
def w12_utils_webhook_filter_view_model():
    return W12UtilsWebhookFilterViewModel(filterType="TypeA", value="ValueA")


def test_w12_utils_webhook_filter_view_model_creation(
    w12_utils_webhook_filter_view_model,
):
    """Test creating a W12UtilsWebhookFilterViewModel instance"""
    assert isinstance(
        w12_utils_webhook_filter_view_model, W12UtilsWebhookFilterViewModel
    )
    assert w12_utils_webhook_filter_view_model.filter_type == "TypeA"
    assert w12_utils_webhook_filter_view_model.value == "ValueA"


def test_w12_utils_webhook_filter_view_model_to_dict(
    w12_utils_webhook_filter_view_model,
):
    """Test converting W12UtilsWebhookFilterViewModel to dictionary"""
    model_dict = w12_utils_webhook_filter_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["filterType"] == "TypeA"
    assert model_dict["value"] == "ValueA"


def test_w12_utils_webhook_filter_view_model_equality(
    w12_utils_webhook_filter_view_model,
):
    """Test equality comparison of W12UtilsWebhookFilterViewModel instances"""
    same_model = W12UtilsWebhookFilterViewModel(filterType="TypeA", value="ValueA")

    different_model = W12UtilsWebhookFilterViewModel(filterType="TypeB", value="ValueB")

    assert w12_utils_webhook_filter_view_model == same_model
    assert w12_utils_webhook_filter_view_model != different_model
    assert w12_utils_webhook_filter_view_model != 1
