from typing import Optional, Union, overload
from threading import Thread

from ..core.api_client import ApiClient
from ..models.notification_api_view_model import NotificationApiViewModel


class NotificationsApi:
    """Notifications API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/notifications"

    @overload
    def create_notification(
        self, notification: NotificationApiViewModel, async_req: bool = True
    ) -> Thread: ...

    @overload
    def create_notification(
        self, notification: NotificationApiViewModel, async_req: bool = False
    ) -> None: ...

    def create_notification(
        self, notification: NotificationApiViewModel, async_req: bool = False
    ) -> Union[None, Thread]:
        """
        Create a new member notification.

        Args:
            notification: The notification details to create
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=notification,
            response_type=None,
            headers={"Accept": "application/json"},
            auth_settings=["Basic"],
            async_req=async_req,
        )