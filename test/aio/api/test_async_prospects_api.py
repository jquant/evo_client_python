"""Tests for the AsyncProspectsApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncProspectsApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.prospect_api_integracao_atualizacao_view_model import (
    ProspectApiIntegracaoAtualizacaoViewModel,
)
from evo_client.models.prospect_api_integracao_view_model import (
    ProspectApiIntegracaoViewModel,
)
from evo_client.models.prospect_id_view_model import ProspectIdViewModel
from evo_client.models.prospect_transferencia_view_model import (
    ProspectTransferenciaViewModel,
)
from evo_client.models.prospects_resumo_api_view_model import (
    ProspectsResumoApiViewModel,
)


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def prospects_api(async_client):
    """Create an AsyncProspectsApi instance for testing."""
    return AsyncProspectsApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_prospects_basic(
    prospects_api: AsyncProspectsApi, mock_api_client: Mock
):
    """Test getting prospects without filters."""
    expected = [ProspectsResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await prospects_api.get_prospects()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/prospects"


@pytest.mark.asyncio
async def test_get_prospects_with_filters(
    prospects_api: AsyncProspectsApi, mock_api_client: Mock
):
    """Test getting prospects with various filters."""
    expected = [ProspectsResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = await prospects_api.get_prospects(
        name="John",
        email="john@example.com",
        document="12345678900",
        phone="1234567890",
        register_date_start=datetime(2023, 1, 1),
        register_date_end=datetime(2023, 12, 31),
        take=50,
        skip=0,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/prospects"
    query_params = args["query_params"]
    assert query_params["name"] == "John"
    assert query_params["email"] == "john@example.com"
    assert query_params["document"] == "12345678900"
    assert query_params["phone"] == "1234567890"
    assert query_params["take"] == 50
    assert query_params["skip"] == 0


@pytest.mark.asyncio
async def test_create_prospect(prospects_api: AsyncProspectsApi, mock_api_client: Mock):
    """Test creating a new prospect."""
    expected = ProspectIdViewModel()
    mock_api_client.return_value = expected
    prospect_data = ProspectApiIntegracaoViewModel()

    result = await prospects_api.create_prospect(prospect=prospect_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/prospects"
    assert args["body"] == prospect_data.model_dump(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_update_prospect(prospects_api: AsyncProspectsApi, mock_api_client: Mock):
    """Test updating a prospect."""
    expected = ProspectIdViewModel()
    mock_api_client.return_value = expected
    prospect_data = ProspectApiIntegracaoAtualizacaoViewModel()

    result = await prospects_api.update_prospect(prospect=prospect_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "PUT"
    assert args["resource_path"] == "/api/v1/prospects"
    assert args["body"] == prospect_data.model_dump(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_transfer_prospect(
    prospects_api: AsyncProspectsApi, mock_api_client: Mock
):
    """Test transferring a prospect."""
    mock_api_client.return_value = None
    transfer_data = ProspectTransferenciaViewModel()

    result = await prospects_api.transfer_prospect(transfer=transfer_data)
    assert result is None

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/prospects/transfer"
    assert args["body"] == transfer_data.model_dump(exclude_unset=True, by_alias=True)


@pytest.mark.asyncio
async def test_error_handling(prospects_api: AsyncProspectsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await prospects_api.get_prospects()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
