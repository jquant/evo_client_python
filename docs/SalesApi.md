# evo_client.SalesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

## Methods

Method | HTTP Request | Description
------------- | ------------- | -------------
[**get_sale_by_id**](SalesApi.md#get_sale_by_id) | **GET** /api/v1/sales/{idSale} | Retrieve a sale by its ID
[**create_sale**](SalesApi.md#create_sale) | **POST** /api/v1/sales | Create a new sale
[**get_sales**](SalesApi.md#get_sales) | **GET** /api/v2/sales | Retrieve a list of sales
[**get_sales_items**](SalesApi.md#get_sales_items) | **GET** /api/v1/sales/sales-items | Retrieve items available for sale (site/totem)
[**get_sales_by_session_id**](SalesApi.md#get_sales_by_session_id) | **GET** /api/v1/sales/by-session-id | Retrieve sales by session ID

## **get_sale_by_id**
> [SalesViewModel](SalesViewModel.md) get_sale_by_id(id_sale: int)

Retrieve a sale by its ID.

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.SalesApi(evo_client.ApiClient(configuration))
id_sale = 56  # int | ID of the sale to retrieve

try:
    # Retrieve sale by ID
    api_response = api_instance.get_sale_by_id(id_sale)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling SalesApi->get_sale_by_id: {e}\n")
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**id_sale** | **int** | ID of the sale to retrieve | 

### Return Type

[**SalesViewModel**](SalesViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

## **create_sale**
> [NewSaleViewModel](NewSaleViewModel.md) create_sale(body: NewSaleViewModel = None)

Create a new sale.

**Payment Methods:**
- Credit Card = 1
- Boleto = 2
- Sale Credits = 3
- Transfer = 4
- ValorZerado = 5
- LinkCheckout = 6 or null
- Pix = 7

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.SalesApi(evo_client.ApiClient(configuration))
body = evo_client.NewSaleViewModel()  # NewSaleViewModel | (optional)

try:
    # Create a new sale
    api_response = api_instance.create_sale(body=body)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling SalesApi->create_sale: {e}\n")
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**body** | [**NewSaleViewModel**](NewSaleViewModel.md) | Details of the sale to create | [optional] 

### Return Type

[**NewSaleViewModel**](NewSaleViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

## **get_sales**
> [SalesViewModel](SalesViewModel.md) get_sales(id_member: int = None, date_sale_start: datetime = None, date_sale_end: datetime = None, removal_date_start: datetime = None, removal_date_end: datetime = None, receivables_registration_date_start: datetime = None, receivables_registration_date_end: datetime = None, show_receivables: bool = False, take: int = 25, skip: int = 0, only_membership: bool = False, at_least_monthly: bool = False, fl_swimming: bool = True, show_only_active_memberships: bool = False, show_allow_locker: bool = True, only_total_pass: bool = True)

Retrieve a list of sales with optional filtering.

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint
from datetime import datetime

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.SalesApi(evo_client.ApiClient(configuration))
id_member = 56  # int | Filter by member ID (optional)
date_sale_start = datetime(2013, 10, 20, 19, 20, 30)  # datetime | Start date for sale registration (optional)
date_sale_end = datetime(2013, 10, 20, 19, 20, 30)    # datetime | End date for sale registration (optional)
removal_date_start = datetime(2013, 10, 20, 19, 20, 30)  # datetime | Start date for sale removal (optional)
removal_date_end = datetime(2013, 10, 20, 19, 20, 30)    # datetime | End date for sale removal (optional)
receivables_registration_date_start = datetime(2013, 10, 20, 19, 20, 30)  # datetime | Start date for receivables registration (optional)
receivables_registration_date_end = datetime(2013, 10, 20, 19, 20, 30)    # datetime | End date for receivables registration (optional)
show_receivables = False  # bool | Show sale receivables and sale value without credit value (optional)
take = 25  # int | Number of records to return (max 100, default 25) (optional)
skip = 0   # int | Number of records to skip (optional)
only_membership = False  # bool | Return only sales with membership (optional)
at_least_monthly = False  # bool | Remove memberships less than 30 days old (optional)
fl_swimming = True   # bool | Filter memberships by swimming flag (optional)
show_only_active_memberships = False  # bool | Show only active memberships (optional)
show_allow_locker = True  # bool | Allow locker display (optional)
only_total_pass = True  # bool | Show only total pass (optional)

try:
    # Retrieve sales
    api_response = api_instance.get_sales(
        id_member=id_member,
        date_sale_start=date_sale_start,
        date_sale_end=date_sale_end,
        removal_date_start=removal_date_start,
        removal_date_end=removal_date_end,
        receivables_registration_date_start=receivables_registration_date_start,
        receivables_registration_date_end=receivables_registration_date_end,
        show_receivables=show_receivables,
        take=take,
        skip=skip,
        only_membership=only_membership,
        at_least_monthly=at_least_monthly,
        fl_swimming=fl_swimming,
        show_only_active_memberships=show_only_active_memberships,
        show_allow_locker=show_allow_locker,
        only_total_pass=only_total_pass
    )
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling SalesApi->get_sales: {e}\n")
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by member ID | [optional] 
**date_sale_start** | **datetime** | Start date for sale registration (yyyy-mm-dd) | [optional] 
**date_sale_end** | **datetime** | End date for sale registration (yyyy-mm-dd) | [optional] 
**removal_date_start** | **datetime** | Start date for sale removal (yyyy-mm-dd) | [optional] 
**removal_date_end** | **datetime** | End date for sale removal (yyyy-mm-dd) | [optional] 
**receivables_registration_date_start** | **datetime** | Start date for receivables registration (yyyy-mm-dd) | [optional] 
**receivables_registration_date_end** | **datetime** | End date for receivables registration (yyyy-mm-dd) | [optional] 
**show_receivables** | **bool** | Show sale receivables and sale value without credit value | [optional] [default to false]
**take** | **int** | Number of records to return (max 100, default 25) | [optional] [default to 25]
**skip** | **int** | Number of records to skip | [optional] [default to 0]
**only_membership** | **bool** | Return only sales with membership | [optional] [default to false]
**at_least_monthly** | **bool** | Remove memberships less than 30 days old | [optional] [default to false]
**fl_swimming** | **bool** | Filter memberships by swimming flag | [optional] 
**show_only_active_memberships** | **bool** | Show only active memberships | [optional] [default to false]
**show_allow_locker** | **bool** | Allow locker display | [optional] 
**only_total_pass** | **bool** | Show only total pass | [optional] 

### Return Type

[**SalesViewModel**](SalesViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

## **get_sales_items**
> list[SalesItemsViewModel] get_sales_items(id_branch: int = None)

Retrieve items available for sale at a specific branch or site/totem.

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.SalesApi(evo_client.ApiClient(configuration))
id_branch = 56  # int | ID of the branch (optional)

try:
    # Retrieve items for sale
    api_response = api_instance.get_sales_items(id_branch=id_branch)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling SalesApi->get_sales_items: {e}\n")
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**id_branch** | **int** | ID of the branch | [optional] 

### Return Type

[**List[SalesItemsViewModel]**](SalesItemsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

## **get_sales_by_session_id**
> int get_sales_by_session_id(session_id: str = None, _date: datetime = None)

Retrieve the number of sales associated with a specific session ID.

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint
from datetime import datetime

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.SalesApi(evo_client.ApiClient(configuration))
session_id = 'session_id_example'  # str | Session ID to filter by (optional)
_date = datetime(2013, 10, 20, 19, 20, 30)  # datetime | Sale registration date (yyyy-mm-dd) (optional)

try:
    # Retrieve sales count by session ID
    api_response = api_instance.get_sales_by_session_id(session_id=session_id, _date=_date)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling SalesApi->get_sales_by_session_id: {e}\n")
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**session_id** | **str** | Session ID to filter by | [optional] 
**_date** | **datetime** | Sale registration date (yyyy-mm-dd) | [optional] 

### Return Type

**int**

### Authorization

[Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
