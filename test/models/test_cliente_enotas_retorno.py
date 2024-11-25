# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest
from evo_client.models.cliente_enotas_retorno import ClienteEnotasRetorno
from evo_client.models.endereco_enotas_retorno import EnderecoEnotasRetorno


@pytest.fixture
def cliente_enotas_retorno():
    return ClienteEnotasRetorno(
        idCliente=123,
        tipoPessoa="Física",
        nome="John Doe",
        email="john.doe@example.com",
        cpfCnpj="12345678901",
        inscricaoMunicipal="123456",
        telefone="1234567890",
        endereco=EnderecoEnotasRetorno(
            logradouro="Rua Exemplo",
            numero="123",
            complemento="Apto 101",
            bairro="Centro",
            cidade="Cidade Exemplo",
            uf="EX",
            cep="12345-678",
        ),
    )


def test_cliente_enotas_retorno_creation(cliente_enotas_retorno):
    """Test creating a ClienteEnotasRetorno instance"""
    assert isinstance(cliente_enotas_retorno, ClienteEnotasRetorno)
    assert cliente_enotas_retorno.id_cliente == 123
    assert cliente_enotas_retorno.tipo_pessoa == "Física"
    assert cliente_enotas_retorno.nome == "John Doe"
    assert cliente_enotas_retorno.email == "john.doe@example.com"
    assert cliente_enotas_retorno.cpf_cnpj == "12345678901"
    assert cliente_enotas_retorno.inscricao_municipal == "123456"
    assert cliente_enotas_retorno.telefone == "1234567890"
    assert cliente_enotas_retorno.endereco is not None
    assert cliente_enotas_retorno.endereco.logradouro == "Rua Exemplo"


def test_cliente_enotas_retorno_to_dict(cliente_enotas_retorno):
    """Test converting ClienteEnotasRetorno to dictionary"""
    model_dict = cliente_enotas_retorno.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idCliente"] == 123
    assert model_dict["tipoPessoa"] == "Física"
    assert model_dict["nome"] == "John Doe"
    assert model_dict["email"] == "john.doe@example.com"
    assert model_dict["cpfCnpj"] == "12345678901"
    assert model_dict["inscricaoMunicipal"] == "123456"
    assert model_dict["telefone"] == "1234567890"
    assert model_dict["endereco"]["logradouro"] == "Rua Exemplo"


def test_cliente_enotas_retorno_equality(cliente_enotas_retorno):
    """Test equality comparison of ClienteEnotasRetorno instances"""
    same_model = ClienteEnotasRetorno(
        idCliente=123,
        tipoPessoa="Física",
        nome="John Doe",
        email="john.doe@example.com",
        cpfCnpj="12345678901",
        inscricaoMunicipal="123456",
        telefone="1234567890",
        endereco=EnderecoEnotasRetorno(
            logradouro="Rua Exemplo",
            numero="123",
            complemento="Apto 101",
            bairro="Centro",
            cidade="Cidade Exemplo",
            uf="EX",
            cep="12345-678",
        ),
    )

    different_model = ClienteEnotasRetorno(
        idCliente=124,
        tipoPessoa="Jurídica",
        nome="Jane Smith",
        email="jane.smith@example.com",
        cpfCnpj="98765432100",
        inscricaoMunicipal="654321",
        telefone="0987654321",
        endereco=EnderecoEnotasRetorno(
            logradouro="Avenida Exemplo",
            numero="456",
            complemento="Sala 202",
            bairro="Bairro Exemplo",
            cidade="Outra Cidade",
            uf="OX",
            cep="87654-321",
        ),
    )

    assert cliente_enotas_retorno == same_model
    assert cliente_enotas_retorno != different_model
    assert cliente_enotas_retorno != 1
