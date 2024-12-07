from __future__ import absolute_import

from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload
from loguru import logger

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
    ) -> Union[bool, AsyncResult[bool]]:
        """
        Remove a specific webhook by ID.

        Args:
            webhook_id: ID of the webhook to delete
            async_req: Execute request asynchronously
        """
        try:
            logger.debug(f"Deleting webhook {webhook_id}")
            params = {"IdWebhook": webhook_id}

            response = self.api_client.call_api(
                resource_path=self.base_path,
                method="DELETE",
                query_params=params,
                auth_settings=["Basic"],
                async_req=async_req,
                _return_http_data_only=True,  # Get just the data
                _preload_content=True  # Parse the response
            )

            # Handle async response
            if isinstance(response, AsyncResult):
                logger.debug("Got AsyncResult response")
                return response

            # Log response
            logger.debug(f"Got response: {response}")
            logger.debug(f"Response type: {type(response)}")

            # If response is boolean, return it directly
            if isinstance(response, bool):
                return response

            # If response has status code, use it
            status = getattr(response, 'status', None)
            if status is not None:
                return 200 <= status < 300

            # If we got this far, assume success
            return True

        except Exception as e:
            logger.error(f"Error deleting webhook: {str(e)}")
            logger.exception("Full traceback:")
            return False

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
        try:
            logger.debug("Getting webhooks")
            
            # Extract branch ID from configuration if available
            branch_id = None
            if hasattr(self.api_client, 'configuration'):
                if hasattr(self.api_client.configuration, 'username'):
                    # Try to extract branch ID from username if it's in the format branch_name:branch_id
                    username = self.api_client.configuration.username
                    if ':' in username:
                        _, branch_id = username.split(':', 1)
            
            # Add branch ID to query parameters if available
            query_params = {}
            if branch_id:
                query_params['idFilial'] = branch_id
                logger.debug(f"Using branch ID in query params: {branch_id}")
            
            response = self.api_client.call_api(
                resource_path=self.base_path,
                method="GET",
                query_params=query_params,
                auth_settings=["Basic"],
                async_req=async_req,
                _return_http_data_only=True,  # Get just the data
                _preload_content=True  # Parse the response
            )

            # Handle async response
            if isinstance(response, AsyncResult):
                logger.debug("Got AsyncResult response")
                return response

            # Log raw response details
            logger.debug(f"Got response: {response}")
            logger.debug(f"Response type: {type(response)}")

            # If we got a list directly, return it
            if isinstance(response, list):
                logger.debug("Got list response directly")
                return response

            # Otherwise try to get data from response
            try:
                if hasattr(response, 'data'):
                    raw_data = response.data
                    logger.debug(f"Raw response data: {raw_data}")
                    if isinstance(raw_data, bytes):
                        try:
                            decoded = raw_data.decode('utf-8', errors='replace')
                            logger.debug(f"Decoded response: {decoded}")
                            try:
                                import json
                                data = json.loads(decoded)
                                logger.debug(f"Parsed JSON data: {data}")
                                return data
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
                            return data
                        except json.JSONDecodeError as e:
                            logger.warning(f"Response is not valid JSON: {e}")
                            return []
                    return raw_data
                return response
            except Exception as e:
                logger.warning(f"Failed to get response data: {e}")
                if isinstance(response, list):
                    return response
                return []

        except Exception as e:
            logger.error(f"Error getting webhooks: {str(e)}")
            logger.exception("Full traceback:")
            return []

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
    ) -> Union[bool, AsyncResult[bool]]:
        """Add new webhook configuration."""
        try:
            webhook_data = W12UtilsWebhookViewModel(
                idBranch=branch_id,
                eventType=event_type,
                urlCallback=url_callback,
                headers=headers or [W12UtilsWebhookHeaderViewModel(nome="Content-Type", valor="application/json")],
                filters=filters or [W12UtilsWebhookFilterViewModel(filterType="All", value="*")]
            ).model_dump(by_alias=True, exclude_none=True)

            logger.debug(f"Creating webhook with data: {webhook_data}")

            # Make the API call
            response = self.api_client.call_api(
                resource_path=self.base_path,
                method="POST",
                body=webhook_data,
                auth_settings=["Basic"],
                _return_http_data_only=True,
                _preload_content=True,
                async_req=async_req
            )

            # Handle async response
            if isinstance(response, AsyncResult):
                logger.debug("Got AsyncResult response")
                return response

            # Log response
            logger.debug(f"Got response: {response}")
            logger.debug(f"Response type: {type(response)}")

            # If response is boolean, return it directly
            if isinstance(response, bool):
                return response

            # If response has status code, use it
            status = getattr(response, 'status', None)
            if status is not None:
                return 200 <= status < 300

            # If we got this far and have a response, assume success
            return response is not None

        except Exception as e:
            logger.error(f"Error creating webhook: {str(e)}")
            logger.exception("Full traceback:")
            return False
