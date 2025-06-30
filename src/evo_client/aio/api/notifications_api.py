"""Clean asynchronous Notifications API."""

from typing import Any

from .base import AsyncBaseApi


class AsyncNotificationsApi(AsyncBaseApi):
    """Clean asynchronous Notifications API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/notifications"

    async def insert_member_notification(self, member_id: int, message: str) -> Any:
        """
        Insert a new member notification.

        Args:
            member_id: The ID of the member to send the notification to
            message: The message content of the notification

        Returns:
            Result of notification insert operation

        Example:
            >>> async with AsyncNotificationsApi() as api:
            ...     notification = NotificationApiViewModel(
            ...         member_id=123,
            ...         message="Welcome to our gym!",
            ...         notification_type="welcome"
            ...     )
            ...     result = await api.insert_member_notification(notification)
            ...     print(f"Notification inserted: {result}")
        """
        body = {
            "idMember": member_id,
            "notificationMessage": message,
        }
        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=body,
            response_type=None,
            headers={"Accept": "application/json"},
            auth_settings=["Basic"],
        )
        return result

    async def insert_prospect_notification(self, prospect_id: int, message: str) -> Any:
        """
        Insert a new prospect notification.
        """
        body = {
            "idProspect": prospect_id,
            "notificationMessage": message,
        }
        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=body,
            response_type=None,
            headers={"Accept": "application/json"},
            auth_settings=["Basic"],
        )
        return result
