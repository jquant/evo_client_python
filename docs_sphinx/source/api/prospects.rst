Prospects API
============

The Prospects API enables you to manage potential gym members throughout their conversion journey. This API provides functionality for creating, updating, and tracking prospects, as well as managing their services and transfers.

Models
------

.. module:: evo_client.models

.. autoclass:: ProspectsResumoApiViewModel
   :members:
   :undoc-members:
   :show-inheritance:

   .. py:attribute:: id_prospect
      :type: int

      Unique identifier for the prospect

   .. py:attribute:: id_branch
      :type: int

      Branch ID where prospect is registered

   .. py:attribute:: branch_name
      :type: str

      Name of the branch

   .. py:attribute:: first_name
      :type: str

      Prospect's first name

   .. py:attribute:: last_name
      :type: str

      Prospect's last name

   .. py:attribute:: document
      :type: str

      Identification document number

   .. py:attribute:: cellphone
      :type: str

      Contact phone number

   .. py:attribute:: email
      :type: str

      Email address

   .. py:attribute:: gympass_id
      :type: str

      Gympass identifier if applicable

   .. py:attribute:: register_date
      :type: datetime

      Date when prospect was registered

   .. py:attribute:: gender
      :type: str

      Gender ("M"=Male, "F"=Female, "P"=Other)

   .. py:attribute:: birth_date
      :type: datetime

      Date of birth

   .. py:attribute:: signup_type
      :type: str

      How the prospect signed up

   .. py:attribute:: mkt_channel
      :type: str

      Marketing channel source

   .. py:attribute:: conversion_date
      :type: datetime

      Date when prospect converted to member

   .. py:attribute:: id_member
      :type: int

      Member ID if prospect has converted

   .. py:attribute:: current_step
      :type: str

      Current step in conversion process

.. autoclass:: ProspectApiIntegracaoViewModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ProspectApiIntegracaoAtualizacaoViewModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ProspectTransferenciaViewModel
   :members:
   :undoc-members:
   :show-inheritance:

API Methods
----------

.. module:: evo_client.api

.. autoclass:: ProspectsApi
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
-------------

Creating a New Prospect
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ProspectsApi
    from evo_client.models import ProspectApiIntegracaoViewModel
    from evo_client.exceptions import ApiException
    from datetime import datetime

    prospects_api = ProspectsApi()

    try:
        # Create new prospect
        prospect = ProspectApiIntegracaoViewModel(
            name="John",
            lastName="Doe",
            email="john.doe@example.com",
            cellphone="1234567890",
            birthday=datetime(1990, 1, 1),
            gender="M",
            visit=1,  # Personal visit
            marketingType="Social Media",
            notes="Interested in personal training",
            currentStep="Initial Contact"
        )
        
        result = prospects_api.create_prospect(prospect)
        print(f"Created prospect with ID: {result.id_prospect}")
        
    except ValueError as e:
        print(f"Invalid prospect data: {e}")
    except ApiException as e:
        if e.status == 400:
            print("Invalid prospect information")
        elif e.status == 409:
            print("Prospect with this email already exists")
        else:
            print(f"API error: {e.status} - {e.reason}")

Searching for Prospects
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime, timedelta

    try:
        # Search for recent prospects
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        prospects = prospects_api.get_prospects(
            register_date_start=start_date,
            register_date_end=end_date,
            take=50  # Maximum allowed records
        )
        
        for prospect in prospects:
            print(f"Name: {prospect.first_name} {prospect.last_name}")
            print(f"Email: {prospect.email}")
            print(f"Status: {prospect.current_step}")
            if prospect.conversion_date:
                print(f"Converted on: {prospect.conversion_date}")
            print("---")
            
    except ApiException as e:
        if e.status == 400:
            print("Invalid search parameters")
        else:
            print(f"API error: {e.status} - {e.reason}")

Updating a Prospect
~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.models import ProspectApiIntegracaoAtualizacaoViewModel

    try:
        # Update prospect status
        update = ProspectApiIntegracaoAtualizacaoViewModel(
            idProspect=12345,
            name="John",
            lastName="Doe",
            email="john.doe@example.com",
            currentStep="Contract Negotiation",
            notes="Scheduled for gym tour tomorrow"
        )
        
        result = prospects_api.update_prospect(update)
        print(f"Updated prospect {result.id_prospect}")
        
    except ApiException as e:
        if e.status == 404:
            print("Prospect not found")
        elif e.status == 400:
            print("Invalid update data")
        else:
            print(f"API error: {e.status} - {e.reason}")

Error Handling
------------

The Prospects API uses standard HTTP status codes:

- 400: Invalid request (e.g., missing required fields, invalid data)
- 401: Authentication failed
- 403: Insufficient permissions
- 404: Prospect not found
- 409: Conflict (e.g., duplicate prospect)
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

    # Get prospects page by page
    page_size = 50
    current_page = 0
    
    while True:
        prospects = prospects_api.get_prospects(
            take=page_size,
            skip=current_page * page_size
        )
        
        if not prospects:
            break
            
        # Process prospects
        for prospect in prospects:
            print(f"Processing prospect: {prospect.first_name}")
            
        current_page += 1

Best Practices
------------

1. **Data Validation**:
   - Always validate required fields before creating/updating prospects
   - Use proper date formats for birth dates and registration dates
   - Ensure email addresses and phone numbers are properly formatted

2. **Error Handling**:
   - Implement proper error handling for all API calls
   - Check for duplicate prospects before creation
   - Handle pagination properly for large result sets

3. **Security**:
   - Never expose prospect personal information
   - Use environment variables for API credentials
   - Validate and sanitize all input data
