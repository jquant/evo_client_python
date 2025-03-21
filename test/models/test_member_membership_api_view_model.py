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

from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)


@pytest.fixture
def member_membership_api_view_model():
    return MemberMembershipApiViewModel(
        idMember=1,
        idMembership=101,
        idMemberMembership=1001,
        startDate=datetime(2023, 1, 1),
        endDate=datetime(2023, 12, 31),
        name="Premium Membership",
        membershipStatus="Active",
        valueNextMonth=99.99,
        idSale=5001,
        saleDate=datetime(2023, 1, 1),
        flRenewed=True,
        flAllowLocker=True,
        flAdditionalMembership=False,
    )


def test_member_membership_api_view_model_creation(member_membership_api_view_model):
    """Test creating a MemberMembershipApiViewModel instance"""
    model = member_membership_api_view_model
    assert isinstance(model, MemberMembershipApiViewModel)
    assert model.id_member == 1
    assert model.id_membership == 101
    assert model.id_member_membership == 1001
    assert model.start_date == datetime(2023, 1, 1)
    assert model.end_date == datetime(2023, 12, 31)
    assert model.name == "Premium Membership"
    assert model.membership_status == "Active"
    assert model.value_next_month == 99.99
    assert model.id_sale == 5001
    assert model.sale_date == datetime(2023, 1, 1)
    assert model.fl_renewed is True
    assert model.fl_allow_locker is True
    assert model.fl_additional_membership is False


def test_member_membership_api_view_model_to_dict(member_membership_api_view_model):
    """Test converting MemberMembershipApiViewModel to dictionary"""
    model_dict = member_membership_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idMember"] == 1
    assert model_dict["idMembership"] == 101
    assert model_dict["idMemberMembership"] == 1001
    assert model_dict["startDate"] == "2023-01-01T00:00:00"
    assert model_dict["endDate"] == "2023-12-31T00:00:00"
    assert model_dict["name"] == "Premium Membership"
    assert model_dict["membershipStatus"] == "Active"
    assert model_dict["valueNextMonth"] == 99.99
    assert model_dict["idSale"] == 5001
    assert model_dict["saleDate"] == "2023-01-01T00:00:00"
    assert model_dict["flRenewed"] is True
    assert model_dict["flAllowLocker"] is True
    assert model_dict["flAdditionalMembership"] is False


def test_member_membership_api_view_model_equality(member_membership_api_view_model):
    """Test equality comparison of MemberMembershipApiViewModel instances"""
    same_model = MemberMembershipApiViewModel(
        idMember=1,
        idMembership=101,
        idMemberMembership=1001,
        startDate=datetime(2023, 1, 1),
        endDate=datetime(2023, 12, 31),
        name="Premium Membership",
        membershipStatus="Active",
        valueNextMonth=99.99,
        idSale=5001,
        saleDate=datetime(2023, 1, 1),
        flRenewed=True,
        flAllowLocker=True,
        flAdditionalMembership=False,
    )

    different_model = MemberMembershipApiViewModel(
        idMember=2,
        idMembership=102,
        idMemberMembership=1002,
        startDate=datetime(2023, 2, 1),
        endDate=datetime(2023, 11, 30),
        name="Basic Membership",
        membershipStatus="Inactive",
        valueNextMonth=49.99,
        idSale=5002,
        saleDate=datetime(2023, 2, 1),
        flRenewed=False,
        flAllowLocker=False,
        flAdditionalMembership=True,
    )

    assert member_membership_api_view_model == same_model
    assert member_membership_api_view_model != different_model
    assert member_membership_api_view_model != 1
