"""Clean asynchronous Notifications API."""

from typing import Any

from ...models.notification_api_view_model import NotificationApiViewModel
from .base import AsyncBaseApi


class AsyncNotificationsApi(AsyncBaseApi):
    """Clean asynchronous Notifications API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/notifications"

    async def create_notification(self, notification: NotificationApiViewModel) -> Any:
        """
        Create a new member notification.

        Args:
            notification: The notification details to create including:
                - Member information
                - Message content and type
                - Delivery preferences
                - Scheduling options

        Returns:
            Result of notification creation operation

        Example:
            >>> async with AsyncNotificationsApi() as api:
            ...     notification = NotificationApiViewModel(
            ...         member_id=123,
            ...         message="Welcome to our gym!",
            ...         notification_type="welcome"
            ...     )
            ...     result = await api.create_notification(notification)
            ...     print(f"Notification created: {result}")
        """
        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=notification.model_dump(exclude_unset=True, by_alias=True),
            response_type=None,
            headers={"Accept": "application/json"},
            auth_settings=["Basic"],
        )
        return result
