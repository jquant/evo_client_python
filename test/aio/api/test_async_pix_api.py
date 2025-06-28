"""Tests for the AsyncPixApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.aio.api import AsyncPixApi
from evo_client.aio import AsyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.pix_payment_details_view_model import PixPaymentDetailsViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def pix_api(async_client):
    """Create an AsyncPixApi instance for testing."""
    return AsyncPixApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_qr_code(pix_api: AsyncPixApi, mock_api_client: Mock):
    """Test getting PIX QR code."""
    expected = PixPaymentDetailsViewModel()
    mock_api_client.return_value = expected

    result = await pix_api.get_qr_code()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/pix/qr-code"


@pytest.mark.asyncio
async def test_get_qr_code_with_receipt_id(pix_api: AsyncPixApi, mock_api_client: Mock):
    """Test getting PIX QR code with receipt ID."""
    expected = PixPaymentDetailsViewModel()
    mock_api_client.return_value = expected

    result = await pix_api.get_qr_code(pix_receipt_id=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/pix/qr-code"
    assert args["query_params"]["idRecebimentoPix"] == 123


@pytest.mark.asyncio
async def test_error_handling(pix_api: AsyncPixApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        await pix_api.get_qr_code()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
