# evo_client.StatesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_states**](StatesApi.md#get_states) | **GET** /api/v1/states | Retrieve a list of available states/provinces

# **get_states**
> get_states(async_req=False)

### Description

Retrieve a list of available states or provinces.

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.StatesApi(evo_client.ApiClient(configuration))

try:
    # Retrieve list of states
    api_response = api_instance.get_states(async_req=False)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatesApi->get_states: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional] [default to False]

### Return type

**list[State]** – A list of state objects containing details such as:
- State ID
- State name
- State abbreviation
- Country information

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
