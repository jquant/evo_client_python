# evo_client.VoucherApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_voucher_get**](VoucherApi.md#api_v1_voucher_get) | **GET** /api/v1/voucher | Get Vouchers

# **api_v1_voucher_get**
> list[VouchersResumoApiViewModel] api_v1_voucher_get(id_voucher=id_voucher, name=name, id_branch=id_branch, take=take, skip=skip, valid=valid, type=type)

Get Vouchers

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
api_instance = evo_client.VoucherApi(evo_client.ApiClient(configuration))
id_voucher = 56 # int | Filter by Voucher Id (optional)
name = 'name_example' # str |  (optional)
id_branch = 56 # int | Filber by Voucher IdBranch (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25 # int | Total of register to return (Maximun of 50) (optional) (default to 25)
skip = 0 # int | Total of register to skip (optional) (default to 0)
valid = true # bool |  (optional)
type = 56 # int |  (optional)

try:
    # Get Vouchers
    api_response = api_instance.api_v1_voucher_get(id_voucher=id_voucher, name=name, id_branch=id_branch, take=take, skip=skip, valid=valid, type=type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VoucherApi->api_v1_voucher_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_voucher** | **int**| Filter by Voucher Id | [optional] 
 **name** | **str**|  | [optional] 
 **id_branch** | **int**| Filber by Voucher IdBranch (Only available when using a multilocation key, ignored otherwise) | [optional] 
 **take** | **int**| Total of register to return (Maximun of 50) | [optional] [default to 25]
 **skip** | **int**| Total of register to skip | [optional] [default to 0]
 **valid** | **bool**|  | [optional] 
 **type** | **int**|  | [optional] 

### Return type

[**list[VouchersResumoApiViewModel]**](VouchersResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

