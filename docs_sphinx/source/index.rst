.. Evo Client Python documentation master file, created by
   sphinx-quickstart on Thu Nov 28 08:55:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Evo Client Python
========================

Evo Client Python is a powerful, feature-rich SDK for seamlessly integrating with the Evo API platform. It provides comprehensive tools and interfaces for managing gym operations, member services, and business analytics.

Key Features
-----------

* **Type Safety**: Strong typing with Pydantic models and modern Python type hints
* **Async Support**: Both synchronous and asynchronous operations for optimal performance
* **Automatic Retries**: Built-in retry mechanism with configurable backoff strategies
* **Rate Limiting**: Intelligent rate limiting with configurable thresholds
* **Error Handling**: Detailed error information with custom exception types
* **Documentation**: Extensive documentation with real-world examples

Installation
-----------

Install via pip:

.. code-block:: bash

   pip install evo-client-python

Authentication
------------

The SDK uses HTTP Basic Authentication where:
 - Username: Your gym's DNS
 - Password: Your secret key

Example:

.. code-block:: python

   from evo_client import EvoClient
   
   # Initialize with your gym's credentials
   client = EvoClient(
       username="mygym.example.com",    # Your gym's DNS
       password="your-secret-key",      # Your secret key
       base_url="https://api.evo.com"   # API base URL
   )

Quick Start
----------

Basic example showing core functionality:

.. code-block:: python

   from evo_client import EvoClient
   from evo_client.api import MembersApi, SalesApi
   from evo_client.models import SaleCreate
   from datetime import datetime
   
   # Initialize the client with your gym's credentials
   client = EvoClient(
       username="mygym.example.com",    # Your gym's DNS
       password="your-secret-key",      # Your secret key
       base_url="https://api.evo.com"   # API base URL
   )
   
   # Create API instances
   members_api = MembersApi(client)
   sales_api = SalesApi(client)
   
   # Fetch member information
   try:
       member = members_api.get_member_profile(id_member=123)
       print(f"Member: {member.first_name} {member.last_name}")
       
       # Process a sale with proper model
       sale = sales_api.create_sale(
           sale=SaleCreate(
               id_member=member.id,
               amount=99.99,
               description="Monthly Membership",
               date=datetime.now(),
               payment_method="credit_card"
           )
       )
       print(f"Sale processed: {sale.id}")
       
   except ApiException as e:
       print(f"API error: {e.status} - {e.reason}")

Documentation Contents
-------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   quickstart
   installation
   authentication
   configuration
   best_practices

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index
   api/models/index
   api/exceptions

.. toctree::
   :maxdepth: 2
   :caption: Core Features

   features/async_operations
   features/error_handling
   features/rate_limiting
   features/models
   features/pagination

.. toctree::
   :maxdepth: 2
   :caption: Examples & Tutorials

   examples/member_management
   examples/sales_processing
   examples/activity_scheduling
   examples/webhook_integration
   examples/reporting

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog
   migration_guide
   security

Core Concepts
-----------

Error Handling
~~~~~~~~~~~

Comprehensive error handling:

.. code-block:: python

   from evo_client.exceptions import (
       ApiException,
       ValidationError,
       AuthenticationError,
       RateLimitError
   )
   
   try:
       member = members_api.get_member_profile(id_member=123)
   except ValidationError as e:
       print(f"Invalid data: {e.errors}")
   except AuthenticationError as e:
       print(f"Authentication failed: {e.message}")
   except RateLimitError as e:
       print(f"Rate limit exceeded. Retry after: {e.retry_after}s")
   except ApiException as e:
       print(f"API error: {e.status} - {e.reason}")

Rate Limiting
~~~~~~~~~~

Built-in rate limiting with configurable settings:

.. code-block:: python

   from evo_client.rate_limiting import RateLimiter
   
   # Configure rate limiting
   client = EvoClient(
       username="mygym.example.com",
       password="your-secret-key",
       rate_limiter=RateLimiter(
           max_requests=100,
           time_window=60,  # 100 requests per minute
           retry_after=5    # Wait 5 seconds before retry
       )
   )

Async Operations
~~~~~~~~~~~~

Efficient async operations for improved performance:

.. code-block:: python

   import asyncio
   from evo_client.async_api import AsyncMembersApi, AsyncSalesApi
   from evo_client.models import MemberProfile
   
   async def process_members(member_ids: list[int], gym_dns: str, secret_key: str):
       async with AsyncMembersApi(
           username=gym_dns,
           password=secret_key
       ) as members_api:
           # Concurrent member processing
           tasks = [
               members_api.get_member_profile(id_member=id_)
               for id_ in member_ids
           ]
           members = await asyncio.gather(*tasks)
           return members
   
   # Process multiple members concurrently
   member_ids = [1, 2, 3, 4, 5]
   members = asyncio.run(
       process_members(
           member_ids,
           gym_dns="mygym.example.com",
           secret_key="your-secret-key"
       )
   )

Support & Resources
----------------

* `GitHub Repository <https://github.com/jquant/evo_client_python>`_
* `Issue Tracker <https://github.com/jquant/evo_client_python/issues>`_
* `API Status <https://status.evo.com>`_

For additional support:

* Email: support@evo.com
* Documentation: https://docs.evo.com
* Community: https://community.evo.com

Indices and Tables
===============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
