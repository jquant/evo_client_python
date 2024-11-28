Sales API
=========

The Sales API provides comprehensive functionality for managing sales operations in your gym or fitness center. 
This API allows you to create new sales, retrieve sale information, manage sale items, and track sales by session.

Key Features
-----------

* Create and manage sales transactions with various payment methods
* Retrieve detailed sale information with flexible filtering options
* Track sales by member, employee, branch, or session
* Manage membership and pass sales
* Handle corporate partnerships and personal training sales
* Support for sale recurrency and migration
* Comprehensive receivables tracking
* Support for both synchronous and asynchronous operations
* Advanced error handling and validation

Getting Started
-------------

The Sales API provides a straightforward interface for managing sales operations. Here's a comprehensive example demonstrating common use cases:

.. code-block:: python

    from evo_client.api import SalesApi
    from evo_client.models import NewSaleViewModel, SaleFilterParams
    from datetime import datetime, timedelta
    
    # Initialize the API
    sales_api = SalesApi()
    
    # Example 1: Create a new membership sale
    new_sale = NewSaleViewModel(
        id_branch=123,
        id_member=456,
        service_value=99.90,
        type_payment="1",  # Credit Card
        total_installments=3,
        sale_date=datetime.now(),
        observations="Annual membership"
    )
    try:
        created_sale = sales_api.create_sale(new_sale)
        print(f"Sale created with ID: {created_sale.id}")
    except ValueError as e:
        print(f"Invalid sale data: {str(e)}")
    except Exception as e:
        print(f"Error creating sale: {str(e)}")
    
    # Example 2: Retrieve sales with filtering
    try:
        # Get sales for last 30 days
        start_date = datetime.now() - timedelta(days=30)
        sales = sales_api.get_sales(
            member_id=456,
            show_receivables=True,
            start_date=start_date,
            payment_type="1"  # Only credit card sales
        )
        
        # Process sales data
        for sale in sales:
            print(f"Sale ID: {sale.id}, Value: {sale.service_value}")
            if sale.receivables:
                for receivable in sale.receivables:
                    print(f"  Installment: {receivable.installment_number}")
    except ValueError as e:
        print(f"Invalid filter parameters: {str(e)}")

API Reference
------------

.. autoclass:: evo_client.api.sales_api.SalesApi
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
   :exclude-members: get_sale_by_id, create_sale, get_sales_items, get_sale_by_session_id

Core Operations
-------------

Creating Sales
~~~~~~~~~~~~

.. automethod:: evo_client.api.sales_api.SalesApi.create_sale

**Payment Types**

The following payment methods are supported:

.. list-table::
   :header-rows: 1
   :widths: 10 30 60

   * - Code
     - Type
     - Description
   * - ``1``
     - Credit Card
     - Standard credit card processing with installment support
   * - ``2``
     - Boleto
     - Brazilian bank slip payment method
   * - ``3``
     - Sale Credits
     - Internal credit system
   * - ``4``
     - Transfer
     - Bank transfer payments
   * - ``5``
     - ValorZerado
     - Zero-value transactions
   * - ``6``
     - LinkCheckout
     - Online payment link
   * - ``7``
     - Pix
     - Brazilian instant payment system

**Required Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``id_branch``
     - int
     - Branch identifier where the sale is processed
   * - ``service_value``
     - float
     - Total value of the service or product
   * - ``type_payment``
     - str
     - Payment method code (see Payment Types table)

**Optional Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``id_member``
     - int
     - Member identifier for member-related sales
   * - ``id_employee``
     - int
     - Employee processing the sale
   * - ``total_installments``
     - int
     - Number of payment installments (default: 1)
   * - ``sale_date``
     - datetime
     - Date and time of the sale (default: current time)
   * - ``observations``
     - str
     - Additional notes about the sale

**Returns**

Returns a :class:`~evo_client.models.SaleViewModel` object containing:

- ``id``: Unique identifier for the created sale
- ``sale_date``: Timestamp of the sale
- ``status``: Current status of the sale
- ``receivables``: List of payment receivables if applicable

**Exceptions**

- ``ValueError``: Raised when required parameters are missing or invalid
- ``ApiException``: Raised when the API request fails
- ``ValidationError``: Raised when the sale data fails validation

Retrieving Sales
~~~~~~~~~~~~~~

.. automethod:: evo_client.api.sales_api.SalesApi.get_sales

**Filter Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``member_id``
     - int
     - Filter sales by member ID
   * - ``start_date``
     - datetime
     - Start date for sale filtering
   * - ``end_date``
     - datetime
     - End date for sale filtering
   * - ``payment_type``
     - str
     - Filter by payment method
   * - ``show_receivables``
     - bool
     - Include payment receivables in response

