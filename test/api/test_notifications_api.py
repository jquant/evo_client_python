"""Tests for the SyncNotificationsApi class."""

from unittest.mock import Mock, patch

import pytest

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
    member_id = 123
    message = "Welcome to our gym!"
    expected_result = {"success": True, "notification_id": 456}

    mock_api_client.return_value = expected_result

    result = notifications_api.insert_member_notification(member_id, message)

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


def test_insert_prospect_notification(
    notifications_api: SyncNotificationsApi, mock_api_client: Mock
):
    """Test inserting a prospect notification."""
    prospect_id = 789
    message = "Thank you for your interest!"
    expected_result = {"success": True, "notification_id": 101}

    mock_api_client.return_value = expected_result

    result = notifications_api.insert_prospect_notification(prospect_id, message)

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


def test_notifications_api_initialization():
    """Test NotificationsApi initialization."""
    api = SyncNotificationsApi()
    assert api.api_client is not None
    assert api.base_path == "/api/v1/notifications"


def test_notifications_api_initialization_with_client(sync_client):
    """Test NotificationsApi initialization with provided client."""
    api = SyncNotificationsApi(sync_client)
    assert api.api_client == sync_client
    assert api.base_path == "/api/v1/notifications"
