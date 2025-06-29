# Migration Guide: Old APIs → New Sync/Async APIs

## Overview

The EVO Client Python SDK has been completely refactored to eliminate the confusing "bundler pattern" and provide clean, separate sync and async implementations.

## What Changed

### ❌ Old Bundler Pattern (Deprecated)
```python
# Confusing async_req parameter 
from evo_client import MembersApi, ApiClient

api = MembersApi()
# Sync call
members = api.get_members(async_req=False)
# Async call  
future = api.get_members(async_req=True)
result = future.get()
```

### ✅ New Clean Implementation
```python
# 🔄 Clean Sync
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncMembersApi

with SyncApiClient() as client:
    members_api = SyncMembersApi(client)
    members = members_api.get_members()

# 🔄 Clean Async  
from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncMembersApi

async with AsyncApiClient() as client:
    members_api = AsyncMembersApi(client)
    members = await members_api.get_members()
```

## Migration Examples

### Members API
```python
# Old (deprecated)
from evo_client import MembersApi
api = MembersApi()
members = api.get_members()

# New sync
from evo_client.sync.api import SyncMembersApi
from evo_client.sync import SyncApiClient

with SyncApiClient() as client:
    api = SyncMembersApi(client)
    members = api.get_members()

# New async
from evo_client.aio.api import AsyncMembersApi
from evo_client.aio import AsyncApiClient

async with AsyncApiClient() as client:
    api = AsyncMembersApi(client)
    members = await api.get_members()
```

### Sales API
```python
# Old (deprecated)
from evo_client import SalesApi
api = SalesApi()
sales = api.get_sales()

# New sync
from evo_client.sync.api import SyncSalesApi
from evo_client.sync import SyncApiClient

with SyncApiClient() as client:
    api = SyncSalesApi(client)
    sales = api.get_sales()

# New async
from evo_client.aio.api import AsyncSalesApi
from evo_client.aio import AsyncApiClient

async with AsyncApiClient() as client:
    api = AsyncSalesApi(client)
    sales = await api.get_sales()
```

### Configuration
```python
# Configuration works the same way
from evo_client.config import ConfigBuilder
from evo_client.sync import SyncApiClient
from evo_client.aio import AsyncApiClient

# Environment-based config
config = ConfigBuilder.from_env()

# Works with both sync and async
with SyncApiClient(config) as sync_client:
    pass

async with AsyncApiClient(config) as async_client:
    pass
```

## Complete API Mapping

| Old API Class | New Sync API | New Async API |
|---------------|-------------|---------------|
| `ActivitiesApi` | `SyncActivitiesApi` | `AsyncActivitiesApi` |
| `BankAccountsApi` | `SyncBankAccountsApi` | `AsyncBankAccountsApi` |
| `EmployeesApi` | `SyncEmployeesApi` | `AsyncEmployeesApi` |
| `EntriesApi` | `SyncEntriesApi` | `AsyncEntriesApi` |
| `InvoicesApi` | `SyncInvoicesApi` | `AsyncInvoicesApi` |
| `ManagementApi` | `SyncManagementApi` | `AsyncManagementApi` |
| `MemberMembershipApi` | `SyncMemberMembershipApi` | `AsyncMemberMembershipApi` |
| `MembersApi` | `SyncMembersApi` | `AsyncMembersApi` |
| `MembershipApi` | `SyncMembershipApi` | `AsyncMembershipApi` |
| `NotificationsApi` | `SyncNotificationsApi` | `AsyncNotificationsApi` |
| `PartnershipApi` | `SyncPartnershipApi` | `AsyncPartnershipApi` |
| `PayablesApi` | `SyncPayablesApi` | `AsyncPayablesApi` |
| `PixApi` | `SyncPixApi` | `AsyncPixApi` |
| `ProspectsApi` | `SyncProspectsApi` | `AsyncProspectsApi` |
| `ReceivablesApi` | `SyncReceivablesApi` | `AsyncReceivablesApi` |
| `SalesApi` | `SyncSalesApi` | `AsyncSalesApi` |
| `ServiceApi` | `SyncServiceApi` | `AsyncServiceApi` |
| `StatesApi` | `SyncStatesApi` | `AsyncStatesApi` |
| `VoucherApi` | `SyncVoucherApi` | `AsyncVoucherApi` |
| `WebhookApi` | `SyncWebhookApi` | `AsyncWebhookApi` |
| `WorkoutApi` | `SyncWorkoutApi` | `AsyncWorkoutApi` |

## Benefits of Migration

✅ **No more confusing `async_req` parameters**  
✅ **Clear separation of sync vs async code**  
✅ **Better type safety and IDE support**  
✅ **Simpler error handling**  
✅ **Context manager support**  
✅ **Modern Python patterns**

## Timeline

- **Now**: Old APIs marked as deprecated with warnings
- **Next release**: Examples and documentation updated  
- **Future release**: Old APIs will be removed

## Need Help?

If you need help migrating your code, please:
1. Check the examples in the `examples/` directory
2. See the full documentation  
3. Open an issue on GitHub

The new APIs provide the same functionality with much cleaner interfaces! 