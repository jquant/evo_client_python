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

from evo_client.models.sales_view_model import SalesViewModel
from evo_client.models.sales_items_view_model import SalesItemsViewModel
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel
from evo_client.models.sales_item_view_model import SalesItemViewModel


@pytest.fixture
def sales_view_model():
    return SalesViewModel(
        idSale=1,
        idMember=2,
        idEmployee=3,
        idProspect=4,
        idEmployeeSale=5,
        saleDate=datetime(2023, 10, 1, 10, 0),
        saleDateServer=datetime(2023, 10, 1, 10, 5),
        idPersonal=6,
        corporatePartnershipName="Corporate Partner",
        coporatePartnershipId=7,
        removed=False,
        idEmployeeRemoval=8,
        removalDate=None,
        idBranch=9,
        observations="Test sale",
        idSaleRecurrency=10,
        saleSource=11,
        idSaleMigration="12",
        saleItens=[
            SalesItemsViewModel(
                idSaleItem=1,
                nameSalePage="Item 1",
                order=2,
                idEmployeeCommission=3,
                itens=[
                    SalesItemViewModel(
                        idMembership=4,
                        name="Item 1",
                        serviceValue=100.0,
                    )
                ],
            )
        ],
        receivables=[
            ReceivablesApiViewModel(
                idReceivable=1, ammount=200.0, dueDate=datetime(2023, 11, 1)
            )
        ],
    )


def test_sales_view_model_creation(sales_view_model):
    """Test creating a SalesViewModel instance"""
    assert isinstance(sales_view_model, SalesViewModel)
    assert sales_view_model.id_sale == 1
    assert sales_view_model.id_member == 2
    assert sales_view_model.id_employee == 3
    assert sales_view_model.corporate_partnership_name == "Corporate Partner"
    assert sales_view_model.removed is False
    assert sales_view_model.observations == "Test sale"


def test_sales_view_model_to_dict(sales_view_model):
    """Test converting SalesViewModel to dictionary"""
    model_dict = sales_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idSale"] == 1
    assert model_dict["idMember"] == 2
    assert model_dict["corporatePartnershipName"] == "Corporate Partner"
    assert model_dict["removed"] is False


def test_sales_view_model_equality(sales_view_model):
    """Test equality comparison of SalesViewModel instances"""
    same_model = SalesViewModel(
        idSale=1,
        idMember=2,
        idEmployee=3,
        idProspect=4,
        idEmployeeSale=5,
        saleDate=datetime(2023, 10, 1, 10, 0),
        saleDateServer=datetime(2023, 10, 1, 10, 5),
        idPersonal=6,
        corporatePartnershipName="Corporate Partner",
        coporatePartnershipId=7,
        removed=False,
        idEmployeeRemoval=8,
        removalDate=None,
        idBranch=9,
        observations="Test sale",
        idSaleRecurrency=10,
        saleSource=11,
        idSaleMigration="12",
        saleItens=[
            SalesItemsViewModel(
                idSaleItem=1,
                nameSalePage="Item 1",
                order=2,
                idEmployeeCommission=3,
                itens=[
                    SalesItemViewModel(
                        idMembership=4,
                        name="Item 1",
                        serviceValue=100.0,
                    )
                ],
            )
        ],
        receivables=[
            ReceivablesApiViewModel(
                idReceivable=1, ammount=200.0, dueDate=datetime(2023, 11, 1)
            )
        ],
    )
    different_model = SalesViewModel(
        idSale=2,
        idMember=3,
        idEmployee=4,
        corporatePartnershipName="Different Partner",
        removed=True,
        observations="Different sale",
    )

    assert sales_view_model == same_model
    assert sales_view_model != different_model