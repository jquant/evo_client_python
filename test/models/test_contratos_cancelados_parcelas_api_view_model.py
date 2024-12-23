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

from evo_client.models.contratos_cancelados_parcelas_api_view_model import (
    ContratosCanceladosParcelasApiViewModel,
)
from evo_client.models.receivables_api_sub_types_view_model import (
    ReceivablesApiSubTypesViewModel,
)


@pytest.fixture
def contratos_cancelados_parcelas_api_view_model():
    return ContratosCanceladosParcelasApiViewModel(
        idReceivable=1,
        description="Monthly installment",
        ammount=100.0,
        ammountPaid=50.0,
        currentInstallment=1,
        totalInstallments=12,
        tid="123456789",
        nsu="987654321",
        authorization="auth123",
        canceled=False,
        cancellationDate=None,
        cancellationDescription=None,
        registrationDate=datetime(2023, 1, 1),
        dueDate=datetime(2023, 2, 1),
        receivingDate=datetime(2023, 1, 15),
        paymentType=ReceivablesApiSubTypesViewModel(id=1, name="Credit Card"),
    )


def test_contratos_cancelados_parcelas_api_view_model_creation(
    contratos_cancelados_parcelas_api_view_model,
):
    """Test creating a ContratosCanceladosParcelasApiViewModel instance"""
    assert isinstance(
        contratos_cancelados_parcelas_api_view_model,
        ContratosCanceladosParcelasApiViewModel,
    )
    assert contratos_cancelados_parcelas_api_view_model.id_receivable == 1
    assert (
        contratos_cancelados_parcelas_api_view_model.description
        == "Monthly installment"
    )
    assert contratos_cancelados_parcelas_api_view_model.ammount == 100.0
    assert contratos_cancelados_parcelas_api_view_model.ammount_paid == 50.0
    assert contratos_cancelados_parcelas_api_view_model.current_installment == 1
    assert contratos_cancelados_parcelas_api_view_model.total_installments == 12
    assert contratos_cancelados_parcelas_api_view_model.canceled is False


def test_contratos_cancelados_parcelas_api_view_model_to_dict(
    contratos_cancelados_parcelas_api_view_model,
):
    """Test converting ContratosCanceladosParcelasApiViewModel to dictionary"""
    model_dict = contratos_cancelados_parcelas_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idReceivable"] == 1
    assert model_dict["description"] == "Monthly installment"
    assert model_dict["ammount"] == 100.0
    assert model_dict["ammountPaid"] == 50.0
    assert model_dict["currentInstallment"] == 1
    assert model_dict["totalInstallments"] == 12
    assert model_dict["canceled"] is False


def test_contratos_cancelados_parcelas_api_view_model_equality(
    contratos_cancelados_parcelas_api_view_model,
):
    """Test equality comparison of ContratosCanceladosParcelasApiViewModel instances"""
    same_model = ContratosCanceladosParcelasApiViewModel(
        idReceivable=1,
        description="Monthly installment",
        ammount=100.0,
        ammountPaid=50.0,
        currentInstallment=1,
        totalInstallments=12,
        tid="123456789",
        nsu="987654321",
        authorization="auth123",
        canceled=False,
        cancellationDate=None,
        cancellationDescription=None,
        registrationDate=datetime(2023, 1, 1),
        dueDate=datetime(2023, 2, 1),
        receivingDate=datetime(2023, 1, 15),
        paymentType=ReceivablesApiSubTypesViewModel(id=1, name="Credit Card"),
    )

    different_model = ContratosCanceladosParcelasApiViewModel(
        idReceivable=2,
        description="Different installment",
        ammount=200.0,
        ammountPaid=100.0,
        currentInstallment=2,
        totalInstallments=12,
        canceled=True,
    )

    assert contratos_cancelados_parcelas_api_view_model == same_model
    assert contratos_cancelados_parcelas_api_view_model != different_model
    assert contratos_cancelados_parcelas_api_view_model != 1
