Financial APIs
==============

This section covers all financial-related APIs in the Evo Client Python SDK.

.. toctree::
   :maxdepth: 2

   invoices
   payables
   receivables
   bank_accounts
   pix

Functions
---------

.. automodule:: evo_client.api.finance_api.functions
   :members:
   :undoc-members:

Examples
--------

.. code-block:: python

   # Example usage of the Financial APIs
   from evo_client.api.finance_api import FinanceAPI
   
   finance_api = FinanceAPI()
   finance_api.process_invoice(...)
