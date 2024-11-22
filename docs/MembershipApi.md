# evo_client.MembershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_membership_category_get**](MembershipApi.md#api_v1_membership_category_get) | **GET** /api/v1/membership/category | Get Memberships Categories
[**api_v1_membership_get**](MembershipApi.md#api_v1_membership_get) | **GET** /api/v1/membership | Get Memberships

# **api_v1_membership_category_get**
> list[W12UtilsCategoryMembershipViewModel] api_v1_membership_category_get()

Get Memberships Categories

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
    # Get Memberships Categories
    api_response = api_instance.api_v1_membership_category_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipApi->api_v1_membership_category_get: %s\n" % e)
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

# **api_v1_membership_get**
> list[ContratosResumoApiViewModel] api_v1_membership_get(id_membership=id_membership, name=name, id_branch=id_branch, take=take, skip=skip, active=active)

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
id_membership = 56 # int | Filter by membership Id (optional)
name = 'name_example' # str |  (optional)
id_branch = 56 # int | Filber by membership IdBranch (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25 # int | Total number of records to return. (Maximum of 50) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
active = true # bool | Filter by active/inactive memberships (optional)

try:
    # Get Memberships
    api_response = api_instance.api_v1_membership_get(id_membership=id_membership, name=name, id_branch=id_branch, take=take, skip=skip, active=active)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipApi->api_v1_membership_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_membership** | **int**| Filter by membership Id | [optional] 
 **name** | **str**|  | [optional] 
 **id_branch** | **int**| Filber by membership IdBranch (Only available when using a multilocation key, ignored otherwise) | [optional] 
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

