MembersBasicApiViewModel
======================

.. autoclass:: evo_client.models.members_basic_api_view_model.MembersBasicApiViewModel
   :members:
   :undoc-members:
   :show-inheritance:

Properties
---------

- ``id_member`` (int): Unique identifier for the member
- ``name`` (str): Full name of the member
- ``email`` (str): Contact email address
- ``phone`` (str): Contact phone number
- ``status`` (int): Current member status

Example
-------

.. code-block:: python

    from evo_client.models import MembersBasicApiViewModel

    member = MembersBasicApiViewModel(
        id_member=123,
        name="John Doe",
        email="john.doe@example.com",
        phone="1234567890",
        status=1
    )
