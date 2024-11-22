# evo_client.MembersApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_members_auth_post**](MembersApi.md#api_v1_members_auth_post) | **POST** /api/v1/members/auth | Authenticate member
[**api_v1_members_basic_get**](MembersApi.md#api_v1_members_basic_get) | **GET** /api/v1/members/basic | Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.
[**api_v1_members_fitcoins_get**](MembersApi.md#api_v1_members_fitcoins_get) | **GET** /api/v1/members/fitcoins | Get member fitcoins
[**api_v1_members_fitcoins_put**](MembersApi.md#api_v1_members_fitcoins_put) | **PUT** /api/v1/members/fitcoins | Update a member fitcoins
[**api_v1_members_get**](MembersApi.md#api_v1_members_get) | **GET** /api/v1/members | Get members
[**api_v1_members_id_member_card_put**](MembersApi.md#api_v1_members_id_member_card_put) | **PUT** /api/v1/members/{idMember}/card | Update a member card number
[**api_v1_members_id_member_get**](MembersApi.md#api_v1_members_id_member_get) | **GET** /api/v1/members/{idMember} | Get member profile
[**api_v1_members_reset_password_get**](MembersApi.md#api_v1_members_reset_password_get) | **GET** /api/v1/members/resetPassword | Get link for reset password
[**api_v1_members_services_get**](MembersApi.md#api_v1_members_services_get) | **GET** /api/v1/members/services | Get member services
[**api_v1_members_transfer_post**](MembersApi.md#api_v1_members_transfer_post) | **POST** /api/v1/members/transfer | 
[**member_data_id_member_patch**](MembersApi.md#member_data_id_member_patch) | **PATCH** /api/v1/members/update-member-data/{idMember} | Update basic member data

# **api_v1_members_auth_post**
> MemberAuthenticateViewModel api_v1_members_auth_post(email=email, password=password, change_password=change_password)

Authenticate member

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
email = 'email_example' # str | Member e-mail (optional)
password = 'password_example' # str | Member password (optional)
change_password = true # bool | Check true if the password has not been set, create a new one (optional)

try:
    # Authenticate member
    api_response = api_instance.api_v1_members_auth_post(email=email, password=password, change_password=change_password)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_auth_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **str**| Member e-mail | [optional] 
 **password** | **str**| Member password | [optional] 
 **change_password** | **bool**| Check true if the password has not been set, create a new one | [optional] 

### Return type

[**MemberAuthenticateViewModel**](MemberAuthenticateViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_basic_get**
> MembersBasicApiViewModel api_v1_members_basic_get(email=email, document=document, phone=phone, id_member=id_member, take=take, skip=skip)

Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
email = 'email_example' # str | Filter by a member e-mail (optional)
document = 'document_example' # str | Filter by a member document (optional)
phone = 'phone_example' # str | Filter by a member telephone or cellphone Ex.:1112341234 (optional)
id_member = 56 # int | Filter by member id (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.
    api_response = api_instance.api_v1_members_basic_get(email=email, document=document, phone=phone, id_member=id_member, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_basic_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **str**| Filter by a member e-mail | [optional] 
 **document** | **str**| Filter by a member document | [optional] 
 **phone** | **str**| Filter by a member telephone or cellphone Ex.:1112341234 | [optional] 
 **id_member** | **int**| Filter by member id | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**MembersBasicApiViewModel**](MembersBasicApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_fitcoins_get**
> api_v1_members_fitcoins_get(id_member=id_member)

Get member fitcoins

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
id_member = 56 # int | Id Member (optional)

try:
    # Get member fitcoins
    api_instance.api_v1_members_fitcoins_get(id_member=id_member)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_fitcoins_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Id Member | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_fitcoins_put**
> api_v1_members_fitcoins_put(id_member=id_member, type=type, fitcoin=fitcoin, reason=reason)

Update a member fitcoins

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
id_member = 56 # int | Id Member (optional)
type = 56 # int | 1 - Add Fitcoins, 2 - Remove Fitcoins (optional)
fitcoin = 56 # int | Quantity add/remove fitcoin (optional)
reason = 'reason_example' # str | Reason add/remove fitcoin (optional)

try:
    # Update a member fitcoins
    api_instance.api_v1_members_fitcoins_put(id_member=id_member, type=type, fitcoin=fitcoin, reason=reason)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_fitcoins_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Id Member | [optional] 
 **type** | **int**| 1 - Add Fitcoins, 2 - Remove Fitcoins | [optional] 
 **fitcoin** | **int**| Quantity add/remove fitcoin | [optional] 
 **reason** | **str**| Reason add/remove fitcoin | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_get**
> MembersApiViewModel api_v1_members_get(name=name, email=email, document=document, phone=phone, conversion_date_start=conversion_date_start, conversion_date_end=conversion_date_end, register_date_start=register_date_start, register_date_end=register_date_end, membership_start_date_start=membership_start_date_start, membership_start_date_end=membership_start_date_end, membership_cancel_date_start=membership_cancel_date_start, membership_cancel_date_end=membership_cancel_date_end, status=status, token_gympass=token_gympass, take=take, skip=skip, ids_members=ids_members, only_personal=only_personal, personal_type=personal_type, show_activity_data=show_activity_data)

Get members

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
name = 'name_example' # str | Filter by members name (optional)
email = 'email_example' # str | Filter by a member e-mail (optional)
document = 'document_example' # str | Filter by a member document (optional)
phone = 'phone_example' # str | Filter by a member telephone or cellphone Ex.:1112341234 (optional)
conversion_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by a member conversion date starting in: (yyyy-mm-dd) (optional)
conversion_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by a member conversion date ending in: (yyyy-mm-dd) (optional)
register_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by a member register date starting in: (yyyy-mm-dd) (optional)
register_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by a member register date ending in: (yyyy-mm-dd) (optional)
membership_start_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by a membership start date from: (yyyy-mm-dd) (optional)
membership_start_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by a membership start date to: (yyyy-mm-dd) (optional)
membership_cancel_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by a membership cancel date from: (yyyy-mm-dd) (optional)
membership_cancel_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by a membership cancel date to: (yyyy-mm-dd) (optional)
status = 56 # int | Filter by a member state: 1 - Active (Suspendeds and Vips included), 2 - Inactive (optional)
token_gympass = 'token_gympass_example' # str | Filter by the member gympass token gympass (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
ids_members = 'ids_members_example' # str | Filter by member ids. Add member ids separated by comma. Example: 1,2,3 (optional)
only_personal = false # bool | Show only personal trainers (optional) (default to false)
personal_type = 56 # int | Filter by personal type: 1 - Internal, 2 - External (optional)
show_activity_data = false # bool |  (optional) (default to false)

try:
    # Get members
    api_response = api_instance.api_v1_members_get(name=name, email=email, document=document, phone=phone, conversion_date_start=conversion_date_start, conversion_date_end=conversion_date_end, register_date_start=register_date_start, register_date_end=register_date_end, membership_start_date_start=membership_start_date_start, membership_start_date_end=membership_start_date_end, membership_cancel_date_start=membership_cancel_date_start, membership_cancel_date_end=membership_cancel_date_end, status=status, token_gympass=token_gympass, take=take, skip=skip, ids_members=ids_members, only_personal=only_personal, personal_type=personal_type, show_activity_data=show_activity_data)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Filter by members name | [optional] 
 **email** | **str**| Filter by a member e-mail | [optional] 
 **document** | **str**| Filter by a member document | [optional] 
 **phone** | **str**| Filter by a member telephone or cellphone Ex.:1112341234 | [optional] 
 **conversion_date_start** | **datetime**| Filter by a member conversion date starting in: (yyyy-mm-dd) | [optional] 
 **conversion_date_end** | **datetime**| Filter by a member conversion date ending in: (yyyy-mm-dd) | [optional] 
 **register_date_start** | **datetime**| Filter by a member register date starting in: (yyyy-mm-dd) | [optional] 
 **register_date_end** | **datetime**| Filter by a member register date ending in: (yyyy-mm-dd) | [optional] 
 **membership_start_date_start** | **datetime**| Filter by a membership start date from: (yyyy-mm-dd) | [optional] 
 **membership_start_date_end** | **datetime**| Filter by a membership start date to: (yyyy-mm-dd) | [optional] 
 **membership_cancel_date_start** | **datetime**| Filter by a membership cancel date from: (yyyy-mm-dd) | [optional] 
 **membership_cancel_date_end** | **datetime**| Filter by a membership cancel date to: (yyyy-mm-dd) | [optional] 
 **status** | **int**| Filter by a member state: 1 - Active (Suspendeds and Vips included), 2 - Inactive | [optional] 
 **token_gympass** | **str**| Filter by the member gympass token gympass | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **ids_members** | **str**| Filter by member ids. Add member ids separated by comma. Example: 1,2,3 | [optional] 
 **only_personal** | **bool**| Show only personal trainers | [optional] [default to false]
 **personal_type** | **int**| Filter by personal type: 1 - Internal, 2 - External | [optional] 
 **show_activity_data** | **bool**|  | [optional] [default to false]

### Return type

[**MembersApiViewModel**](MembersApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_id_member_card_put**
> api_v1_members_id_member_card_put(id_member, card_number=card_number)

Update a member card number

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
id_member = 56 # int | Filter by a member
card_number = 'card_number_example' # str | Card number (optional)

try:
    # Update a member card number
    api_instance.api_v1_members_id_member_card_put(id_member, card_number=card_number)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_id_member_card_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Filter by a member | 
 **card_number** | **str**| Card number | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_id_member_get**
> ClienteDetalhesBasicosApiViewModel api_v1_members_id_member_get(id_member)

Get member profile

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
id_member = 56 # int | Filter by a member

try:
    # Get member profile
    api_response = api_instance.api_v1_members_id_member_get(id_member)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_id_member_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Filter by a member | 

### Return type

[**ClienteDetalhesBasicosApiViewModel**](ClienteDetalhesBasicosApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_reset_password_get**
> MemberAuthenticateViewModel api_v1_members_reset_password_get(sign_in=sign_in, user=user)

Get link for reset password

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
sign_in = true # bool | Check true if after change password you want sign in (optional)
user = 'user_example' # str | Filter by CPF, idMember or e-mail (optional)

try:
    # Get link for reset password
    api_response = api_instance.api_v1_members_reset_password_get(sign_in=sign_in, user=user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_reset_password_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sign_in** | **bool**| Check true if after change password you want sign in | [optional] 
 **user** | **str**| Filter by CPF, idMember or e-mail | [optional] 

### Return type

[**MemberAuthenticateViewModel**](MemberAuthenticateViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_services_get**
> list[MemberServiceViewModel] api_v1_members_services_get(id_member=id_member)

Get member services

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
id_member = 56 # int | Filter by member id (optional)

try:
    # Get member services
    api_response = api_instance.api_v1_members_services_get(id_member=id_member)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_services_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Filter by member id | [optional] 

### Return type

[**list[MemberServiceViewModel]**](MemberServiceViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_members_transfer_post**
> api_v1_members_transfer_post(body=body)



### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
body = evo_client.ClienteTransferenciaViewModel() # ClienteTransferenciaViewModel |  (optional)

try:
    api_instance.api_v1_members_transfer_post(body=body)
except ApiException as e:
    print("Exception when calling MembersApi->api_v1_members_transfer_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ClienteTransferenciaViewModel**](ClienteTransferenciaViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **member_data_id_member_patch**
> bool member_data_id_member_patch(id_member, body=body)

Update basic member data

Example body                     Body           {              {                  \"idContactType\": 1, { 1 = Telephone, 2 = Cellphone}              }              \"gender\": \"string\", { \"M\" = Male, \"F\" = Female, \"P\" = Other }              \"idState\": 0 {1 = AC, 2 = AL, 3 = AP, 4 = AM, 5 = BA, 6 = CE, 7 = DF, 8 = ES, 9 = GO, 10 = MA, 11 = MT, 12 = MS, 13 = MG, 14 = PA, 15 = PB, 16 = PR, 17 = PE, 18 = PI, 19 = RJ, 20 = RN, 21 = RS, 22 = RO, 23 = RR, 24 = SC, 25 = SP, 26 = SE, 27 = TO}            }

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.MembersApi(evo_client.ApiClient(configuration))
id_member = 56 # int | 
body = evo_client.MemberDataViewModel() # MemberDataViewModel |  (optional)

try:
    # Update basic member data
    api_response = api_instance.member_data_id_member_patch(id_member, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembersApi->member_data_id_member_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**|  | 
 **body** | [**MemberDataViewModel**](MemberDataViewModel.md)|  | [optional] 

### Return type

**bool**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

