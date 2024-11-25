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

from evo_client.models.business_hours_view_model import BusinessHoursViewModel


@pytest.fixture
def business_hours_view_model():
    return BusinessHoursViewModel(
        idHour=1,
        idBranch=2,
        weekDay="Monday",
        hoursFrom=datetime(2023, 1, 1, 9, 0),
        hoursTo=datetime(2023, 1, 1, 17, 0),
        flDeleted=False,
        idTmp=3,
        creationDate=datetime(2023, 1, 1),
        idEmployeeCreation=4,
    )


def test_business_hours_view_model_creation(business_hours_view_model):
    """Test creating a BusinessHoursViewModel instance"""
    assert isinstance(business_hours_view_model, BusinessHoursViewModel)
    assert business_hours_view_model.id_hour == 1
    assert business_hours_view_model.id_branch == 2
    assert business_hours_view_model.week_day == "Monday"
    assert business_hours_view_model.hours_from == datetime(2023, 1, 1, 9, 0)
    assert business_hours_view_model.hours_to == datetime(2023, 1, 1, 17, 0)
    assert business_hours_view_model.fl_deleted is False
    assert business_hours_view_model.id_tmp == 3
    assert business_hours_view_model.creation_date == datetime(2023, 1, 1)
    assert business_hours_view_model.id_employee_creation == 4


def test_business_hours_view_model_to_dict(business_hours_view_model):
    """Test converting BusinessHoursViewModel to dictionary"""
    model_dict = business_hours_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idHour"] == 1
    assert model_dict["idBranch"] == 2
    assert model_dict["weekDay"] == "Monday"
    assert model_dict["hoursFrom"] == datetime(2023, 1, 1, 9, 0)
    assert model_dict["hoursTo"] == datetime(2023, 1, 1, 17, 0)
    assert model_dict["flDeleted"] is False
    assert model_dict["idTmp"] == 3
    assert model_dict["creationDate"] == datetime(2023, 1, 1)
    assert model_dict["idEmployeeCreation"] == 4


def test_business_hours_view_model_equality(business_hours_view_model):
    """Test equality comparison of BusinessHoursViewModel instances"""
    same_model = BusinessHoursViewModel(
        idHour=1,
        idBranch=2,
        weekDay="Monday",
        hoursFrom=datetime(2023, 1, 1, 9, 0),
        hoursTo=datetime(2023, 1, 1, 17, 0),
        flDeleted=False,
        idTmp=3,
        creationDate=datetime(2023, 1, 1),
        idEmployeeCreation=4,
    )

    different_model = BusinessHoursViewModel(
        idHour=2,
        idBranch=3,
        weekDay="Tuesday",
        hoursFrom=datetime(2023, 1, 1, 10, 0),
        hoursTo=datetime(2023, 1, 1, 18, 0),
        flDeleted=True,
        idTmp=4,
        creationDate=datetime(2023, 1, 2),
        idEmployeeCreation=5,
    )

    assert business_hours_view_model == same_model
    assert business_hours_view_model != different_model
    assert business_hours_view_model != 1
