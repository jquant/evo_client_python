from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from ..models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from ..models.w12_utils_webhook_view_model import W12UtilsWebhookViewModel


class WebhookApi:
    """Webhook API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/webhook"

    @overload
    def delete_webhook(self, webhook_id: int, async_req: Literal[False] = False) -> Any:
        ...

    @overload
    def delete_webhook(
        self, webhook_id: int, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    def delete_webhook(
        self, webhook_id: int, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Remove a specific webhook by ID.

        Args:
            webhook_id: ID of the webhook to delete
            async_req: Execute request asynchronously
        """
        params = {"IdWebhook": webhook_id}

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="DELETE",
            query_params=params,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_webhooks(self, async_req: Literal[False] = False) -> Any:
        ...

    @overload
    def get_webhooks(self, async_req: Literal[True] = True) -> AsyncResult[Any]:
        ...

    def get_webhooks(self, async_req: bool = False) -> Union[Any, AsyncResult[Any]]:
        """
        List all webhooks created.

        Args:
            async_req: Execute request asynchronously

        Returns:
            List of webhook configurations
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def create_webhook(
        self,
        event_type: str,
        url_callback: str,
        branch_id: Optional[int] = None,
        headers: Optional[List[W12UtilsWebhookHeaderViewModel]] = None,
        filters: Optional[List[W12UtilsWebhookFilterViewModel]] = None,
        async_req: Literal[False] = False,
    ) -> Any:
        ...

    @overload
    def create_webhook(
        self,
        event_type: str,
        url_callback: str,
        branch_id: Optional[int] = None,
        headers: Optional[List[W12UtilsWebhookHeaderViewModel]] = None,
        filters: Optional[List[W12UtilsWebhookFilterViewModel]] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    def create_webhook(
        self,
        event_type: str,
        url_callback: str,
        branch_id: Optional[int] = None,
        headers: Optional[List[W12UtilsWebhookHeaderViewModel]] = None,
        filters: Optional[List[W12UtilsWebhookFilterViewModel]] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Add new webhook configuration.

        Args:
            event_type: Type of event that will trigger this webhook
                Available types: NewSale, CreateMember, AlterMember, EndedSessionActivity,
                ClearedDebt, AlterReceivables, Freeze, RecurrentSale, entries,
                ActivityEnroll, SalesItensUpdated, CreateMembership, AlterMembership,
                CreateService, AlterService, CreateProduct, AlterProduct
            url_callback: URL that will be called after the event
            branch_id: Branch number for webhook registration (multilocation key only)
            headers: Optional list of custom headers to include in webhook calls
            filters: Optional filters (only available for NewSale event type)
            async_req: Execute request asynchronously

        Example filters format:
            [
                {
                    "FilterType": "SaleItemDescription",
                    "Value": "filter_string"
                }
            ]
        """
        webhook_data = W12UtilsWebhookViewModel(
            idBranch=branch_id,
            eventType=event_type,
            urlCallback=url_callback,
            headers=headers or [W12UtilsWebhookHeaderViewModel()],
            filters=filters or [W12UtilsWebhookFilterViewModel()],
        )

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=webhook_data,
            headers={
                "Accept": ["text/plain", "application/json", "text/json"],
                "Content-Type": [
                    "application/json-patch+json",
                    "application/json",
                    "text/json",
                    "application/*+json",
                ],
            },
            auth_settings=["Basic"],
            async_req=async_req,
        )
