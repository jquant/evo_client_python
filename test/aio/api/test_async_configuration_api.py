"""Tests for the AsyncConfigurationApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncConfigurationApi
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
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def configuration_api(async_client):
    """Create an AsyncConfigurationApi instance for testing."""
    return AsyncConfigurationApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_gateway_config(
    configuration_api: AsyncConfigurationApi, mock_api_client: Mock
):
    """Test getting gateway configurations."""
    expected = EmpresasFiliaisGatewayViewModel()
    mock_api_client.return_value = expected

    result = await configuration_api.get_gateway_config()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/gateway"


@pytest.mark.asyncio
async def test_get_branch_config(
    configuration_api: AsyncConfigurationApi, mock_api_client: Mock
):
    """Test getting branch configurations."""
    expected = [ConfiguracaoApiViewModel()]
    mock_api_client.return_value = expected

    result = await configuration_api.get_branch_config()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration"


@pytest.mark.asyncio
async def test_get_occupations(
    configuration_api: AsyncConfigurationApi, mock_api_client: Mock
):
    """Test getting occupation configurations."""
    expected = [EmpresasFiliaisOcupacaoViewModel()]
    mock_api_client.return_value = expected

    result = await configuration_api.get_occupations()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/occupation"


@pytest.mark.asyncio
async def test_get_card_flags(
    configuration_api: AsyncConfigurationApi, mock_api_client: Mock
):
    """Test getting card flags."""
    expected = [BandeirasBasicoViewModel()]
    mock_api_client.return_value = expected

    result = await configuration_api.get_card_flags()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/card-flags"


@pytest.mark.asyncio
async def test_get_translations(
    configuration_api: AsyncConfigurationApi, mock_api_client: Mock
):
    """Test getting translations."""
    expected = {"key": "value"}
    mock_api_client.return_value = expected

    result = await configuration_api.get_translations()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/card-translation"


@pytest.mark.asyncio
async def test_error_handling(
    configuration_api: AsyncConfigurationApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await configuration_api.get_gateway_config()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
