from typing import List, Dict, Optional
import asyncio
from loguru import logger

from ...models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from ...models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from ...api.webhook_api import WebhookApi
from ..data_fetchers import BaseDataFetcher
from ...utils.pagination_utils import paginated_api_call


class WebhookManagement(BaseDataFetcher):
    async def _delete_webhook_with_retry(
        self,
        webhook_api: WebhookApi,
        webhook_id: int,
        max_retries: int = 3,
        base_delay: float = 1.5,
    ) -> bool:
        """Delete webhook with retry logic."""
        for attempt in range(max_retries):
            try:
                response = webhook_api.delete_webhook(webhook_id, async_req=False)
                # If response is boolean, use it directly
                if isinstance(response, bool):
                    if response:
                        logger.debug(f"Successfully deleted webhook {webhook_id}")
                        return True
                    else:
                        logger.error(f"Failed to delete webhook {webhook_id}")
                        return False

                # Otherwise try to get success from response data
                success = getattr(response, "data", None)
                if success:
                    logger.debug(f"Successfully deleted webhook {webhook_id}")
                    return True

                logger.error(f"Failed to delete webhook {webhook_id}")

            except Exception as e:
                if "429" in str(e):  # Rate limit error
                    delay = base_delay * (2**attempt)  # Exponential backoff
                    logger.warning(
                        f"Rate limit hit, waiting {delay} seconds before retry"
                    )
                    await asyncio.sleep(delay)
                    continue
                logger.error(f"Error deleting webhook {webhook_id}: {str(e)}")

        # Wait between attempts
        return False


from ..data_fetchers.webhook_data_fetcher import WebhookDataFetcher
from ..data_fetchers import BranchApiClientManager
from ...models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from ...models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel


class WebhookManagementService:
    """Service for managing webhook subscriptions."""

    def __init__(self, client_manager: BranchApiClientManager):
        """Initialize the webhook management service.

        Args:
            client_manager: The client manager instance
        """
        self.client_manager = client_manager
        self.webhook_fetcher = WebhookDataFetcher(client_manager)

    def manage_webhooks(
        self,
        url_callback: str,
        branch_ids: Optional[List[int]] = None,
        event_types: Optional[List[str]] = None,
        headers: Optional[List[Dict[str, str]]] = None,
        filters: Optional[List[Dict[str, str]]] = None,
        unsubscribe: bool = False,
    ) -> bool:
        """Manage webhook subscriptions."""
        try:
            logger.info(f"Managing webhooks for URL: {url_callback}")
            logger.info(f"Operation: {'unsubscribe' if unsubscribe else 'subscribe'}")

            # Define all possible event types
            all_event_types = [
                "NewSale",
                "CreateMember",
                "AlterMember",
                "EndedSessionActivity",
                "ClearedDebt",
                "AlterReceivables",
                "Freeze",
                "RecurrentSale",
                "entries",
                "ActivityEnroll",
                "SalesItensUpdated",
                "CreateMembership",
                "AlterMembership",
                "CreateService",
                "AlterService",
                "CreateProduct",
                "AlterProduct",
            ]
            event_types = event_types or all_event_types
            logger.info(f"Using event types: {event_types}")

            # Convert headers and filters to view models
            webhook_headers = [
                W12UtilsWebhookHeaderViewModel(nome=h["nome"], valor=h["valor"])
                for h in (headers or [])
            ] or [
                W12UtilsWebhookHeaderViewModel(
                    nome="Content-Type", valor="application/json"
                )
            ]
            logger.debug(f"Using headers: {webhook_headers}")

            webhook_filters = [
                W12UtilsWebhookFilterViewModel(
                    filterType=f["filterType"], value=f["value"]
                )
                for f in (filters or [])
            ] or [W12UtilsWebhookFilterViewModel(filterType="All", value="*")]
            logger.debug(f"Using filters: {webhook_filters}")

            if not branch_ids:
                branch_ids = self.webhook_fetcher.get_available_branch_ids()

            # Handle unsubscribe
            if unsubscribe:
                logger.debug("Getting existing webhooks for unsubscribe")
                # Get webhooks for each branch
                for branch_id in branch_ids:
                    if branch_id in self.webhook_fetcher.get_available_branch_ids():
                        logger.debug(f"Getting webhooks for branch {branch_id}")
                        branch_webhook_api = WebhookApi(
                            self.webhook_fetcher.get_branch_api(branch_id)
                        )
                        existing_webhooks = paginated_api_call(
                            api_func=branch_webhook_api.get_webhooks,
                            branch_id=str(branch_id),
                            async_req=False,
                        )
                        logger.debug(
                            f"Found webhooks for branch {branch_id}: {existing_webhooks}"
                        )

                        for webhook in existing_webhooks:
                            webhook_id = webhook.get("idWebhook")
                            webhook_url = webhook.get("urlCallback")
                            webhook_event = webhook.get("tipoEvento")
                            webhook_branch = webhook.get("idFilial")

                            logger.debug(
                                f"Checking webhook: ID={webhook_id}, URL={webhook_url}, Event={webhook_event}, Branch={webhook_branch}"
                            )

                            if webhook_id and (
                                webhook_url == url_callback
                                and webhook_event in event_types
                                and str(webhook_branch) == branch_id
                            ):
                                success = await self._delete_webhook_with_retry(
                                    branch_webhook_api, webhook_id
                                )
                                if not success:
                                    continue  # Try next webhook

                return True

            # Handle subscribe
            # Create webhooks for each branch and event type
            for branch_id in branch_ids:
                logger.debug(f"Processing branch {branch_id}")
                # Get branch-specific API client
                if branch_id not in self.webhook_fetcher.get_available_branch_ids():
                    logger.warning(f"Branch {branch_id} not found, skipping")
                    continue

                client = self.webhook_fetcher.get_branch_api(branch_id)
                if client:
                    logger.debug(f"Using branch-specific client for branch {branch_id}")
                    logger.debug(
                        f"Branch {branch_id} username: {client.configuration.username}"
                    )
                    webhook_api = WebhookApi(client)
                else:
                    logger.error(f"No configuration for branch {branch_id}")
                    raise ValueError(f"No configuration for branch {branch_id}")

                if webhook_api:
                    for event_type in event_types:
                        logger.debug(
                            f"Creating webhook for branch {branch_id}, event {event_type}"
                        )
                        success = paginated_api_call(
                            api_func=webhook_api.create_webhook,
                            branch_id=str(branch_id),
                            event_type=event_type,
                            url_callback=url_callback,
                            headers=webhook_headers,
                            filters=(
                                webhook_filters if event_type == "NewSale" else None
                            ),
                            async_req=False,
                        )
                        if not success:
                            logger.error(
                                f"Failed to create webhook for branch {branch_id}, event {event_type}"
                            )
                            return False
                        logger.debug(
                            f"Successfully created webhook for branch {branch_id}, event {event_type}"
                        )

            return True

        except Exception as e:
            logger.error(f"Error managing webhooks: {str(e)}")
            logger.exception("Full traceback:")
            return False
