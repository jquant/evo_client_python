Member Membership API
=====================

The Member Membership API provides comprehensive functionality for managing individual member subscriptions, including membership cancellations, status updates, and detailed membership information. This API is specifically designed for operations that affect a member's relationship with their membership plan.

Key Features
------------

* Manage individual member membership statuses
* Process membership cancellations with flexible options
* Handle membership transfers between branches
* Track membership history and changes
* Manage cancellation fees and refunds
* Configure automated renewal settings

Models
------

.. autoclass:: evo_client.models.member_membership_model.MemberMembershipModel
   :members:
   :undoc-members:

   **Fields**:
       - **id_member** (Optional[int]): Member's unique identifier
       - **id_membership** (Optional[int]): Membership plan identifier
       - **id_member_membership** (Optional[int]): Unique identifier for this membership instance
       - **start_date** (Optional[datetime]): When the membership becomes active
       - **end_date** (Optional[datetime]): When the membership expires
       - **name** (Optional[str]): Name of the membership plan
       - **cancel_date** (Optional[datetime]): When the membership was/will be cancelled
       - **membership_status** (Optional[str]): Current status (Active, Cancelled, Expired)
       - **value_next_month** (Optional[float]): Next month's membership fee
       - **freezes** (Optional[List[FreezeViewModel]]): History of membership freezes
       - **disponible_suspension_days** (Optional[int]): Remaining freeze days available
       - **days_left_to_freeze** (Optional[int]): Days until next available freeze
       - **weekly_limit** (Optional[int]): Maximum weekly visits allowed
       - **pending_sessions** (Optional[int]): Number of unused sessions
       - **scheduled_sessions** (Optional[int]): Number of upcoming scheduled sessions

.. autoclass:: evo_client.models.cancellation_model.CancellationModel
   :members:
   :undoc-members:

Basic Usage
-----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import MemberMembershipApi
    from datetime import datetime, timedelta

    # Initialize the API client
    client = EvoClient(username="mygym.example.com", password="your-secret-key")
    api = MemberMembershipApi(client)

    # Example: Process a membership cancellation with notice period
    cancellation_date = datetime.now() + timedelta(days=30)  # 30-day notice
    try:
        result = api.cancel_membership(
            id_member_membership=123,
            id_member_branch=456,
            cancellation_date=cancellation_date,
            reason_cancellation="Relocation",
            send_notification=True
        )
        print(f"Cancellation processed: {result['status']}")
    except ApiException as e:
        if e.status == 404:
            print("Membership not found")
        elif e.status == 403:
            print("Insufficient permissions to cancel membership")
        elif e.status == 400:
            print(f"Invalid request: {e.body}")
        else:
            print(f"Error processing cancellation: {e}")

API Reference
-------------

.. autoclass:: evo_client.api.member_membership_api.MemberMembershipApi
   :members:
   :undoc-members:
   :special-members: __init__

Methods
-------

cancel_membership
~~~~~~~~~~~~~~~~~

Process a membership cancellation with comprehensive options for handling fees, notifications, and effective dates.

Parameters:
    - **id_member_membership** (int): Unique identifier of the member's membership
    - **id_member_branch** (int): Branch ID where the cancellation is being processed
    - **cancellation_date** (datetime): Effective date of cancellation
        - Must be a future date
        - Cannot be before membership start date
    - **reason_cancellation** (str): Reason for cancellation
        - Required field
        - Maximum length: 500 characters
    - **notice_cancellation** (Optional[str]): Additional notes about the cancellation
    - **cancel_future_releases** (bool): Cancel all future billing releases (default: False)
    - **cancel_future_sessions** (bool): Cancel scheduled training sessions (default: False)
    - **convert_credit_days** (bool): Convert remaining credits to days (default: False)
    - **schedule_cancellation** (bool): Schedule future cancellation (default: False)
    - **schedule_cancellation_date** (Optional[datetime]): Future cancellation date
    - **add_fine** (bool): Apply cancellation fee (default: False)
    - **value_fine** (Optional[float]): Amount of cancellation fee if applicable

Returns:
    Dict[str, Any]: Cancellation details including:
        - Confirmation ID
        - Effective end date
        - Fee calculations
        - Refund information (if applicable)
        - Updated membership status

Raises:
    - **ApiException**: When the API request fails
        - 400: Invalid request parameters
        - 403: Insufficient permissions
        - 404: Membership not found
        - 409: Cancellation already processed
    - **ValidationError**: When parameters fail validation
    - **AuthenticationError**: When credentials are invalid

