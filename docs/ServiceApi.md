# evo_client.ServiceApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_services**](ServiceApi.md#get_services) | **GET** /api/v1/service | Get Services

# **get_services**
> list[ServicosResumoApiViewModel] get_services(service_id=service_id, name=name, branch_id=branch_id, take=take, skip=skip, active=active)

Get Services

### Example
```python
from __future__ import print_function
import time
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.ServiceApi(evo_client.ApiClient(configuration))
service_id = 56  # int | Filter by Service Id (optional)
name = 'name_example'  # str |  (optional)
branch_id = 56  # int | Filter by service branch ID (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25  # int | Total number of records to return. (Maximum of 50) (optional) (default to 25)
skip = 0  # int | Total number of records to skip. (optional) (default to 0)
active = True  # bool | Filter by active/inactive services (optional)

try:
    # Get Services
    api_response = api_instance.get_services(
        service_id=service_id,
        name=name,
        branch_id=branch_id,
        take=take,
        skip=skip,
        active=active
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceApi->get_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**service_id** | **int** | Filter by Service Id | [optional] 
**name** | **str** |  | [optional] 
**branch_id** | **int** | Filter by service branch ID (Only available when using a multilocation key, ignored otherwise) | [optional] 
**take** | **int** | Total number of records to return. (Maximum of 50) | [optional] [default to 25]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]
**active** | **bool** | Filter by active/inactive services | [optional] 

### Return type

[**list[ServicosResumoApiViewModel]**](ServicosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


