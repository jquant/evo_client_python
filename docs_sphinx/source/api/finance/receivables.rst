Receivables API
==============

The Receivables API provides functionality for managing accounts receivable, including member payments, outstanding balances, and payment tracking. It supports comprehensive filtering options for retrieving receivables and marking them as received.

Key Features
-----------
* Extensive filtering by multiple date types (registration, due, receiving, etc.)
* Support for multiple payment types and account statuses
* Member and sale-specific filtering
* Pagination support
* Asynchronous operations
* Revenue center management

Basic Usage
----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import ReceivablesApi
    from datetime import datetime, timedelta

    # Initialize client with your gym's credentials
    client = EvoClient(
        username="mygym.example.com",    # Your gym's DNS
        password="your-secret-key"       # Your secret key
    )
    
    # Create receivables API instance
    api = ReceivablesApi(client)
    
    # Get receivables for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    receivables = api.get_receivables(
        registration_date_start=start_date,
        registration_date_end=end_date,
        account_status="1",  # 1=Opened
        take=50
    )

API Reference
------------

.. autoclass:: evo_client.api.receivables_api.ReceivablesApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

ReceivablesApiViewModel
~~~~~~~~~~~~~~~~~~~~~

Model representing a receivable record with detailed information about payments, status, and related entities.

Fields include:
* Basic information (ID, description, amounts)
* Dates (registration, due, receiving, competence, etc.)
* Status and payment type information
* Member and sale relationships
* Invoice and credit details
* Card payment information (when applicable)

.. autopydantic_model:: evo_client.models.ReceivablesApiViewModel
   :members:
   :undoc-members:
   :validate:

ReceivablesMaskReceivedViewModel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model for marking receivables as received. Used with the mark_received method.

Fields:
* ids_receivables: List of receivable IDs to mark as received
* id_bank_account: Optional bank account ID

.. autopydantic_model:: evo_client.models.ReceivablesMaskReceivedViewModel
   :members:
   :undoc-members:
   :validate:

RevenueCenterApiViewModel
~~~~~~~~~~~~~~~~~~~~~~

Model for revenue center information, representing financial grouping and hierarchy.

Fields:
* id_revenue_center: Revenue center identifier
* description: Center description
* active: Activity status
* id_revenue_center_parent: Parent center ID for hierarchical structure
* abreviation: Short name
* level: Hierarchy level

.. autopydantic_model:: evo_client.models.RevenueCenterApiViewModel
   :members:
   :undoc-members:
   :validate:

Examples
--------

Filtering Receivables
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ReceivablesApi
    from datetime import datetime, timedelta

    api = ReceivablesApi()

    # Get overdue receivables
    overdue = api.get_receivables(
        account_status="4",  # 4=Overdue
        due_date_end=datetime.now()
    )

    # Get receivables by payment type
    credit_card = api.get_receivables(
        payment_types="2",  # 2=Credit Card
        account_status="1"  # 1=Opened
    )

    # Get receivables for a specific member with date filtering
    member_receivables = api.get_receivables(
        member_id=123,
        registration_date_start=datetime.now() - timedelta(days=90),
        registration_date_end=datetime.now(),
        take=50
    )

Marking Receivables as Received
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ReceivablesApi
    from evo_client.models import ReceivablesMaskReceivedViewModel

    api = ReceivablesApi()

    # Mark multiple receivables as received with a specific bank account
    received = ReceivablesMaskReceivedViewModel(
        ids_receivables=[1, 2, 3],
        id_bank_account=456
    )
    api.mark_received(received)

Revenue Center Management
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ReceivablesApi

    api = ReceivablesApi()

    # Get revenue centers with pagination
    centers = api.get_revenue_centers(
        take=50,
        skip=0
    )

    # Process revenue centers
    for center in centers:
        print(f"Center: {center.description}")
        print(f"Level: {center.level}")
        if center.id_revenue_center_parent:
            print(f"Parent ID: {center.id_revenue_center_parent}")

Payment Types
-----------

The following payment types are supported:

* 0 = Balance Due
* 1 = Money
* 2 = Credit Card
* 3 = Debit Card
* 4 = Check
* 5 = Boleto Bancário
* 6 = PagSeguro
* 7 = Deposit
* 8 = Account Debit
* 9 = Internet
* 11 = Sale Credits
* 12 = On-line Credit Card
* 13 = Transfer
* 18 = Pix

Account Status
------------

Receivables can have the following status:

* 1 = Opened
* 2 = Received
* 3 = Canceled
* 4 = Overdue

See Also
--------
* :doc:`../sales` - For managing sales that generate receivables
* :doc:`../members` - For member-related operations
* :doc:`payables` - For managing accounts payable
