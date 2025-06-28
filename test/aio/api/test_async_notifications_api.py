"""Tests for the AsyncNotificationsApi class."""

from unittest.mock import Mock, patch

import pytest

from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncNotificationsApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.notification_api_view_model import NotificationApiViewModel


@pytest.fixture
def async_client():
    """Create an AsyncApiClient instance for testing."""
    return AsyncApiClient()


@pytest.fixture
def notifications_api(async_client):
    """Create an AsyncNotificationsApi instance for testing."""
    return AsyncNotificationsApi(async_client)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.aio.core.api_client.AsyncApiClient.call_api") as mock:
        yield mock


@pytest.mark.asyncio
async def test_create_notification(
    notifications_api: AsyncNotificationsApi, mock_api_client: Mock
):
    """Test creating a notification."""
    expected = {"success": True}
    mock_api_client.return_value = expected
    notification_data = NotificationApiViewModel()
    notification_data.id_member = 123
    notification_data.notification_message = "Welcome to our gym!"

    result = await notifications_api.create_notification(notification=notification_data)

    assert result == expected
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["method"] == "POST"
    assert args["resource_path"] == "/api/v1/notifications"
    assert args["body"] == notification_data.model_dump(
        exclude_unset=True, by_alias=True
    )


@pytest.mark.asyncio
async def test_error_handling(
    notifications_api: AsyncNotificationsApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")
    notification_data = NotificationApiViewModel()

    with pytest.raises(ApiException) as exc:
        await notifications_api.create_notification(notification=notification_data)

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
