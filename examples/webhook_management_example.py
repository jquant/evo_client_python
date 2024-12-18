from typing import cast, List
from multiprocessing.pool import AsyncResult

from evo_client.api.gym_api import GymApi
from evo_client.models.w12_utils_webhook_view_model import W12UtilsWebhookViewModel

# Initialize the API client
gym_api = GymApi()

# Example 1: Subscribe to all events
print("\n=== Subscribing to All Events ===")
try:
    result = gym_api.manage_webhooks(
        url_callback="https://example.com/webhook",
    )
    print(f"Subscription successful: {result}")
except Exception as e:
    print(f"Error subscribing to webhooks: {str(e)}")

# Example 2: Subscribe to specific events with custom headers
print("\n=== Subscribing to Specific Events with Headers ===")
try:
    result = gym_api.manage_webhooks(
        url_callback="https://example.com/webhook/sales",
        event_types=["NewSale", "CreateMember"],
        headers=[
            {"nome": "X-API-Key", "valor": "your-api-key"},
            {"nome": "Content-Type", "valor": "application/json"}
        ]
    )
    print(f"Subscription successful: {result}")
except Exception as e:
    print(f"Error subscribing to webhooks: {str(e)}")

# Example 3: Subscribe with filters for NewSale events
print("\n=== Subscribing with Sale Filters ===")
try:
    result = gym_api.manage_webhooks(
        url_callback="https://example.com/webhook/filtered-sales",
        event_types=["NewSale"],
        filters=[
            {"filterType": "SaleItemDescription", "value": "Premium Membership"},
            {"filterType": "SaleItemDescription", "value": "Personal Training"}
        ]
    )
    print(f"Subscription successful: {result}")
except Exception as e:
    print(f"Error subscribing to webhooks: {str(e)}")

# Example 4: Multi-branch webhook management
print("\n=== Managing Webhooks for Multiple Branches ===")
try:
    result = gym_api.manage_webhooks(
        url_callback="https://example.com/webhook/multi-branch",
        branch_ids=["1", "2", "3"],
        event_types=["NewSale", "CreateMember", "AlterMember"],
        headers=[{"nome": "X-Branch-ID", "valor": "dynamic"}]
    )
    
    if isinstance(result, AsyncResult):
        success = cast(bool, result.get())
        print(f"Multi-branch subscription successful: {success}")
except Exception as e:
    print(f"Error managing multi-branch webhooks: {str(e)}")

# Example 5: Unsubscribe from webhooks
print("\n=== Unsubscribing from Webhooks ===")
try:
    result = gym_api.manage_webhooks(
        url_callback="https://example.com/webhook",
        event_types=["NewSale", "CreateMember"],
        unsubscribe=True
    )
    print(f"Unsubscription successful: {result}")
except Exception as e:
    print(f"Error unsubscribing from webhooks: {str(e)}")

# Example 6: List existing webhooks
print("\n=== Listing Existing Webhooks ===")
try:
    webhooks = gym_api.webhook_api.get_webhooks()
    if isinstance(webhooks, AsyncResult):
        webhooks = cast(List[W12UtilsWebhookViewModel], webhooks.get())
    
    for webhook in webhooks:
        print(f"Branch ID: {webhook.id_branch}")
        print(f"Event Type: {webhook.event_type}")
        print(f"URL: {webhook.url_callback}")
        if webhook.headers:
            print("Headers:")
            for header in webhook.headers:
                print(f"  {header.nome}: {header.valor}")
        if webhook.filters:
            print("Filters:")
            for filter in webhook.filters:
                print(f"  {filter.filter_type}: {filter.value}")
        print("---")
except Exception as e:
    print(f"Error listing webhooks: {str(e)}") 