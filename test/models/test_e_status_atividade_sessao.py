# coding: utf-8

"""
EVO API

Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

OpenAPI spec version: v1

Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

from evo_client.models.e_status_atividade_sessao import EStatusAtividadeSessao


def test_e_status_atividade_sessao_creation():
    """Test creating an EStatusAtividadeSessao instance"""
    assert isinstance(EStatusAtividadeSessao._0, EStatusAtividadeSessao)
    assert EStatusAtividadeSessao._0 == EStatusAtividadeSessao(0)
    assert EStatusAtividadeSessao._1 == EStatusAtividadeSessao(1)
    assert EStatusAtividadeSessao._2 == EStatusAtividadeSessao(2)


def test_e_status_atividade_sessao_to_dict():
    """Test converting EStatusAtividadeSessao to dictionary"""
    assert EStatusAtividadeSessao._0.to_dict() == 0
    assert EStatusAtividadeSessao._1.to_dict() == 1


def test_e_status_atividade_sessao_equality():
    """Test equality comparison of EStatusAtividadeSessao instances"""
    assert EStatusAtividadeSessao._0 == EStatusAtividadeSessao(0)
    assert EStatusAtividadeSessao._1 != EStatusAtividadeSessao(0)
    assert EStatusAtividadeSessao._0 != "1"
