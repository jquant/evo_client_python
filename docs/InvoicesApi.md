# evo_client.InvoicesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**invoices_get**](InvoicesApi.md#invoices_get) | **GET** /api/v1/invoices/get-invoices | Get invoices by date

# **invoices_get**
> EnotasRetorno invoices_get(issue_date_start=issue_date_start, issue_date_end=issue_date_end, competency_date_start=competency_date_start, competency_date_end=competency_date_end, send_date_start=send_date_start, send_date_end=send_date_end, take=take, skip=skip, id_member=id_member, status_invoice=status_invoice, types_invoice=types_invoice)

Get invoices by date

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
api_instance = evo_client.InvoicesApi(evo_client.ApiClient(configuration))
issue_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by the invoice issuance that starts on a date (yyyy-mm-dd) (optional)
issue_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by the invoice issuance that ends on a date (yyyy-mm-dd) (optional)
competency_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
competency_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by the invoice competency that ends on a date (yyyy-mm-dd) (optional)
send_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by the invoice sending that starts on a date (yyyy-mm-dd) (optional)
send_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by the invoice sending that ends on a date (yyyy-mm-dd) (optional)
take = 25 # int | Total number of records to return. (Maximum of 250) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
id_member = 56 # int | Filter by a member Id (optional)
status_invoice = 'status_invoice_example' # str | Filter by a comma separated list of status invoice. Status: 1 - Issued, 2 - With error, 3 - Canceled (optional)
types_invoice = 'types_invoice_example' # str | Filter by types of invoice separated by comma.: 1 - NFSe, 2 - NFe, 3 - NFCe. Example: 1,2,3 (optional)

try:
    # Get invoices by date
    api_response = api_instance.invoices_get(issue_date_start=issue_date_start, issue_date_end=issue_date_end, competency_date_start=competency_date_start, competency_date_end=competency_date_end, send_date_start=send_date_start, send_date_end=send_date_end, take=take, skip=skip, id_member=id_member, status_invoice=status_invoice, types_invoice=types_invoice)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvoicesApi->invoices_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_date_start** | **datetime**| Filter by the invoice issuance that starts on a date (yyyy-mm-dd) | [optional] 
 **issue_date_end** | **datetime**| Filter by the invoice issuance that ends on a date (yyyy-mm-dd) | [optional] 
 **competency_date_start** | **datetime**|  | [optional] 
 **competency_date_end** | **datetime**| Filter by the invoice competency that ends on a date (yyyy-mm-dd) | [optional] 
 **send_date_start** | **datetime**| Filter by the invoice sending that starts on a date (yyyy-mm-dd) | [optional] 
 **send_date_end** | **datetime**| Filter by the invoice sending that ends on a date (yyyy-mm-dd) | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 250) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **id_member** | **int**| Filter by a member Id | [optional] 
 **status_invoice** | **str**| Filter by a comma separated list of status invoice. Status: 1 - Issued, 2 - With error, 3 - Canceled | [optional] 
 **types_invoice** | **str**| Filter by types of invoice separated by comma.: 1 - NFSe, 2 - NFe, 3 - NFCe. Example: 1,2,3 | [optional] 

### Return type

[**EnotasRetorno**](EnotasRetorno.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

