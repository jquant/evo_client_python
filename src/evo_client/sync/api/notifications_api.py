"""Clean synchronous Notifications API."""

from typing import Any

from ...models.common_models import NotificationCreateResponse
from ...models.notification_api_view_model import NotificationApiViewModel
from .base import SyncBaseApi


class SyncNotificationsApi(SyncBaseApi):
    """Clean synchronous Notifications API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/notifications"

    def create_notification(
        self, notification: NotificationApiViewModel
    ) -> NotificationCreateResponse:
        """
        Create a new member notification.

        Args:
            notification: The notification details to create including:
                - Member information
                - Message content and type
                - Delivery preferences
                - Scheduling options

        Returns:
            Result of notification creation operation with status and details

        Example:
            >>> with SyncNotificationsApi() as api:
            ...     notification = NotificationApiViewModel(
            ...         member_id=123,
            ...         message="Welcome to our gym!",
            ...         notification_type="welcome"
            ...     )
            ...     result = api.create_notification(notification)
            ...     if result.success:
            ...         print(f"Notification created with ID: {result.notification_id}")
        """
        try:
            result: Any = self.api_client.call_api(
                resource_path=self.base_path,
                method="POST",
                body=notification.model_dump(exclude_unset=True, by_alias=True),
                response_type=None,
                headers={"Accept": "application/json"},
                auth_settings=["Basic"],
            )

            # Parse response or create success response
            if isinstance(result, dict):
                return NotificationCreateResponse.model_validate(result)
            else:
                # If API doesn't return structured response, create our own
                return NotificationCreateResponse(
                    success=True, message="Notification created successfully"
                )
        except Exception as e:
            return NotificationCreateResponse(
                success=False,
                message=f"Error creating notification: {str(e)}",
                errors=[str(e)],
            )
