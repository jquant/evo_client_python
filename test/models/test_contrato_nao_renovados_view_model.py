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

from evo_client.models.contrato_nao_renovados_view_model import (
    ContratoNaoRenovadosViewModel,
)


@pytest.fixture
def contrato_nao_renovados_view_model():
    return ContratoNaoRenovadosViewModel(
        idFilial=1,
        nomeFilial="Main Branch",
        idCliente=123,
        status="Active",
        contratoAtivo="Yes",
        nome="John",
        sobrenome="Doe",
        contratoVencido="No",
        dataInicio=datetime(2023, 1, 1),
        dataFim=datetime(2023, 12, 31),
        mesesPermanencia=12,
        valor=999.99,
        flCancelado=False,
        dtCancelamento=None,
        contratoCancelado="No",
        motivoCancelamento=None,
        nomeConsultor="Jane Smith",
        celular="1234567890",
        email="john.doe@example.com",
    )


def test_contrato_nao_renovados_view_model_creation(contrato_nao_renovados_view_model):
    """Test creating a ContratoNaoRenovadosViewModel instance"""
    assert isinstance(contrato_nao_renovados_view_model, ContratoNaoRenovadosViewModel)
    assert contrato_nao_renovados_view_model.id_filial == 1
    assert contrato_nao_renovados_view_model.nome_filial == "Main Branch"
    assert contrato_nao_renovados_view_model.id_cliente == 123
    assert contrato_nao_renovados_view_model.status == "Active"
    assert contrato_nao_renovados_view_model.contrato_ativo == "Yes"
    assert contrato_nao_renovados_view_model.nome == "John"
    assert contrato_nao_renovados_view_model.sobrenome == "Doe"
    assert contrato_nao_renovados_view_model.valor == 999.99
    assert contrato_nao_renovados_view_model.fl_cancelado is False


def test_contrato_nao_renovados_view_model_to_dict(contrato_nao_renovados_view_model):
    """Test converting ContratoNaoRenovadosViewModel to dictionary"""
    model_dict = contrato_nao_renovados_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idFilial"] == 1
    assert model_dict["nomeFilial"] == "Main Branch"
    assert model_dict["idCliente"] == 123
    assert model_dict["status"] == "Active"
    assert model_dict["contratoAtivo"] == "Yes"
    assert model_dict["nome"] == "John"
    assert model_dict["sobrenome"] == "Doe"
    assert model_dict["valor"] == 999.99
    assert model_dict["flCancelado"] is False


def test_contrato_nao_renovados_view_model_equality(contrato_nao_renovados_view_model):
    """Test equality comparison of ContratoNaoRenovadosViewModel instances"""
    same_model = ContratoNaoRenovadosViewModel(
        idFilial=1,
        nomeFilial="Main Branch",
        idCliente=123,
        status="Active",
        contratoAtivo="Yes",
        nome="John",
        sobrenome="Doe",
        contratoVencido="No",
        dataInicio=datetime(2023, 1, 1),
        dataFim=datetime(2023, 12, 31),
        mesesPermanencia=12,
        valor=999.99,
        flCancelado=False,
        dtCancelamento=None,
        contratoCancelado="No",
        motivoCancelamento=None,
        nomeConsultor="Jane Smith",
        celular="1234567890",
        email="john.doe@example.com",
    )

    different_model = ContratoNaoRenovadosViewModel(
        idFilial=2,
        nomeFilial="Secondary Branch",
        idCliente=456,
        status="Inactive",
        contratoAtivo="No",
        nome="Jane",
        sobrenome="Smith",
        valor=499.99,
        flCancelado=True,
    )

    assert contrato_nao_renovados_view_model == same_model
    assert contrato_nao_renovados_view_model != different_model
    assert contrato_nao_renovados_view_model != 1
