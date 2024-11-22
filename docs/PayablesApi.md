# evo_client.PayablesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_costcenter_get**](PayablesApi.md#api_v1_costcenter_get) | **GET** /api/v1/costcenter | Get Cost Center
[**api_v1_payables_get**](PayablesApi.md#api_v1_payables_get) | **GET** /api/v1/payables | Get payables

# **api_v1_costcenter_get**
> CostCenterApiViewModel api_v1_costcenter_get(take=take, skip=skip)

Get Cost Center

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
api_instance = evo_client.PayablesApi(evo_client.ApiClient(configuration))
take = 50 # int | Total number of records to return. (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get Cost Center
    api_response = api_instance.api_v1_costcenter_get(take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayablesApi->api_v1_costcenter_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **take** | **int**| Total number of records to return. | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**CostCenterApiViewModel**](CostCenterApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_payables_get**
> PayablesApiViewModel api_v1_payables_get(description=description, date_input_start=date_input_start, date_input_end=date_input_end, due_date_start=due_date_start, due_date_end=due_date_end, date_payment_start=date_payment_start, date_payment_end=date_payment_end, compentence_start=compentence_start, competence_end=competence_end, bank_account=bank_account, ammount_start=ammount_start, ammount_end=ammount_end, account_status=account_status, take=take, skip=skip)

Get payables

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
api_instance = evo_client.PayablesApi(evo_client.ApiClient(configuration))
description = 'description_example' # str | Filter by account description (optional)
date_input_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by input of the account starting in a date (yyyy-mm-dd) (optional)
date_input_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by input of the account ending in a date (yyyy-mm-dd) (optional)
due_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account starting in a date (yyyy-mm-dd) (optional)
due_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account ending in a date (yyyy-mm-dd) (optional)
date_payment_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
date_payment_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
compentence_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
competence_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
bank_account = 'bank_account_example' # str | Filter by bank account id. The bank account id can be obtained from the BankAccounts API. Accounts can be concatenated with a comma to search, for example (2,215), in which case it will return payments from bank accounts 2 and 215. (optional)
ammount_start = 1.2 # float | Filter by minimun ammount (optional)
ammount_end = 1.2 # float | Filter by maximun ammount (optional)
account_status = 'account_status_example' # str | Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Paid, 3 - Canceled (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get payables
    api_response = api_instance.api_v1_payables_get(description=description, date_input_start=date_input_start, date_input_end=date_input_end, due_date_start=due_date_start, due_date_end=due_date_end, date_payment_start=date_payment_start, date_payment_end=date_payment_end, compentence_start=compentence_start, competence_end=competence_end, bank_account=bank_account, ammount_start=ammount_start, ammount_end=ammount_end, account_status=account_status, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayablesApi->api_v1_payables_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **description** | **str**| Filter by account description | [optional] 
 **date_input_start** | **datetime**| Filter by input of the account starting in a date (yyyy-mm-dd) | [optional] 
 **date_input_end** | **datetime**| Filter by input of the account ending in a date (yyyy-mm-dd) | [optional] 
 **due_date_start** | **datetime**| Filter by due of the account starting in a date (yyyy-mm-dd) | [optional] 
 **due_date_end** | **datetime**| Filter by due of the account ending in a date (yyyy-mm-dd) | [optional] 
 **date_payment_start** | **datetime**|  | [optional] 
 **date_payment_end** | **datetime**|  | [optional] 
 **compentence_start** | **datetime**|  | [optional] 
 **competence_end** | **datetime**|  | [optional] 
 **bank_account** | **str**| Filter by bank account id. The bank account id can be obtained from the BankAccounts API. Accounts can be concatenated with a comma to search, for example (2,215), in which case it will return payments from bank accounts 2 and 215. | [optional] 
 **ammount_start** | **float**| Filter by minimun ammount | [optional] 
 **ammount_end** | **float**| Filter by maximun ammount | [optional] 
 **account_status** | **str**| Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Paid, 3 - Canceled | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**PayablesApiViewModel**](PayablesApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

