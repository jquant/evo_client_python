PIX API
=======

The PIX API provides functionality for managing PIX payments, a Brazilian instant payment system. It enables instant transfers and payments 24/7, including holidays and weekends, with the funds being made available to the recipient in real-time.

Key Features
-----------
* Generate PIX QR codes for payments
* Get payment details including expiration date
* Support for synchronous and asynchronous operations

Basic Usage
----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import PixApi

    # Initialize client with your gym's credentials
    client = EvoClient(
        username="mygym.example.com",    # Your gym's DNS
        password="your-secret-key"       # Your secret key
    )
    
    # Create PIX API instance
    api = PixApi(client)
    
    # Get QR code details for a PIX payment
    payment_details = api.get_qr_code(pix_receipt_id=123)
    
    # Access payment information
    print(f"QR Code: {payment_details.qr_code}")
    print(f"Value: R$ {payment_details.value}")
    print(f"Expires at: {payment_details.expiration_date}")

API Reference
------------

.. autoclass:: evo_client.api.pix_api.PixApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

PixPaymentDetailsViewModel
~~~~~~~~~~~~~~~~~~~~~~~

Model representing PIX payment details including QR code and expiration information.

.. autopydantic_model:: evo_client.models.PixPaymentDetailsViewModel
   :members:
   :undoc-members:
   :validate:

.. note::
   All monetary values are in Brazilian Real (BRL) and are represented as decimal numbers with two decimal places.
   QR codes have a default expiration of 24 hours unless otherwise specified.

Examples
--------

Generating a QR Code
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import PixApi
    from evo_client.exceptions import ApiException

    # Initialize client
    client = EvoClient(
        username="mygym.example.com",
        password="your-secret-key"
    )
    
    api = PixApi(client)

    try:
        # Generate a new PIX QR code
        payment_details = api.get_qr_code(
            pix_receipt_id=123,
            value=99.90,  # Amount in BRL
            description="Monthly gym membership"
        )
        print(f"QR Code: {payment_details.qr_code}")
        print(f"Value: R$ {payment_details.value}")
        print(f"Expires at: {payment_details.expiration_date}")
    except ApiException as e:
        print(f"Error generating PIX QR code: {e}")

Asynchronous QR Code Retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import PixApi

    api = PixApi()

    # Get QR code details asynchronously
    async_result = api.get_qr_code(
        pix_receipt_id=123,
        async_req=True
    )
    
    # Get the result when needed
    payment_details = async_result.get()
    print(f"QR Code: {payment_details.qr_code}")

Error Handling
~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import PixApi
    from evo_client.exceptions import ApiException

    api = PixApi()

    try:
        payment_details = api.get_qr_code(pix_receipt_id=123)
    except ApiException as e:
        if e.status == 404:
            print("PIX receipt not found")
        else:
            print(f"Error retrieving PIX details: {e}")

See Also
--------
* :doc:`../sales` - For managing sales with PIX payments
* :doc:`receivables` - For managing accounts receivable
