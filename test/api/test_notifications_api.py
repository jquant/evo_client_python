"""Tests for the SyncNotificationsApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.models.notification_api_view_model import NotificationApiViewModel
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncNotificationsApi


@pytest.fixture
def sync_client():
    """Create a SyncApiClient instance for testing."""
    return SyncApiClient()


@pytest.fixture
def notifications_api(sync_client):
    """Create a SyncNotificationsApi instance for testing."""
    return SyncNotificationsApi(sync_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.sync.core.api_client.SyncApiClient.call_api") as mock:
        yield mock


def test_insert_member_notification(
    notifications_api: SyncNotificationsApi, mock_api_client: Mock
):
    """Test inserting a member notification."""
    expected = {"success": True}
    mock_api_client.return_value = expected
    notification_data = NotificationApiViewModel()
    notification_data.id_member = 123
    notification_data.notification_message = "Welcome to our gym!"

    result = notifications_api.insert_member_notification(
        member_id=123, message="Welcome to our gym!"
    )

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/notifications"
