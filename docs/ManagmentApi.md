# evo_client.ManagementApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_active_clients**](ManagmentApi.md#get_active_clients) | **GET** /api/v1/management/activeclients | Get active Clients
[**get_prospects**](ManagmentApi.md#get_prospects) | **GET** /api/v1/management/prospects | Get Prospects
[**get_non_renewed_clients**](ManagmentApi.md#get_non_renewed_clients) | **GET** /api/v1/management/not-renewed | Get non-renewed Clients

# **get_active_clients**
> list[ClientesAtivosViewModel] get_active_clients()

Get active Clients

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
api_instance = evo_client.ManagementApi(evo_client.ApiClient(configuration))

try:
    # Get active Clients
    api_response = api_instance.get_active_clients()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagementApi->get_active_clients: %s\n" % e)
```

### Parameters
This endpoint does not need any parameters.

### Return type

[**list[ClientesAtivosViewModel]**](ClientesAtivosViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_prospects**
> list[SpsRelProspectsCadastradosConvertidos] get_prospects(dt_start=dt_start, dt_end=dt_end)

Get Prospects

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
api_instance = evo_client.ManagementApi(evo_client.ApiClient(configuration))
dt_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
dt_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

try:
    # Get Prospects
    api_response = api_instance.get_prospects(dt_start=dt_start, dt_end=dt_end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagementApi->get_prospects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**dt_start** | **datetime**| Start date filter | [optional] 
**dt_end** | **datetime**| End date filter | [optional] 

### Return type

[**list[SpsRelProspectsCadastradosConvertidos]**](SpsRelProspectsCadastradosConvertidos.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_non_renewed_clients**
> list[ContratoNaoRenovadosViewModel] get_non_renewed_clients(dt_start=dt_start, dt_end=dt_end)

Get non-renewed Clients

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
api_instance = evo_client.ManagementApi(evo_client.ApiClient(configuration))
dt_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
dt_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

try:
    # Get non-renewed Clients
    api_response = api_instance.get_non_renewed_clients(dt_start=dt_start, dt_end=dt_end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagementApi->get_non_renewed_clients: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**dt_start** | **datetime**| Start date filter | [optional] 
**dt_end** | **datetime**| End date filter | [optional] 

### Return type

[**list[ContratoNaoRenovadosViewModel]**](ContratoNaoRenovadosViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
