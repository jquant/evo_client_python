Membership API
==============

The Membership API provides comprehensive functionality for managing gym membership programs, including membership categories, plans, and member subscriptions. This API enables you to retrieve, filter, and manage membership-related information across your gym's locations.

Key Features
------------

* Comprehensive membership category management
* Flexible membership plan retrieval with advanced filtering
* Multi-location membership support
* Detailed membership status tracking
* Access to pricing and duration information
* Integration with billing and member systems

Models
------

.. autoclass:: evo_client.models.membership_category_model.MembershipCategoryModel
   :members:
   :undoc-members:

.. autoclass:: evo_client.models.membership_model.MembershipModel
   :members:
   :undoc-members:

Basic Usage
-----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import MembershipApi
    from datetime import datetime

    # Initialize the API client
    client = EvoClient(username="mygym.example.com", password="your-secret-key")
    api = MembershipApi(client)

    # Get active membership categories
    categories = api.get_categories(active_only=True)
    for category in categories:
        print(f"Category: {category.name} - Duration: {category.duration_months} months")

    # Get available memberships for a specific branch
    memberships = api.get_memberships(
        branch_id=123,
        active=True,
        include_prices=True
    )

API Reference
-------------

.. autoclass:: evo_client.api.membership_api.MembershipApi
   :members:
   :undoc-members:
   :special-members: __init__

Methods
-------

get_categories
~~~~~~~~~~~~~~

Retrieve membership categories with optional filtering.

Parameters:
    - **active_only** (Optional[bool]): Filter for active categories only
    - **branch_id** (Optional[int]): Filter categories by branch ID
    - **include_prices** (Optional[bool]): Include pricing information
    - **include_restrictions** (Optional[bool]): Include membership restrictions
    - **take** (Optional[int]): Number of records to return (default=50, max=100)
    - **skip** (Optional[int]): Number of records to skip for pagination

Returns:
    List[:class:`~evo_client.models.membership_category_model.MembershipCategoryModel`]: List of membership categories with the following information:
        - Category ID and name
        - Duration in months
        - Price information (if requested)
        - Restrictions and requirements
        - Status and availability

Raises:
    - **ApiException**: When the API request fails
    - **ValidationError**: When parameters are invalid
    - **AuthenticationError**: When credentials are invalid

get_memberships
~~~~~~~~~~~~~~~~

Retrieve memberships with comprehensive filtering options.

Parameters:
    - **branch_id** (Optional[int]): Filter by branch ID
    - **active** (Optional[bool]): Filter by active status
    - **category_id** (Optional[int]): Filter by category ID
    - **include_prices** (Optional[bool]): Include current pricing
    - **include_members** (Optional[bool]): Include member count
    - **start_date** (Optional[str]): Filter by start date (YYYY-MM-DD)
    - **end_date** (Optional[str]): Filter by end date (YYYY-MM-DD)
    - **take** (Optional[int]): Number of records to return (default=50, max=100)
    - **skip** (Optional[int]): Number of records to skip

Returns:
    List[:class:`~evo_client.models.membership_model.MembershipModel`]: List of memberships containing:
        - Membership details (ID, name, description)
        - Category information
        - Pricing and duration
        - Member counts (if requested)
        - Status and availability
        - Branch-specific information

Raises:
    - **ApiException**: When the API request fails
    - **ValidationError**: When parameters are invalid
    - **AuthenticationError**: When credentials are invalid

Examples
--------

1. Retrieve Active Categories with Pricing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        # Get active categories with pricing information
        categories = api.get_categories(
            active_only=True,
            include_prices=True,
            branch_id=123
        )
        
        for category in categories:
            print(f"Category: {category.name}")
            print(f"Duration: {category.duration_months} months")
            print(f"Price: ${category.price:.2f}")
            print("---")
    except ApiException as e:
        print(f"Error retrieving categories: {e}")

2. Filter Memberships by Date Range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime, timedelta

    # Calculate date range for last month
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    try:
        # Get memberships created in the last 30 days
        recent_memberships = api.get_memberships(
            branch_id=123,
            active=True,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-d"),
            include_members=True
        )
        
        for membership in recent_memberships:
            print(f"Membership: {membership.name}")
            print(f"Members: {membership.member_count}")
            print(f"Status: {'Active' if membership.is_active else 'Inactive'}")
            print("---")
    except ApiException as e:
        print(f"Error retrieving memberships: {e}")

Error Handling
--------------

The Membership API uses standard HTTP status codes and may raise the following exceptions:

- **ApiException**: Base exception for API-related errors
    - 400: Invalid parameters or request
    - 401: Authentication failed
    - 403: Insufficient permissions
    - 404: Resource not found
    - 429: Rate limit exceeded
    - 500: Server error

- **ValidationError**: Raised when:
    - Invalid date formats are provided
    - Invalid branch_id is specified
    - Take/skip parameters are out of range

- **AuthenticationError**: Raised when:
    - API credentials are invalid
    - Token has expired
    - Account is locked or disabled

Best Practices
-------------

1. **Filtering and Pagination**
   - Always use pagination for large datasets
   - Combine filters to reduce response size
   - Cache frequently accessed category data

2. **Error Handling**
   - Implement proper error handling for all API calls
   - Log API errors for troubleshooting
   - Provide meaningful error messages to users

3. **Performance**
   - Request only needed information (use include_* parameters wisely)
   - Implement caching for static data like categories
   - Use appropriate page sizes for pagination

4. **Data Consistency**
   - Regularly sync membership data across branches
   - Validate membership status before operations
   - Keep pricing information up to date

See Also
--------

* :doc:`members` - For managing member-related operations
* :doc:`finance/receivables` - For managing member payments
* :doc:`voucher` - For managing membership discounts
