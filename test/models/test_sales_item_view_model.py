# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.sales_item_view_model import SalesItemViewModel


@pytest.fixture
def sales_item_view_model():
    return SalesItemViewModel(
        idMembership=1,
        membership="Gold Membership",
        loyaltyInstallment=True,
        membershipType="Annual",
        loyaltyTime=12,
        validityDescription="Valid for 12 months",
        reverseInstallmentsDescription="No reverse installments",
        valueDaysMonthsDefinedValidity=365,
        serviceValue=1000.0,
        serviceName="Gym Access",
        remark="Includes all classes",
        membershipText="Gold Membership Plan",
        annuityServiceName="Annual Fee",
        annuityServiceValue=100.0,
        annuityDay=1,
        annuityMonth=1,
        annuityChargeType=1,
        annuityInstallmentsCount=12,
        promotionalDaysCount=30,
        promoDayMonthType=1,
        installmentsCount=12,
        promotionalValueDescription="Discounted for first month",
        idService=101,
        name="Gold Membership",
        flSpotlight=True,
        order=1,
        type=1,
        chargeValue=1000.0,
        chargeValueDescription="Standard charge",
        totalValue=1200.0,
        taxValue=200.0,
        percentageType=True,
        flChargeServiceAutomaticRenew=True,
        flBankSlip=False,
        flCard=True,
        flCreditBalance=False,
        flRegisterRequiredAddress=True,
        flPrioritizeRegistrationSale=False,
        ageFrom=18,
        ageTo=65,
        differentials=[],
        membershipBranches=[1, 2, 3],
    )


def test_sales_item_view_model_creation(sales_item_view_model):
    """Test creating a SalesItemViewModel instance"""
    assert isinstance(sales_item_view_model, SalesItemViewModel)
    assert sales_item_view_model.id_membership == 1
    assert sales_item_view_model.membership == "Gold Membership"
    assert sales_item_view_model.loyalty_installment is True
    assert sales_item_view_model.service_value == 1000.0
    assert sales_item_view_model.service_name == "Gym Access"
    assert sales_item_view_model.fl_spotlight is True


def test_sales_item_view_model_to_dict(sales_item_view_model):
    """Test converting SalesItemViewModel to dictionary"""
    model_dict = sales_item_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idMembership"] == 1
    assert model_dict["membership"] == "Gold Membership"
    assert model_dict["loyaltyInstallment"] is True
    assert model_dict["serviceValue"] == 1000.0
    assert model_dict["serviceName"] == "Gym Access"
    assert model_dict["flSpotlight"] is True


def test_sales_item_view_model_equality(sales_item_view_model):
    """Test equality comparison of SalesItemViewModel instances"""
    same_model = SalesItemViewModel(
        idMembership=1,
        membership="Gold Membership",
        loyaltyInstallment=True,
        membershipType="Annual",
        loyaltyTime=12,
        validityDescription="Valid for 12 months",
        reverseInstallmentsDescription="No reverse installments",
        valueDaysMonthsDefinedValidity=365,
        serviceValue=1000.0,
        serviceName="Gym Access",
        remark="Includes all classes",
        membershipText="Gold Membership Plan",
        annuityServiceName="Annual Fee",
        annuityServiceValue=100.0,
        annuityDay=1,
        annuityMonth=1,
        annuityChargeType=1,
        annuityInstallmentsCount=12,
        promotionalDaysCount=30,
        promoDayMonthType=1,
        installmentsCount=12,
        promotionalValueDescription="Discounted for first month",
        idService=101,
        name="Gold Membership",
        flSpotlight=True,
        order=1,
        type=1,
        chargeValue=1000.0,
        chargeValueDescription="Standard charge",
        totalValue=1200.0,
        taxValue=200.0,
        percentageType=True,
        flChargeServiceAutomaticRenew=True,
        flBankSlip=False,
        flCard=True,
        flCreditBalance=False,
        flRegisterRequiredAddress=True,
        flPrioritizeRegistrationSale=False,
        ageFrom=18,
        ageTo=65,
        differentials=[],
        membershipBranches=[1, 2, 3],
    )

    different_model = SalesItemViewModel(
        idMembership=2,
        membership="Silver Membership",
        loyaltyInstallment=False,
        serviceValue=800.0,
        serviceName="Gym Access Limited",
        flSpotlight=False,
    )

    assert sales_item_view_model == same_model
    assert sales_item_view_model != different_model
    assert sales_item_view_model != 1
