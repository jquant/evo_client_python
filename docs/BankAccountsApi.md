# evo_client.BankAccountsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_accounts**](BankAccountsApi.md#get_accounts) | **GET** /api/v1/bank-accounts | Get bank accounts

# **get_accounts**
> BankAccountsViewModel get_accounts()

Get bank accounts

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
api_instance = evo_client.BankAccountsApi(evo_client.ApiClient(configuration))

try:
    # Get bank accounts
    api_response = api_instance.get_accounts()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankAccountsApi->get_accounts: %s\n" % e)
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

