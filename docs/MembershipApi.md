# evo_client.MembershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_categories**](MembershipApi.md#get_categories) | **GET** /api/v1/membership/category | Get Membership Categories
[**get_memberships**](MembershipApi.md#get_memberships) | **GET** /api/v1/membership | Get Memberships

# **get_categories**
> list[W12UtilsCategoryMembershipViewModel] get_categories()

Get Membership Categories

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
api_instance = evo_client.MembershipApi(evo_client.ApiClient(configuration))

try:
    # Get Membership Categories
    api_response = api_instance.get_categories()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipApi->get_categories: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[W12UtilsCategoryMembershipViewModel]**](W12UtilsCategoryMembershipViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_memberships**
> list[ContratosResumoApiViewModel] get_memberships(membership_id=membership_id, name=name, branch_id=branch_id, take=take, skip=skip, active=active)

Get Memberships

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
api_instance = evo_client.MembershipApi(evo_client.ApiClient(configuration))
membership_id = 56 # int | Filter by membership ID (optional)
name = 'name_example' # str |  (optional)
branch_id = 56 # int | Filter by branch ID (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25 # int | Total number of records to return. (Maximum of 50) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
active = True # bool | Filter by active/inactive memberships (optional)

try:
    # Get Memberships
    api_response = api_instance.get_memberships(membership_id=membership_id, name=name, branch_id=branch_id, take=take, skip=skip, active=active)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipApi->get_memberships: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **membership_id** | **int**| Filter by membership ID | [optional] 
 **name** | **str**|  | [optional] 
 **branch_id** | **int**| Filter by branch ID (Only available when using a multilocation key, ignored otherwise) | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **active** | **bool**| Filter by active/inactive memberships | [optional] 

### Return type

[**list[ContratosResumoApiViewModel]**](ContratosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
# End of Selection
```
