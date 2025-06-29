from typing import List, Optional

from loguru import logger

from ...models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from ...models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from ...models.webhook_model import Webhook, WebhookEventType
from ...sync.api.webhook_api import SyncWebhookApi
from . import BaseDataFetcher


class WebhookDataFetcher(BaseDataFetcher):
    """Handles fetching and processing webhook-related data."""

    def fetch_webhooks(self) -> List[Webhook]:
        """Fetch all webhooks.

        Returns:
            List[Webhook]: List of webhook configurations
        """
        # Use available branch IDs from base class
        branch_ids = self.get_available_branch_ids()

        result = []
        for branch_id in branch_ids:
            branch_api = SyncWebhookApi(api_client=self.get_branch_api(branch_id))
            if branch_api:
                try:
                    webhooks = branch_api.get_webhooks()
                    if webhooks:
                        result.extend([Webhook(**webhook) for webhook in webhooks])
                except Exception as e:
                    logger.warning(
                        f"Failed to fetch webhooks for branch {branch_id}: {e}"
                    )

        return result

    def create_webhook(
        self,
        url_callback: str,
        event_type: WebhookEventType,
        branch_id: Optional[int] = None,
        headers: Optional[List[W12UtilsWebhookHeaderViewModel]] = None,
        filters: Optional[List[W12UtilsWebhookFilterViewModel]] = None,
    ) -> bool:
        """Create a new webhook configuration.

        Args:
            url_callback: The webhook callback URL
            event_type: Type of events to subscribe to
            branch_id: Optional branch ID for the webhook
            headers: Optional list of webhook headers
            filters: Optional list of webhook filters

        Returns:
            bool: True if webhook was created successfully
        """
        # Use available branch IDs from base class
        branch_ids = self.get_available_branch_ids()

        # If branch_id is provided, only try that specific branch
        if branch_id is not None:
            if branch_id not in branch_ids:
                return False
            branch_ids = [branch_id]

        for current_branch_id in branch_ids:
            branch_api = SyncWebhookApi(
                api_client=self.get_branch_api(current_branch_id)
            )
            if branch_api:
                try:
                    success = branch_api.create_webhook(
                        event_type=event_type.value,
                        url_callback=url_callback,
                        branch_id=current_branch_id,
                        headers=headers,
                        filters=filters,
                    )
                    if success:
                        return True
                except Exception as e:
                    logger.warning(
                        f"Failed to create webhook for branch {current_branch_id}: {e}"
                    )

        return False

    def delete_webhook(self, webhook_id: int, branch_id: Optional[int] = None) -> bool:
        """Delete a webhook configuration.

        Args:
            webhook_id: ID of the webhook to delete
            branch_id: Optional branch ID to delete from

        Returns:
            bool: True if webhook was deleted successfully
        """
        # Use available branch IDs from base class
        branch_ids = self.get_available_branch_ids()

        # If branch_id is provided, only try that specific branch
        if branch_id is not None:
            if branch_id not in branch_ids:
                return False
            branch_ids = [branch_id]

        for current_branch_id in branch_ids:
            branch_api = SyncWebhookApi(
                api_client=self.get_branch_api(current_branch_id)
            )
            if branch_api:
                try:
                    # Convert webhook_id to int if it's an object with id_webhook property
                    webhook_id_value = (
                        int(webhook_id)
                        if isinstance(webhook_id, (int, str))
                        else getattr(webhook_id, "id_webhook", None)
                    )
                    if webhook_id_value is None:
                        logger.warning(f"Invalid webhook ID: {webhook_id}")
                        continue

                    success = branch_api.delete_webhook(webhook_id=webhook_id_value)
                    if success:
                        return True
                except Exception as e:
                    logger.warning(
                        f"Failed to delete webhook {webhook_id} from branch {current_branch_id}: {e}"
                    )

        return False
