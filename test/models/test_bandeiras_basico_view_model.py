# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
from typing import Optional

import pytest
from evo_client.models.bandeiras_basico_view_model import BandeirasBasicoViewModel


@pytest.fixture
def bandeiras_basico_view_model():
    return BandeirasBasicoViewModel(
        value="Visa", text="Visa Card", logoUrl="https://example.com/visa_logo.png"
    )


def test_bandeiras_basico_view_model_creation(bandeiras_basico_view_model):
    """Test creating a BandeirasBasicoViewModel instance"""
    assert isinstance(bandeiras_basico_view_model, BandeirasBasicoViewModel)
    assert bandeiras_basico_view_model.value == "Visa"
    assert bandeiras_basico_view_model.text == "Visa Card"
    assert bandeiras_basico_view_model.logo_url == "https://example.com/visa_logo.png"


def test_bandeiras_basico_view_model_to_dict(bandeiras_basico_view_model):
    """Test converting BandeirasBasicoViewModel to dictionary"""
    model_dict = bandeiras_basico_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["value"] == "Visa"
    assert model_dict["text"] == "Visa Card"
    assert model_dict["logoUrl"] == "https://example.com/visa_logo.png"


def test_bandeiras_basico_view_model_equality(bandeiras_basico_view_model):
    """Test equality comparison of BandeirasBasicoViewModel instances"""
    same_model = BandeirasBasicoViewModel(
        value="Visa", text="Visa Card", logoUrl="https://example.com/visa_logo.png"
    )

    different_model = BandeirasBasicoViewModel(
        value="MasterCard",
        text="MasterCard",
        logoUrl="https://example.com/mastercard_logo.png",
    )

    assert bandeiras_basico_view_model == same_model
    assert bandeiras_basico_view_model != different_model
    assert bandeiras_basico_view_model != 1
