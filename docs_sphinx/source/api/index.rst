API Reference
============

The Evo Client Python SDK provides a comprehensive set of APIs for interacting with the Evo platform. Each API module is designed to handle specific aspects of gym management and operations.

Core APIs
--------

.. toctree::
   :maxdepth: 2
   :caption: Member Management

   members
   activities
   member_membership
   membership

.. toctree::
   :maxdepth: 2
   :caption: Business Operations

   sales
   finance/index
   prospects
   partnership
   service
   voucher

.. toctree::
   :maxdepth: 2
   :caption: System Management

   management/index
   configuration
   webhooks
   notifications

.. toctree::
   :maxdepth: 2
   :caption: Employee Management

   employees

.. toctree::
   :maxdepth: 2
   :caption: Workout Management

   workout

.. toctree::
   :maxdepth: 2
   :caption: General Operations

   entries

API Architecture
--------------

The SDK is built on a robust architecture that ensures reliability, performance, and ease of use:

Client Architecture
~~~~~~~~~~~~~~~~

.. code-block:: python

   from evo_client import EvoClient
   from evo_client.api import MembersApi
   
   # Create the main client
   client = EvoClient(
       api_key="your-api-key",
       base_url="https://api.yourgym.com",
       timeout=30
   )
   
   # Initialize specific API modules
   members_api = MembersApi(client)
   
   # Use the API
   member = members_api.get_member_profile(id_member=123)

Authentication & Security
~~~~~~~~~~~~~~~~~~~~~~

The SDK supports multiple authentication methods:

.. code-block:: python

   # API Key Authentication
   client = EvoClient(api_key="your-api-key")
   
   # OAuth2 Authentication
   client = EvoClient(
       client_id="your-client-id",
       client_secret="your-client-secret",
       oauth_token_url="https://auth.yourgym.com/token"
   )
   
   # Custom Authentication
   client = EvoClient(
       auth_handler=CustomAuthHandler(),
       base_url="https://api.yourgym.com"
   )

Error Handling
~~~~~~~~~~~~

Comprehensive error handling across all APIs:

.. code-block:: python

   from evo_client.exceptions import (
       ApiException,
       ValidationError,
       AuthenticationError,
       RateLimitError
   )
   
   try:
       result = api.some_operation()
   except ValidationError as e:
       print(f"Invalid data: {e.errors}")
   except AuthenticationError as e:
       print(f"Auth failed: {e.message}")
   except RateLimitError as e:
       print(f"Rate limit exceeded. Retry after: {e.retry_after}s")
   except ApiException as e:
       print(f"API error: {e.status} - {e.reason}")

Rate Limiting
~~~~~~~~~~~

Built-in rate limiting support:

.. code-block:: python

   from evo_client.rate_limiting import RateLimiter
   
   # Configure rate limiting
   client = EvoClient(
       api_key="your-api-key",
       rate_limiter=RateLimiter(
           max_requests=100,
           time_window=60  # 100 requests per minute
       )
   )

Async Operations
~~~~~~~~~~~~~

Support for async/await operations:

.. code-block:: python

   import asyncio
   from evo_client.async_api import AsyncMembersApi
   
   async def get_members(ids: List[int]):
       async with AsyncMembersApi() as api:
           tasks = [api.get_member_profile(id_) for id_ in ids]
           members = await asyncio.gather(*tasks)
           return members

Core Components
-------------

The SDK is built on several core components that handle the underlying API communication, authentication, and data serialization.

API Client
~~~~~~~~~

The :class:`~evo_client.api_client.ApiClient` class handles all HTTP communication:

* Automatic retries for transient failures
* Request/response logging
* Response parsing and validation
* Error handling and conversion

.. code-block:: python

   from evo_client.api_client import ApiClient, RetryConfig
   
   client = ApiClient(
       base_url="https://api.yourgym.com",
       retry_config=RetryConfig(
           max_retries=3,
           backoff_factor=1.5
       ),
       timeout=30
   )

Configuration
~~~~~~~~~~~

The :class:`~evo_client.configuration.Configuration` class manages SDK settings:

* API endpoints and credentials
* Timeout and retry settings
* Logging configuration
* Proxy settings

.. code-block:: python

   from evo_client.configuration import Configuration
   
   config = Configuration(
       host="https://api.yourgym.com",
       api_key={"ApiKeyAuth": "your-api-key"},
       logger_file="api.log",
       logger_format="%(asctime)s %(levelname)s %(message)s",
       proxy="http://proxy.local:8080"
   )

Models
------

.. toctree::
   :maxdepth: 1
   :caption: Data Models

   models/index

The SDK uses Pydantic models for request/response data:

.. code-block:: python

   from evo_client.models import MemberProfile
   
   # Models provide type validation and serialization
   profile = MemberProfile(
       first_name="John",
       last_name="Doe",
       email="john@example.com"
   )
   
   # Access data with IDE support
   print(f"Member: {profile.first_name} {profile.last_name}")
   
   # Serialize to JSON
   json_data = profile.model_dump_json()

Best Practices
------------

1. **Always use with context managers for cleanup**:

   .. code-block:: python

      with EvoClient() as client:
          api = MembersApi(client)
          result = api.some_operation()

2. **Configure appropriate timeouts**:

   .. code-block:: python

      client = EvoClient(
          api_key="your-key",
          timeout=30,  # 30 seconds
          connect_timeout=10  # 10 seconds for connection
      )

3. **Use pagination for large result sets**:

   .. code-block:: python

      results = []
      page = 1
      while True:
          batch = api.list_items(page=page, limit=100)
          if not batch:
              break
          results.extend(batch)
          page += 1

4. **Handle rate limits gracefully**:

   .. code-block:: python

      from evo_client.utils import retry_with_backoff
      
      @retry_with_backoff(max_retries=3)
      def get_data():
          return api.get_some_data()
