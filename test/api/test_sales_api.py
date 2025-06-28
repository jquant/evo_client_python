"""Tests for the SyncSalesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.new_sale_view_model import NewSaleViewModel
from evo_client.models.sales_items_view_model import SalesItemsViewModel
from evo_client.models.sales_view_model import SalesViewModel
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncSalesApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def sales_api(sync_client):
    """Create a SyncSalesApi instance for testing."""
    return SyncSalesApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_get_sale_by_id_basic(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test getting sale by ID."""
    expected = SalesViewModel()
    mock_api_client.return_value = expected

    result = sales_api.get_sale_by_id(sale_id=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/sales/123"
    assert args["auth_settings"] == ["Basic"]


def test_get_sale_by_id_error(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test error handling for getting sale by ID."""

    with pytest.raises(ValueError):
        sales_api.get_sale_by_id(sale_id=0)


def test_create_sale(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test creating a sale."""
    sale_data = NewSaleViewModel()
    expected = sale_data
    mock_api_client.return_value = expected

    result = sales_api.create_sale(body=sale_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/sales"


def test_get_sales_basic(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test getting sales list."""
    expected = [SalesViewModel()]
    mock_api_client.return_value = expected

    result = sales_api.get_sales(member_id=123, take=10, skip=0)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/sales"


def test_get_sales_with_dates(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test getting sales with date filters."""
    expected = [SalesViewModel()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    result = sales_api.get_sales(
        date_sale_start=start_date, date_sale_end=end_date, take=5
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/sales"


def test_get_sales_items(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test getting sales items."""
    expected = [SalesItemsViewModel()]
    mock_api_client.return_value = expected

    result = sales_api.get_sales_items(branch_id=123)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/sales/sales-items"
    assert args["query_params"]["idBranch"] == 123


def test_get_sale_by_session_id(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test getting sale by session ID."""
    expected = 123
    mock_api_client.return_value = expected

    result = sales_api.get_sale_by_session_id(
        session_id="abc123", date=datetime(2023, 1, 1)
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/sales/by-session-id"
    assert args["query_params"]["sessionId"] == "abc123"


def test_error_handling(sales_api: SyncSalesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        sales_api.get_sales()

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
