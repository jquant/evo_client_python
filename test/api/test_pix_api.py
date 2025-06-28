"""Tests for the SyncPixApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncPixApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.pix_payment_details_view_model import PixPaymentDetailsViewModel


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def pix_api(sync_client):
    """Create a SyncPixApi instance for testing."""
    return SyncPixApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_qr_code(pix_api: SyncPixApi, mock_api_client: Mock):
    """Test getting PIX QR code."""
    expected = PixPaymentDetailsViewModel()
    mock_api_client.return_value = expected

    result = pix_api.get_qr_code()

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/pix/qr-code"


def test_get_qr_code_with_receipt_id(pix_api: SyncPixApi, mock_api_client: Mock):
    """Test getting PIX QR code with receipt ID."""
    expected = PixPaymentDetailsViewModel()
    mock_api_client.return_value = expected

    result = pix_api.get_qr_code(pix_receipt_id=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/pix/qr-code"
    assert args["query_params"]["idRecebimentoPix"] == 123


def test_error_handling(pix_api: SyncPixApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")

    with pytest.raises(ApiException) as exc:
        pix_api.get_qr_code()

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
