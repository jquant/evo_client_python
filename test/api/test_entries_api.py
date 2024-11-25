"""Tests for the EntriesApi class."""

import pytest
from datetime import datetime
from unittest.mock import patch, Mock

from evo_client.api.entries_api import EntriesApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.entradas_resumo_api_view_model import EntradasResumoApiViewModel


@pytest.fixture
def entries_api():
    """Create an EntriesApi instance for testing."""
    return EntriesApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.entries_api.ApiClient.call_api") as mock:
        yield mock


def test_get_entries_basic(entries_api: EntriesApi, mock_api_client: Mock):
    """Test getting entries list with no parameters."""
    expected = [EntradasResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = entries_api.get_entries(async_req=False)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "GET"
    assert args["resource_path"] == "/api/v1/entries"


def test_get_entries_with_filters(entries_api: EntriesApi, mock_api_client: Mock):
    """Test getting entries with search filters."""
    expected = [EntradasResumoApiViewModel()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = entries_api.get_entries(
        register_date_start=start_date,
        register_date_end=end_date,
        take=10,
        skip=0,
        entry_id=123,
        member_id=456,
        async_req=False,
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "registerDateStart": start_date,
        "registerDateEnd": end_date,
        "take": 10,
        "skip": 0,
        "IdEntry": 123,
        "idMember": 456,
    }


def test_get_entries_max_take(entries_api: EntriesApi, mock_api_client: Mock):
    """Test error when take parameter exceeds maximum."""
    with pytest.raises(ValueError) as exc:
        entries_api.get_entries(take=1001, async_req=False)

    assert str(exc.value) == "Maximum number of records to return is 1000"
    mock_api_client.assert_not_called()


def test_get_member_entries(entries_api: EntriesApi, mock_api_client: Mock):
    """Test getting entries for a specific member."""
    expected = [EntradasResumoApiViewModel()]
    mock_api_client.return_value = expected
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)

    result = entries_api.get_member_entries(
        member_id=123, start_date=start_date, end_date=end_date, async_req=False
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {
        "registerDateStart": start_date,
        "registerDateEnd": end_date,
        "idMember": 123,
    }


def test_get_entry_by_id(entries_api: EntriesApi, mock_api_client: Mock):
    """Test getting a specific entry by ID."""
    expected = [EntradasResumoApiViewModel()]
    mock_api_client.return_value = expected

    result = entries_api.get_entry_by_id(entry_id=123, async_req=False)

    assert result == expected[0]
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["query_params"] == {"IdEntry": 123}


def test_get_entry_by_id_not_found(entries_api: EntriesApi, mock_api_client: Mock):
    """Test getting a non-existent entry by ID."""
    mock_api_client.return_value = []

    result = entries_api.get_entry_by_id(entry_id=123, async_req=False)

    assert result is None


def test_error_handling(entries_api: EntriesApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")

    with pytest.raises(ApiException) as exc:
        entries_api.get_entries(async_req=False)

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
