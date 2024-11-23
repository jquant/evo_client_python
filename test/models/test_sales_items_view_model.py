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

from evo_client.models.sales_items_view_model import SalesItemsViewModel
from evo_client.models.sales_item_view_model import SalesItemViewModel


@pytest.fixture
def sales_items_view_model():
    return SalesItemsViewModel(
        nameSalePage="Sale Page 1",
        order=1,
        idEmployeeCommission=2,
        idBranch=3,
        idSaleItem=4,
        checkoutUrl="https://example.com/checkout",
        notInaugurated=True,
        itens=[
            SalesItemViewModel(
                idMembership=5,
                name="Item 1",
                serviceValue=100.0,
            )
        ],
    )


def test_sales_items_view_model_creation(sales_items_view_model):
    """Test creating a SalesItemsViewModel instance"""
    assert isinstance(sales_items_view_model, SalesItemsViewModel)
    assert sales_items_view_model.name_sale_page == "Sale Page 1"
    assert sales_items_view_model.order == 1
    assert sales_items_view_model.id_employee_commission == 2
    assert sales_items_view_model.id_branch == 3
    assert sales_items_view_model.id_sale_item == 4
    assert sales_items_view_model.checkout_url == "https://example.com/checkout"
    assert sales_items_view_model.not_inaugurated is True


def test_sales_items_view_model_to_dict(sales_items_view_model):
    """Test converting SalesItemsViewModel to dictionary"""
    model_dict = sales_items_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["nameSalePage"] == "Sale Page 1"
    assert model_dict["order"] == 1
    assert model_dict["idEmployeeCommission"] == 2
    assert model_dict["idBranch"] == 3
    assert model_dict["idSaleItem"] == 4
    assert model_dict["checkoutUrl"] == "https://example.com/checkout"
    assert model_dict["notInaugurated"] is True


def test_sales_items_view_model_equality(sales_items_view_model):
    """Test equality comparison of SalesItemsViewModel instances"""
    same_model = SalesItemsViewModel(
        nameSalePage="Sale Page 1",
        order=1,
        idEmployeeCommission=2,
        idBranch=3,
        idSaleItem=4,
        checkoutUrl="https://example.com/checkout",
        notInaugurated=True,
    )

    different_model = SalesItemsViewModel(
        nameSalePage="Different Page",
        order=2,
        idEmployeeCommission=3,
        idBranch=4,
        idSaleItem=5,
        checkoutUrl="https://example.com/different",
        notInaugurated=False,
    )

    assert sales_items_view_model == same_model
    assert sales_items_view_model != different_model
