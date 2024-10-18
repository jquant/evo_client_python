# swagger_client.EntriesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_entries_get**](EntriesApi.md#api_v1_entries_get) | **GET** /api/v1/entries | Get Entries

# **api_v1_entries_get**
> list[EntradasResumoApiViewModel] api_v1_entries_get(register_date_start=register_date_start, register_date_end=register_date_end, take=take, skip=skip, id_entry=id_entry, id_member=id_member)

Get Entries

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
api_instance = swagger_client.EntriesApi(swagger_client.ApiClient(configuration))
register_date_start = '2013-10-20T19:20:30+01:00' # datetime | DateTime date start (optional)
register_date_end = '2013-10-20T19:20:30+01:00' # datetime | DateTime date end (optional)
take = 50 # int | Total number of records to return. (Maximum of 1000) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
id_entry = 0 # int | ID of the entry to return. (optional) (default to 0)
id_member = 56 # int | ID of the member to return (optional)

try:
    # Get Entries
    api_response = api_instance.api_v1_entries_get(register_date_start=register_date_start, register_date_end=register_date_end, take=take, skip=skip, id_entry=id_entry, id_member=id_member)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EntriesApi->api_v1_entries_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **register_date_start** | **datetime**| DateTime date start | [optional] 
 **register_date_end** | **datetime**| DateTime date end | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 1000) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **id_entry** | **int**| ID of the entry to return. | [optional] [default to 0]
 **id_member** | **int**| ID of the member to return | [optional] 

### Return type

[**list[EntradasResumoApiViewModel]**](EntradasResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

