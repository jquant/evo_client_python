"""Tests for the ConfigurationApi class."""

from typing import List
from unittest.mock import Mock, patch

import pytest



from evo_client.api.configuration_api import ConfigurationApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.bandeiras_basico_view_model import BandeirasBasicoViewModel
from evo_client.models.configuracao_api_view_model import ConfiguracaoApiViewModel
from evo_client.models.empresas_filiais_gateway_view_model import (
    EmpresasFiliaisGatewayViewModel,
)
from evo_client.models.empresas_filiais_ocupacao_view_model import (
    EmpresasFiliaisOcupacaoViewModel,
)


@pytest.fixture
def configuration_api():
    """Create a ConfigurationApi instance for testing."""
    return ConfigurationApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.configuration_api.ApiClient.call_api") as mock:
        yield mock


def test_get_gateway_config(configuration_api: ConfigurationApi, mock_api_client: Mock):
    """Test getting gateway configurations."""
    expected = EmpresasFiliaisGatewayViewModel()
    mock_api_client.return_value = expected

    await result = await configuration_api.get_gateway_config(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/gateway"
    assert args["response_type"] == EmpresasFiliaisGatewayViewModel


def test_get_branch_config(configuration_api: ConfigurationApi, mock_api_client: Mock):
    """Test getting branch configurations."""
    expected = [ConfiguracaoApiViewModel()]
    mock_api_client.return_value = expected

    await result = await configuration_api.get_branch_config(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration"
    assert args["response_type"] == List[ConfiguracaoApiViewModel]


def test_get_occupations(configuration_api: ConfigurationApi, mock_api_client: Mock):
    """Test getting occupation configurations."""
    expected = [EmpresasFiliaisOcupacaoViewModel()]
    mock_api_client.return_value = expected

    await result = await configuration_api.get_occupations(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/occupation"
    assert args["response_type"] == List[EmpresasFiliaisOcupacaoViewModel]


def test_get_card_flags(configuration_api: ConfigurationApi, mock_api_client: Mock):
    """Test getting card flags."""
    expected = [BandeirasBasicoViewModel()]
    mock_api_client.return_value = expected

    await result = await configuration_api.get_card_flags(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/card-flags"
    assert args["response_type"] == List[BandeirasBasicoViewModel]


def test_get_translations(configuration_api: ConfigurationApi, mock_api_client: Mock):
    """Test getting translations."""
    expected = {"key": "value"}
    mock_api_client.return_value = expected

    await result = await configuration_api.get_translations(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/card-translation"


def test_error_handling(configuration_api: ConfigurationApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await configuration_api.get_gateway_config(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
