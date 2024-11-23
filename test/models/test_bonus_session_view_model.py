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

from evo_client.models.bonus_session_view_model import BonusSessionViewModel


@pytest.fixture
def bonus_session_view_model():
    return BonusSessionViewModel(
        idSession=1,
        expirationDate=datetime(2024, 3, 15, 9, 0),
        flBonusSession=True,
    )


def test_bonus_session_view_model_creation(bonus_session_view_model):
    """Test creating a BonusSessionViewModel instance"""
    assert isinstance(bonus_session_view_model, BonusSessionViewModel)
    assert bonus_session_view_model.id_session == 1
    assert bonus_session_view_model.expiration_date == datetime(2024, 3, 15, 9, 0)
    assert bonus_session_view_model.fl_bonus_session is True


def test_bonus_session_view_model_to_dict(bonus_session_view_model):
    """Test converting BonusSessionViewModel to dictionary"""
    model_dict = bonus_session_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idSession"] == 1
    assert model_dict["expirationDate"] == "2024-03-15T09:00:00"
    assert model_dict["flBonusSession"] is True


def test_bonus_session_view_model_equality(bonus_session_view_model):
    """Test equality comparison of BonusSessionViewModel instances"""
    same_model = BonusSessionViewModel(
        idSession=1,
        expirationDate=datetime(2024, 3, 15, 9, 0),
        flBonusSession=True,
    )

    different_model = BonusSessionViewModel(
        idSession=2,
        expirationDate=datetime(2025, 4, 20, 10, 0),
        flBonusSession=False,
    )

    assert bonus_session_view_model == same_model
    assert bonus_session_view_model != different_model
