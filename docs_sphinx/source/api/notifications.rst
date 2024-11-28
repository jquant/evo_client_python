Notifications
============

The Notifications API allows you to manage member notifications in the EVO system.

.. module:: evo_client.api.notifications_api

NotificationsApi
---------------

.. autoclass:: NotificationsApi
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

.. module:: evo_client.models.notification_api_view_model

NotificationApiViewModel
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NotificationApiViewModel
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
------------

Here's an example of how to create a notification for a member:

.. code-block:: python

    from evo_client.api import NotificationsApi
    from evo_client.models import NotificationApiViewModel

    # Initialize the API client
    notifications_api = NotificationsApi()

    # Create a notification
    notification = NotificationApiViewModel(
        id_member=123,  # Member ID to send notification to
        notification_message="Welcome to our gym!"  # Message content
    )

    # Send the notification
    notifications_api.create_notification(notification)

    # For async operation
    async_result = notifications_api.create_notification(notification, async_req=True)
    # ... do other work ...
    # Wait for the result if needed
    async_result.get()

Authentication
-------------

This API requires Basic Authentication using your gym's DNS as the username and Secret Key as the password.
