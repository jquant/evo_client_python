"""Tests for the SyncBaseApi class."""

from unittest.mock import Mock

import pytest

from evo_client.sync.api.base import SyncBaseApi
from evo_client.sync.core.api_client import SyncApiClient


@pytest.fixture
def sync_api_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


def test_sync_base_api_initialization_with_client(sync_api_client):
    """Test initializing SyncBaseApi with provided client."""
    api = SyncBaseApi(sync_api_client)
    assert api.api_client == sync_api_client


def test_sync_base_api_initialization_without_client():
    """Test initializing SyncBaseApi without provided client."""
    api = SyncBaseApi()
    assert api.api_client is not None
    assert isinstance(api.api_client, SyncApiClient)


def test_sync_base_api_context_manager_with_enter_exit():
    """Test context manager when api_client has __enter__ and __exit__."""
    mock_client = Mock()
    mock_client.__enter__ = Mock(return_value=mock_client)
    mock_client.__exit__ = Mock()

    api = SyncBaseApi(mock_client)

    with api as context_api:
        assert context_api == api
        mock_client.__enter__.assert_called_once()

    mock_client.__exit__.assert_called_once()


def test_sync_base_api_context_manager_without_enter_exit():
    """Test context manager when api_client doesn't have __enter__ and __exit__."""
    mock_client = Mock()
    # Remove __enter__ and __exit__ methods
    if hasattr(mock_client, "__enter__"):
        delattr(mock_client, "__enter__")
    if hasattr(mock_client, "__exit__"):
        delattr(mock_client, "__exit__")

    api = SyncBaseApi(mock_client)

    # Should not raise an error
    with api as context_api:
        assert context_api == api


def test_sync_base_api_context_manager_integration():
    """Test full context manager integration."""
    api = SyncBaseApi()

    # Should work without errors
    with api as context_api:
        assert context_api == api
        assert context_api.api_client is not None
