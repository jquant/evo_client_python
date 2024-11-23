# evo_client.VoucherApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_vouchers**](VoucherApi.md#get_vouchers) | **GET** /api/v1/voucher | Get Vouchers
[**get_voucher_details**](VoucherApi.md#get_voucher_details) | **GET** /api/v1/voucher/{voucher_id} | Get Voucher Details
[**create_voucher**](VoucherApi.md#create_voucher) | **POST** /api/v1/voucher | Create a new Voucher

# **get_vouchers**
> list[VouchersResumoApiViewModel] get_vouchers(voucher_id=None, name=None, branch_id=None, take=25, skip=0, valid=None, voucher_type=None, async_req=False)

Get Vouchers

### Example
```python
from __future__ import print_function
import evo_client

from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint
import time

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.VoucherApi(evo_client.ApiClient(configuration))
voucher_id = 56 # int | Filter by Voucher Id (optional)
name = 'name_example' # str |  (optional)
branch_id = 56 # int | Filter by Voucher Branch Id (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25 # int | Total number of records to return (Maximum of 50) (optional) (default to 25)
skip = 0 # int | Total number of records to skip (optional) (default to 0)
valid = True # bool |  (optional)
voucher_type = 56 # int |  (optional)

try:
    # Get Vouchers
    api_response = api_instance.get_vouchers(voucher_id=voucher_id, name=name, branch_id=branch_id, take=take, skip=skip, valid=valid, voucher_type=voucher_type, async_req=False)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VoucherApi->get_vouchers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**voucher_id** | **int**| Filter by Voucher Id | [optional] 
**name** | **str**|  | [optional] 
**branch_id** | **int**| Filter by Voucher Branch Id (Only available when using a multilocation key, ignored otherwise) | [optional] 
**take** | **int**| Total number of records to return (Maximum of 50) | [optional] [default to 25]
**skip** | **int**| Total number of records to skip | [optional] [default to 0]
**valid** | **bool**|  | [optional] 
**voucher_type** | **int**|  | [optional] 

### Return type

**list[VouchersResumoApiViewModel]**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_voucher_details**
> dict get_voucher_details(voucher_id, async_req=False)

Get detailed information about a specific voucher.

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
api_instance = evo_client.VoucherApi(evo_client.ApiClient(configuration))
voucher_id = 56 # int | ID of the voucher to retrieve

try:
    # Get Voucher Details
    api_response = api_instance.get_voucher_details(voucher_id=voucher_id, async_req=False)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VoucherApi->get_voucher_details: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**voucher_id** | **int**| ID of the voucher to retrieve | [required] 

### Return type

**dict** – Detailed voucher information including:
- Basic voucher details
- Usage history
- Restrictions and conditions
- Related transactions

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_voucher**
> dict create_voucher(name, discount_type, discount_value, valid_from, valid_until, branch_id=None, usage_limit=None, min_value=None, async_req=False)

Create a new Voucher.

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
api_instance = evo_client.VoucherApi(evo_client.ApiClient(configuration))
name = 'New Year Discount' # str | Name/code of the voucher
discount_type = 1 # int | Type of discount (1=Percentage, 2=Fixed amount)
discount_value = 10.0 # float | Value of the discount
valid_from = '2024-01-01' # str | Start date of validity (format: YYYY-MM-DD)
valid_until = '2024-12-31' # str | End date of validity (format: YYYY-MM-DD)
branch_id = 56 # int | Branch ID for voucher (multilocation only) (optional)
usage_limit = 100 # int | Maximum number of times voucher can be used (optional)
min_value = 50.0 # float | Minimum purchase value required (optional)

try:
    # Create a new Voucher
    api_response = api_instance.create_voucher(name=name, discount_type=discount_type, discount_value=discount_value, valid_from=valid_from, valid_until=valid_until, branch_id=branch_id, usage_limit=usage_limit, min_value=min_value, async_req=False)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VoucherApi->create_voucher: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**name** | **str**| Name/code of the voucher | [required]
**discount_type** | **int**| Type of discount (1=Percentage, 2=Fixed amount) | [required]
**discount_value** | **float**| Value of the discount | [required]
**valid_from** | **str**| Start date of validity (format: YYYY-MM-DD) | [required]
**valid_until** | **str**| End date of validity (format: YYYY-MM-DD) | [required]
**branch_id** | **int**| Branch ID for voucher (multilocation only) | [optional]
**usage_limit** | **int**| Maximum number of times voucher can be used | [optional]
**min_value** | **float**| Minimum purchase value required | [optional]

### Return type

**dict** – Created voucher details

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
```
