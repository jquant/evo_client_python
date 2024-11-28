Payables API
============

The Payables API provides functionality for managing accounts payable, expenses, and payment obligations. It allows you to retrieve payable accounts with various filtering options and manage cost centers.

Key Features
-----------
* Query payables with comprehensive filtering options
* View payment status and details
* Manage cost centers
* Track payment due dates and amounts
* Monitor payment statuses

Basic Usage
----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import PayablesApi
    from datetime import datetime, timedelta

    # Initialize client with your gym's credentials
    client = EvoClient(
        username="mygym.example.com",
        password="your-secret-key"
    )
    
    # Create Payables API instance
    api = PayablesApi(client)
    
    # Get payables for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        payables = api.get_payables(
            date_input_start=start_date,
            date_input_end=end_date,
            account_status="1",  # 1=Opened
            take=50  # Limit to 50 records
        )
        
        # Process the results
        for payable in payables:
            print(f"Description: {payable.description}")
            print(f"Amount: R$ {payable.amount}")
            print(f"Due Date: {payable.due_date}")
            print("---")
            
    except Exception as e:
        print(f"Error retrieving payables: {e}")

API Reference
------------

.. autoclass:: evo_client.api.payables_api.PayablesApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

PayablesApiViewModel
~~~~~~~~~~~~~~~~~~~

Model representing a payable account with its details.

.. autopydantic_model:: evo_client.models.payables_api_view_model.PayablesApiViewModel
   :members:
   :undoc-members:
   :validate:

.. note::
   All monetary values are in Brazilian Real (BRL) and are represented as decimal numbers with two decimal places.

CostCenterApiViewModel
~~~~~~~~~~~~~~~~~~~

Model representing a cost center for expense categorization.

.. autopydantic_model:: evo_client.models.cost_center_api_view_model.CostCenterApiViewModel
   :members:
   :undoc-members:
   :validate:

Examples
--------

Filtering Payables by Status
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import PayablesApi

    api = PayablesApi()

    # Get all open payables
    open_payables = api.get_payables(
        account_status="1",  # Status: 1=Opened
        take=25
    )
    
    # Get all paid payables from last month
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    paid_payables = api.get_payables(
        account_status="2",  # Status: 2=Paid
        date_payment_start=start_date,
        date_payment_end=end_date,
        take=25
    )

Managing Cost Centers
~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import PayablesApi

    api = PayablesApi()

    # Get all cost centers with pagination
    cost_centers = api.get_cost_centers(
        take=50,
        skip=0
    )
    
    for center in cost_centers:
        print(f"ID: {center.id}")
        print(f"Name: {center.name}")
        print("---")

Account Status Reference
--------------------

The following status codes are used for payable accounts:

* ``1`` = Opened
* ``2`` = Paid
* ``3`` = Canceled

See Also
--------
* :doc:`receivables` - For managing accounts receivable
* :doc:`bank_accounts` - For managing bank accounts
