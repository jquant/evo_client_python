# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import pytest
from evo_client.models.contratos_resumo_pagina_venda_view_model import (
    ContratosResumoPaginaVendaViewModel,
)


@pytest.fixture
def contratos_resumo_pagina_venda_view_model():
    return ContratosResumoPaginaVendaViewModel(
        idSalesPage=1, order=2, salesPageDescription="Sample Description"
    )


def test_contratos_resumo_pagina_venda_view_model_creation(
    contratos_resumo_pagina_venda_view_model,
):
    """Test creating a ContratosResumoPaginaVendaViewModel instance"""
    assert isinstance(
        contratos_resumo_pagina_venda_view_model, ContratosResumoPaginaVendaViewModel
    )
    assert contratos_resumo_pagina_venda_view_model.id_sales_page == 1
    assert contratos_resumo_pagina_venda_view_model.order == 2
    assert (
        contratos_resumo_pagina_venda_view_model.sales_page_description
        == "Sample Description"
    )


def test_contratos_resumo_pagina_venda_view_model_to_dict(
    contratos_resumo_pagina_venda_view_model,
):
    """Test converting ContratosResumoPaginaVendaViewModel to dictionary"""
    model_dict = contratos_resumo_pagina_venda_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idSalesPage"] == 1
    assert model_dict["order"] == 2
    assert model_dict["salesPageDescription"] == "Sample Description"


def test_contratos_resumo_pagina_venda_view_model_equality(
    contratos_resumo_pagina_venda_view_model,
):
    """Test equality comparison of ContratosResumoPaginaVendaViewModel instances"""
    same_model = ContratosResumoPaginaVendaViewModel(
        idSalesPage=1, order=2, salesPageDescription="Sample Description"
    )

    different_model = ContratosResumoPaginaVendaViewModel(
        idSalesPage=2, order=3, salesPageDescription="Different Description"
    )

    assert contratos_resumo_pagina_venda_view_model == same_model
    assert contratos_resumo_pagina_venda_view_model != different_model
    assert contratos_resumo_pagina_venda_view_model != 1
