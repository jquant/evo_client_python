# evo_client.MembersApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authenticate_member**](MembersApi.md#authenticate_member) | **POST** /api/v1/members/auth | Authenticate member
[**get_basic_info**](MembersApi.md#get_basic_info) | **GET** /api/v1/members/basic | Get basic member information
[**get_fitcoins**](MembersApi.md#get_fitcoins) | **GET** /api/v1/members/fitcoins | Get member fitcoins
[**update_fitcoins**](MembersApi.md#update_fitcoins) | **PUT** /api/v1/members/fitcoins | Update member fitcoins
[**get_members**](MembersApi.md#get_members) | **GET** /api/v1/members | Get members list
[**update_member_card**](MembersApi.md#update_member_card) | **PUT** /api/v1/members/{idMember}/card | Update member card number
[**get_member_profile**](MembersApi.md#get_member_profile) | **GET** /api/v1/members/{idMember} | Get member profile
[**reset_password**](MembersApi.md#reset_password) | **GET** /api/v1/members/resetPassword | Get password reset link
[**get_member_services**](MembersApi.md#get_member_services) | **GET** /api/v1/members/services | Get member services
[**transfer_member**](MembersApi.md#transfer_member) | **POST** /api/v1/members/transfer | Transfer member to another branch
[**update_member_data**](MembersApi.md#update_member_data) | **PATCH** /api/v1/members/update-member-data/{idMember} | Update basic member data

# **authenticate_member**
> MemberAuthenticateViewModel authenticate_member(email: str, password: str, change_password: bool = False, async_req: bool = False)

Authenticate member.

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Authenticate member
    response = api_instance.authenticate_member(
        email="user@example.com",
        password="password123",
        change_password=False
    )
    print(response)
except Exception as e:
    print(f"Exception when calling authenticate_member: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**email** | **str** | Member email | 
**password** | **str** | Member password |
**change_password** | **bool** | True if password needs to be changed | [optional] [default to False]
**async_req** | **bool** | Execute request asynchronously | [optional] [default to False]

### Return type

[**MemberAuthenticateViewModel**](MemberAuthenticateViewModel.md)

# **get_basic_info**
> MembersBasicApiViewModel get_basic_info(email: str, document: str, phone: str, id_member: int, take: int = 50, skip: int = 0)

Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.
    response = api_instance.get_basic_info(
        email="user@example.com",
        document="1234567890",
        phone="1112341234",
        id_member=56
    )
    print(response)
except Exception as e:
    print(f"Exception when calling get_basic_info: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**email** | **str** | Filter by a member e-mail | 
**document** | **str** | Filter by a member document | 
**phone** | **str** | Filter by a member telephone or cellphone Ex.:1112341234 | 
**id_member** | **int** | Filter by member id | 
**take** | **int** | Total number of records to return. (Maximum of 50) | [optional] [default to 50]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]

### Return type

[**MembersBasicApiViewModel**](MembersBasicApiViewModel.md)

# **get_fitcoins**
> void get_fitcoins(id_member: int)

Get member fitcoins

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get member fitcoins
    api_instance.get_fitcoins(id_member=56)
except Exception as e:
    print(f"Exception when calling get_fitcoins: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Id Member | 

### Return type

void (empty response body)

# **update_fitcoins**
> void update_fitcoins(id_member: int, type: int, fitcoin: int, reason: str)

Update member fitcoins

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Update member fitcoins
    api_instance.update_fitcoins(
        id_member=56,
        type=1,
        fitcoin=56,
        reason="Reason for adding fitcoins"
    )
except Exception as e:
    print(f"Exception when calling update_fitcoins: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Id Member | 
**type** | **int** | 1 - Add Fitcoins, 2 - Remove Fitcoins | 
**fitcoin** | **int** | Quantity add/remove fitcoin | 
**reason** | **str** | Reason add/remove fitcoin | 

### Return type

void (empty response body)

# **get_members**
> MembersApiViewModel get_members(name: str, email: str, document: str, phone: str, conversion_date_start: datetime, conversion_date_end: datetime, register_date_start: datetime, register_date_end: datetime, membership_start_date_start: datetime, membership_start_date_end: datetime, membership_cancel_date_start: datetime, membership_cancel_date_end: datetime, status: int, token_gympass: str, take: int = 50, skip: int = 0, ids_members: str = None, only_personal: bool = False, personal_type: int = None, show_activity_data: bool = False)

Get members

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get members
    response = api_instance.get_members(
        name="John Doe",
        email="john@example.com",
        document="1234567890",
        phone="1112341234",
        conversion_date_start="2013-10-20T19:20:30+01:00",
        conversion_date_end="2013-10-20T19:20:30+01:00",
        register_date_start="2013-10-20T19:20:30+01:00",
        register_date_end="2013-10-20T19:20:30+01:00",
        membership_start_date_start="2013-10-20T19:20:30+01:00",
        membership_start_date_end="2013-10-20T19:20:30+01:00",
        membership_cancel_date_start="2013-10-20T19:20:30+01:00",
        membership_cancel_date_end="2013-10-20T19:20:30+01:00",
        status=1,
        token_gympass="gympass123",
        take=50,
        skip=0,
        ids_members="1,2,3",
        only_personal=False,
        personal_type=1,
        show_activity_data=False
    )
    print(response)
except Exception as e:
    print(f"Exception when calling get_members: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**name** | **str** | Filter by members name | 
**email** | **str** | Filter by a member e-mail | 
**document** | **str** | Filter by a member document | 
**phone** | **str** | Filter by a member telephone or cellphone Ex.:1112341234 | 
**conversion_date_start** | **datetime** | Filter by a member conversion date starting in: (yyyy-mm-dd) | 
**conversion_date_end** | **datetime** | Filter by a member conversion date ending in: (yyyy-mm-dd) | 
**register_date_start** | **datetime** | Filter by a member register date starting in: (yyyy-mm-dd) | 
**register_date_end** | **datetime** | Filter by a member register date ending in: (yyyy-mm-dd) | 
**membership_start_date_start** | **datetime** | Filter by a membership start date from: (yyyy-mm-dd) | 
**membership_start_date_end** | **datetime** | Filter by a membership start date to: (yyyy-mm-dd) | 
**membership_cancel_date_start** | **datetime** | Filter by a membership cancel date from: (yyyy-mm-dd) | 
**membership_cancel_date_end** | **datetime** | Filter by a membership cancel date to: (yyyy-mm-dd) | 
**status** | **int** | Filter by a member state: 1 - Active (Suspendeds and Vips included), 2 - Inactive | 
**token_gympass** | **str** | Filter by the member gympass token gympass | 
**take** | **int** | Total number of records to return. (Maximum of 50) | [optional] [default to 50]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]
**ids_members** | **str** | Filter by member ids. Add member ids separated by comma. Example: 1,2,3 | [optional]
**only_personal** | **bool** | Show only personal trainers | [optional] [default to False]
**personal_type** | **int** | Filter by personal type: 1 - Internal, 2 - External | [optional]
**show_activity_data** | **bool** |  | [optional] [default to False]

### Return type

[**MembersApiViewModel**](MembersApiViewModel.md)

# **update_member_card**
> void update_member_card(id_member: int, card_number: str)

Update member card number

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Update member card number
    api_instance.update_member_card(
        id_member=56,
        card_number="1234567890"
    )
except Exception as e:
    print(f"Exception when calling update_member_card: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by a member | 
**card_number** | **str** | Card number | [optional]

### Return type

void (empty response body)

# **get_member_profile**
> ClienteDetalhesBasicosApiViewModel get_member_profile(id_member: int)

Get member profile

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get member profile
    response = api_instance.get_member_profile(id_member=56)
    print(response)
except Exception as e:
    print(f"Exception when calling get_member_profile: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by a member | 

### Return type

[**ClienteDetalhesBasicosApiViewModel**](ClienteDetalhesBasicosApiViewModel.md)

# **reset_password**
> MemberAuthenticateViewModel reset_password(sign_in: bool, user: str)

Get password reset link

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get password reset link
    response = api_instance.reset_password(
        sign_in=True,
        user="1234567890"
    )
    print(response)
except Exception as e:
    print(f"Exception when calling reset_password: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**sign_in** | **bool** | Check true if after change password you want sign in | [optional]
**user** | **str** | Filter by CPF, idMember or e-mail | 

### Return type

[**MemberAuthenticateViewModel**](MemberAuthenticateViewModel.md)

# **get_member_services**
> list[MemberServiceViewModel] get_member_services(id_member: int)

Get member services

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get member services
    response = api_instance.get_member_services(id_member=56)
    print(response)
except Exception as e:
    print(f"Exception when calling get_member_services: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by member id | 

### Return type

[**list[MemberServiceViewModel]**](MemberServiceViewModel.md)

# **transfer_member**
> void transfer_member(body: ClienteTransferenciaViewModel)

Transfer member to another branch

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Transfer member to another branch
    api_instance.transfer_member(body=ClienteTransferenciaViewModel())
except Exception as e:
    print(f"Exception when calling transfer_member: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**body** | [**ClienteTransferenciaViewModel**](ClienteTransferenciaViewModel.md) |  | 

### Return type

void (empty response body)

# **update_member_data**
> bool update_member_data(id_member: int, body: MemberDataViewModel)

Update basic member data

Example body                     Body           {              {                  \"idContactType\": 1, { 1 = Telephone, 2 = Cellphone}              }              \"gender\": \"string\", { \"M\" = Male, \"F\" = Female, \"P\" = Other }              \"idState\": 0 {1 = AC, 2 = AL, 3 = AP, 4 = AM, 5 = BA, 6 = CE, 7 = DF, 8 = ES, 9 = GO, 10 = MA, 11 = MT, 12 = MS, 13 = MG, 14 = PA, 15 = PB, 16 = PR, 17 = PE, 18 = PI, 19 = RJ, 20 = RN, 21 = RS, 22 = RO, 23 = RR, 24 = SC, 25 = SP, 26 = SE, 27 = TO}            }

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Update basic member data
    response = api_instance.update_member_data(
        id_member=56,
        body=MemberDataViewModel()
    )
    print(response)
except Exception as e:
    print(f"Exception when calling update_member_data: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** |  | 
**body** | [**MemberDataViewModel**](MemberDataViewModel.md) |  | [optional]

### Return type

**bool**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

