Entries API
===========

The Entries API enables you to manage and track gym member entries and access control. This API provides functionality for retrieving entry records with various filtering options.

Models
------

.. module:: evo_client.models

.. autoclass:: EntradasResumoApiViewModel
   :members:
   :undoc-members:
   :show-inheritance:

   .. py:attribute:: date
      :type: datetime

      The date and time when the entry was registered

   .. py:attribute:: date_turn
      :type: datetime

      The date and time of the turn/shift when the entry occurred

   .. py:attribute:: time_zone
      :type: str

      Timezone of the entry record

   .. py:attribute:: id_member
      :type: int

      Unique identifier of the member

   .. py:attribute:: name_member
      :type: str

      Name of the member

   .. py:attribute:: id_prospect
      :type: int

      Unique identifier of the prospect (if applicable)

   .. py:attribute:: name_prospect
      :type: str

      Name of the prospect (if applicable)

   .. py:attribute:: id_employee
      :type: int

      Unique identifier of the employee who processed the entry

   .. py:attribute:: name_employee
      :type: str

      Name of the employee who processed the entry

   .. py:attribute:: entry_type
      :type: str

      Type of entry (e.g., "member", "prospect", "guest")

   .. py:attribute:: device
      :type: str

      Device used for entry registration

   .. py:attribute:: releases_by_id
      :type: int

      ID of the release if entry was manually released

   .. py:attribute:: id_branch
      :type: int

      ID of the gym branch where entry occurred

   .. py:attribute:: block_reason
      :type: str

      Reason for entry block if access was denied

   .. py:attribute:: entry_action
      :type: str

      Action taken during entry (e.g., "allowed", "denied")

   .. py:attribute:: id_migration
      :type: str

      Migration ID if the record was imported

API Methods
----------

.. module:: evo_client.api

.. autoclass:: EntriesApi
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: get_entries
      :noindex:

Usage Examples
-------------

Basic Entry Query
~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import EntriesApi
    from datetime import datetime, timedelta
    from evo_client.exceptions import ApiException

    entries_api = EntriesApi()

    try:
        # Get entries for the last 24 hours
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        
        entries = entries_api.get_entries(
            register_date_start=start_date,
            register_date_end=end_date,
            take=100  # Limit to 100 records
        )
        
        for entry in entries:
            print(f"Member: {entry.name_member}")
            print(f"Entry Time: {entry.date}")
            print(f"Status: {entry.entry_action}")
            print("---")
            
    except ValueError as e:
        print(f"Invalid parameter: {e}")
    except ApiException as e:
        if e.status == 400:
            print("Invalid date range")
        elif e.status == 401:
            print("Authentication failed")
        else:
            print(f"API error: {e.status} - {e.reason}")

Filtered Member Entries
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        # Get entries for a specific member
        member_entries = entries_api.get_entries(
            member_id=12345,
            register_date_start=datetime.now() - timedelta(days=30),
            take=1000  # Maximum allowed records
        )
        
        # Process entries
        for entry in member_entries:
            if entry.block_reason:
                print(f"Access denied on {entry.date}: {entry.block_reason}")
            else:
                print(f"Access granted on {entry.date}")
                
    except ApiException as e:
        if e.status == 404:
            print("Member not found")
        else:
            print(f"API error: {e.status} - {e.reason}")

Error Handling
------------

The Entries API uses standard HTTP status codes:

- 400: Invalid request parameters (e.g., invalid date range)
- 401: Authentication failed
- 403: Insufficient permissions to access entries
- 404: Requested entry or member not found
- 429: Too many requests
- 500: Internal server error

All errors are wrapped in :class:`~evo_client.exceptions.ApiException` with detailed error messages.

Pagination
---------

The API supports pagination through the following parameters:

- ``take``: Number of records to return (maximum 1000)
- ``skip``: Number of records to skip

Example pagination:

.. code-block:: python

    # Get entries page by page
    page_size = 100
    current_page = 0
    
    while True:
        entries = entries_api.get_entries(
            take=page_size,
            skip=current_page * page_size
        )
        
        if not entries:
            break
            
        # Process entries
        for entry in entries:
            print(f"Processing entry: {entry.date}")
            
        current_page += 1
