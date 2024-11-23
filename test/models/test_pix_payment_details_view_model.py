# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
from datetime import datetime

import pytest

from evo_client.models.pix_payment_details_view_model import PixPaymentDetailsViewModel


@pytest.fixture
def pix_payment_details_view_model():
    return PixPaymentDetailsViewModel(
        qrCode="sampleQRCode",
        expirationDate=datetime(2024, 3, 15, 9, 0),
        value=100.50,
    )


def test_pix_payment_details_view_model_creation(pix_payment_details_view_model):
    """Test creating a PixPaymentDetailsViewModel instance"""
    model = pix_payment_details_view_model
    assert isinstance(model, PixPaymentDetailsViewModel)
    assert model.qr_code == "sampleQRCode"
    assert model.expiration_date == datetime(2024, 3, 15, 9, 0)
    assert model.value == 100.50


def test_pix_payment_details_view_model_to_dict(pix_payment_details_view_model):
    """Test converting PixPaymentDetailsViewModel to dictionary"""
    model_dict = pix_payment_details_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["qrCode"] == "sampleQRCode"
    assert model_dict["expirationDate"] == "2024-03-15T09:00:00"
    assert model_dict["value"] == 100.50


def test_pix_payment_details_view_model_equality(pix_payment_details_view_model):
    """Test equality comparison of PixPaymentDetailsViewModel instances"""
    same_model = PixPaymentDetailsViewModel(
        qrCode="sampleQRCode",
        expirationDate=datetime(2024, 3, 15, 9, 0),
        value=100.50,
    )

    different_model = PixPaymentDetailsViewModel(
        qrCode="differentQRCode",
        expirationDate=datetime(2024, 3, 16, 10, 0),
        value=200.75,
    )

    assert pix_payment_details_view_model == same_model
    assert pix_payment_details_view_model != different_model
