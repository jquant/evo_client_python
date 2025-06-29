"""Tests for the SyncConfigurationApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.bandeiras_basico_view_model import BandeirasBasicoViewModel
from evo_client.models.configuracao_api_view_model import ConfiguracaoApiViewModel
from evo_client.models.empresas_filiais_gateway_view_model import (
    EmpresasFiliaisGatewayViewModel,
)
from evo_client.models.empresas_filiais_ocupacao_view_model import (
    EmpresasFiliaisOcupacaoViewModel,
)
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncConfigurationApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def configuration_api(sync_client):
    """Create a SyncConfigurationApi instance for testing."""
    return SyncConfigurationApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_gateway_config(
    configuration_api: SyncConfigurationApi, mock_api_client: Mock
):
    """Test getting gateway configurations."""
    expected = EmpresasFiliaisGatewayViewModel()
    mock_api_client.return_value = expected

    result = configuration_api.get_gateway_config()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/gateway"


def test_get_branch_config(
    configuration_api: SyncConfigurationApi, mock_api_client: Mock
):
    """Test getting branch configurations."""
    expected = [ConfiguracaoApiViewModel()]
    mock_api_client.return_value = expected

    result = configuration_api.get_branch_config()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration"


def test_get_occupations(
    configuration_api: SyncConfigurationApi, mock_api_client: Mock
):
    """Test getting occupation configurations."""
    expected = [EmpresasFiliaisOcupacaoViewModel()]
    mock_api_client.return_value = expected

    result = configuration_api.get_occupations()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/occupation"


def test_get_card_flags(configuration_api: SyncConfigurationApi, mock_api_client: Mock):
    """Test getting card flags."""
    expected = [BandeirasBasicoViewModel()]
    mock_api_client.return_value = expected

    result = configuration_api.get_card_flags()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/card-flags"


def test_get_translations(
    configuration_api: SyncConfigurationApi, mock_api_client: Mock
):
    """Test getting translations."""
    expected = {"key": "value"}
    mock_api_client.return_value = expected

    result = configuration_api.get_translations()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/configuration/card-translation"


def test_error_handling(configuration_api: SyncConfigurationApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        configuration_api.get_gateway_config()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
