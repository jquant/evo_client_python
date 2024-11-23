# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest
from evo_client.models.metadados_enotas_retorno import MetadadosEnotasRetorno


@pytest.fixture
def metadados_enotas_retorno():
    return MetadadosEnotasRetorno()


def test_metadados_enotas_retorno_creation(metadados_enotas_retorno):
    """Test creating a MetadadosEnotasRetorno instance"""
    assert isinstance(metadados_enotas_retorno, MetadadosEnotasRetorno)


def test_metadados_enotas_retorno_to_dict(metadados_enotas_retorno):
    """Test converting MetadadosEnotasRetorno to dictionary"""
    model_dict = metadados_enotas_retorno.to_dict()

    assert isinstance(model_dict, dict)


def test_metadados_enotas_retorno_equality(metadados_enotas_retorno):
    """Test equality comparison of MetadadosEnotasRetorno instances"""
    same_model = MetadadosEnotasRetorno()

    assert metadados_enotas_retorno == same_model
    assert metadados_enotas_retorno != MetadadosEnotasRetorno()
