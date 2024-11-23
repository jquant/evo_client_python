# evo_client.PixApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_qr_code**](PixApi.md#get_qr_code) | **GET** /api/v1/pix/qr-code | Get QR code

# **get_qr_code**
> PixPaymentDetailsViewModel get_qr_code(pix_receipt_id=pix_receipt_id)

Get QR code

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
api_instance = evo_client.PixApi(evo_client.ApiClient(configuration))
pix_receipt_id = 56 # int |  (optional)

try:
    # Get QR code
    api_response = api_instance.get_qr_code(pix_receipt_id=pix_receipt_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PixApi->get_qr_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pix_receipt_id** | **int**| PIX receipt ID | [optional] 

### Return type

[**PixPaymentDetailsViewModel**](PixPaymentDetailsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# End of Selection
```