get_membership_details
~~~~~~~~~~~~~~~~~~~~~

Retrieve detailed information about a member's specific membership.

Parameters:
    - **id_member_membership** (int): Unique identifier of the member's membership
    - **include_history** (Optional[bool]): Include membership status history
    - **include_payments** (Optional[bool]): Include payment history
    - **include_usage** (Optional[bool]): Include facility usage data

Returns:
    :class:`~evo_client.models.member_membership_model.MemberMembershipModel`: Detailed membership information including:
        - Current status and plan details
        - Payment history (if requested)
        - Usage statistics (if requested)
        - Renewal information
        - Associated agreements and documents

Raises:
    - **ApiException**: When the API request fails
    - **ValidationError**: When parameters are invalid
    - **AuthenticationError**: When credentials are invalid

Examples
--------

1. Process Immediate Cancellation with Fee
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime

    try:
        # Process immediate cancellation with fee
        result = api.cancel_membership(
            id_member_membership=123,
            id_member_branch=456,
            cancellation_date=datetime.now(),
            reason_cancellation="Contract breach",
            add_fine=True,
            value_fine=75.0,
            override_notice_period=True,
            notes="Member violated facility rules repeatedly"
        )
        
        print(f"Cancellation Status: {result['status']}")
        print(f"Effective End Date: {result['end_date']}")
        print(f"Fee Applied: ${result['fee_amount']}")
    except ApiException as e:
        print(f"Error processing cancellation: {e}")

2. Future Cancellation with Notice Period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime, timedelta

    try:
        # Calculate end date after notice period
        notice_period = timedelta(days=30)
        cancellation_date = datetime.now() + notice_period
        
        # Process future cancellation
        result = api.cancel_membership(
            id_member_membership=789,
            id_member_branch=456,
            cancellation_date=cancellation_date,
            reason_cancellation="Relocation",
            send_notification=True,
            process_refund=True,
            notes="Member moving to another city"
        )
        
        if result['refund_eligible']:
            print(f"Refund Amount: ${result['refund_amount']}")
            print(f"Refund Processing Date: {result['refund_date']}")
    except ApiException as e:
        print(f"Error scheduling cancellation: {e}")

3. Retrieve Detailed Membership Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        # Get comprehensive membership details
        membership_details = api.get_membership_details(
            id_member_membership=123,
            include_history=True,
            include_payments=True,
            include_usage=True
        )
        
        print(f"Status: {membership_details.status}")
        print(f"Plan: {membership_details.plan_name}")
        print(f"Start Date: {membership_details.start_date}")
        print(f"Next Billing: {membership_details.next_billing_date}")
        
        if membership_details.usage_data:
            print(f"Last Visit: {membership_details.usage_data.last_visit}")
            print(f"Visit Count: {membership_details.usage_data.visit_count}")
    except ApiException as e:
        print(f"Error retrieving membership details: {e}")

Error Handling
--------------

The Member Membership API uses standard HTTP status codes and may raise the following exceptions:

- **ApiException**: Base exception for API-related errors
    - 400: Invalid parameters or request
    - 401: Authentication failed
    - 403: Insufficient permissions
    - 404: Membership not found
    - 409: Conflict with existing operations
    - 429: Rate limit exceeded
    - 500: Server error

- **ValidationError**: Raised when:
    - Invalid membership or branch IDs
    - Invalid cancellation date (e.g., in the past)
    - Invalid fee amounts
    - Missing required fields

- **PermissionError**: Raised when attempting to:
    - Override notice periods without permission
    - Process refunds without authorization
    - Access restricted membership data

Best Practices
-------------

1. **Cancellation Processing**
   - Always provide clear cancellation reasons
   - Document special circumstances in notes
   - Verify fee calculations before applying
   - Consider notice period requirements

2. **Member Communication**
   - Enable notification options for important changes
   - Provide clear cancellation confirmation
   - Include refund information when applicable
   - Document all communication in notes

3. **Data Management**
   - Regularly verify membership status accuracy
   - Maintain detailed cancellation records
   - Track membership history for compliance
   - Secure sensitive member information

4. **Error Prevention**
   - Validate all input parameters
   - Implement proper error handling
   - Double-check fee calculations
   - Verify permissions before operations

See Also
--------

* :doc:`members` - For managing member-related operations
* :doc:`membership` - For managing general membership operations
* :doc:`finance/receivables` - For managing payments and refunds
* :doc:`notifications` - For managing member communications
