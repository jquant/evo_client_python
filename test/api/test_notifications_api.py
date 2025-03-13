"""Tests for the NotificationsApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.api.notifications_api import NotificationsApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.notification_api_view_model import NotificationApiViewModel


@pytest.fixture
def notifications_api():
    """Create a NotificationsApi instance for testing."""
    return NotificationsApi()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.notifications_api.ApiClient.call_api") as mock:
        yield mock


def test_create_notification(
    notifications_api: NotificationsApi, mock_api_client: Mock
):
    """Test creating a notification."""
    mock_api_client.return_value = None
    notification = NotificationApiViewModel()

    notifications_api.create_notification(notification=notification, async_req=False)

    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/notifications"
    assert args["body"] == notification.model_dump(exclude_unset=True)


def test_error_handling(notifications_api: NotificationsApi, mock_api_client: Mock):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=404, reason="Not Found")
    notification = NotificationApiViewModel()

    with pytest.raises(ApiException) as exc:
        notifications_api.create_notification(
            notification=notification, async_req=False
        )

    assert exc.value.status == 404
    assert exc.value.reason == "Not Found"