**Returns**

Returns a list of :class:`~evo_client.models.SaleViewModel` objects.

**Exceptions**

- ``ValueError``: Raised when filter parameters are invalid
- ``ApiException``: Raised when the API request fails

Advanced Filtering
----------------

The Sales API provides comprehensive filtering options when retrieving sales. Here are some common use cases:

Membership Sales
~~~~~~~~~~~~~~

.. code-block:: python

    # Get active membership sales
    sales = api.get_sales(
        only_membership=True,
        show_only_active_memberships=True,
        at_least_monthly=True  # Filter out short-term memberships
    )

Corporate Sales
~~~~~~~~~~~~~

.. code-block:: python

    # Get corporate partnership sales
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    sales = api.get_sales(
        date_sale_start=start_date,
        date_sale_end=end_date,
        corporate_partnership_id=789
    )

Pagination and Date Filtering
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get paginated sales with date range
    sales = api.get_sales(
        date_sale_start=start_date,
        date_sale_end=end_date,
        take=50,        # Items per page
        skip=100        # Skip first 100 items
    )

Managing Sale Items
----------------

.. automethod:: evo_client.api.sales_api.SalesApi.get_sales_items

Example of retrieving and filtering sale items:

.. code-block:: python

    # Get items for a specific branch
    items = api.get_sales_items(branch_id=456)
    
    # Process items
    for item in items:
        print(f"Item: {item.name}")
        print(f"Price: {item.price}")
        print(f"Category: {item.category}")

Session-Based Operations
---------------------

.. automethod:: evo_client.api.sales_api.SalesApi.get_sale_by_session_id

Asynchronous Operations
---------------------

All methods in the Sales API support asynchronous operations by setting ``async_req=True``. 
When used asynchronously, methods return an ``AsyncResult`` object that can be used to retrieve 
the result when it's ready.

Example of asynchronous usage:

.. code-block:: python

    # Async request for sale details
    async_result = sales_api.get_sale_by_id(sale_id=123, async_req=True)
    
    # Do other work while the request is processing...
    
    # Get the result when ready
    sale = async_result.get()
    
    # Parallel async requests
    sales_result = sales_api.get_sales(
        member_id=123,
        async_req=True
    )
    items_result = sales_api.get_sales_items(
        branch_id=456,
        async_req=True
    )
    
    # Get results
    sales = sales_result.get()
    items = items_result.get()

Data Models
----------

The Sales API uses the following primary data models:

NewSaleViewModel
~~~~~~~~~~~~~
Main model for creating new sales:

- ``id_branch``: Branch ID where the sale is made
- ``id_member``: Member ID (optional)
- ``service_value``: Value of the service/product
- ``type_payment``: Payment method code
- ``total_installments``: Number of payment installments
- ``sale_date``: Date of the sale
- ``observations``: Additional notes

SaleViewModel
~~~~~~~~~~
Response model for sale information:

- ``id_sale``: Unique sale identifier
- ``sale_date``: Transaction date
- ``total_value``: Total sale amount
- ``payment_status``: Current payment status
- ``receivables``: List of associated receivables

Best Practices
------------

1. **Error Handling**
   - Implement proper exception handling for all operations
   - Check for specific error status codes
   - Provide meaningful error messages
   - Handle timeout scenarios appropriately

2. **Performance Optimization**
   - Use async operations for long-running requests
   - Implement batch operations when possible
   - Cache frequently accessed sale data
   - Use pagination for large result sets

3. **Security**
   - Validate all input data
   - Implement proper authorization checks
   - Follow secure payment processing guidelines
   - Keep sensitive payment data encrypted

API Versioning
------------

The Sales API supports multiple versions:

- ``/api/v1/sales``: Base endpoint for most operations
- ``/api/v2/sales``: Enhanced endpoint with additional filtering options

Error Handling
------------

The API uses standard HTTP status codes and provides detailed error messages. Common errors:

* ``400 Bad Request``: Invalid parameters or request body
* ``401 Unauthorized``: Authentication required
* ``403 Forbidden``: Insufficient permissions
* ``404 Not Found``: Sale, member, or item not found
* ``500 Internal Server Error``: Server-side error

Example of error handling:

.. code-block:: python

    try:
        sale = sales_api.get_sale_by_id(sale_id=123)
    except ValueError as e:
        print(f"Invalid parameter: {e}")
    except Exception as e:
        print(f"API error: {e}")

See Also
--------

* :doc:`models/sales` - Detailed information about sales-related data models
* :doc:`../authentication` - Authentication requirements for using the API