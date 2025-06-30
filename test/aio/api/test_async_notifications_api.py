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
async def test_insert_member_notification(
    notifications_api: AsyncNotificationsApi, mock_api_client: Mock
):
    """Test inserting a member notification."""
    member_id = 123
    message = "Welcome to our gym!"
    expected_result = {"success": True, "notification_id": 456}

    mock_api_client.return_value = expected_result

    result = await notifications_api.insert_member_notification(member_id, message)

    assert result == expected_result
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["resource_path"] == "/api/v1/notifications"
    assert args["method"] == "POST"
    assert args["body"] == {
        "idMember": member_id,
        "notificationMessage": message,
    }
    assert args["response_type"] is None
    assert args["headers"] == {"Accept": "application/json"}
    assert args["auth_settings"] == ["Basic"]


@pytest.mark.asyncio
async def test_insert_prospect_notification(
    notifications_api: AsyncNotificationsApi, mock_api_client: Mock
):
    """Test inserting a prospect notification."""
    prospect_id = 789
    message = "Thank you for your interest!"
    expected_result = {"success": True, "notification_id": 101}

    mock_api_client.return_value = expected_result

    result = await notifications_api.insert_prospect_notification(prospect_id, message)

    assert result == expected_result
    mock_api_client.assert_called_once()
    args = mock_api_client.call_args[1]
    assert args["resource_path"] == "/api/v1/notifications"
    assert args["method"] == "POST"
    assert args["body"] == {
        "idProspect": prospect_id,
        "notificationMessage": message,
    }
    assert args["response_type"] is None
    assert args["headers"] == {"Accept": "application/json"}
    assert args["auth_settings"] == ["Basic"]


@pytest.mark.asyncio
async def test_notifications_api_initialization():
    """Test AsyncNotificationsApi initialization."""
    api = AsyncNotificationsApi()
    assert api.api_client is not None
    assert api.base_path == "/api/v1/notifications"


@pytest.mark.asyncio
async def test_notifications_api_initialization_with_client(async_client):
    """Test AsyncNotificationsApi initialization with provided client."""
    api = AsyncNotificationsApi(async_client)
    assert api.api_client == async_client
    assert api.base_path == "/api/v1/notifications"


@pytest.mark.asyncio
async def test_error_handling(
    notifications_api: AsyncNotificationsApi, mock_api_client: Mock
):
    """Test API error handling."""
    mock_api_client.side_effect = ApiException(status=500, reason="Server Error")
    notification_data = NotificationApiViewModel()

    with pytest.raises(ApiException) as exc:
        await notifications_api.insert_member_notification(
            member_id=123, message="Welcome to our gym!"
        )

    assert exc.value.status == 500
    assert exc.value.reason == "Server Error"
