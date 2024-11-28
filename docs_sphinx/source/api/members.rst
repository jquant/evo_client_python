Members API
===========

The Members API enables management of gym member data and operations. It provides secure endpoints for member authentication, profile management, and basic member operations.

Key Features
-----------

* Member authentication and password management
* Profile information retrieval and updates
* Member service management
* Member transfer between branches
* Fitcoins system integration (where available)
* Support for both synchronous and asynchronous operations
* Pagination and filtering capabilities

Basic Usage
----------

.. code-block:: python

    from evo_client import EvoClient
    from evo_client.api import MembersApi
    from evo_client.models import MemberDataViewModel
    from datetime import datetime

    # Initialize the API client
    client = EvoClient(
        username="mygym.example.com",
        password="your-secret-key"
    )
    api = MembersApi(client)

    # Get member basic information
    try:
        member = api.get_basic_info(email="member@example.com")
        print(f"Member ID: {member.id_member}")
        print(f"Name: {member.name}")
        print(f"Status: {member.membership_status}")
        
        # Get detailed profile
        if member.id_member:
            profile = api.get_member_profile(id_member=member.id_member)
            print(f"Email: {profile.email}")
            print(f"Gender: {profile.gender}")
            print(f"Document: {profile.document}")
    except Exception as e:
        print(f"Error: {e}")

API Reference
------------

.. autoclass:: evo_client.api.members_api.MembersApi
   :members:
   :undoc-members:
   :special-members: __init__

Models
------

MembersApiViewModel
~~~~~~~~~~~~~~~~

Complete member information model including profile, membership, and status details.

.. autopydantic_model:: evo_client.models.members_api_view_model.MembersApiViewModel
   :members:
   :undoc-members:
   :validate:

MembersBasicApiViewModel
~~~~~~~~~~~~~~~~~~~~~

Basic member information model for quick lookups and listings.

.. autopydantic_model:: evo_client.models.members_basic_api_view_model.MembersBasicApiViewModel
   :members:
   :undoc-members:
   :validate:

MemberDataViewModel
~~~~~~~~~~~~~~~~

Model for member profile data and updates. Contains personal information and contact details.

Fields:
    - cellphone: Optional[TelefoneApiViewModel] - Member's cellphone information
    - email: Optional[TelefoneApiViewModel] - Member's email information
    - gender: Optional[str] - Member's gender (M/F)
    - document: Optional[str] - Member's identification document
    - zip_code: Optional[str] - Postal code
    - address: Optional[str] - Street address
    - number: Optional[str] - Address number
    - complement: Optional[str] - Additional address information
    - neighborhood: Optional[str] - Neighborhood
    - city: Optional[str] - City
    - id_state: Optional[int] - State identifier
    - birth_day: Optional[datetime] - Member's birth date

Examples
--------

Authentication
~~~~~~~~~~~~

.. code-block:: python

    # Authenticate a member
    try:
        result = api.authenticate_member(
            email="member@example.com",
            password="secure_password"
        )
        print(f"Authentication successful: {result.authenticated}")
    except Exception as e:
        print(f"Authentication failed: {e}")

Profile Management
~~~~~~~~~~~~~~~

.. code-block:: python

    # Update member profile
    try:
        update_data = MemberDataViewModel(
            email="new.email@example.com",
            cellphone="+1234567890",
            gender="M",
            birth_day=datetime(1990, 1, 1)
        )
        
        success = api.update_member_data(
            id_member=123,
            body=update_data
        )
        print("Profile updated successfully" if success else "Update failed")
    except Exception as e:
        print(f"Error updating profile: {e}")

Member Services
~~~~~~~~~~~~

.. code-block:: python

    # Get member services
    try:
        services = api.get_member_services(id_member=123)
        for service in services:
            print(f"Service: {service.description}")
            print(f"Status: {service.status}")
    except Exception as e:
        print(f"Error retrieving services: {e}")

Error Handling
------------

The API uses standard HTTP status codes and may raise the following exceptions:

* ``ValueError``: When invalid parameters are provided (e.g., take > 50)
* ``ApiException``: For API-related errors (authentication, not found, etc.)

Common error status codes:

* 400: Bad Request - Invalid parameters
* 401: Unauthorized - Authentication required
* 404: Not Found - Member not found
* 422: Unprocessable Entity - Validation error

See Also
--------

* :doc:`sales` - For managing member sales and transactions
* :doc:`finance/receivables` - For managing member payments
* :doc:`api/access` - For managing member access control
