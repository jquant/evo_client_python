Partnership API
===============

The Partnership API provides functionality for managing partnerships and their associated discounts. This API enables you to retrieve and filter partnerships based on various criteria such as status, description, and creation date.

Key Features
------------

* Retrieve partnerships with optional filtering
* View partnership details including discount information
* Check partnership status and validity
* Access associated company information

Models
-------

.. autoclass:: evo_client.models.convenios_api_view_model.ConveniosApiViewModel
   :members:
   :undoc-members:

   **Fields**:
       - **id_partnership** (Optional[int]): Unique identifier for the partnership
       - **description** (Optional[str]): Name or description of the partnership
       - **is_blocked_flag** (Optional[bool]): Whether the partnership is currently blocked
       - **is_inactive_flag** (Optional[bool]): Whether the partnership is inactive
       - **company** (Optional[EmpresasConveniosApiViewModel]): Associated company details
       - **is_recurring_discount_flag** (Optional[bool]): Whether the discount applies to recurring payments
       - **discount** (Optional[float]): Discount amount
       - **discount_type** (Optional[float]): Type of discount (percentage or fixed value)
       - **advanced_discount** (Optional[int]): Number of days in advance for discount application

.. autoclass:: evo_client.models.empresas_convenios_api_view_model.EmpresasConveniosApiViewModel
   :members:
   :undoc-members:

Basic Usage
-----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import PartnershipApi
    from datetime import datetime

    # Initialize the API client
    client = EvoClient(username="mygym.example.com", password="your-secret-key")
    api = PartnershipApi(client)

    try:
        # Get active partnerships
        partnerships = api.get_partnerships(status=1)
        for partnership in partnerships:
            print(f"Partnership: {partnership.description}")
            print(f"Discount: {partnership.discount}%")
            if partnership.company:
                print(f"Company: {partnership.company.name}")
    except ApiException as e:
        if e.status == 401:
            print("Authentication failed. Check your credentials.")
        elif e.status == 403:
            print("Insufficient permissions to access partnerships")
        else:
            print(f"Error retrieving partnerships: {e}")

API Reference
-------------

.. autoclass:: evo_client.api.partnership_api.PartnershipApi
   :members:
   :undoc-members:
   :special-members: __init__

Methods
-------

get_partnerships
~~~~~~~~~~~~~~~~

Retrieve partnerships with optional filters.

Parameters:
    - **status** (Optional[int]): Filter by partnership status
        - 0: Both active and inactive
        - 1: Active only
        - 2: Inactive only
    - **description** (Optional[str]): Filter by partnership name/description
        - Case-insensitive partial match
    - **dt_created** (Optional[datetime]): Filter by creation date
    - **async_req** (bool): Execute request asynchronously (default: False)

Returns:
    List[ConveniosApiViewModel]: List of partnerships matching the filter criteria, each containing:
        - Partnership ID and description
        - Status flags (blocked, inactive)
        - Discount information
        - Associated company details

Raises:
    - **ApiException**: When the API request fails
        - 401: Authentication failed
        - 403: Insufficient permissions
        - 500: Server error
    - **ValidationError**: When parameters are invalid

Examples
--------

Retrieve Active Partnerships
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Retrieve active partnerships
    partnerships = api.get_partnerships(status=1)
    for partnership in partnerships:
        print(f"Partnership: {partnership.description}")
        if partnership.discount:
            print(f"Discount: {partnership.discount}%")
            print(f"Recurring: {partnership.is_recurring_discount_flag}")

Search by Description
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Search partnerships by description
    partnerships = api.get_partnerships(description="Corporate")
    for partnership in partnerships:
        print(f"Found: {partnership.description}")
        if not partnership.is_inactive_flag:
            print("Status: Active")

Error Handling
--------------

The API uses standard HTTP status codes and may raise exceptions for invalid parameters or API errors:

- **401 Unauthorized**: Invalid or missing authentication credentials
- **403 Forbidden**: Insufficient permissions to access partnerships
- **404 Not Found**: Requested partnership does not exist
- **500 Internal Server Error**: Server-side error processing the request

See Also
--------

* :doc:`members` - For managing member-related operations
* :doc:`membership` - For managing general membership operations
