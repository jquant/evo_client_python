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

from evo_client.models.cliente_enotas_retorno import ClienteEnotasRetorno
from evo_client.models.enotas_retorno import EnotasRetorno
from evo_client.models.metadados_enotas_retorno import MetadadosEnotasRetorno
from evo_client.models.servico_enotas_retorno import ServicoEnotasRetorno


@pytest.fixture
def enotas_retorno():
    return EnotasRetorno(
        id="123",
        tipo="NFSE",
        idExterno="ext-456",
        status="ISSUED",
        motivoStatus="None",
        ambienteEmissao="Production",
        enviadaPorEmail=True,
        dataCriacao=datetime(2023, 11, 1),
        dataUltimaAlteracao=datetime(2023, 11, 2),
        cliente=ClienteEnotasRetorno(nome="John Doe"),
        numero="789",
        codigoVerificacao="abc123",
        chaveAcesso="key-456",
        dataAutorizacao=datetime(2023, 11, 3),
        linkDownloadPDF="https://example.com/invoice.pdf",
        linkDownloadXML="https://example.com/invoice.xml",
        numeroRps=101,
        serieRps="A1",
        dataCompetenciaRps=datetime(2023, 11, 1),
        servico=ServicoEnotasRetorno(descricao="Service Description"),
        naturezaOperacao="Operation Nature",
        valorCofins=10.0,
        valorCsll=5.0,
        valorInss=3.0,
        valorIr=2.0,
        valorPis=1.0,
        deducoes=0.0,
        descontos=0.0,
        outrasRetencoes=0.0,
        valorTotal=100.0,
        valorIss=8.0,
        observacoes="No observations",
        metadados=MetadadosEnotasRetorno(),
        tipoNf="NFSE",
        idFilial=1,
    )


def test_enotas_retorno_creation(enotas_retorno):
    """Test creating an EnotasRetorno instance"""
    assert isinstance(enotas_retorno, EnotasRetorno)
    assert enotas_retorno.id == "123"
    assert enotas_retorno.tipo == "NFSE"
    assert enotas_retorno.status == "ISSUED"
    assert enotas_retorno.enviada_por_email is True
    assert enotas_retorno.valor_total == 100.0


def test_enotas_retorno_to_dict(enotas_retorno):
    """Test converting EnotasRetorno to dictionary"""
    model_dict = enotas_retorno.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["id"] == "123"
    assert model_dict["tipo"] == "NFSE"
    assert model_dict["status"] == "ISSUED"
    assert model_dict["enviadaPorEmail"] is True
    assert model_dict["valorTotal"] == 100.0


def test_enotas_retorno_equality(enotas_retorno):
    """Test equality comparison of EnotasRetorno instances"""
    same_model = EnotasRetorno(
        id="123",
        tipo="NFSE",
        idExterno="ext-456",
        status="ISSUED",
        motivoStatus="None",
        ambienteEmissao="Production",
        enviadaPorEmail=True,
        dataCriacao=datetime(2023, 11, 1),
        dataUltimaAlteracao=datetime(2023, 11, 2),
        cliente=ClienteEnotasRetorno(nome="John Doe"),
        numero="789",
        codigoVerificacao="abc123",
        chaveAcesso="key-456",
        dataAutorizacao=datetime(2023, 11, 3),
        linkDownloadPDF="https://example.com/invoice.pdf",
        linkDownloadXML="https://example.com/invoice.xml",
        numeroRps=101,
        serieRps="A1",
        dataCompetenciaRps=datetime(2023, 11, 1),
        servico=ServicoEnotasRetorno(descricao="Service Description"),
        naturezaOperacao="Operation Nature",
        valorCofins=10.0,
        valorCsll=5.0,
        valorInss=3.0,
        valorIr=2.0,
        valorPis=1.0,
        deducoes=0.0,
        descontos=0.0,
        outrasRetencoes=0.0,
        valorTotal=100.0,
        valorIss=8.0,
        observacoes="No observations",
        metadados=MetadadosEnotasRetorno(),
        tipoNf="NFSE",
        idFilial=1,
    )

    different_model = EnotasRetorno(
        id="456",
        tipo="NFE",
        status="CANCELED",
        enviadaPorEmail=False,
        valorTotal=200.0,
    )

    assert enotas_retorno == same_model
    assert enotas_retorno != different_model
    assert enotas_retorno != 1
