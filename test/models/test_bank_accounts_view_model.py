# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
from typing import Optional

import pytest
from evo_client.models.bank_accounts_view_model import BankAccountsViewModel


@pytest.fixture
def bank_accounts_view_model():
    return BankAccountsViewModel(
        idBankAccount=1,
        description="Main Bank Account",
        accountType=True,
        bankCode=123,
        agency="001",
        account="123456-7",
        observations="Primary account for transactions",
        inactive=False,
        bankIntegration=True,
    )


def test_bank_accounts_view_model_creation(bank_accounts_view_model):
    """Test creating a BankAccountsViewModel instance"""
    assert isinstance(bank_accounts_view_model, BankAccountsViewModel)
    assert bank_accounts_view_model.id_bank_account == 1
    assert bank_accounts_view_model.description == "Main Bank Account"
    assert bank_accounts_view_model.account_type is True
    assert bank_accounts_view_model.bank_code == 123
    assert bank_accounts_view_model.agency == "001"
    assert bank_accounts_view_model.account == "123456-7"
    assert bank_accounts_view_model.observations == "Primary account for transactions"
    assert bank_accounts_view_model.inactive is False
    assert bank_accounts_view_model.bank_integration is True


def test_bank_accounts_view_model_to_dict(bank_accounts_view_model):
    """Test converting BankAccountsViewModel to dictionary"""
    model_dict = bank_accounts_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idBankAccount"] == 1
    assert model_dict["description"] == "Main Bank Account"
    assert model_dict["accountType"] is True
    assert model_dict["bankCode"] == 123
    assert model_dict["agency"] == "001"
    assert model_dict["account"] == "123456-7"
    assert model_dict["observations"] == "Primary account for transactions"
    assert model_dict["inactive"] is False
    assert model_dict["bankIntegration"] is True


def test_bank_accounts_view_model_equality(bank_accounts_view_model):
    """Test equality comparison of BankAccountsViewModel instances"""
    same_model = BankAccountsViewModel(
        idBankAccount=1,
        description="Main Bank Account",
        accountType=True,
        bankCode=123,
        agency="001",
        account="123456-7",
        observations="Primary account for transactions",
        inactive=False,
        bankIntegration=True,
    )

    different_model = BankAccountsViewModel(
        idBankAccount=2,
        description="Secondary Bank Account",
        accountType=False,
        bankCode=456,
        agency="002",
        account="765432-1",
        observations="Secondary account for backup",
        inactive=True,
        bankIntegration=False,
    )

    assert bank_accounts_view_model == same_model
    assert bank_accounts_view_model != different_model