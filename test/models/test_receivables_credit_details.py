# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

from evo_client.models.receivables_credit_details import ReceivablesCreditDetails


@pytest.fixture
def receivables_credit_details():
    return ReceivablesCreditDetails(
        idCredit=1,
        idCancelationCredit=None,
        idBranchOrigin=10,
        ammount=100.0,
        branchDocument="DOC123",
        idSaleOrigin=5,
        idReceivableOrigin=3,
    )


def test_receivables_credit_details_creation(receivables_credit_details):
    """Test creating a ReceivablesCreditDetails instance"""
    assert isinstance(receivables_credit_details, ReceivablesCreditDetails)
    assert receivables_credit_details.id_credit == 1
    assert receivables_credit_details.id_branch_origin == 10
    assert receivables_credit_details.ammount == 100.0
    assert receivables_credit_details.branch_document == "DOC123"
    assert receivables_credit_details.id_sale_origin == 5


def test_receivables_credit_details_to_dict(receivables_credit_details):
    """Test converting ReceivablesCreditDetails to dictionary"""
    model_dict = receivables_credit_details.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idCredit"] == 1
    assert model_dict["idBranchOrigin"] == 10
    assert model_dict["ammount"] == 100.0
    assert model_dict["branchDocument"] == "DOC123"
    assert model_dict["idSaleOrigin"] == 5


def test_receivables_credit_details_equality(receivables_credit_details):
    """Test equality comparison of ReceivablesCreditDetails instances"""
    same_model = ReceivablesCreditDetails(
        idCredit=1,
        idCancelationCredit=None,
        idBranchOrigin=10,
        ammount=100.0,
        branchDocument="DOC123",
        idSaleOrigin=5,
        idReceivableOrigin=3,
    )

    different_model = ReceivablesCreditDetails(
        idCredit=2,
        idCancelationCredit=1,
        idBranchOrigin=20,
        ammount=200.0,
        branchDocument="DOC124",
        idSaleOrigin=6,
        idReceivableOrigin=4,
    )

    assert receivables_credit_details == same_model
    assert receivables_credit_details != different_model
    assert receivables_credit_details != 1
