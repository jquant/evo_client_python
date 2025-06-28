"""Tests for the SyncNotificationsApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.sync.api import SyncNotificationsApi
from evo_client.sync import SyncApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.notification_api_view_model import NotificationApiViewModel
from evo_client.models.common_models import NotificationCreateResponse


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


def test_create_notification(
    notifications_api: SyncNotificationsApi, mock_api_client: Mock
):
    """Test creating a notification."""
    expected = {"success": True}
    mock_api_client.return_value = expected
    notification_data = NotificationApiViewModel()
    notification_data.id_member = 123
    notification_data.notification_message = "Welcome to our gym!"

    result = notifications_api.create_notification(notification=notification_data)

    assert result == NotificationCreateResponse.model_validate(expected)
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/notifications"
    assert args["body"] == notification_data.model_dump(
        exclude_unset=True, by_alias=True
    )


def test_error_handling(notifications_api: SyncNotificationsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")
    notification_data = NotificationApiViewModel()

    with pytest.raises(ApiException) as exc:
        notifications_api.create_notification(notification=notification_data)

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
