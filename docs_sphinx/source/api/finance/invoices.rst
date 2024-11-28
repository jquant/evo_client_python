Invoices API
============

The Invoices API provides functionality for managing electronic invoices (Notas Fiscais) in your gym or fitness center. It allows you to retrieve, filter, and track invoices with comprehensive filtering options.

Key Features
-----------
* Query invoices with flexible date-based filtering
* Filter by invoice status and type
* Support for pagination with customizable page size
* Track invoice issuance and competency dates
* Member-specific invoice retrieval

Basic Usage
----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import InvoicesApi
    from datetime import datetime, timedelta
    from evo_client.models.enotas_retorno import InvoiceStatus

    # Initialize client with your gym's credentials
    client = EvoClient(
        username="mygym.example.com",
        password="your-secret-key"
    )
    
    # Create Invoices API instance
    api = InvoicesApi(client)
    
    # Get invoices for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        invoices = api.get_invoices(
            issue_date_start=start_date,
            issue_date_end=end_date,
            status_invoice=[InvoiceStatus.ISSUED],  # Get only issued invoices
            take=100  # Limit to 100 records
        )
        
        # Process the results
        for invoice in invoices:
            print(f"Invoice Number: {invoice.number}")
            print(f"Issue Date: {invoice.issue_date}")
            print(f"Value: R$ {invoice.value}")
            print("---")
            
    except Exception as e:
        print(f"Error retrieving invoices: {e}")

API Reference
------------

.. autoclass:: evo_client.api.invoices_api.InvoicesApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

EnotasRetorno
~~~~~~~~~~~

Model representing an electronic invoice with its details.

.. autopydantic_model:: evo_client.models.enotas_retorno.EnotasRetorno
   :members:
   :undoc-members:
   :validate:

.. note::
   All monetary values are in Brazilian Real (BRL) and are represented as decimal numbers with two decimal places.

Examples
--------

Filtering Invoices by Status
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import InvoicesApi
    from evo_client.models.enotas_retorno import InvoiceStatus

    api = InvoicesApi()

    # Get all issued invoices
    issued_invoices = api.get_invoices(
        status_invoice=[InvoiceStatus.ISSUED],
        take=25
    )
    
    # Get all canceled invoices from last month
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    canceled_invoices = api.get_invoices(
        status_invoice=[InvoiceStatus.CANCELED],
        issue_date_start=start_date,
        issue_date_end=end_date,
        take=25
    )

Retrieving Member Invoices
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import InvoicesApi

    api = InvoicesApi()

    # Get invoices for a specific member
    member_invoices = api.get_invoices(
        member_id=123,  # Member's unique identifier
        take=50,
        skip=0
    )
    
    for invoice in member_invoices:
        print(f"Invoice Number: {invoice.number}")
        print(f"Issue Date: {invoice.issue_date}")
        print(f"Status: {invoice.status}")
        print("---")

Invoice Status Reference
--------------------

The following status codes are used for invoices:

* ``ISSUED`` = Invoice has been issued
* ``CANCELED`` = Invoice has been canceled
* ``PROCESSING`` = Invoice is being processed
* ``ERROR`` = Error occurred during invoice processing

See Also
--------
* :doc:`receivables` - For managing accounts receivable
* :doc:`payables` - For managing accounts payable
* :doc:`sales` - For managing sales transactions
