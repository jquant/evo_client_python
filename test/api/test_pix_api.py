"""Tests for the PixApi class."""

from unittest.mock import Mock, patch

import pytest


from evo_client.api.pix_api import PixApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.pix_payment_details_view_model import PixPaymentDetailsViewModel


@pytest.fixture
def pix_api():
    """Create a PixApi instance for testing."""
    return PixApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.pix_api.ApiClient.call_api") as mock:
        yield mock


def test_get_qr_code_basic(pix_api: PixApi, mock_api_client: Mock):
    """Test getting QR code with no parameters."""
    expected = PixPaymentDetailsViewModel()
    mock_api_client.return_value = expected

    result = pix_api.get_qr_code(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/pix/qr-code"
    assert args["auth_settings"] == ["Basic"]


def test_get_qr_code_with_receipt_id(pix_api: PixApi, mock_api_client: Mock):
    """Test getting QR code with receipt ID."""
    expected = PixPaymentDetailsViewModel()
    mock_api_client.return_value = expected

    result = pix_api.get_qr_code(pix_receipt_id=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {"idRecebimentoPix": 123}


def test_error_handling(pix_api: PixApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        await pix_api.get_qr_code(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
