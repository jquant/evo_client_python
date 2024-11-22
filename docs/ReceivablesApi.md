# evo_client.ReceivablesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_receivables_get**](ReceivablesApi.md#api_v1_receivables_get) | **GET** /api/v1/receivables | Get receivables
[**api_v1_revenuecenter_get**](ReceivablesApi.md#api_v1_revenuecenter_get) | **GET** /api/v1/revenuecenter | Get Cost Center
[**received_put**](ReceivablesApi.md#received_put) | **PUT** /api/v1/receivables/mark-received | 

# **api_v1_receivables_get**
> api_v1_receivables_get(registration_date_start=registration_date_start, registration_date_end=registration_date_end, due_date_start=due_date_start, due_date_end=due_date_end, receiving_date_start=receiving_date_start, receiving_date_end=receiving_date_end, competence_date_end=competence_date_end, competence_date_start=competence_date_start, cancellation_date_start=cancellation_date_start, cancellation_date_end=cancellation_date_end, charge_date_start=charge_date_start, charge_date_end=charge_date_end, update_date_start=update_date_start, update_date_end=update_date_end, description=description, ammount_start=ammount_start, ammount_end=ammount_end, payment_types=payment_types, account_status=account_status, take=take, skip=skip, member_id=member_id, id_sale=id_sale, id_receivable=id_receivable, invoice_date_start=invoice_date_start, invoice_date_end=invoice_date_end, invoice_canceled_date_start=invoice_canceled_date_start, invoice_canceled_date_end=invoice_canceled_date_end, sale_date_start=sale_date_start, sale_date_end=sale_date_end)

Get receivables

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
api_instance = evo_client.ReceivablesApi(evo_client.ApiClient(configuration))
registration_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration of the account starting in a date (yyyy-mm-dd) (optional)
registration_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration of the account ending in a date (yyyy-mm-dd) (optional)
due_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account starting in a date (yyyy-mm-dd) (optional)
due_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account ending in a date (yyyy-mm-dd) (optional)
receiving_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by receiving of the account starting in a date (yyyy-mm-dd) (optional)
receiving_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by receiving of the account ending in a date (yyyy-mm-dd) (optional)
competence_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by competence of the account ending in a date (yyyy-mm-dd) (optional)
competence_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by competence of the account starting in a date (yyyy-mm-dd) (optional)
cancellation_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by cancellation of the account starting in a date (yyyy-mm-dd) (optional)
cancellation_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by cancellation of the account ending in a date (yyyy-mm-dd) (optional)
charge_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by charge of the account starting in a date (yyyy-mm-dd) (optional)
charge_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by charge of the account ending in a date (yyyy-mm-dd) (optional)
update_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by update of the account starting in a date (yyyy-mm-dd) (optional)
update_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by update of the account ending in a date (yyyy-mm-dd) (optional)
description = 'description_example' # str | Filter by description (optional)
ammount_start = 1.2 # float | Filter by minimun ammount (optional)
ammount_end = 1.2 # float | Filter by maximun ammount (optional)
payment_types = 'payment_types_example' # str | Filter by a comma separated list of payment types id. Types: 1 - Money, 2 - Credit Card, 3 - Debit Card, 4 - Check, 5 - Boleto Bancário, 6 - PagSeguro, 7 - Deposit, 8 - Account Debit, 9 - Internet, 11 - Sale Credits, 12 - On-line Credit Card, 13 - Transfer, 18 - Pix, 0 - Balance Due. (optional)
account_status = 'account_status_example' # str | Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Received, 3 - Canceled, 4 - Overdue (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
member_id = 56 # int | Filter by a member Id. (optional)
id_sale = 56 # int | Filter by a sale Id. (optional)
id_receivable = 56 # int | Filter by a receivable Id. (optional)
invoice_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by invoice date (yyyy-mm-dd) (optional)
invoice_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by invoice date (yyyy-mm-dd) (optional)
invoice_canceled_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by canceled invoice date (yyyy-mm-dd) (optional)
invoice_canceled_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by canceled invoice date (yyyy-mm-dd) (optional)
sale_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by sale date (yyyy-mm-dd) (optional)
sale_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by sale date (yyyy-mm-dd) (optional)

try:
    # Get receivables
    api_instance.api_v1_receivables_get(registration_date_start=registration_date_start, registration_date_end=registration_date_end, due_date_start=due_date_start, due_date_end=due_date_end, receiving_date_start=receiving_date_start, receiving_date_end=receiving_date_end, competence_date_end=competence_date_end, competence_date_start=competence_date_start, cancellation_date_start=cancellation_date_start, cancellation_date_end=cancellation_date_end, charge_date_start=charge_date_start, charge_date_end=charge_date_end, update_date_start=update_date_start, update_date_end=update_date_end, description=description, ammount_start=ammount_start, ammount_end=ammount_end, payment_types=payment_types, account_status=account_status, take=take, skip=skip, member_id=member_id, id_sale=id_sale, id_receivable=id_receivable, invoice_date_start=invoice_date_start, invoice_date_end=invoice_date_end, invoice_canceled_date_start=invoice_canceled_date_start, invoice_canceled_date_end=invoice_canceled_date_end, sale_date_start=sale_date_start, sale_date_end=sale_date_end)
except ApiException as e:
    print("Exception when calling ReceivablesApi->api_v1_receivables_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registration_date_start** | **datetime**| Filter by registration of the account starting in a date (yyyy-mm-dd) | [optional] 
 **registration_date_end** | **datetime**| Filter by registration of the account ending in a date (yyyy-mm-dd) | [optional] 
 **due_date_start** | **datetime**| Filter by due of the account starting in a date (yyyy-mm-dd) | [optional] 
 **due_date_end** | **datetime**| Filter by due of the account ending in a date (yyyy-mm-dd) | [optional] 
 **receiving_date_start** | **datetime**| Filter by receiving of the account starting in a date (yyyy-mm-dd) | [optional] 
 **receiving_date_end** | **datetime**| Filter by receiving of the account ending in a date (yyyy-mm-dd) | [optional] 
 **competence_date_end** | **datetime**| Filter by competence of the account ending in a date (yyyy-mm-dd) | [optional] 
 **competence_date_start** | **datetime**| Filter by competence of the account starting in a date (yyyy-mm-dd) | [optional] 
 **cancellation_date_start** | **datetime**| Filter by cancellation of the account starting in a date (yyyy-mm-dd) | [optional] 
 **cancellation_date_end** | **datetime**| Filter by cancellation of the account ending in a date (yyyy-mm-dd) | [optional] 
 **charge_date_start** | **datetime**| Filter by charge of the account starting in a date (yyyy-mm-dd) | [optional] 
 **charge_date_end** | **datetime**| Filter by charge of the account ending in a date (yyyy-mm-dd) | [optional] 
 **update_date_start** | **datetime**| Filter by update of the account starting in a date (yyyy-mm-dd) | [optional] 
 **update_date_end** | **datetime**| Filter by update of the account ending in a date (yyyy-mm-dd) | [optional] 
 **description** | **str**| Filter by description | [optional] 
 **ammount_start** | **float**| Filter by minimun ammount | [optional] 
 **ammount_end** | **float**| Filter by maximun ammount | [optional] 
 **payment_types** | **str**| Filter by a comma separated list of payment types id. Types: 1 - Money, 2 - Credit Card, 3 - Debit Card, 4 - Check, 5 - Boleto Bancário, 6 - PagSeguro, 7 - Deposit, 8 - Account Debit, 9 - Internet, 11 - Sale Credits, 12 - On-line Credit Card, 13 - Transfer, 18 - Pix, 0 - Balance Due. | [optional] 
 **account_status** | **str**| Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Received, 3 - Canceled, 4 - Overdue | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **member_id** | **int**| Filter by a member Id. | [optional] 
 **id_sale** | **int**| Filter by a sale Id. | [optional] 
 **id_receivable** | **int**| Filter by a receivable Id. | [optional] 
 **invoice_date_start** | **datetime**| Filter by invoice date (yyyy-mm-dd) | [optional] 
 **invoice_date_end** | **datetime**| Filter by invoice date (yyyy-mm-dd) | [optional] 
 **invoice_canceled_date_start** | **datetime**| Filter by canceled invoice date (yyyy-mm-dd) | [optional] 
 **invoice_canceled_date_end** | **datetime**| Filter by canceled invoice date (yyyy-mm-dd) | [optional] 
 **sale_date_start** | **datetime**| Filter by sale date (yyyy-mm-dd) | [optional] 
 **sale_date_end** | **datetime**| Filter by sale date (yyyy-mm-dd) | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_revenuecenter_get**
> RevenueCenterApiViewModel api_v1_revenuecenter_get(take=take, skip=skip)

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
api_instance = evo_client.ReceivablesApi(evo_client.ApiClient(configuration))
take = 50 # int | Total number of records to return. (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get Cost Center
    api_response = api_instance.api_v1_revenuecenter_get(take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReceivablesApi->api_v1_revenuecenter_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **take** | **int**| Total number of records to return. | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**RevenueCenterApiViewModel**](RevenueCenterApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **received_put**
> received_put(body=body)



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
api_instance = evo_client.ReceivablesApi(evo_client.ApiClient(configuration))
body = evo_client.ReceivablesMaskReceivedViewModel() # ReceivablesMaskReceivedViewModel |  (optional)

try:
    api_instance.received_put(body=body)
except ApiException as e:
    print("Exception when calling ReceivablesApi->received_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReceivablesMaskReceivedViewModel**](ReceivablesMaskReceivedViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

