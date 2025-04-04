# coding: utf-8

"""
EVO API

Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

OpenAPI spec version: v1

Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

from evo_client.models.e_tipo_gateway import ETipoGateway


def test_e_tipo_gateway_creation():
    """Test creating an ETipoGateway instance"""
    assert isinstance(ETipoGateway._0, ETipoGateway)
    assert ETipoGateway._0 == ETipoGateway(0)
    assert ETipoGateway._1 == ETipoGateway(1)
    assert ETipoGateway._2 == ETipoGateway(2)


def test_e_tipo_gateway_to_dict():
    """Test converting ETipoGateway to dictionary"""
    assert ETipoGateway._0.to_dict() == 0
    assert ETipoGateway._1.to_dict() == 1


def test_e_tipo_gateway_equality():
    """Test equality comparison of ETipoGateway instances"""
    assert ETipoGateway._0 == ETipoGateway(0)
    assert ETipoGateway._1 != ETipoGateway(0)
    assert ETipoGateway._0 != "1"
