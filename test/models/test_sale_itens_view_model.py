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

from evo_client.models.sale_itens_view_model import SaleItensViewModel


@pytest.fixture
def sale_itens_view_model():
    return SaleItensViewModel(
        idSaleItem=1,
        description="Sample Item",
        item="Item Name",
        itemValue=100.0,
        saleValue=120.0,
        saleValueWithoutCreditValue=110.0,
        quantity=2,
        idMembership=3,
        idMembershipRenewed=4,
        numMembers=5,
        idProduct=6,
        idService=7,
        corporatePartnershipName="Corporate Partner",
        coporatePartnershipId=8,
        membershipStartDate=datetime(2023, 1, 1),
        discount=10.0,
        corporateDiscount=5.0,
        tax=2.0,
        voucher="VOUCHER123",
        accountingCode="ACC123",
        municipalServiceCode="MUN123",
        flReceiptOnly=True,
        idSaleItemMigration="MIG123",
        flSwimming=False,
        flAllowLocker=True,
        idMemberMembership=9,
        valueNextMonth=130.0,
    )


def test_sale_itens_view_model_creation(sale_itens_view_model):
    """Test creating a SaleItensViewModel instance"""
    assert isinstance(sale_itens_view_model, SaleItensViewModel)
    assert sale_itens_view_model.id_sale_item == 1
    assert sale_itens_view_model.description == "Sample Item"
    assert sale_itens_view_model.item == "Item Name"
    assert sale_itens_view_model.item_value == 100.0
    assert sale_itens_view_model.sale_value == 120.0
    assert sale_itens_view_model.quantity == 2
    assert sale_itens_view_model.corporate_partnership_name == "Corporate Partner"
    assert sale_itens_view_model.fl_receipt_only is True


def test_sale_itens_view_model_to_dict(sale_itens_view_model):
    """Test converting SaleItensViewModel to dictionary"""
    model_dict = sale_itens_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idSaleItem"] == 1
    assert model_dict["description"] == "Sample Item"
    assert model_dict["item"] == "Item Name"
    assert model_dict["itemValue"] == 100.0
    assert model_dict["saleValue"] == 120.0
    assert model_dict["quantity"] == 2
    assert model_dict["corporatePartnershipName"] == "Corporate Partner"
    assert model_dict["flReceiptOnly"] is True


def test_sale_itens_view_model_equality(sale_itens_view_model):
    """Test equality comparison of SaleItensViewModel instances"""
    same_model = SaleItensViewModel(
        idSaleItem=1,
        description="Sample Item",
        item="Item Name",
        itemValue=100.0,
        saleValue=120.0,
        saleValueWithoutCreditValue=110.0,
        quantity=2,
        idMembership=3,
        idMembershipRenewed=4,
        numMembers=5,
        idProduct=6,
        idService=7,
        corporatePartnershipName="Corporate Partner",
        coporatePartnershipId=8,
        membershipStartDate=datetime(2023, 1, 1),
        discount=10.0,
        corporateDiscount=5.0,
        tax=2.0,
        voucher="VOUCHER123",
        accountingCode="ACC123",
        municipalServiceCode="MUN123",
        flReceiptOnly=True,
        idSaleItemMigration="MIG123",
        flSwimming=False,
        flAllowLocker=True,
        idMemberMembership=9,
        valueNextMonth=130.0,
    )

    different_model = SaleItensViewModel(
        idSaleItem=2,
        description="Different Item",
        item="Different Name",
        itemValue=200.0,
        saleValue=220.0,
        quantity=3,
        corporatePartnershipName="Different Partner",
        flReceiptOnly=False,
    )

    assert sale_itens_view_model == same_model
    assert sale_itens_view_model != different_model