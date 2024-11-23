# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
import pytest
from evo_client.models.log_tef_api_view_model import LogTefApiViewModel


@pytest.fixture
def log_tef_api_view_model():
    return LogTefApiViewModel(
        authorization="auth123", tefId="tef123", merchantCheckoutGuid="guid123"
    )


def test_log_tef_api_view_model_creation(log_tef_api_view_model):
    """Test creating a LogTefApiViewModel instance"""
    model = log_tef_api_view_model
    assert isinstance(model, LogTefApiViewModel)
    assert model.authorization == "auth123"
    assert model.tef_id == "tef123"
    assert model.merchant_checkout_guid == "guid123"


def test_log_tef_api_view_model_to_dict(log_tef_api_view_model):
    """Test converting LogTefApiViewModel to dictionary"""
    model_dict = log_tef_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["authorization"] == "auth123"
    assert model_dict["tefId"] == "tef123"
    assert model_dict["merchantCheckoutGuid"] == "guid123"


def test_log_tef_api_view_model_equality(log_tef_api_view_model):
    """Test equality comparison of LogTefApiViewModel instances"""
    same_model = LogTefApiViewModel(
        authorization="auth123", tefId="tef123", merchantCheckoutGuid="guid123"
    )

    different_model = LogTefApiViewModel(
        authorization="auth456", tefId="tef456", merchantCheckoutGuid="guid456"
    )

    assert log_tef_api_view_model == same_model
    assert log_tef_api_view_model != different_model