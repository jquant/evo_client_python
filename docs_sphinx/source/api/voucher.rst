Voucher API
==========

Overview
--------

The Voucher API enables you to create and manage discount vouchers for your gym's products and services. It provides comprehensive functionality for:

- Creating percentage and fixed-amount discount vouchers
- Managing voucher validity periods and usage limits
- Tracking voucher usage and redemptions
- Supporting branch-specific vouchers for multi-location gyms

Key Features
-----------

- **Flexible Discount Types**
    - Percentage discounts (0.01% - 100%)
    - Fixed amount discounts (minimum 0.01 in account currency)
    - Support for both product and service discounts

- **Advanced Validation Rules**
    - Validity period controls
    - Usage limits per voucher
    - Minimum purchase requirements
    - Product/service restrictions

- **Multi-Location Support**
    - Branch-specific voucher management
    - Centralized tracking across locations
    - Branch-level usage statistics

Authentication
------------

The API uses Basic Authentication:

- Username: Your gym's DNS (e.g., "mygym.example.com")
- Password: Your Secret Key

API Reference
------------

.. autoclass:: evo_client.api.voucher_api.VoucherApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

.. autoclass:: evo_client.models.vouchers_resumo_api_view_model.VouchersResumoApiViewModel
   :members:
   :undoc-members:

   The main voucher model with the following key fields:

   - **id_voucher** (int): Unique identifier for the voucher
   - **name_voucher** (str): Voucher code/name used for redemption
   - **type_voucher** (str): Type of discount (percentage or fixed amount)
   - **limited** (bool): Whether the voucher has usage limits
   - **available** (int): Number of remaining uses
   - **used** (int): Number of times used
   - **site_available** (bool): Whether voucher can be used on website
   - **id_memberships** (List[int]): List of applicable membership IDs

Basic Usage
-----------

Here's a complete example showing common voucher operations:

.. code-block:: python

    from evo_client.api import VoucherApi
    from evo_client.core.api_client import ApiClient
    from evo_client.exceptions import ApiException
    from datetime import datetime, timedelta

    # Initialize the API client
    api_client = ApiClient()
    api_client.configuration.username = "mygym.example.com"
    api_client.configuration.password = "your-secret-key"
    voucher_api = VoucherApi(api_client)

    try:
        # Create a 20% discount voucher valid for 30 days
        new_voucher = voucher_api.create_voucher(
            name="SUMMER2024",
            discount_type=1,  # 1 = Percentage discount
            discount_value=20.0,
            valid_from=datetime.now().strftime("%Y-%m-%d"),
            valid_until=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            usage_limit=100,  # Maximum 100 uses
            min_value=50.0    # Minimum purchase of $50
        )
        print(f"Created voucher ID: {new_voucher['id']}")

        # List all active vouchers
        active_vouchers = voucher_api.get_vouchers(
            valid=True,
            take=10,
            skip=0
        )
        for voucher in active_vouchers:
            print(f"Voucher {voucher.name_voucher}:")
            print(f"- Type: {voucher.type_voucher}")
            print(f"- Available uses: {voucher.available}")
            print(f"- Times used: {voucher.used}")
            print("---")

        # Get detailed information about a specific voucher
        voucher_details = voucher_api.get_voucher_details(voucher_id=123)
        print(f"Voucher details: {voucher_details}")

    except ValueError as e:
        print(f"Invalid voucher data: {e}")
    except ApiException as e:
        print(f"API error: {e.status} - {e.reason}")

Error Handling
-------------

The API may raise these exceptions:

ValueError
~~~~~~~~~
Raised when invalid data is provided:

- Invalid discount type or value
- Invalid date format
- Missing required fields
- Usage limit less than 1
- Minimum value less than 0

ApiException
~~~~~~~~~~
Raised when the API request fails:

- ``401``: Authentication failed
- ``403``: Permission denied
- ``404``: Voucher not found
- ``422``: Validation error
- ``500``: Server error

Example error handling:

.. code-block:: python

    try:
        # Attempt to create a voucher with invalid discount
        voucher = voucher_api.create_voucher(
            name="INVALID",
            discount_type=1,
            discount_value=150.0,  # Invalid: > 100%
            valid_from="2024-01-01",
            valid_until="2024-12-31"
        )
    except ValueError as e:
        print(f"Invalid voucher data: {e}")
    except ApiException as e:
        if e.status == 422:
            print("Validation error - check discount value")
        else:
            print(f"API error: {e.status} - {e.reason}")

Best Practices
-------------

1. **Naming Conventions**
    - Use clear, memorable voucher codes
    - Include expiry date in name (e.g., SUMMER2024)
    - Avoid ambiguous characters (0/O, 1/I)

2. **Usage Limits**
    - Always set appropriate usage limits
    - Consider peak vs. off-peak seasons
    - Monitor usage patterns to adjust limits

3. **Validation Rules**
    - Set minimum purchase values for percentage discounts
    - Use fixed amounts for low-value purchases
    - Consider product/service restrictions

4. **Error Handling**
    - Validate voucher codes before applying
    - Handle all possible API exceptions
    - Provide clear error messages to users

5. **Maintenance**
    - Regularly check for expired vouchers
    - Monitor usage statistics
    - Update or remove unused vouchers

See Also
--------

- :ref:`sales_api`: For applying vouchers to sales
- :ref:`products_api`: For product-specific vouchers
- :ref:`services_api`: For service-specific vouchers
