# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
from datetime import datetime
import pytest

from evo_client.models.installment_view_model import InstallmentViewModel


@pytest.fixture
def installment_view_model():
    return InstallmentViewModel(
        totalValue=200.0,
        value=100.0,
        date=datetime(2023, 11, 1),
        serviceName="Gym Membership",
        serviceValue=150.0,
        loyaltyMonthlyPaymentDescription="Monthly Loyalty Payment",
        loyaltyMonthlyPaymentValueDescription="Loyalty Payment Value",
        annuityServiceName="Annual Service",
        annuityServiceValue=50.0,
    )


def test_installment_view_model_creation(installment_view_model):
    """Test creating an InstallmentViewModel instance"""
    model = installment_view_model
    assert isinstance(model, InstallmentViewModel)
    assert model.total_value == 200.0
    assert model.value == 100.0
    assert model.date == datetime(2023, 11, 1)
    assert model.service_name == "Gym Membership"
    assert model.service_value == 150.0
    assert model.loyalty_monthly_payment_description == "Monthly Loyalty Payment"
    assert model.loyalty_monthly_payment_value_description == "Loyalty Payment Value"
    assert model.annuity_service_name == "Annual Service"
    assert model.annuity_service_value == 50.0


def test_installment_view_model_to_dict(installment_view_model):
    """Test converting InstallmentViewModel to dictionary"""
    model_dict = installment_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["totalValue"] == 200.0
    assert model_dict["value"] == 100.0
    assert model_dict["date"] == "2023-11-01T00:00:00"
    assert model_dict["serviceName"] == "Gym Membership"
    assert model_dict["serviceValue"] == 150.0
    assert model_dict["loyaltyMonthlyPaymentDescription"] == "Monthly Loyalty Payment"
    assert (
        model_dict["loyaltyMonthlyPaymentValueDescription"] == "Loyalty Payment Value"
    )
    assert model_dict["annuityServiceName"] == "Annual Service"
    assert model_dict["annuityServiceValue"] == 50.0


def test_installment_view_model_equality(installment_view_model):
    """Test equality comparison of InstallmentViewModel instances"""
    same_model = InstallmentViewModel(
        totalValue=200.0,
        value=100.0,
        date=datetime(2023, 11, 1),
        serviceName="Gym Membership",
        serviceValue=150.0,
        loyaltyMonthlyPaymentDescription="Monthly Loyalty Payment",
        loyaltyMonthlyPaymentValueDescription="Loyalty Payment Value",
        annuityServiceName="Annual Service",
        annuityServiceValue=50.0,
    )

    different_model = InstallmentViewModel(
        totalValue=300.0,
        value=150.0,
        date=datetime(2023, 12, 1),
        serviceName="Premium Membership",
        serviceValue=200.0,
        loyaltyMonthlyPaymentDescription="Premium Loyalty Payment",
        loyaltyMonthlyPaymentValueDescription="Premium Payment Value",
        annuityServiceName="Premium Service",
        annuityServiceValue=100.0,
    )

    assert installment_view_model == same_model
    assert installment_view_model != different_model
    assert installment_view_model != 1
