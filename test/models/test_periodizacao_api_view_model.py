# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest
from evo_client.models.periodizacao_api_view_model import PeriodizacaoApiViewModel


@pytest.fixture
def periodizacao_api_view_model():
    return PeriodizacaoApiViewModel(
        name="Strength Training",
        characteristics="High intensity, muscle building",
        color="#FF5733",
        intensityNumber=5,
        type="Strength",
    )


def test_periodizacao_api_view_model_creation(periodizacao_api_view_model):
    """Test creating a PeriodizacaoApiViewModel instance"""
    model = periodizacao_api_view_model
    assert isinstance(model, PeriodizacaoApiViewModel)
    assert model.name == "Strength Training"
    assert model.characteristics == "High intensity, muscle building"
    assert model.color == "#FF5733"
    assert model.intensity_number == 5
    assert model.type == "Strength"


def test_periodizacao_api_view_model_to_dict(periodizacao_api_view_model):
    """Test converting PeriodizacaoApiViewModel to dictionary"""
    model_dict = periodizacao_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["name"] == "Strength Training"
    assert model_dict["characteristics"] == "High intensity, muscle building"
    assert model_dict["color"] == "#FF5733"
    assert model_dict["intensityNumber"] == 5
    assert model_dict["type"] == "Strength"


def test_periodizacao_api_view_model_equality(periodizacao_api_view_model):
    """Test equality comparison of PeriodizacaoApiViewModel instances"""
    same_model = PeriodizacaoApiViewModel(
        name="Strength Training",
        characteristics="High intensity, muscle building",
        color="#FF5733",
        intensityNumber=5,
        type="Strength",
    )

    different_model = PeriodizacaoApiViewModel(
        name="Cardio",
        characteristics="Endurance, heart health",
        color="#33FF57",
        intensityNumber=3,
        type="Cardio",
    )

    assert periodizacao_api_view_model == same_model
    assert periodizacao_api_view_model != different_model
    assert periodizacao_api_view_model != 1
