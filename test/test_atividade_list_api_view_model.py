# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest

import evo_client
from evo_client.models.atividade_list_api_view_model import (
    AtividadeListApiViewModel,
)  # noqa: E501
from evo_client.rest import ApiException


@pytest.fixture
def atividade_list_api_view_model():
    return AtividadeListApiViewModel()


def test_atividade_list_api_view_model(atividade_list_api_view_model):
    """Test AtividadeListApiViewModel"""
    # FIXME: construct object with mandatory attributes with example values
    # model = evo_client.models.atividade_list_api_view_model.AtividadeListApiViewModel()  # noqa: E501
    pass
