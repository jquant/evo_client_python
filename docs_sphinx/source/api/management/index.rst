Management APIs
===============

This section covers all management-related APIs in the Evo Client Python SDK.

.. toctree::
   :maxdepth: 2

   employees
   services
   membership
   prospects
   workout
   entries
   partnership
   voucher
   notifications

Functions
---------

.. automodule:: evo_client.api.management_api.functions
   :members:
   :undoc-members:

Examples
--------

.. code-block:: python

   # Example usage of the Management APIs
   from evo_client.api.management_api import ManagementAPI
   
   management_api = ManagementAPI()
   management_api.manage_employee(...)
