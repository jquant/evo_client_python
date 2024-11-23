# evo_client.receivables_api.ReceivablesApi

This documentation refers to `receivables_api.py`.

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

## Methods

Method | HTTP Request | Description
--- | --- | ---
[**api_v1_receivables_get**](ReceivablesApi.md#api_v1_receivables_get) | **GET** /api/v1/receivables | Retrieve receivables
[**api_v1_revenuecenter_get**](ReceivablesApi.md#api_v1_revenuecenter_get) | **GET** /api/v1/revenuecenter | Retrieve cost centers
[**received_put**](ReceivablesApi.md#received_put) | **PUT** /api/v1/receivables/mark-received | Mark receivables as received

### **api_v1_receivables_get**
> `api_v1_receivables_get(registration_date_start, registration_date_end, due_date_start, due_date_end, receiving_date_start, receiving_date_end, competence_date_start, competence_date_end, cancellation_date_start, cancellation_date_end, charge_date_start, charge_date_end, update_date_start, update_date_end, description, ammount_start, ammount_end, payment_types, account_status, take, skip, member_id, id_sale, id_receivable, invoice_date_start, invoice_date_end, invoice_canceled_date_start, invoice_canceled_date_end, sale_date_start, sale_date_end)`

Retrieve receivables based on provided filters.

#### Example
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
api_instance = evo_client.receivables_api.ReceivablesApi(evo_client.ApiClient(configuration))

# Define filter parameters
registration_date_start = '2023-01-01T00:00:00+00:00'  # datetime | Start date for registration (optional)
registration_date_end = '2023-12-31T23:59:59+00:00'    # datetime | End date for registration (optional)
# ... (other parameters)

try:
    # Retrieve receivables
    api_instance.api_v1_receivables_get(
        registration_date_start=registration_date_start,
        registration_date_end=registration_date_end,
        # ... (other parameters)
    )
except ApiException as e:
    print(f"Exception when calling ReceivablesApi->api_v1_receivables_get: {e}\n")
```

#### Parameters

Name | Type | Description | Notes
--- | --- | --- | ---
**registration_date_start** | **datetime** | Start date for account registration (yyyy-mm-dd) | [optional]
**registration_date_end** | **datetime** | End date for account registration (yyyy-mm-dd) | [optional]
**due_date_start** | **datetime** | Start date for account due (yyyy-mm-dd) | [optional]
**due_date_end** | **datetime** | End date for account due (yyyy-mm-dd) | [optional]
**receiving_date_start** | **datetime** | Start date for account receiving (yyyy-mm-dd) | [optional]
**receiving_date_end** | **datetime** | End date for account receiving (yyyy-mm-dd) | [optional]
**competence_date_start** | **datetime** | Start date for account competence (yyyy-mm-dd) | [optional]
**competence_date_end** | **datetime** | End date for account competence (yyyy-mm-dd) | [optional]
**cancellation_date_start** | **datetime** | Start date for account cancellation (yyyy-mm-dd) | [optional]
**cancellation_date_end** | **datetime** | End date for account cancellation (yyyy-mm-dd) | [optional]
**charge_date_start** | **datetime** | Start date for account charge (yyyy-mm-dd) | [optional]
**charge_date_end** | **datetime** | End date for account charge (yyyy-mm-dd) | [optional]
**update_date_start** | **datetime** | Start date for account update (yyyy-mm-dd) | [optional]
**update_date_end** | **datetime** | End date for account update (yyyy-mm-dd) | [optional]
**description** | **str** | Filter by description | [optional]
**ammount_start** | **float** | Minimum amount filter | [optional]
**ammount_end** | **float** | Maximum amount filter | [optional]
**payment_types** | **str** | Comma-separated payment type IDs (e.g., 1,2,3) | [optional]
**account_status** | **str** | Comma-separated account status IDs (e.g., 1,2) | [optional]
**take** | **int** | Number of records to return (max 50) | [optional, default: 50]
**skip** | **int** | Number of records to skip | [optional, default: 0]
**member_id** | **int** | Filter by member ID | [optional]
**id_sale** | **int** | Filter by sale ID | [optional]
**id_receivable** | **int** | Filter by receivable ID | [optional]
**invoice_date_start** | **datetime** | Start date for invoice (yyyy-mm-dd) | [optional]
**invoice_date_end** | **datetime** | End date for invoice (yyyy-mm-dd) | [optional]
**invoice_canceled_date_start** | **datetime** | Start date for canceled invoice (yyyy-mm-dd) | [optional]
**invoice_canceled_date_end** | **datetime** | End date for canceled invoice (yyyy-mm-dd) | [optional]
**sale_date_start** | **datetime** | Start date for sale (yyyy-mm-dd) | [optional]
**sale_date_end** | **datetime** | End date for sale (yyyy-mm-dd) | [optional]

#### Return type

`void` (empty response body)

#### Authorization

[Basic](../README.md#Basic)

#### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

### **api_v1_revenuecenter_get**
> `RevenueCenterApiViewModel api_v1_revenuecenter_get(take, skip)`

Retrieve cost centers.

#### Example
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
api_instance = evo_client.receivables_api.ReceivablesApi(evo_client.ApiClient(configuration))
take = 50  # int | Number of records to return (default: 50)
skip = 0   # int | Number of records to skip (default: 0)

try:
    # Retrieve cost centers
    api_response = api_instance.api_v1_revenuecenter_get(take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling ReceivablesApi->api_v1_revenuecenter_get: {e}\n")
```

#### Parameters

Name | Type | Description | Notes
--- | --- | --- | ---
**take** | **int** | Number of records to return | [optional, default: 50]
**skip** | **int** | Number of records to skip | [optional, default: 0]

#### Return type

[`RevenueCenterApiViewModel`](RevenueCenterApiViewModel.md)

#### Authorization

[Basic](../README.md#Basic)

#### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

### **received_put**
> `received_put(body)`

Mark receivables as received.

#### Example
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
api_instance = evo_client.receivables_api.ReceivablesApi(evo_client.ApiClient(configuration))
body = evo_client.ReceivablesMaskReceivedViewModel()  # ReceivablesMaskReceivedViewModel | (optional)

try:
    api_instance.received_put(body=body)
except ApiException as e:
    print(f"Exception when calling ReceivablesApi->received_put: {e}\n")
```

#### Parameters

Name | Type | Description | Notes
--- | --- | --- | ---
**body** | [`ReceivablesMaskReceivedViewModel`](ReceivablesMaskReceivedViewModel.md) | Data to mark receivables as received | [optional]

#### Return type

`void` (empty response body)

#### Authorization

[Basic](../README.md#Basic)

#### HTTP Request Headers

- **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
- **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
/* End of Selection */
```
