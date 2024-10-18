# swagger_client.ManagmentApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_managment_activeclients_get**](ManagmentApi.md#api_v1_managment_activeclients_get) | **GET** /api/v1/managment/activeclients | Get active Clients
[**api_v1_managment_prospects_get**](ManagmentApi.md#api_v1_managment_prospects_get) | **GET** /api/v1/managment/prospects | Get Prospects
[**renewed_get**](ManagmentApi.md#renewed_get) | **GET** /api/v1/managment/not-renewed | Get non-renewed Clients

# **api_v1_managment_activeclients_get**
> list[ClientesAtivosViewModel] api_v1_managment_activeclients_get()

Get active Clients

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
api_instance = swagger_client.ManagmentApi(swagger_client.ApiClient(configuration))

try:
    # Get active Clients
    api_response = api_instance.api_v1_managment_activeclients_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagmentApi->api_v1_managment_activeclients_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ClientesAtivosViewModel]**](ClientesAtivosViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_managment_prospects_get**
> list[SpsRelProspectsCadastradosConvertidos] api_v1_managment_prospects_get(dt_start=dt_start, dt_end=dt_end)

Get Prospects

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
api_instance = swagger_client.ManagmentApi(swagger_client.ApiClient(configuration))
dt_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
dt_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

try:
    # Get Prospects
    api_response = api_instance.api_v1_managment_prospects_get(dt_start=dt_start, dt_end=dt_end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagmentApi->api_v1_managment_prospects_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dt_start** | **datetime**|  | [optional] 
 **dt_end** | **datetime**|  | [optional] 

### Return type

[**list[SpsRelProspectsCadastradosConvertidos]**](SpsRelProspectsCadastradosConvertidos.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **renewed_get**
> list[ContratoNaoRenovadosViewModel] renewed_get(dt_start=dt_start, dt_end=dt_end)

Get non-renewed Clients

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
api_instance = swagger_client.ManagmentApi(swagger_client.ApiClient(configuration))
dt_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
dt_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

try:
    # Get non-renewed Clients
    api_response = api_instance.renewed_get(dt_start=dt_start, dt_end=dt_end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagmentApi->renewed_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dt_start** | **datetime**|  | [optional] 
 **dt_end** | **datetime**|  | [optional] 

### Return type

[**list[ContratoNaoRenovadosViewModel]**](ContratoNaoRenovadosViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

