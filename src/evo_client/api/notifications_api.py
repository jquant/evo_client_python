from multiprocessing.pool import AsyncResult
from typing import Any, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.notification_api_view_model import NotificationApiViewModel
from .base import BaseApi


class NotificationsApi(BaseApi):
    """Notifications API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = "/api/v1/notifications"

    @overload
    def create_notification(
        self, notification: NotificationApiViewModel, async_req: Literal[False] = False
    ) -> Any:
        ...

    @overload
    def create_notification(
        self, notification: NotificationApiViewModel, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    def create_notification(
        self, notification: NotificationApiViewModel, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Create a new member notification.

        Args:
            notification: The notification details to create
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=notification.model_dump(exclude_unset=True),
            response_type=None,
            headers={"Accept": "application/json"},
            auth_settings=["Basic"],
            async_req=async_req,
        )
