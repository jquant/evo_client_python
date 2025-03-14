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

from evo_client.models.freeze_view_model import FreezeViewModel


@pytest.fixture
def freeze_view_model():
    return FreezeViewModel(
        startSuspend=datetime(2023, 11, 1),
        endSuspend=datetime(2023, 12, 1),
        unlockDate=datetime(2023, 12, 2),
        idEmployee=123,
        reason="Vacation",
        flUseMembershipFreezeDays=True,
        daysFreeze=30,
        idFreeze=456,
    )


def test_freeze_view_model_creation(freeze_view_model):
    """Test creating a FreezeViewModel instance"""
    model = freeze_view_model
    assert isinstance(model, FreezeViewModel)
    assert model.start_suspend == datetime(2023, 11, 1)
    assert model.end_suspend == datetime(2023, 12, 1)
    assert model.unlock_date == datetime(2023, 12, 2)
    assert model.id_employee == 123
    assert model.reason == "Vacation"
    assert model.fl_use_membership_freeze_days is True
    assert model.days_freeze == 30
    assert model.id_freeze == 456


def test_freeze_view_model_to_dict(freeze_view_model):
    """Test converting FreezeViewModel to dictionary"""
    model_dict = freeze_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["startSuspend"] == "2023-11-01T00:00:00"
    assert model_dict["endSuspend"] == "2023-12-01T00:00:00"
    assert model_dict["unlockDate"] == "2023-12-02T00:00:00"
    assert model_dict["idEmployee"] == 123
    assert model_dict["reason"] == "Vacation"
    assert model_dict["flUseMembershipFreezeDays"] is True
    assert model_dict["daysFreeze"] == 30
    assert model_dict["idFreeze"] == 456


def test_freeze_view_model_equality(freeze_view_model):
    """Test equality comparison of FreezeViewModel instances"""
    same_model = FreezeViewModel(
        startSuspend=datetime(2023, 11, 1),
        endSuspend=datetime(2023, 12, 1),
        unlockDate=datetime(2023, 12, 2),
        idEmployee=123,
        reason="Vacation",
        flUseMembershipFreezeDays=True,
        daysFreeze=30,
        idFreeze=456,
    )

    different_model = FreezeViewModel(
        startSuspend=datetime(2023, 10, 1),
        endSuspend=datetime(2023, 11, 1),
        unlockDate=datetime(2023, 11, 2),
        idEmployee=789,
        reason="Medical",
        flUseMembershipFreezeDays=False,
        daysFreeze=15,
        idFreeze=789,
    )

    assert freeze_view_model == same_model
    assert freeze_view_model != different_model
    assert freeze_view_model != 1
