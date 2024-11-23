# evo_client.PartnershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

## Methods

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_partnerships**](PartnershipApi.md#get_partnerships) | **GET** /api/v1/partnership | Get partnerships

## **get_partnerships**
> list[ConveniosApiViewModel] get_partnerships(status=status, description=description, dt_created=dt_created)

Get partnerships

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

# create an instance of the API class
api_instance = evo_client.PartnershipApi(evo_client.ApiClient(configuration))
status = 56 # int | Filter by status: 0 Both, 1 Active, 2 Inactive (optional)
description = 'description_example' # str | Filter by Partnership name (optional)
dt_created = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration date (optional)

try:
    # Get partnerships
    api_response = api_instance.get_partnerships(status=status, description=description, dt_created=dt_created)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PartnershipApi->get_partnerships: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **int**| Filter by status: 0 Both, 1 Active, 2 Inactive | [optional] 
 **description** | **str**| Filter by Partnership name | [optional] 
 **dt_created** | **datetime**| Filter by registration date | [optional] 

### Return type

[**list[ConveniosApiViewModel]**](ConveniosApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
# End of Selection
```
