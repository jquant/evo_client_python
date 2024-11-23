 // Start of Selection
# evo_client.InvoicesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_invoices**](InvoicesApi.md#get_invoices) | **GET** /api/v1/invoices/get-invoices | Get invoices by date and filters

# **get_invoices**
> Union[EnotasRetorno, AsyncResult[Any]] get_invoices(issue_date_start=issue_date_start, issue_date_end=issue_date_end, competency_date_start=competency_date_start, competency_date_end=competency_date_end, send_date_start=send_date_start, send_date_end=send_date_end, take=take, skip=skip, member_id=member_id, status_invoice=status_invoice, types_invoice=types_invoice, async_req=async_req)

Get invoices by date and various filters.

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
api_instance = evo_client.InvoicesApi(evo_client.ApiClient(configuration))
issue_date_start = '2023-01-01T00:00:00+00:00'  # datetime | Filter by the invoice issuance start date (yyyy-mm-dd) (optional)
issue_date_end = '2023-12-31T23:59:59+00:00'    # datetime | Filter by the invoice issuance end date (yyyy-mm-dd) (optional)
competency_date_start = '2023-01-01T00:00:00+00:00'  # datetime | Filter by competency start date (yyyy-mm-dd) (optional)
competency_date_end = '2023-12-31T23:59:59+00:00'    # datetime | Filter by competency end date (yyyy-mm-dd) (optional)
send_date_start = '2023-01-01T00:00:00+00:00'        # datetime | Filter by the invoice sending start date (yyyy-mm-dd) (optional)
send_date_end = '2023-12-31T23:59:59+00:00'          # datetime | Filter by the invoice sending end date (yyyy-mm-dd) (optional)
take = 25                                           # int | Total number of records to return. (Maximum of 250) (optional, default to 25)
skip = 0                                            # int | Total number of records to skip. (optional, default to 0)
member_id = 56                                      # int | Filter by a member ID (optional)
status_invoice = [evro_client.InvoiceStatus.ISSUED, evro_client.InvoiceStatus.CANCELED]  # List[InvoiceStatus] | Filter by a list of invoice statuses (optional)
types_invoice = [evro_client.InvoiceType.NFSE, evro_client.InvoiceType.NFE]                # List[InvoiceType] | Filter by a list of invoice types (optional)
async_req = False                                   # bool | Execute request asynchronously (optional)

try:
    # Get invoices by date and filters
    api_response = api_instance.get_invoices(
        issue_date_start=issue_date_start,
        issue_date_end=issue_date_end,
        competency_date_start=competency_date_start,
        competency_date_end=competency_date_end,
        send_date_start=send_date_start,
        send_date_end=send_date_end,
        take=take,
        skip=skip,
        member_id=member_id,
        status_invoice=status_invoice,
        types_invoice=types_invoice,
        async_req=async_req
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvoicesApi->get_invoices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_date_start** | **datetime** | Filter by the invoice issuance start date (yyyy-mm-dd) | [optional] 
 **issue_date_end** | **datetime** | Filter by the invoice issuance end date (yyyy-mm-dd) | [optional] 
 **competency_date_start** | **datetime** | Filter by competency start date (yyyy-mm-dd) | [optional] 
 **competency_date_end** | **datetime** | Filter by competency end date (yyyy-mm-dd) | [optional] 
 **send_date_start** | **datetime** | Filter by the invoice sending start date (yyyy-mm-dd) | [optional] 
 **send_date_end** | **datetime** | Filter by the invoice sending end date (yyyy-mm-dd) | [optional] 
 **take** | **int** | Total number of records to return. (Maximum of 250) | [optional] [default to 25]
 **skip** | **int** | Total number of records to skip. | [optional] [default to 0]
 **member_id** | **int** | Filter by a member ID | [optional] 
 **status_invoice** | **List[InvoiceStatus]** | Filter by a list of invoice statuses. Status options: 1 - Issued, 2 - With error, 3 - Canceled | [optional] 
 **types_invoice** | **List[InvoiceType]** | Filter by a list of invoice types. Type options: 1 - NFSe, 2 - NFe, 3 - NFCe | [optional] 
 **async_req** | **bool** | Execute request asynchronously | [optional] 

### Return type

[**Union[EnotasRetorno, AsyncResult[Any]]**](EnotasRetorno.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
