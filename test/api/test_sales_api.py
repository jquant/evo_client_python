"""Tests for the SalesApi class."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from evo_client.api.sales_api import SalesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.new_sale_view_model import NewSaleViewModel
from evo_client.models.sales_items_view_model import SalesItemsViewModel
from evo_client.models.sales_view_model import SalesViewModel


@pytest.fixture
def sales_api():
    """Create a SalesApi instance for testing."""
    return SalesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.sales_api.ApiClient.call_api") as mock:
        yield mock


def test_get_sale_by_id_basic(sales_api: SalesApi, mock_api_client: Mock):
    """Test getting sale by ID."""
    expected = SalesViewModel()
    mock_api_client.return_value = expected

    result = sales_api.get_sale_by_id(sale_id=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/sales/123"
    assert args["auth_settings"] == ["Basic"]


def test_get_sale_by_id_error(sales_api: SalesApi, mock_api_client: Mock):
    """Test error handling for getting sale by ID."""

    with pytest.raises(ValueError):
        sales_api.get_sale_by_id(sale_id=0, async_req=False)


def test_create_sale(sales_api: SalesApi, mock_api_client: Mock):
    """Test creating a new sale."""
    expected = NewSaleViewModel()
    mock_api_client.return_value = expected
    sale_data = NewSaleViewModel()

    result = sales_api.create_sale(body=sale_data, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/sales"
    assert args["body"] == sale_data


def test_get_sales_with_filters(sales_api: SalesApi, mock_api_client: Mock):
    """Test getting sales with filters."""
    expected = SalesViewModel()
    mock_api_client.return_value = expected

    result = sales_api.get_sales(
        member_id=123,
        date_sale_start=datetime(2023, 1, 1),
        date_sale_end=datetime(2023, 12, 31),
        take=10,
        skip=0,
        only_membership=True,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v2/sales"
    assert args["query_params"]["idMember"] == 123
    assert args["query_params"]["take"] == 10
    assert args["query_params"]["skip"] == 0
    assert args["query_params"]["onlyMembership"] is True


def test_get_sales_items(sales_api: SalesApi, mock_api_client: Mock):
    """Test getting sales items."""
    expected = [SalesItemsViewModel()]
    mock_api_client.return_value = expected

    result = sales_api.get_sales_items(branch_id=123, async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/sales/sales-items"
    assert args["query_params"]["idBranch"] == 123


def test_get_sale_by_session_id(sales_api: SalesApi, mock_api_client: Mock):
    """Test getting sale by session ID."""
    expected = 123
    mock_api_client.return_value = expected

    result = sales_api.get_sale_by_session_id(
        session_id="abc123", date=datetime(2023, 1, 1), async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/sales/by-session-id"
    assert args["query_params"]["sessionId"] == "abc123"


def test_error_handling(sales_api: SalesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        sales_api.get_sale_by_id(sale_id=123, async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
