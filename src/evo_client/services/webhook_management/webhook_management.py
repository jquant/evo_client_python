    async def _delete_webhook_with_retry(self, webhook_api: WebhookApi, webhook_id: int, max_retries: int = 3, base_delay: float = 1.5) -> bool:
        """Delete webhook with retry logic."""
        for attempt in range(max_retries):
            try:
                response = webhook_api.delete_webhook(webhook_id, async_req=False)
                # If response is boolean, use it directly
                if isinstance(response, bool):
                    if response:
                        logger.debug(f"Successfully deleted webhook {webhook_id}")
                        await self._handle_rate_limit()
                        return True
                    else:
                        logger.error(f"Failed to delete webhook {webhook_id}")
                        return False
                
                # Otherwise try to get success from response data
                success = getattr(response, 'data', None)
                if success:
                    logger.debug(f"Successfully deleted webhook {webhook_id}")
                    await self._handle_rate_limit()
                    return True
                
                logger.error(f"Failed to delete webhook {webhook_id}")
                
            except Exception as e:
                if "429" in str(e):  # Rate limit error
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit, waiting {delay} seconds before retry")
                    await asyncio.sleep(delay)
                    continue
                logger.error(f"Error deleting webhook {webhook_id}: {str(e)}")
            
            await self._handle_rate_limit()  # Wait between attempts
        
        return False

    async def manage_webhooks(
        self,
        url_callback: str,
        branch_ids: Optional[List[str]] = None,
        event_types: Optional[List[str]] = None,
        headers: Optional[List[Dict[str, str]]] = None,
        filters: Optional[List[Dict[str, str]]] = None,
        unsubscribe: bool = False,
        async_req: bool = False
    ) -> Union[bool, TypedAsyncResult[bool]]:
        """Manage webhook subscriptions."""
        try:
            logger.debug(f"Managing webhooks for URL: {url_callback}")
            logger.debug(f"Branch IDs: {branch_ids}")
            logger.debug(f"Event types: {event_types}")
            logger.debug(f"Operation: {'unsubscribe' if unsubscribe else 'subscribe'}")

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
                "AlterProduct"
            ]
            event_types = event_types or all_event_types
            logger.debug(f"Using event types: {event_types}")

            # Convert headers and filters to view models
            webhook_headers = [
                W12UtilsWebhookHeaderViewModel(nome=h["nome"], valor=h["valor"])
                for h in (headers or [])
            ] or [W12UtilsWebhookHeaderViewModel(nome="Content-Type", valor="application/json")]
            logger.debug(f"Using headers: {webhook_headers}")

            webhook_filters = [
                W12UtilsWebhookFilterViewModel(filterType=f["filterType"], value=f["value"])
                for f in (filters or [])
            ] or [W12UtilsWebhookFilterViewModel(filterType="All", value="*")]
            logger.debug(f"Using filters: {webhook_filters}")

            # Handle unsubscribe
            if unsubscribe:
                logger.debug("Getting existing webhooks for unsubscribe")
                if branch_ids:
                    # Get webhooks for each branch
                    for branch_id in branch_ids:
                        if branch_id in self.branch_api_clients:
                            logger.debug(f"Getting webhooks for branch {branch_id}")
                            branch_webhook_api = WebhookApi(self.branch_api_clients[branch_id])
                            existing_webhooks = await self._make_api_call(
                                branch_webhook_api.get_webhooks,
                                "Error getting webhooks",
                                async_req=False
                            )
                            logger.debug(f"Found webhooks for branch {branch_id}: {existing_webhooks}")
                            await self._handle_rate_limit()
                            
                            for webhook in existing_webhooks:
                                webhook_id = webhook.get('idWebhook')
                                webhook_url = webhook.get('urlCallback')
                                webhook_event = webhook.get('tipoEvento')
                                webhook_branch = webhook.get('idFilial')
                                
                                logger.debug(f"Checking webhook: ID={webhook_id}, URL={webhook_url}, Event={webhook_event}, Branch={webhook_branch}")
                                
                                if webhook_id and (
                                    webhook_url == url_callback and 
                                    webhook_event in event_types and
                                    str(webhook_branch) == branch_id
                                ):
                                    success = await self._delete_webhook_with_retry(branch_webhook_api, webhook_id)
                                    if not success:
                                        continue  # Try next webhook
                else:
                    # Get webhooks using default client
                    if self.default_api_client:
                        existing_webhooks = await self._make_api_call(
                            self.webhook_api.get_webhooks,
                            "Error getting webhooks",
                            async_req=False
                        )
                        logger.debug(f"Found webhooks: {existing_webhooks}")
                        await self._handle_rate_limit()
                        
                        for webhook in existing_webhooks:
                            webhook_id = webhook.get('idWebhook')
                            webhook_url = webhook.get('urlCallback')
                            webhook_event = webhook.get('tipoEvento')
                            
                            logger.debug(f"Checking webhook: ID={webhook_id}, URL={webhook_url}, Event={webhook_event}")
                            
                            if webhook_id and webhook_url == url_callback and webhook_event in event_types:
                                success = await self._delete_webhook_with_retry(self.webhook_api, webhook_id)
                                if not success:
                                    continue  # Try next webhook
                return True

            # Handle subscribe
            if branch_ids:
                # Create webhooks for each branch and event type
                for branch_id in branch_ids:
                    logger.debug(f"Processing branch {branch_id}")
                    # Get branch-specific API client
                    if branch_id in self.branch_api_clients and self.branch_api_clients[branch_id]:
                        client = self.branch_api_clients[branch_id]
                        if client.configuration:
                            logger.debug(f"Using branch-specific client for branch {branch_id}")
                            logger.debug(f"Branch {branch_id} username: {client.configuration.username}")
                            webhook_api = WebhookApi(client)
                        else:
                            logger.warning(f"No configuration for branch {branch_id}, using default client")
                            webhook_api = WebhookApi(self.default_api_client) if self.default_api_client else None
                    else:
                        logger.warning(f"No credentials found for branch {branch_id}, using default client")
                        webhook_api = WebhookApi(self.default_api_client) if self.default_api_client else None

                    if webhook_api:
                        for event_type in event_types:
                            logger.debug(f"Creating webhook for branch {branch_id}, event {event_type}")
                            try:
                                success = await self._make_api_call(
                                    webhook_api.create_webhook,
                                    "Error creating webhook",
                                    event_type=event_type,
                                    url_callback=url_callback,
                                    branch_id=int(branch_id),
                                    headers=webhook_headers,
                                    filters=webhook_filters if event_type == "NewSale" else None,
                                    async_req=False
                                )
                                if not success:
                                    logger.error(f"Failed to create webhook for branch {branch_id}, event {event_type}")
                                    return False
                                logger.debug(f"Successfully created webhook for branch {branch_id}, event {event_type}")
                                await self._handle_rate_limit()
                            except Exception as e:
                                if "429" in str(e):  # Rate limit error
                                    logger.warning("Rate limit hit, retrying with longer delay")
                                    await self._handle_rate_limit(3)  # Longer delay on rate limit
                                    continue
                                logger.error(f"Error creating webhook: {str(e)}")
                                return False
            else:
                # Create webhooks for each event type without branch ID
                if self.default_api_client:
                    logger.debug("Using default client for webhook creation")
                    if self.default_api_client.configuration:
                        logger.debug(f"Default client username: {self.default_api_client.configuration.username}")
                    
                    for event_type in event_types:
                        logger.debug(f"Creating webhook for event {event_type}")
                        try:
                            success = await self._make_api_call(
                                self.webhook_api.create_webhook,
                                "Error creating webhook",
                                event_type=event_type,
                                url_callback=url_callback,
                                headers=webhook_headers,
                                filters=webhook_filters if event_type == "NewSale" else None,
                                async_req=False
                            )
                            if not success:
                                logger.error(f"Failed to create webhook for event {event_type}")
                                return False
                            logger.debug(f"Successfully created webhook for event {event_type}")
                            await self._handle_rate_limit()
                        except Exception as e:
                            if "429" in str(e):  # Rate limit error
                                logger.warning("Rate limit hit, retrying with longer delay")
                                await self._handle_rate_limit(3)  # Longer delay on rate limit
                                continue
                            logger.error(f"Error creating webhook: {str(e)}")
                            return False

            return True

        except Exception as e:
            logger.error(f"Error managing webhooks: {str(e)}")
            logger.exception("Full traceback:")
            return False