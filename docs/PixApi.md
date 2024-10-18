# swagger_client.PixApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**code_get**](PixApi.md#code_get) | **GET** /api/v1/pix/qr-code | Get Qr-code

# **code_get**
> PixPaymentDetailsViewModel code_get(id_recebimento_pix=id_recebimento_pix)

Get Qr-code

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
api_instance = swagger_client.PixApi(swagger_client.ApiClient(configuration))
id_recebimento_pix = 56 # int |  (optional)

try:
    # Get Qr-code
    api_response = api_instance.code_get(id_recebimento_pix=id_recebimento_pix)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PixApi->code_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_recebimento_pix** | **int**|  | [optional] 

### Return type

[**PixPaymentDetailsViewModel**](PixPaymentDetailsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

