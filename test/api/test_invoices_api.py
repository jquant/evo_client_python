"""Tests for the InvoicesApi class."""

import pytest
from datetime import datetime
from unittest.mock import patch, Mock

from evo_client.api.invoices_api import InvoicesApi, InvoiceStatus, InvoiceType
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.enotas_retorno import EnotasRetorno


@pytest.fixture
def invoices_api():
    """Create an InvoicesApi instance for testing."""
    return InvoicesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.invoices_api.ApiClient.call_api") as mock:
        yield mock


def test_get_invoices_basic(invoices_api: InvoicesApi, mock_api_client: Mock):
    """Test getting invoices list with no parameters."""
    expected = EnotasRetorno()
    mock_api_client.return_value = expected

    result = invoices_api.get_invoices(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/invoices/get-invoices"


def test_get_invoices_with_filters(invoices_api: InvoicesApi, mock_api_client: Mock):
    """Test getting invoices with search filters."""
    expected = EnotasRetorno()
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = invoices_api.get_invoices(
        issue_date_start=start_date,
        issue_date_end=end_date,
        competency_date_start=start_date,
        competency_date_end=end_date,
        send_date_start=start_date,
        send_date_end=end_date,
        take=10,
        skip=0,
        member_id=123,
        status_invoice=[InvoiceStatus.ISSUED, InvoiceStatus.CANCELED],
        types_invoice=[InvoiceType.NFSE, InvoiceType.NFE],
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "issueDateStart": start_date,
        "issueDateEnd": end_date,
        "competencyDateStart": start_date,
        "competencyDateEnd": end_date,
        "sendDateStart": start_date,
        "sendDateEnd": end_date,
        "take": 10,
        "skip": 0,
        "idMember": 123,
        "statusInvoice": "1,3",
        "typesInvoice": "1,2",
    }


def test_get_invoices_take_limit(invoices_api: InvoicesApi, mock_api_client: Mock):
    """Test error when take parameter exceeds limit."""
    with pytest.raises(ValueError) as exc:
        invoices_api.get_invoices(take=251, async_req=False)

    assert str(exc.value) == "Maximum number of records to return is 250"
    mock_api_client.assert_not_called()


def test_error_handling(invoices_api: InvoicesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        invoices_api.get_invoices(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
