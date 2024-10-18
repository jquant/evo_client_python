# swagger_client.SalesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_sales_id_sale_get**](SalesApi.md#api_v1_sales_id_sale_get) | **GET** /api/v1/sales/{idSale} | Get sale by Id
[**api_v1_sales_post**](SalesApi.md#api_v1_sales_post) | **POST** /api/v1/sales | Create a new sale
[**api_v2_sales_get**](SalesApi.md#api_v2_sales_get) | **GET** /api/v2/sales | Get sales
[**items_get**](SalesApi.md#items_get) | **GET** /api/v1/sales/sales-items | Return itens for sale -&gt; site/totem
[**session_id_get**](SalesApi.md#session_id_get) | **GET** /api/v1/sales/by-session-id | Get sales

# **api_v1_sales_id_sale_get**
> SalesViewModel api_v1_sales_id_sale_get(id_sale)

Get sale by Id

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
api_instance = swagger_client.SalesApi(swagger_client.ApiClient(configuration))
id_sale = 56 # int | 

try:
    # Get sale by Id
    api_response = api_instance.api_v1_sales_id_sale_get(id_sale)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesApi->api_v1_sales_id_sale_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_sale** | **int**|  | 

### Return type

[**SalesViewModel**](SalesViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_sales_post**
> NewSaleViewModel api_v1_sales_post(body=body)

Create a new sale

payment:        Credit Card = 1,      Boleto = 2,      Sale Credits = 3,      Transfer = 4,      ValorZerado = 5,      LinkCheckout = 6 or null,      Pix = 7

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
api_instance = swagger_client.SalesApi(swagger_client.ApiClient(configuration))
body = swagger_client.NewSaleViewModel() # NewSaleViewModel |  (optional)

try:
    # Create a new sale
    api_response = api_instance.api_v1_sales_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesApi->api_v1_sales_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NewSaleViewModel**](NewSaleViewModel.md)|  | [optional] 

### Return type

[**NewSaleViewModel**](NewSaleViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v2_sales_get**
> SalesViewModel api_v2_sales_get(id_member=id_member, date_sale_start=date_sale_start, date_sale_end=date_sale_end, removal_date_start=removal_date_start, removal_date_end=removal_date_end, receivables_registration_date_start=receivables_registration_date_start, receivables_registration_date_end=receivables_registration_date_end, show_receivables=show_receivables, take=take, skip=skip, only_membership=only_membership, at_least_monthly=at_least_monthly, fl_swimming=fl_swimming, show_only_active_memberships=show_only_active_memberships, show_allow_locker=show_allow_locker, only_total_pass=only_total_pass)

Get sales

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
api_instance = swagger_client.SalesApi(swagger_client.ApiClient(configuration))
id_member = 56 # int | Filter by a member Id. (optional)
date_sale_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration of the sales starting in a date (yyyy-mm-dd) (optional)
date_sale_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration of the sales ending  in a date (yyyy-mm-dd) (optional)
removal_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by removal of the sales starting in a date (yyyy-mm-dd) (optional)
removal_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by removal of the sales ending  in a date  (yyyy-mm-dd) (optional)
receivables_registration_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter sales that had recievables starting in a date (yyyy-mm-dd) (optional)
receivables_registration_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter sales that had recievables ending in a date (yyyy-mm-dd) (optional)
show_receivables = false # bool | Flag to show sale receivables and sale value without credit value (optional) (default to false)
take = 25 # int | Total number of records to return. (Maximum of 100, default of 25) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
only_membership = false # bool | Return only sales with membership. (optional) (default to false)
at_least_monthly = false # bool | remove membership less than 30 days (as old removeMonthly) (optional) (default to false)
fl_swimming = true # bool | Filters memberships by the swimming flag (optional)
show_only_active_memberships = false # bool |  (optional) (default to false)
show_allow_locker = true # bool |  (optional)
only_total_pass = true # bool |  (optional)

try:
    # Get sales
    api_response = api_instance.api_v2_sales_get(id_member=id_member, date_sale_start=date_sale_start, date_sale_end=date_sale_end, removal_date_start=removal_date_start, removal_date_end=removal_date_end, receivables_registration_date_start=receivables_registration_date_start, receivables_registration_date_end=receivables_registration_date_end, show_receivables=show_receivables, take=take, skip=skip, only_membership=only_membership, at_least_monthly=at_least_monthly, fl_swimming=fl_swimming, show_only_active_memberships=show_only_active_memberships, show_allow_locker=show_allow_locker, only_total_pass=only_total_pass)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesApi->api_v2_sales_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Filter by a member Id. | [optional] 
 **date_sale_start** | **datetime**| Filter by registration of the sales starting in a date (yyyy-mm-dd) | [optional] 
 **date_sale_end** | **datetime**| Filter by registration of the sales ending  in a date (yyyy-mm-dd) | [optional] 
 **removal_date_start** | **datetime**| Filter by removal of the sales starting in a date (yyyy-mm-dd) | [optional] 
 **removal_date_end** | **datetime**| Filter by removal of the sales ending  in a date  (yyyy-mm-dd) | [optional] 
 **receivables_registration_date_start** | **datetime**| Filter sales that had recievables starting in a date (yyyy-mm-dd) | [optional] 
 **receivables_registration_date_end** | **datetime**| Filter sales that had recievables ending in a date (yyyy-mm-dd) | [optional] 
 **show_receivables** | **bool**| Flag to show sale receivables and sale value without credit value | [optional] [default to false]
 **take** | **int**| Total number of records to return. (Maximum of 100, default of 25) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **only_membership** | **bool**| Return only sales with membership. | [optional] [default to false]
 **at_least_monthly** | **bool**| remove membership less than 30 days (as old removeMonthly) | [optional] [default to false]
 **fl_swimming** | **bool**| Filters memberships by the swimming flag | [optional] 
 **show_only_active_memberships** | **bool**|  | [optional] [default to false]
 **show_allow_locker** | **bool**|  | [optional] 
 **only_total_pass** | **bool**|  | [optional] 

### Return type

[**SalesViewModel**](SalesViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **items_get**
> list[SalesItemsViewModel] items_get(id_branch=id_branch)

Return itens for sale -> site/totem

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
api_instance = swagger_client.SalesApi(swagger_client.ApiClient(configuration))
id_branch = 56 # int |  (optional)

try:
    # Return itens for sale -> site/totem
    api_response = api_instance.items_get(id_branch=id_branch)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesApi->items_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_branch** | **int**|  | [optional] 

### Return type

[**list[SalesItemsViewModel]**](SalesItemsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **session_id_get**
> int session_id_get(session_id=session_id, _date=_date)

Get sales

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
api_instance = swagger_client.SalesApi(swagger_client.ApiClient(configuration))
session_id = 'session_id_example' # str | Filter by a session Id. (optional)
_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration of the sale in a date (yyyy-mm-dd) (optional)

try:
    # Get sales
    api_response = api_instance.session_id_get(session_id=session_id, _date=_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesApi->session_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Filter by a session Id. | [optional] 
 **_date** | **datetime**| Filter by registration of the sale in a date (yyyy-mm-dd) | [optional] 

### Return type

**int**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

