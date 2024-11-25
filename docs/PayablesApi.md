# evo_client.PayablesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_cost_centers**](PayablesApi.md#get_cost_centers) | **GET** /api/v1/costcenter | Get Cost Centers
[**get_payables**](PayablesApi.md#get_payables) | **GET** /api/v1/payables | Retrieve payables

# **get_cost_centers**
> CostCenterApiViewModel get_cost_centers(take: int = 50, skip: int = 0, async_req: bool = False)

Get Cost Centers with pagination.

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
api_instance = evo_client.PayablesApi(evo_client.ApiClient(configuration))
take = 50 # int | Total number of records to return. (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get Cost Centers
    api_response = api_instance.get_cost_centers(take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayablesApi->get_cost_centers: %s\n" % e)
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

# **get_payables**
> PayablesApiViewModel get_payables(description: str = None, date_input_start: datetime = None, date_input_end: datetime = None, due_date_start: datetime = None, due_date_end: datetime = None, date_payment_start: datetime = None, date_payment_end: datetime = None, competence_start: datetime = None, competence_end: datetime = None, bank_account: str = None, amount_start: float = None, amount_end: float = None, account_status: str = None, take: int = 50, skip: int = 0, async_req: bool = False)

Retrieve payables with optional filtering.

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
api_instance = evo_client.PayablesApi(evo_client.ApiClient(configuration))
description = 'description_example' # str | Filter by account description (optional)
date_input_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by input of the account starting on a date (yyyy-mm-dd) (optional)
date_input_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by input of the account ending on a date (yyyy-mm-dd) (optional)
due_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account starting on a date (yyyy-mm-dd) (optional)
due_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account ending on a date (yyyy-mm-dd) (optional)
date_payment_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
date_payment_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
competence_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
competence_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
bank_account = 'bank_account_example' # str | Filter by bank account id. The bank account id can be obtained from the BankAccounts API. Accounts can be concatenated with a comma to search, for example (2,215), in which case it will return payments from bank accounts 2 and 215. (optional)
amount_start = 1.2 # float | Filter by minimum amount (optional)
amount_end = 1.2 # float | Filter by maximum amount (optional)
account_status = 'account_status_example' # str | Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Paid, 3 - Canceled (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Retrieve payables
    api_response = api_instance.get_payables(description=description, date_input_start=date_input_start, date_input_end=date_input_end, due_date_start=due_date_start, due_date_end=due_date_end, date_payment_start=date_payment_start, date_payment_end=date_payment_end, competence_start=competence_start, competence_end=competence_end, bank_account=bank_account, amount_start=amount_start, amount_end=amount_end, account_status=account_status, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayablesApi->get_payables: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **description** | **str**| Filter by account description | [optional]
 **date_input_start** | **datetime**| Filter by input of the account starting on a date (yyyy-mm-dd) | [optional]
 **date_input_end** | **datetime**| Filter by input of the account ending on a date (yyyy-mm-dd) | [optional]
 **due_date_start** | **datetime**| Filter by due of the account starting on a date (yyyy-mm-dd) | [optional]
 **due_date_end** | **datetime**| Filter by due of the account ending on a date (yyyy-mm-dd) | [optional]
 **date_payment_start** | **datetime**|  | [optional]
 **date_payment_end** | **datetime**|  | [optional]
 **competence_start** | **datetime**|  | [optional]
 **competence_end** | **datetime**|  | [optional]
 **bank_account** | **str**| Filter by bank account id. The bank account id can be obtained from the BankAccounts API. Accounts can be concatenated with a comma to search, for example (2,215), in which case it will return payments from bank accounts 2 and 215. | [optional]
 **amount_start** | **float**| Filter by minimum amount | [optional]
 **amount_end** | **float**| Filter by maximum amount | [optional]
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
# End of Selection
```
