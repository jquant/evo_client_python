.. _webhooks_api:

Webhooks API
===========

Overview
--------

The Webhooks API enables real-time event notifications for your gym management system. It allows you to:

- Create webhook subscriptions for specific events
- Manage and monitor existing webhooks
- Receive instant notifications about important system events

Key Features
-----------

- **Event-Based Notifications**: Get real-time updates for various system events
- **Flexible Configuration**: Customize webhooks with headers and filters
- **Branch-Specific Monitoring**: Set up webhooks for specific branches in multi-location setups
- **Secure Delivery**: Uses Basic Authentication for all webhook operations

Basic Usage
----------

Here's a basic example of creating and managing webhooks:

.. code-block:: python

    from evo_client.api import WebhookApi
    from evo_client.core.api_client import ApiClient
    from evo_client.models import (
        W12UtilsWebhookViewModel,
        W12UtilsWebhookHeaderViewModel,
        W12UtilsWebhookFilterViewModel
    )
    from evo_client.exceptions import ApiException

    # Initialize with authentication
    api_client = ApiClient()
    api_client.configuration.username = "your-gym-dns"
    api_client.configuration.password = "your-secret-key"
    webhook_api = WebhookApi(api_client)

    try:
        # Create a webhook for new sales
        webhook_api.create_webhook(
            event_type="NewSale",
            url_callback="https://your-endpoint.com/webhook",
            headers=[
                W12UtilsWebhookHeaderViewModel(
                    key="X-Custom-Header",
                    value="custom-value"
                )
            ],
            filters=[
                W12UtilsWebhookFilterViewModel(
                    filter_type="SaleItemDescription",
                    value="Premium Membership"
                )
            ]
        )

        # List all webhooks
        webhooks = webhook_api.get_webhooks()
        for webhook in webhooks:
            print(f"ID: {webhook['id']}")
            print(f"Event Type: {webhook['eventType']}")
            print(f"URL: {webhook['urlCallback']}")
            print("---")

    except ValueError as e:
        print(f"Invalid webhook data: {e}")
    except ApiException as e:
        print(f"API error: {e.status} - {e.reason}")

API Reference
------------

.. autoclass:: evo_client.api.webhook_api.WebhookApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

.. autoclass:: evo_client.models.w12_utils_webhook_view_model.W12UtilsWebhookViewModel
   :members:

.. autoclass:: evo_client.models.w12_utils_webhook_header_view_model.W12UtilsWebhookHeaderViewModel
   :members:

.. autoclass:: evo_client.models.w12_utils_webhook_filter_view_model.W12UtilsWebhookFilterViewModel
   :members:

Event Types Reference
------------------

Member Events
~~~~~~~~~~~
- ``CreateMember``: Triggered when a new member is created
- ``AlterMember``: Triggered when member information is updated

Activity Events
~~~~~~~~~~~~~
- ``EndedSessionActivity``: Triggered when an activity session is completed
- ``ActivityEnroll``: Triggered when a member enrolls in an activity

Payment Events
~~~~~~~~~~~~
- ``NewSale``: Triggered when a new sale is created (supports filters)
- ``ClearedDebt``: Triggered when a debt is cleared
- ``AlterReceivables``: Triggered when receivables are modified
- ``RecurrentSale``: Triggered when a recurring sale is processed
- ``SalesItensUpdated``: Triggered when sale items are updated

Membership Events
~~~~~~~~~~~~~~
- ``CreateMembership``: Triggered when a new membership is created
- ``AlterMembership``: Triggered when a membership is modified
- ``Freeze``: Triggered when a membership is frozen

Product/Service Events
~~~~~~~~~~~~~~~~~~~
- ``CreateService``: Triggered when a new service is created
- ``AlterService``: Triggered when a service is modified
- ``CreateProduct``: Triggered when a new product is created
- ``AlterProduct``: Triggered when a product is modified

Other Events
~~~~~~~~~~
- ``entries``: Triggered for entry tracking events

Error Handling
------------

The API may raise these exceptions:

ValueError
~~~~~~~~~
Raised when invalid data is provided:

- Invalid event type
- Invalid URL format
- Invalid filter configuration

ApiException
~~~~~~~~~~
Raised when the API request fails:

- ``401``: Authentication failed
- ``403``: Permission denied
- ``404``: Webhook not found
- ``500``: Server error

Example error handling:

.. code-block:: python

    try:
        webhook_api.create_webhook(
            event_type="InvalidEvent",  # This will raise ValueError
            url_callback="https://endpoint.com"
        )
    except ValueError as e:
        print(f"Invalid data: {e}")
    except ApiException as e:
        if e.status == 401:
            print("Authentication failed")
        elif e.status == 403:
            print("Permission denied")
        else:
            print(f"API error: {e.status} - {e.reason}")

See Also
--------

- :ref:`sales_api`: For more details about sales events
- :ref:`members_api`: For member-related events
- :ref:`activities_api`: For activity-related events
