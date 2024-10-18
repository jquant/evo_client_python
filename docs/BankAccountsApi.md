# swagger_client.BankAccountsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accounts_get**](BankAccountsApi.md#accounts_get) | **GET** /api/v1/bank-accounts | Get bank accounts

# **accounts_get**
> BankAccountsViewModel accounts_get()

Get bank accounts

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
api_instance = swagger_client.BankAccountsApi(swagger_client.ApiClient(configuration))

try:
    # Get bank accounts
    api_response = api_instance.accounts_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankAccountsApi->accounts_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BankAccountsViewModel**](BankAccountsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

