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

from evo_client.models.receivables_invoice_api_view_model import (
    ReceivablesInvoiceApiViewModel,
)


@pytest.fixture
def receivables_invoice_api_view_model():
    return ReceivablesInvoiceApiViewModel(
        invoiceNumber="INV123",
        issuedAmount=150.0,
        status="Issued",
        sendDate=datetime(2023, 1, 1),
        canceledDate=None,
        urlPdf="https://example.com/invoice.pdf",
        idInvoiceType=1,
        invoiceType="Standard",
    )


def test_receivables_invoice_api_view_model_creation(
    receivables_invoice_api_view_model,
):
    """Test creating a ReceivablesInvoiceApiViewModel instance"""
    assert isinstance(
        receivables_invoice_api_view_model, ReceivablesInvoiceApiViewModel
    )
    assert receivables_invoice_api_view_model.invoice_number == "INV123"
    assert receivables_invoice_api_view_model.issued_amount == 150.0
    assert receivables_invoice_api_view_model.status == "Issued"
    assert (
        receivables_invoice_api_view_model.url_pdf == "https://example.com/invoice.pdf"
    )
    assert receivables_invoice_api_view_model.id_invoice_type == 1


def test_receivables_invoice_api_view_model_to_dict(receivables_invoice_api_view_model):
    """Test converting ReceivablesInvoiceApiViewModel to dictionary"""
    model_dict = receivables_invoice_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["invoiceNumber"] == "INV123"
    assert model_dict["issuedAmount"] == 150.0
    assert model_dict["status"] == "Issued"
    assert model_dict["urlPdf"] == "https://example.com/invoice.pdf"
    assert model_dict["idInvoiceType"] == 1


def test_receivables_invoice_api_view_model_equality(
    receivables_invoice_api_view_model,
):
    """Test equality comparison of ReceivablesInvoiceApiViewModel instances"""
    same_model = ReceivablesInvoiceApiViewModel(
        invoiceNumber="INV123",
        issuedAmount=150.0,
        status="Issued",
        sendDate=datetime(2023, 1, 1),
        canceledDate=None,
        urlPdf="https://example.com/invoice.pdf",
        idInvoiceType=1,
        invoiceType="Standard",
    )

    different_model = ReceivablesInvoiceApiViewModel(
        invoiceNumber="INV124",
        issuedAmount=200.0,
        status="Paid",
        urlPdf="https://example.com/different_invoice.pdf",
        idInvoiceType=2,
    )

    assert receivables_invoice_api_view_model == same_model
    assert receivables_invoice_api_view_model != different_model
    assert receivables_invoice_api_view_model != 1
