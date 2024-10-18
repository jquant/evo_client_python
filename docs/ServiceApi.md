# swagger_client.ServiceApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_service_get**](ServiceApi.md#api_v1_service_get) | **GET** /api/v1/service | Get Services

# **api_v1_service_get**
> list[ServicosResumoApiViewModel] api_v1_service_get(id_service=id_service, name=name, id_branch=id_branch, take=take, skip=skip, active=active)

Get Services

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
api_instance = swagger_client.ServiceApi(swagger_client.ApiClient(configuration))
id_service = 56 # int | Filter by Service Id (optional)
name = 'name_example' # str |  (optional)
id_branch = 56 # int | Filber by service IdBranch (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25 # int | Total number of records to return. (Maximum of 50) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
active = true # bool | Filter by active/inactive services (optional)

try:
    # Get Services
    api_response = api_instance.api_v1_service_get(id_service=id_service, name=name, id_branch=id_branch, take=take, skip=skip, active=active)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceApi->api_v1_service_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_service** | **int**| Filter by Service Id | [optional] 
 **name** | **str**|  | [optional] 
 **id_branch** | **int**| Filber by service IdBranch (Only available when using a multilocation key, ignored otherwise) | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **active** | **bool**| Filter by active/inactive services | [optional] 

### Return type

[**list[ServicosResumoApiViewModel]**](ServicosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

