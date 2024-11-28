Service API
===========

The Service API enables you to manage and query gym services and classes. This API provides functionality for retrieving service information, including pricing, availability, and configuration details.

Models
------

.. module:: evo_client.models

.. autoclass:: ServicosResumoApiViewModel
   :members:
   :undoc-members:
   :show-inheritance:

   .. py:attribute:: id_service
      :type: int

      Unique identifier for the service

   .. py:attribute:: id_branch
      :type: int

      Branch ID where service is offered (for multi-location gyms)

   .. py:attribute:: name_service
      :type: str

      Name of the service

   .. py:attribute:: value
      :type: float

      Price of the service

   .. py:attribute:: allow_entries
      :type: bool

      Whether the service grants access to gym entries

   .. py:attribute:: experimental_class
      :type: bool

      Indicates if this is an experimental/trial service

   .. py:attribute:: max_amount_installments
      :type: int

      Maximum number of installments allowed for payment

   .. py:attribute:: url_sale
      :type: str

      URL for online sales of this service

   .. py:attribute:: inactive
      :type: bool

      Whether the service is currently inactive

   .. py:attribute:: online_sales_observations
      :type: str

      Additional notes for online sales

API Methods
----------

.. module:: evo_client.api

.. autoclass:: ServiceApi
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: get_services
      :noindex:

Usage Examples
-------------

Retrieving All Active Services
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ServiceApi
    from evo_client.exceptions import ApiException

    service_api = ServiceApi()

    try:
        # Get all active services
        services = service_api.get_services(
            active=True,
            take=50  # Maximum allowed records
        )
        
        for service in services:
            print(f"Service: {service.name_service}")
            print(f"Price: ${service.value:.2f}")
            if service.max_amount_installments > 1:
                print(f"Available in up to {service.max_amount_installments} installments")
            if service.experimental_class:
                print("(Trial Class)")
            print("---")
            
    except ApiException as e:
        if e.status == 400:
            print("Invalid query parameters")
        elif e.status == 403:
            print("Insufficient permissions to view services")
        else:
            print(f"API error: {e.status} - {e.reason}")

Searching for Specific Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        # Search for services by name
        yoga_services = service_api.get_services(
            name="yoga",
            branch_id=123,  # Specific branch
            active=True
        )
        
        if not yoga_services:
            print("No yoga services found at this branch")
        else:
            for service in yoga_services:
                print(f"Service: {service.name_service}")
                if service.allow_entries:
                    print("Includes gym access")
                if service.url_sale:
                    print(f"Book online: {service.url_sale}")
                print("---")
                
    except ApiException as e:
        if e.status == 404:
            print("Branch not found")
        else:
            print(f"API error: {e.status} - {e.reason}")

Error Handling
------------

The Service API uses standard HTTP status codes:

- 400: Invalid request parameters
- 401: Authentication failed
- 403: Insufficient permissions to access services
- 404: Service or branch not found
- 429: Too many requests
- 500: Internal server error

All errors are wrapped in :class:`~evo_client.exceptions.ApiException` with detailed error messages.

Pagination
---------

The API supports pagination through the following parameters:

- ``take``: Number of records to return (maximum 50)
- ``skip``: Number of records to skip

Example pagination:

.. code-block:: python

    # Get all services page by page
    page_size = 50
    current_page = 0
    
    while True:
        services = service_api.get_services(
            take=page_size,
            skip=current_page * page_size,
            active=True  # Only active services
        )
        
        if not services:
            break
            
        # Process services
        for service in services:
            print(f"Processing service: {service.name_service}")
            
        current_page += 1

Best Practices
------------

1. **Service Queries**:
   - Always specify `active=True` when looking for available services
   - Use the `branch_id` parameter in multi-location setups
   - Implement proper pagination for large result sets

2. **Error Handling**:
   - Handle service not found scenarios gracefully
   - Implement proper error handling for all API calls
   - Consider retry logic for rate limit errors

3. **Display and Formatting**:
   - Format prices appropriately for display
   - Check `experimental_class` flag before displaying to customers
   - Use `online_sales_observations` in customer-facing interfaces
