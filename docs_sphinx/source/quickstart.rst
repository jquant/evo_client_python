Quickstart Guide
===============

Installation
-----------

Install the Evo Client Python package using pip:

.. code-block:: bash

    pip install evo-client-python

Basic Usage
----------

Here's a simple example to get you started:

.. code-block:: python

    from evo_client import Configuration, ApiClient
    from evo_client.api import MembersApi

    # Configure API key authorization
    configuration = Configuration(
        host="https://api.evo.example.com",
        api_key={'ApiKeyAuth': 'YOUR_API_KEY'}
    )

    # Create an instance of the API client
    api_client = ApiClient(configuration)

    # Create an instance of the MembersApi
    members_api = MembersApi(api_client)

    # Get member details
    try:
        member = members_api.get_member(member_id="123")
        print(f"Member name: {member.name}")
    except ApiException as e:
        print(f"Exception when calling MembersApi: {e}")

Authentication
-------------

Before using the SDK, you'll need to obtain an API key. See the :doc:`authentication` guide for details.

Next Steps
---------

- Check out the :doc:`api/index` for detailed API documentation
- View more :doc:`examples/index` for common use cases
- Read the :doc:`contributing` guide if you want to contribute to the project
