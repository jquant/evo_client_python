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

from evo_client.models.atividade_basico_api_view_model import (
    AtividadeBasicoApiViewModel,
)
from evo_client.models.e_status_atividade import EStatusAtividade


@pytest.fixture
def atividade_basico_api_view_model():
    return AtividadeBasicoApiViewModel(
        idGroupActivity=1,
        idActivitySession=2,
        idConfiguration=3,
        name="Pilates Class",
        date=datetime(2024, 3, 15, 9, 0),
        capacity=25,
        ocupation=20,
        instructor="Jane Doe",
        instructorPhoto="https://example.com/instructor.jpg",
        area="Studio 2",
        status=EStatusAtividade._0,
        selectedSpot="A1",
        exibirParticipantes=True,
        code="PILATES101",
        statusName="Active",
        weekDay=3,
        allowChoosingSpot=True,
        timeTick=32400,
        durationTick=3600,
        startTime="09:00",
        endTime="10:00",
        branchName="Main Branch",
        color="#FF5733",
        description="Intermediate Pilates class",
        imageUrl="https://example.com/pilates.jpg",
        enrollments=[],
        spots=[],
        title="Pilates",
        jsonConfigVagaPersonalizada="{}",
    )


def test_atividade_basico_api_view_model_creation(atividade_basico_api_view_model):
    """Test creating an AtividadeBasicoApiViewModel instance"""
    assert isinstance(atividade_basico_api_view_model, AtividadeBasicoApiViewModel)
    assert atividade_basico_api_view_model.id_group_activity == 1
    assert atividade_basico_api_view_model.id_activity_session == 2
    assert atividade_basico_api_view_model.name == "Pilates Class"
    assert atividade_basico_api_view_model.capacity == 25
    assert atividade_basico_api_view_model.ocupation == 20
    assert atividade_basico_api_view_model.instructor == "Jane Doe"
    assert atividade_basico_api_view_model.status == EStatusAtividade._0


def test_atividade_basico_api_view_model_to_dict(atividade_basico_api_view_model):
    """Test converting AtividadeBasicoApiViewModel to dictionary"""
    model_dict = atividade_basico_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idGroupActivity"] == 1
    assert model_dict["idActivitySession"] == 2
    assert model_dict["name"] == "Pilates Class"
    assert model_dict["capacity"] == 25
    assert model_dict["ocupation"] == 20
    assert model_dict["instructor"] == "Jane Doe"


def test_atividade_basico_api_view_model_equality(atividade_basico_api_view_model):
    """Test equality comparison of AtividadeBasicoApiViewModel instances"""
    same_model = AtividadeBasicoApiViewModel(
        idGroupActivity=1,
        idActivitySession=2,
        idConfiguration=3,
        name="Pilates Class",
        date=datetime(2024, 3, 15, 9, 0),
        capacity=25,
        ocupation=20,
        instructor="Jane Doe",
        instructorPhoto="https://example.com/instructor.jpg",
        area="Studio 2",
        status=EStatusAtividade._0,
        selectedSpot="A1",
        exibirParticipantes=True,
        code="PILATES101",
        statusName="Active",
        weekDay=3,
        allowChoosingSpot=True,
        timeTick=32400,
        durationTick=3600,
        startTime="09:00",
        endTime="10:00",
        branchName="Main Branch",
        color="#FF5733",
        description="Intermediate Pilates class",
        imageUrl="https://example.com/pilates.jpg",
        enrollments=[],
        spots=[],
        title="Pilates",
        jsonConfigVagaPersonalizada="{}",
    )

    different_model = AtividadeBasicoApiViewModel(
        idGroupActivity=2,
        idActivitySession=3,
        name="Different Class",
        capacity=30,
        ocupation=25,
        instructor="John Smith",
        status=EStatusAtividade._1,
    )

    assert atividade_basico_api_view_model == same_model
    assert atividade_basico_api_view_model != different_model
    assert atividade_basico_api_view_model != 1
