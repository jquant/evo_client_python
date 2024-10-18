# swagger_client.MemberMembershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_membermembership_cancellation_post**](MemberMembershipApi.md#api_v1_membermembership_cancellation_post) | **POST** /api/v1/membermembership/cancellation | Cancel MemberMembership
[**api_v1_membermembership_id_member_membership_get**](MemberMembershipApi.md#api_v1_membermembership_id_member_membership_get) | **GET** /api/v1/membermembership/{idMemberMembership} | Get summary of MemberMemberships by id
[**api_v2_membermembership_get**](MemberMembershipApi.md#api_v2_membermembership_get) | **GET** /api/v2/membermembership | Get summary of canceled MemberMemberships

# **api_v1_membermembership_cancellation_post**
> api_v1_membermembership_cancellation_post(id_member_membership=id_member_membership, id_member_branch=id_member_branch, cancellation_date=cancellation_date, reason_cancellation=reason_cancellation, notice_cancellaton=notice_cancellaton, cancel_future_releases=cancel_future_releases, cancel_future_sessions=cancel_future_sessions, convert_credit_days=convert_credit_days, schedule_cancellation=schedule_cancellation, schedule_cancellation_date=schedule_cancellation_date, add_fine=add_fine, value_fine=value_fine)

Cancel MemberMembership

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.MemberMembershipApi(swagger_client.ApiClient(configuration))
id_member_membership = 56 # int | Id MemberMembership (optional)
id_member_branch = 56 # int | Id Member Branch of Cancellation (optional)
cancellation_date = '2013-10-20T19:20:30+01:00' # datetime | Date of cancellation (optional)
reason_cancellation = 'reason_cancellation_example' # str | Reason of Cancellation (optional)
notice_cancellaton = '' # str | Notes of Cancellation (optional)
cancel_future_releases = false # bool | If 'true' all the releases will be canceled (optional) (default to false)
cancel_future_sessions = false # bool | If 'true' all the sessions will be canceled (optional) (default to false)
convert_credit_days = false # bool | Convert all remaining credits e days to use (optional) (default to false)
schedule_cancellation = false # bool | Activate or deactivate schedule cancellation date (optional) (default to false)
schedule_cancellation_date = '2013-10-20T19:20:30+01:00' # datetime | Date of Cancellation if ScheduleCancellation = 'true' (optional)
add_fine = false # bool | Activate or deactivate Fine (optional) (default to false)
value_fine = 1.2 # float | Value of Fine, to use param AddFine must have activated (optional)

try:
    # Cancel MemberMembership
    api_instance.api_v1_membermembership_cancellation_post(id_member_membership=id_member_membership, id_member_branch=id_member_branch, cancellation_date=cancellation_date, reason_cancellation=reason_cancellation, notice_cancellaton=notice_cancellaton, cancel_future_releases=cancel_future_releases, cancel_future_sessions=cancel_future_sessions, convert_credit_days=convert_credit_days, schedule_cancellation=schedule_cancellation, schedule_cancellation_date=schedule_cancellation_date, add_fine=add_fine, value_fine=value_fine)
except ApiException as e:
    print("Exception when calling MemberMembershipApi->api_v1_membermembership_cancellation_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member_membership** | **int**| Id MemberMembership | [optional] 
 **id_member_branch** | **int**| Id Member Branch of Cancellation | [optional] 
 **cancellation_date** | **datetime**| Date of cancellation | [optional] 
 **reason_cancellation** | **str**| Reason of Cancellation | [optional] 
 **notice_cancellaton** | **str**| Notes of Cancellation | [optional] 
 **cancel_future_releases** | **bool**| If &#x27;true&#x27; all the releases will be canceled | [optional] [default to false]
 **cancel_future_sessions** | **bool**| If &#x27;true&#x27; all the sessions will be canceled | [optional] [default to false]
 **convert_credit_days** | **bool**| Convert all remaining credits e days to use | [optional] [default to false]
 **schedule_cancellation** | **bool**| Activate or deactivate schedule cancellation date | [optional] [default to false]
 **schedule_cancellation_date** | **datetime**| Date of Cancellation if ScheduleCancellation &#x3D; &#x27;true&#x27; | [optional] 
 **add_fine** | **bool**| Activate or deactivate Fine | [optional] [default to false]
 **value_fine** | **float**| Value of Fine, to use param AddFine must have activated | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_membermembership_id_member_membership_get**
> MemberMembershipApiViewModel api_v1_membermembership_id_member_membership_get(id_member_membership)

Get summary of MemberMemberships by id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.MemberMembershipApi(swagger_client.ApiClient(configuration))
id_member_membership = 56 # int | Id MemberMembership

try:
    # Get summary of MemberMemberships by id
    api_response = api_instance.api_v1_membermembership_id_member_membership_get(id_member_membership)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MemberMembershipApi->api_v1_membermembership_id_member_membership_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member_membership** | **int**| Id MemberMembership | 

### Return type

[**MemberMembershipApiViewModel**](MemberMembershipApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v2_membermembership_get**
> list[ContratosCanceladosResumoApiViewModel] api_v2_membermembership_get(id_member=id_member, id_membership=id_membership, member_name=member_name, register_date_start=register_date_start, register_date_end=register_date_end, cancel_date_start=cancel_date_start, cancel_date_end=cancel_date_end, show_transfers=show_transfers, show_aggregators=show_aggregators, show_vips=show_vips, contract_type=contract_type, take=take, skip=skip)

Get summary of canceled MemberMemberships

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.MemberMembershipApi(swagger_client.ApiClient(configuration))
id_member = 56 # int |  (optional)
id_membership = 56 # int |  (optional)
member_name = 'member_name_example' # str |  (optional)
register_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
register_date_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
cancel_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
cancel_date_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
show_transfers = false # bool | Show transferred contracts. (optional) (default to false)
show_aggregators = false # bool | Show aggregators contracts. (optional) (default to false)
show_vips = false # bool | Show VIP category contracts. (optional) (default to false)
contract_type = 'contract_type_example' # str | Filter by a comma separated list of types of contract. types: 1 - Common, 3 - Plan extension, 4 - Locking extension, 5 - Monthly recurring, 6 - Recurring monthly with validity, 7 - Monthly recurring with automatic renewal, 8 - Additional dependent, 9 - Annual with a specific end, 10 - Additional contract (optional)
take = 25 # int | Total number of records to return. (Maximum of 25) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get summary of canceled MemberMemberships
    api_response = api_instance.api_v2_membermembership_get(id_member=id_member, id_membership=id_membership, member_name=member_name, register_date_start=register_date_start, register_date_end=register_date_end, cancel_date_start=cancel_date_start, cancel_date_end=cancel_date_end, show_transfers=show_transfers, show_aggregators=show_aggregators, show_vips=show_vips, contract_type=contract_type, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MemberMembershipApi->api_v2_membermembership_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**|  | [optional] 
 **id_membership** | **int**|  | [optional] 
 **member_name** | **str**|  | [optional] 
 **register_date_start** | **datetime**|  | [optional] 
 **register_date_end** | **datetime**|  | [optional] 
 **cancel_date_start** | **datetime**|  | [optional] 
 **cancel_date_end** | **datetime**|  | [optional] 
 **show_transfers** | **bool**| Show transferred contracts. | [optional] [default to false]
 **show_aggregators** | **bool**| Show aggregators contracts. | [optional] [default to false]
 **show_vips** | **bool**| Show VIP category contracts. | [optional] [default to false]
 **contract_type** | **str**| Filter by a comma separated list of types of contract. types: 1 - Common, 3 - Plan extension, 4 - Locking extension, 5 - Monthly recurring, 6 - Recurring monthly with validity, 7 - Monthly recurring with automatic renewal, 8 - Additional dependent, 9 - Annual with a specific end, 10 - Additional contract | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 25) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**list[ContratosCanceladosResumoApiViewModel]**](ContratosCanceladosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

