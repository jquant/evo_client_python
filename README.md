# EVO Client Python SDK 🚀

**Modern, Clean, and Powerful Python SDK for EVO API**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Async Support](https://img.shields.io/badge/async-supported-green.svg)](https://docs.python.org/3/library/asyncio.html)
[![Type Hints](https://img.shields.io/badge/type-hints-supported-brightgreen.svg)](https://docs.python.org/3/library/typing.html)

---

## 🎊 **FULLY REFACTORED: BUNDLER PROBLEM ELIMINATED!**

This SDK has been completely refactored to provide **clean, separate sync and async implementations**:

- ✅ **Real async/await** (no more fake AsyncResult)
- ✅ **Clean import patterns** (no more complex overloads)
- ✅ **Configuration helpers** (one-line setup)
- ✅ **Type-safe APIs** (no more confusing Union types)
- ✅ **Backward compatibility** (existing code still works)

---

## 📋 **Table of Contents**

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Authentication](#-authentication)
- [Usage Examples](#-usage-examples)
  - [Sync Usage](#sync-usage)  
  - [Async Usage](#async-usage)
  - [Configuration](#configuration)
- [Import Patterns](#-import-patterns)
- [Configuration Helpers](#-configuration-helpers)
- [Migration Guide](#-migration-guide)
- [API Reference](#-api-reference)
- [Examples](#-examples)

---

## 🚀 **Quick Start**

### Sync Usage (Simple & Direct)
```python
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncMembersApi
from evo_client.config import ConfigBuilder

# One-line configuration
config = ConfigBuilder.basic_auth("your_gym_dns", "your_secret_key")

# Clean sync usage
with SyncApiClient(config) as client:
    members_api = SyncMembersApi(client)
    members = members_api.get_members()
    print(f"Found {len(members)} members")
```

### Async Usage (Real async/await)
```python
import asyncio
from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncMembersApi, AsyncSalesApi
from evo_client.config import ConfigPresets

async def main():
    # Pre-configured setup
    config = ConfigPresets.gym_production()
    config.username = "your_gym_dns"
    config.password = "your_secret_key"
    
    # Real async with concurrent requests
    async with AsyncApiClient(config) as client:
        members_api = AsyncMembersApi(client)
        sales_api = AsyncSalesApi(client)
        
        # Execute requests concurrently
        members, sales = await asyncio.gather(
            members_api.get_members(),
            sales_api.get_sales()
        )
        
        print(f"Found {len(members)} members and {len(sales)} sales")

# Run the async function
asyncio.run(main())
```

---

## 📦 **Installation**

### Via pip (Recommended)
```bash
pip install git+https://github.com/jquant/evo_client_python
```

### Development Installation
```bash
git clone https://github.com/jquant/evo_client_python
cd evo_client_python
pip install -e .
```

### Requirements
- Python 3.7+
- aiohttp (for async support)
- requests (for sync support)

---

## 🔐 **Authentication**

EVO API uses **Basic Authentication** with your gym's DNS as username and Secret Key as password.

### Quick Setup
```python
from evo_client.config import ConfigBuilder

# Method 1: Direct setup
config = ConfigBuilder.basic_auth("your_gym_dns", "your_secret_key")

# Method 2: Environment variables (recommended)
# Set EVO_USERNAME and EVO_PASSWORD environment variables
config = ConfigBuilder.from_env()

# Method 3: Configuration presets
from evo_client.config import ConfigPresets
config = ConfigPresets.gym_production()  # or gym_development()
config.username = "your_gym_dns"
config.password = "your_secret_key"
```

---

## 💡 **Usage Examples**

### Sync Usage

#### Basic Member Management
```python
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncMembersApi
from evo_client.config import ConfigBuilder

config = ConfigBuilder.from_env()

with SyncApiClient(config) as client:
    members_api = SyncMembersApi(client)
    
    # Get all members
    members = members_api.get_members()
    
    # Get specific member
    member = members_api.get_member_by_id(member_id=123)
    
    # Search members
    search_results = members_api.search_members(search="John")
```

#### Multiple APIs in One Session
```python
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncMembersApi, SyncSalesApi, SyncActivitiesApi

with SyncApiClient(config) as client:
    # Create multiple API instances sharing the same client
    members_api = SyncMembersApi(client)
    sales_api = SyncSalesApi(client)
    activities_api = SyncActivitiesApi(client)
    
    # Use all APIs in the same session
    members = members_api.get_members()
    sales = sales_api.get_sales()
    activities = activities_api.get_activities()
```

### Async Usage

#### Basic Async Operations
```python
import asyncio
from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncMembersApi

async def get_members():
    config = ConfigBuilder.from_env()
    
    async with AsyncApiClient(config) as client:
        members_api = AsyncMembersApi(client)
        members = await members_api.get_members()
        return members

# Run the async function
members = asyncio.run(get_members())
```

#### Concurrent Requests (Real Async Power)
```python
import asyncio
from evo_client.aio import AsyncApiClient
from evo_client.aio.api import AsyncMembersApi, AsyncSalesApi, AsyncActivitiesApi

async def get_dashboard_data():
    config = ConfigBuilder.from_env()
    
    async with AsyncApiClient(config) as client:
        members_api = AsyncMembersApi(client)
        sales_api = AsyncSalesApi(client)
        activities_api = AsyncActivitiesApi(client)
        
        # Execute all requests concurrently
        members, sales, activities = await asyncio.gather(
            members_api.get_members(),
            sales_api.get_sales(),
            activities_api.get_activities()
        )
        
        return {
            "members": members,
            "sales": sales,
            "activities": activities
        }

# 3x faster than sequential requests!
dashboard = asyncio.run(get_dashboard_data())
```

### Configuration

#### Environment-Based Configuration (Recommended)
```bash
# .env file
EVO_USERNAME=your_gym_dns
EVO_PASSWORD=your_secret_key
EVO_HOST=https://evo-integracao-api.w12app.com.br
EVO_TIMEOUT=30
EVO_VERIFY_SSL=true
```

```python
from evo_client.config import ConfigBuilder

# Automatically loads from environment variables
config = ConfigBuilder.from_env()
```

#### Configuration Validation
```python
from evo_client.config import ConfigValidator

# Validate configuration before use
is_valid, errors, warnings = ConfigValidator.validate_config(config)

if not is_valid:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration is valid!")
```

---

## 🎯 **Import Patterns**

### 1. Clean & Simple (Recommended)
```python
# Main clients
from evo_client import SyncApiClient, AsyncApiClient

# Specific APIs
from evo_client.sync import SyncMembersApi, SyncSalesApi
from evo_client.aio import AsyncMembersApi, AsyncSalesApi

# Configuration helpers
from evo_client.config import ConfigBuilder, ConfigPresets
```

### 2. Module-Based
```python
# Import from specific modules
from evo_client.sync import SyncApiClient
from evo_client.aio import AsyncApiClient
from evo_client.sync.api import SyncMembersApi
from evo_client.aio.api import AsyncMembersApi
```

### 3. Backward Compatible (Existing Code)
```python
# Old imports still work!
from evo_client import ApiClient, MembersApi, SalesApi
# ApiClient is automatically mapped to SyncApiClient
```

---

## ⚙️ **Configuration Helpers**

### ConfigBuilder - Factory Methods
```python
from evo_client.config import ConfigBuilder

# Environment-based (recommended)
config = ConfigBuilder.from_env()

# Quick setups
config = ConfigBuilder.basic_auth("gym_dns", "secret_key")
config = ConfigBuilder.development()  # Dev-friendly defaults
config = ConfigBuilder.production()   # Production-optimized
```

### ConfigPresets - Instant Setup
```python
from evo_client.config import ConfigPresets

config = ConfigPresets.gym_development()    # Debug-friendly
config = ConfigPresets.gym_production()     # Security-focused
config = ConfigPresets.high_performance()   # Bulk operations
config = ConfigPresets.low_latency()        # Fast responses
config = ConfigPresets.testing()            # Test isolation
```

### QuickConfig - One-Line Setup
```python
from evo_client.config import QuickConfig

config = QuickConfig.gym_basic("gym_dns", "secret_key")
config = QuickConfig.local_dev()
```

---

## 🔄 **Migration Guide**

### From Old to New Sync API
```python
# OLD (Complex, confusing)
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
members = api_instance.get_members(async_req=False)  # Confusing!

# NEW (Clean, simple)
with SyncApiClient(config) as client:
    members_api = SyncMembersApi(client)
    members = members_api.get_members()  # No async_req parameter!
```

### From Fake Async to Real Async
```python
# OLD (Fake async with ThreadPool)
result = api_instance.get_members(async_req=True)  # Returns AsyncResult
members = result.get()  # Not real async!

# NEW (Real async/await)
async with AsyncApiClient(config) as client:
    members_api = AsyncMembersApi(client)
    members = await members_api.get_members()  # Real async!
```

### Configuration Migration
```python
# OLD (Manual setup)
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# NEW (One-line setup)
config = ConfigBuilder.basic_auth("YOUR_USERNAME", "YOUR_PASSWORD")
# or even better:
config = ConfigBuilder.from_env()  # Reads from environment
```

---

## 📚 **API Reference**

### Available APIs (22 Total)

**Member Management:**
- `MembersApi` - Member operations
- `MemberMembershipApi` - Member membership management
- `WorkoutApi` - Workout tracking
- `EmployeesApi` - Employee management

**Sales & Financial:**
- `SalesApi` - Sales operations
- `ReceivablesApi` - Accounts receivable
- `PayablesApi` - Accounts payable
- `InvoicesApi` - Invoice management
- `PixApi` - PIX payment integration
- `BankAccountsApi` - Bank account management
- `VoucherApi` - Voucher management

**Operations:**
- `ActivitiesApi` - Activity management
- `MembershipApi` - Membership types
- `EntriesApi` - Entry logging
- `ProspectsApi` - Prospect management

**System & Configuration:**
- `ConfigurationApi` - System configuration
- `StatesApi` - State management
- `ServiceApi` - Service operations
- `ManagementApi` - Management operations
- `NotificationsApi` - Notification system
- `WebhookApi` - Webhook management
- `PartnershipApi` - Partnership management

### Import All APIs
```python
# Sync APIs
from evo_client.sync.api import (
    SyncMembersApi, SyncSalesApi, SyncActivitiesApi,
    SyncMembershipApi, SyncReceivablesApi, SyncPayablesApi,
    # ... all 22 sync APIs available
)

# Async APIs  
from evo_client.aio.api import (
    AsyncMembersApi, AsyncSalesApi, AsyncActivitiesApi,
    AsyncMembershipApi, AsyncReceivablesApi, AsyncPayablesApi,
    # ... all 22 async APIs available
)
```

---

## 📝 **Examples**

### Comprehensive Examples Available

1. **Configuration Showcase** (`examples/v1/configuration_showcase.py`)
   - Environment-based configuration
   - Configuration presets and validation
   - Error prevention and helpful messages

2. **Modern Sync Example** (`examples/v2/modern_sync_example.py`)
   - Clean sync patterns
   - Multiple API usage
   - Error handling and resource management

3. **Modern Async Example** (`examples/v2/modern_async_example.py`)
   - Real async/await patterns
   - Concurrent requests
   - Resource management and connection pooling

4. **Migration Guide** (`examples/v2/migration_guide.py`)
   - Step-by-step migration from old to new patterns
   - Before/after comparisons
   - Risk-free upgrade path

### Run Examples
```bash
# Configuration examples
python examples/v1/configuration_showcase.py

# Modern sync patterns
python examples/v2/modern_sync_example.py

# Modern async patterns  
python examples/v2/modern_async_example.py

# Migration guide
python examples/v2/migration_guide.py
```

---

## 🧪 **Testing**

### Run Integration Tests
```bash
# Run all integration tests
python -m pytest test/integration/ -v

# Run specific test categories
python -m pytest test/integration/test_integration.py::TestPhase4ImportPatterns -v
python -m pytest test/integration/test_integration.py::TestPhase4ConfigurationHelpers -v
```

### Test Coverage
- ✅ **17 Integration Tests** - All import patterns and workflows
- ✅ **Configuration Helper Tests** - All 5 helper modules
- ✅ **Backward Compatibility Tests** - Legacy code continues to work
- ✅ **End-to-End Workflow Tests** - Both sync and async clients

---

## 🏆 **Key Achievements**

### Core Refactoring Success
- ✅ **22/22 APIs Converted** - 100% API coverage
- ✅ **107+ @overload decorators eliminated** - Simplified method signatures  
- ✅ **65+ async_req parameters eliminated** - No more confusing parameters
- ✅ **ThreadPool completely removed** - No more fake async
- ✅ **Real async/await implemented** - True asyncio integration

### User Experience Revolution  
- ✅ **3 Beautiful Import Patterns** - Clean, intuitive, backward compatible
- ✅ **5 Configuration Helper Modules** - One-line setup capabilities
- ✅ **7 Configuration Presets** - Common scenarios automated
- ✅ **Complete Migration Guide** - Risk-free upgrade path

### Quality Assurance Excellence
- ✅ **Type Safety** - Clean, intuitive APIs throughout
- ✅ **Error Prevention** - Configuration validation prevents issues
- ✅ **Backward Compatibility** - Legacy code continues to work
- ✅ **Performance Improvements** - Real async concurrency

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 **Support**

- **Documentation**: Check the `examples/` directory for comprehensive usage examples
- **Issues**: Open an issue on GitHub for bug reports or feature requests
- **Migration Help**: See `examples/v2/migration_guide.py` for upgrade assistance

---

## 🎯 **API Version**

- **API Version**: v1
- **Package Version**: 1.0.0  
- **Base URL**: `https://evo-integracao-api.w12app.com.br`

---

**🎊 The EVO Client Python SDK has been completely transformed from a confusing "bundler problem" into a clean, modern, and powerful toolkit for gym management integration!**


## Documentation for API Endpoints

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ActivitiesApi* | [**get_activities**](docs/ActivitiesApi.md#get_activities) | **GET** /api/v1/activities | Get activities
*ActivitiesApi* | [**get_schedule_detail**](docs/ActivitiesApi.md#get_schedule_detail) | **GET** /api/v1/activities/schedule/detail | Get activities schedule details
*ActivitiesApi* | [**enroll**](docs/ActivitiesApi.md#enroll) | **POST** /api/v1/activities/schedule/enroll | Enroll member in activity schedule
*ActivitiesApi* | [**get_schedule**](docs/ActivitiesApi.md#get_schedule) | **GET** /api/v1/activities/schedule | Get activities schedule
*ActivitiesApi* | [**create_experimental_class**](docs/ActivitiesApi.md#create_experimental_class) | **POST** /api/v1/activities/schedule/experimental-class | Create a new experimental class and enroll the member on it
*ActivitiesApi* | [**change_status**](docs/ActivitiesApi.md#change_status) | **POST** /api/v1/activities/schedule/enroll/change-status | Change status of a member in activity schedule
*ActivitiesApi* | [**get_unavailable_spots**](docs/ActivitiesApi.md#get_unavailable_spots) | **GET** /api/v1/activities/list-unavailable-spots | List of spots that are already filled in the activity session
*BankAccountsApi* | [**get_accounts**](docs/BankAccountsApi.md#get_accounts) | **GET** /api/v1/bank-accounts | Get bank accounts
*ConfigurationApi* | [**get_gateway_config**](docs/ConfigurationApi.md#get_gateway_config) | **GET** /api/v1/configuration/gateway | Get gateway configurations
*ConfigurationApi* | [**get_branch_config**](docs/ConfigurationApi.md#get_branch_config) | **GET** /api/v1/configuration | Get branch configurations
*ConfigurationApi* | [**get_occupations**](docs/ConfigurationApi.md#get_occupations) | **GET** /api/v1/configuration/occupation | Get Occupation
*ConfigurationApi* | [**get_card_flags**](docs/ConfigurationApi.md#get_card_flags) | **GET** /api/v1/configuration/card-flags | Get card flag
*ConfigurationApi* | [**get_translations**](docs/ConfigurationApi.md#get_translations) | **GET** /api/v1/configuration/card-translation | Get card translation
*EmployeesApi* | [**delete_employee**](docs/EmployeesApi.md#delete_employee) | **DELETE** /api/v1/employees | Delete Employees
*EmployeesApi* | [**get_employees**](docs/EmployeesApi.md#get_employees) | **GET** /api/v1/employees | Get Employees
*EmployeesApi* | [**update_employee**](docs/EmployeesApi.md#update_employee) | **POST** /api/v1/employees | Update Employees
*EmployeesApi* | [**create_employee**](docs/EmployeesApi.md#create_employee) | **PUT** /api/v1/employees | Add Employees
*EntriesApi* | [**get_entries**](docs/EntriesApi.md#get_entries) | **GET** /api/v1/entries | Get Entries
*InvoicesApi* | [**get_invoices**](docs/InvoicesApi.md#get_invoices) | **GET** /api/v1/invoices/get-invoices | Get invoices by date
*ManagmentApi* | [**get_active_clients**](docs/ManagmentApi.md#get_active_clients) | **GET** /api/v1/managment/activeclients | Get active Clients
*ManagmentApi* | [**get_prospects**](docs/ManagmentApi.md#get_prospects) | **GET** /api/v1/managment/prospects | Get Prospects
*ManagmentApi* | [**renewed_get**](docs/ManagmentApi.md#renewed_get) | **GET** /api/v1/managment/not-renewed | Get non-renewed Clients
*MemberMembershipApi* | [**cancel_membership**](docs/MemberMembershipApi.md#cancel_membership) | **POST** /api/v1/membermembership/cancellation | Cancel MemberMembership
*MemberMembershipApi* | [**get_membership**](docs/MemberMembershipApi.md#get_membership) | **GET** /api/v1/membermembership/{idMemberMembership} | Get summary of MemberMemberships by id
*MemberMembershipApi* | [**get_canceled_member_memberships**](docs/MemberMembershipApi.md#get_canceled_member_memberships) | **GET** /api/v2/membermembership | Get summary of canceled MemberMemberships
*MembersApi* | [**authenticate_member**](docs/MembersApi.md#authenticate_member) | **POST** /api/v1/members/auth | Authenticate member
*MembersApi* | [**get_basic_info**](docs/MembersApi.md#get_basic_info) | **GET** /api/v1/members/basic | Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.
*MembersApi* | [**get_fitcoins**](docs/MembersApi.md#get_fitcoins) | **GET** /api/v1/members/fitcoins | Get member fitcoins
*MembersApi* | [**update_fitcoins**](docs/MembersApi.md#update_fitcoins) | **PUT** /api/v1/members/fitcoins | Update a member fitcoins
*MembersApi* | [**get_members**](docs/MembersApi.md#get_members) | **GET** /api/v1/members | Get members
*MembersApi* | [**update_member_card**](docs/MembersApi.md#update_member_card) | **PUT** /api/v1/members/{idMember}/card | Update a member card number
*MembersApi* | [**get_member_profile**](docs/MembersApi.md#get_member_profile) | **GET** /api/v1/members/{idMember} | Get member profile
*MembersApi* | [**reset_password**](docs/MembersApi.md#reset_password) | **GET** /api/v1/members/resetPassword | Get link for reset password
*MembersApi* | [**get_member_services**](docs/MembersApi.md#get_member_services) | **GET** /api/v1/members/services | Get member services
*MembersApi* | [**transfer_member**](docs/MembersApi.md#transfer_member) | **POST** /api/v1/members/transfer | 
*MembersApi* | [**update_member_data**](docs/MembersApi.md#update_member_data) | **PATCH** /api/v1/members/update-member-data/{idMember} | Update basic member data
*MembershipApi* | [**get_categories**](docs/MembershipApi.md#get_categories) | **GET** /api/v1/membership/category | Get Memberships Categories
*MembershipApi* | [**get_memberships**](docs/MembershipApi.md#get_memberships) | **GET** /api/v1/membership | Get Memberships
*NotificationsApi* | [**create_notification**](docs/NotificationsApi.md#create_notification) | **POST** /api/v1/notifications | Insert a member notification
*PartnershipApi* | [**get_partnerships**](docs/PartnershipApi.md#get_partnerships) | **GET** /api/v1/partnership | Get partnerships
*PayablesApi* | [**get_cost_center**](docs/PayablesApi.md#get_cost_center) | **GET** /api/v1/costcenter | Get Cost Center
*PayablesApi* | [**get_payables**](docs/PayablesApi.md#get_payables) | **GET** /api/v1/payables | Get payables
*PixApi* | [**get_qr_code**](docs/PixApi.md#get_qr_code) | **GET** /api/v1/pix/qr-code | Get Qr-code
*ProspectsApi* | [**get_prospects**](docs/ProspectsApi.md#get_prospects) | **GET** /api/v1/prospects | Get prospects
*ProspectsApi* | [**create_prospect**](docs/ProspectsApi.md#create_prospect) | **POST** /api/v1/prospects | Add prospects
*ProspectsApi* | [**update_prospect**](docs/ProspectsApi.md#update_prospect) | **PUT** /api/v1/prospects | Update prospect
*ProspectsApi* | [**get_services**](docs/ProspectsApi.md#get_services) | **GET** /api/v1/prospects/services | Get prospect services
*ProspectsApi* | [**transfer_prospect**](docs/ProspectsApi.md#transfer_prospect) | **POST** /api/v1/prospects/transfer | 
*ReceivablesApi* | [**get_receivables**](docs/ReceivablesApi.md#get_receivables) | **GET** /api/v1/receivables | Get receivables
*ReceivablesApi* | [**get_revenue_center**](docs/ReceivablesApi.md#get_revenue_center) | **GET** /api/v1/revenuecenter | Get Cost Center
*ReceivablesApi* | [**mark_received**](docs/ReceivablesApi.md#mark_received) | **PUT** /api/v1/receivables/mark-received | 
*SalesApi* | [**get_sale_by_id**](docs/SalesApi.md#get_sale_by_id) | **GET** /api/v1/sales/{idSale} | Get sale by Id
*SalesApi* | [**create_sale**](docs/SalesApi.md#create_sale) | **POST** /api/v1/sales | Create a new sale
*SalesApi* | [**get_sales**](docs/SalesApi.md#get_sales) | **GET** /api/v2/sales | Get sales
*SalesApi* | [**get_sales_items**](docs/SalesApi.md#get_sales_items) | **GET** /api/v1/sales/sales-items | Return itens for sale -&gt; site/totem
*SalesApi* | [**get_sales_by_session_id**](docs/SalesApi.md#get_sales_by_session_id) | **GET** /api/v1/sales/by-session-id | Get sales
*ServiceApi* | [**get_services**](docs/ServiceApi.md#get_services) | **GET** /api/v1/service | Get Services
*StatesApi* | [**get_states**](docs/StatesApi.md#get_states) | **GET** /api/v1/states | 
*VoucherApi* | [**get_vouchers**](docs/VoucherApi.md#get_vouchers) | **GET** /api/v1/voucher | Get Vouchers
*WebhookApi* | [**delete_webhook**](docs/WebhookApi.md#delete_webhook) | **DELETE** /api/v1/webhook | Remove a specific webhook by id
*WebhookApi* | [**get_webhooks**](docs/WebhookApi.md#get_webhooks) | **GET** /api/v1/webhook | List all webhooks created
*WebhookApi* | [**create_webhook**](docs/WebhookApi.md#create_webhook) | **POST** /api/v1/webhook | Add new webhook
*WorkoutApi* | [**update_workout**](docs/WorkoutApi.md#update_workout) | **PUT** /api/v1/workout | Change data from a client&#x27;s prescribed workout
*WorkoutApi* | [**get_client_workouts**](docs/WorkoutApi.md#get_client_workouts) | **GET** /api/v1/workout/default-client-workout | Get All Client&#x27;s or Prospect&#x27;s or Employee&#x27;s workouts
*WorkoutApi* | [**get_workouts_by_month_year_professor**](docs/WorkoutApi.md#get_workouts_by_month_year_professor) | **GET** /api/v1/workout/workout-monthyear-professor | Get All Client&#x27;s or Prospect&#x27;s or Employee&#x27;s workouts by Month, Year or idProfessor
*WorkoutApi* | [**get_default_workouts**](docs/WorkoutApi.md#get_default_workouts) | **GET** /api/v1/workout/default-workout | Get All default Workouts
*WorkoutApi* | [**link_workout_to_client**](docs/WorkoutApi.md#link_workout_to_client) | **POST** /api/v1/workout/link-workout-to-client | Link Workout for Client


## Documentation For Models

 - [AtividadeAgendaApiViewModel](docs/AtividadeAgendaApiViewModel.md)
 - [AtividadeBasicoApiViewModel](docs/AtividadeBasicoApiViewModel.md)
 - [AtividadeListApiViewModel](docs/AtividadeListApiViewModel.md)
 - [AtividadeLugarReservaApiViewModel](docs/AtividadeLugarReservaApiViewModel.md)
 - [AtividadeLugarReservaViewModel](docs/AtividadeLugarReservaViewModel.md)
 - [AtividadeSessaoParticipanteApiViewModel](docs/AtividadeSessaoParticipanteApiViewModel.md)
 - [BandeirasBasicoViewModel](docs/BandeirasBasicoViewModel.md)
 - [BankAccountsViewModel](docs/BankAccountsViewModel.md)
 - [BasicFreezeViewModel](docs/BasicFreezeViewModel.md)
 - [BasicMemberMembershipApiViewModel](docs/BasicMemberMembershipApiViewModel.md)
 - [BonusSessionViewModel](docs/BonusSessionViewModel.md)
 - [BusinessHoursViewModel](docs/BusinessHoursViewModel.md)
 - [CardDataViewModel](docs/CardDataViewModel.md)
 - [ClienteDetalhesBasicosApiViewModel](docs/ClienteDetalhesBasicosApiViewModel.md)
 - [ClienteEnotasRetorno](docs/ClienteEnotasRetorno.md)
 - [ClienteTransferenciaViewModel](docs/ClienteTransferenciaViewModel.md)
 - [ClientesAtivosViewModel](docs/ClientesAtivosViewModel.md)
 - [ConfiguracaoApiViewModel](docs/ConfiguracaoApiViewModel.md)
 - [ContratoEntradasApiViewModel](docs/ContratoEntradasApiViewModel.md)
 - [ContratoFiliaisResumoApiViewModel](docs/ContratoFiliaisResumoApiViewModel.md)
 - [ContratoNaoRenovadosViewModel](docs/ContratoNaoRenovadosViewModel.md)
 - [ContratosCanceladosParcelasApiViewModel](docs/ContratosCanceladosParcelasApiViewModel.md)
 - [ContratosCanceladosResumoApiViewModel](docs/ContratosCanceladosResumoApiViewModel.md)
 - [ContratosResumoApiViewModel](docs/ContratosResumoApiViewModel.md)
 - [ContratosResumoPaginaVendaViewModel](docs/ContratosResumoPaginaVendaViewModel.md)
 - [ConveniosApiViewModel](docs/ConveniosApiViewModel.md)
 - [CostCenterApiViewModel](docs/CostCenterApiViewModel.md)
 - [DadosContratoTrasnferenciaApiViewModel](docs/DadosContratoTrasnferenciaApiViewModel.md)
 - [DadosTrocaContratoApiViewModel](docs/DadosTrocaContratoApiViewModel.md)
 - [DiferenciaisApiViewModel](docs/DiferenciaisApiViewModel.md)
 - [DifferentialsViewModel](docs/DifferentialsViewModel.md)
 - [EFormaContato](docs/EFormaContato.md)
 - [EFormaPagamentoTotem](docs/EFormaPagamentoTotem.md)
 - [EOrigemAgendamento](docs/EOrigemAgendamento.md)
 - [EStatusAtividade](docs/EStatusAtividade.md)
 - [EStatusAtividadeSessao](docs/EStatusAtividadeSessao.md)
 - [ETipoContrato](docs/ETipoContrato.md)
 - [ETipoGateway](docs/ETipoGateway.md)
 - [EmployeeApiIntegracaoAtualizacaoViewModel](docs/EmployeeApiIntegracaoAtualizacaoViewModel.md)
 - [EmployeeApiIntegracaoViewModel](docs/EmployeeApiIntegracaoViewModel.md)
 - [EmpresasConveniosApiViewModel](docs/EmpresasConveniosApiViewModel.md)
 - [EmpresasFiliaisGatewayViewModel](docs/EmpresasFiliaisGatewayViewModel.md)
 - [EmpresasFiliaisOcupacaoViewModel](docs/EmpresasFiliaisOcupacaoViewModel.md)
 - [EnderecoEnotasRetorno](docs/EnderecoEnotasRetorno.md)
 - [EnotasRetorno](docs/EnotasRetorno.md)
 - [EntradasResumoApiViewModel](docs/EntradasResumoApiViewModel.md)
 - [FreezeViewModel](docs/FreezeViewModel.md)
 - [FuncionariosResumoApiViewModel](docs/FuncionariosResumoApiViewModel.md)
 - [HttpResponseError](docs/HttpResponseError.md)
 - [InstallmentViewModel](docs/InstallmentViewModel.md)
 - [LogTefApiViewModel](docs/LogTefApiViewModel.md)
 - [MemberAuthenticateViewModel](docs/MemberAuthenticateViewModel.md)
 - [MemberBasicResponsibleViewModel](docs/MemberBasicResponsibleViewModel.md)
 - [MemberDataViewModel](docs/MemberDataViewModel.md)
 - [MemberMembershipApiViewModel](docs/MemberMembershipApiViewModel.md)
 - [MemberNewSaleViewModel](docs/MemberNewSaleViewModel.md)
 - [MemberResponsibleViewModel](docs/MemberResponsibleViewModel.md)
 - [MemberServiceViewModel](docs/MemberServiceViewModel.md)
 - [MemberTransferViewModel](docs/MemberTransferViewModel.md)
 - [MembersApiViewModel](docs/MembersApiViewModel.md)
 - [MembersBasicApiViewModel](docs/MembersBasicApiViewModel.md)
 - [MetadadosEnotasRetorno](docs/MetadadosEnotasRetorno.md)
 - [MonthDiscountViewModel](docs/MonthDiscountViewModel.md)
 - [NewSaleViewModel](docs/NewSaleViewModel.md)
 - [NotificationApiViewModel](docs/NotificationApiViewModel.md)
 - [PayablesApiSubTypesViewModel](docs/PayablesApiSubTypesViewModel.md)
 - [PayablesApiViewModel](docs/PayablesApiViewModel.md)
 - [PeriodizacaoApiViewModel](docs/PeriodizacaoApiViewModel.md)
 - [PixPaymentDetailsViewModel](docs/PixPaymentDetailsViewModel.md)
 - [ProspectApiIntegracaoAtualizacaoViewModel](docs/ProspectApiIntegracaoAtualizacaoViewModel.md)
 - [ProspectApiIntegracaoViewModel](docs/ProspectApiIntegracaoViewModel.md)
 - [ProspectIdViewModel](docs/ProspectIdViewModel.md)
 - [ProspectResponsavelResumoApiViewModel](docs/ProspectResponsavelResumoApiViewModel.md)
 - [ProspectTransferenciaViewModel](docs/ProspectTransferenciaViewModel.md)
 - [ProspectsResumoApiViewModel](docs/ProspectsResumoApiViewModel.md)
 - [PublicoAtividadeViewModel](docs/PublicoAtividadeViewModel.md)
 - [ReceivablesApiSubTypesViewModel](docs/ReceivablesApiSubTypesViewModel.md)
 - [ReceivablesApiViewModel](docs/ReceivablesApiViewModel.md)
 - [ReceivablesCreditDetails](docs/ReceivablesCreditDetails.md)
 - [ReceivablesInvoiceApiViewModel](docs/ReceivablesInvoiceApiViewModel.md)
 - [ReceivablesMaskReceivedViewModel](docs/ReceivablesMaskReceivedViewModel.md)
 - [RevenueCenterApiViewModel](docs/RevenueCenterApiViewModel.md)
 - [SaleItensViewModel](docs/SaleItensViewModel.md)
 - [SalesItemViewModel](docs/SalesItemViewModel.md)
 - [SalesItemsViewModel](docs/SalesItemsViewModel.md)
 - [SalesViewModel](docs/SalesViewModel.md)
 - [ServiceDiscountViewModel](docs/ServiceDiscountViewModel.md)
 - [ServicoAdicionalApiViewModel](docs/ServicoAdicionalApiViewModel.md)
 - [ServicoAnualApiViewModel](docs/ServicoAnualApiViewModel.md)
 - [ServicoEnotasRetorno](docs/ServicoEnotasRetorno.md)
 - [ServicosResumoApiViewModel](docs/ServicosResumoApiViewModel.md)
 - [SpsRelProspectsCadastradosConvertidos](docs/SpsRelProspectsCadastradosConvertidos.md)
 - [TaxDataViewModel](docs/TaxDataViewModel.md)
 - [TelefoneApiViewModel](docs/TelefoneApiViewModel.md)
 - [VouchersResumoApiViewModel](docs/VouchersResumoApiViewModel.md)
 - [W12UtilsCategoryMembershipViewModel](docs/W12UtilsCategoryMembershipViewModel.md)
 - [W12UtilsWebhookHeaderViewModel](docs/W12UtilsWebhookHeaderViewModel.md)
 - [W12UtilsWebhookViewModel](docs/W12UtilsWebhookViewModel.md)
 - [W12UtilzWebHookFilterViewModel](docs/W12UtilzWebHookFilterViewModel.md)
 - [YearDiscountViewModel](docs/YearDiscountViewModel.md)

## Documentation For Authorization


## Basic

- **Type**: HTTP basic authentication


## Author


