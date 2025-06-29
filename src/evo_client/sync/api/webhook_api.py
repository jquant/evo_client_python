"""Clean synchronous Webhook API."""

from typing import Any, List, Optional

from loguru import logger

from ...models.common_models import WebhookResponse
from ...models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from ...models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from ...models.w12_utils_webhook_view_model import W12UtilsWebhookViewModel
from .base import SyncBaseApi


class SyncWebhookApi(SyncBaseApi):
    """Clean synchronous Webhook API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/webhook"

    def delete_webhook(self, webhook_id: int) -> bool:
        """
        Remove a specific webhook by ID.

        Args:
            webhook_id: ID of the webhook to delete

        Returns:
            True if webhook was successfully deleted, False otherwise

        Example:
            >>> with SyncWebhookApi() as api:
            ...     success = api.delete_webhook(webhook_id=123)
            ...     if success:
            ...         print("Webhook deleted successfully")
            ...     else:
            ...         print("Failed to delete webhook")
        """
        try:
            logger.debug(f"Deleting webhook {webhook_id}")

            # Pass webhook ID as a string in query parameters
            params = {"IdWebhook": str(webhook_id)}

            response: Any = self.api_client.call_api(
                resource_path=self.base_path,
                method="DELETE",
                query_params=params,
                auth_settings=["Basic"],
                _return_http_data_only=True,  # Get just the data
                _preload_content=True,  # Parse the response
            )

            # Log response
            logger.debug(f"Got response: {response}")
            logger.debug(f"Response type: {type(response)}")

            # If response is boolean, return it directly
            if isinstance(response, bool):
                return response

            # If response has status code, use it
            status = getattr(response, "status", None)
            if status is not None:
                return 200 <= status < 300

            # If we got this far, assume success
            return True

        except Exception as e:
            logger.error(f"Error deleting webhook: {str(e)}")
            logger.exception("Full traceback:")
            return False

    def get_webhooks(self) -> List[WebhookResponse]:
        """
        List all webhooks created.

        Returns:
            List of webhook configurations including:
            - Webhook IDs and event types
            - Callback URLs and headers
            - Filter configurations
            - Branch assignments

        Example:
            >>> with SyncWebhookApi() as api:
            ...     webhooks = api.get_webhooks()
            ...     for webhook in webhooks:
            ...         print(f"Webhook: {webhook.event_type} -> {webhook.url_callback}")
        """
        try:
            logger.debug("Getting webhooks")

            # Extract branch ID from configuration if available
            branch_id = None
            if hasattr(self.api_client, "configuration"):
                if hasattr(self.api_client.configuration, "username"):
                    # Try to extract branch ID from username if it's in the format branch_name:branch_id
                    username = self.api_client.configuration.username
                    if ":" in username:
                        _, branch_id = username.split(":", 1)

            # Add branch ID to query parameters if available
            query_params = {}
            if branch_id:
                query_params["idFilial"] = branch_id
                logger.debug(f"Using branch ID in query params: {branch_id}")

            response: Any = self.api_client.call_api(
                resource_path=self.base_path,
                method="GET",
                query_params=query_params,
                auth_settings=["Basic"],
                _return_http_data_only=True,  # Get just the data
                _preload_content=True,  # Parse the response
            )

            # Log raw response details
            logger.debug(f"Got response: {response}")
            logger.debug(f"Response type: {type(response)}")

            # If we got a list directly, return it
            if isinstance(response, list):
                logger.debug("Got list response directly")
                return [WebhookResponse.model_validate(webhook) for webhook in response]

            # Otherwise try to get data from response
            try:
                if hasattr(response, "data"):
                    raw_data = response.data
                    logger.debug(f"Raw response data: {raw_data}")
                    if isinstance(raw_data, bytes):
                        try:
                            decoded = raw_data.decode("utf-8", errors="replace")
                            logger.debug(f"Decoded response: {decoded}")
                            try:
                                import json

                                data = json.loads(decoded)
                                logger.debug(f"Parsed JSON data: {data}")
                                if isinstance(data, list):
                                    return [
                                        WebhookResponse.model_validate(webhook)
                                        for webhook in data
                                    ]
                                else:
                                    return []
                            except json.JSONDecodeError as e:
                                logger.warning(f"Response is not valid JSON: {e}")
                                return []
                        except Exception as e:
                            logger.warning(f"Failed to decode response: {e}")
                            return []
                    elif isinstance(raw_data, str):
                        try:
                            import json

                            data = json.loads(raw_data)
                            logger.debug(f"Parsed JSON data: {data}")
                            if isinstance(data, list):
                                return [
                                    WebhookResponse.model_validate(webhook)
                                    for webhook in data
                                ]
                            else:
                                return []
                        except json.JSONDecodeError as e:
                            logger.warning(f"Response is not valid JSON: {e}")
                            return []
                    if isinstance(raw_data, list):
                        return [
                            WebhookResponse.model_validate(webhook)
                            for webhook in raw_data
                        ]
                    else:
                        return []
                if isinstance(response, list):
                    return [
                        WebhookResponse.model_validate(webhook) for webhook in response
                    ]
                else:
                    return []
            except Exception as e:
                logger.warning(f"Failed to get response data: {e}")
                if isinstance(response, list):
                    return [
                        WebhookResponse.model_validate(webhook) for webhook in response
                    ]
                return []

        except Exception as e:
            logger.error(f"Error getting webhooks: {str(e)}")
            logger.exception("Full traceback:")
            return []

    def create_webhook(
        self,
        event_type: str,
        url_callback: str,
        branch_id: Optional[int] = None,
        headers: Optional[List[W12UtilsWebhookHeaderViewModel]] = None,
        filters: Optional[List[W12UtilsWebhookFilterViewModel]] = None,
    ) -> bool:
        """
        Add new webhook configuration.

        Args:
            event_type: Type of event to listen for (e.g., 'member.created', 'payment.completed')
            url_callback: URL to receive webhook notifications
            branch_id: Branch ID for webhook scope (optional)
            headers: Custom headers to include in webhook requests
            filters: Filters to apply to webhook events

        Returns:
            True if webhook was successfully created, False otherwise

        Example:
            >>> with SyncWebhookApi() as api:
            ...     success = api.create_webhook(
            ...         event_type="member.created",
            ...         url_callback="https://mysite.com/webhooks/member",
            ...         branch_id=1
            ...     )
            ...     if success:
            ...         print("Webhook created successfully")
        """
        try:
            webhook_data = W12UtilsWebhookViewModel(
                IdBranch=branch_id or None,
                eventType=event_type,
                urlCallback=url_callback,
                headers=headers or None,
                filters=filters or None,
            ).model_dump(by_alias=True, exclude_none=True)

            logger.debug(f"Creating webhook with data: {webhook_data}")

            # Make the API call
            response: Any = self.api_client.call_api(
                resource_path=self.base_path,
                method="POST",
                body=webhook_data,
                auth_settings=["Basic"],
                _return_http_data_only=True,
                _preload_content=True,
            )

            # Log response
            logger.debug(f"Got response: {response}")
            logger.debug(f"Response type: {type(response)}")

            # If response is boolean, return it directly
            if isinstance(response, bool):
                return response

            # If response has status code, use it
            status = getattr(response, "status", None)
            if status is not None:
                return 200 <= status < 300

            # If we got this far and have a response, assume success
            return response is not None

        except Exception as e:
            logger.error(f"Error creating webhook: {str(e)}")
            logger.exception("Full traceback:")
            return False
