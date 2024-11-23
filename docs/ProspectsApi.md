# evo_client.ProspectsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

## Methods

Method | HTTP Request | Description
------------- | ------------- | -------------
[**get_prospects**](ProspectsApi.md#get_prospects) | **GET** /api/v1/prospects | Retrieve a list of prospects
[**add_prospects**](ProspectsApi.md#add_prospects) | **POST** /api/v1/prospects | Add new prospects
[**update_prospect**](ProspectsApi.md#update_prospect) | **PUT** /api/v1/prospects | Update an existing prospect
[**get_prospect_services**](ProspectsApi.md#get_prospect_services) | **GET** /api/v1/prospects/services | Retrieve services associated with a prospect
[**transfer_prospect**](ProspectsApi.md#transfer_prospect) | **POST** /api/v1/prospects/transfer | Transfer a prospect to another branch or representative

---

## **get_prospects**
> `List[ProspectsResumoApiViewModel] get_prospects(id_prospect: Optional[int] = None, name: Optional[str] = None, document: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, register_date_start: Optional[datetime] = None, register_date_end: Optional[datetime] = None, conversion_date_start: Optional[datetime] = None, conversion_date_end: Optional[datetime] = None, take: Optional[int] = 50, skip: Optional[int] = 0, gympass_id: Optional[str] = None)`

Retrieve a list of prospects based on the provided filters.

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
id_prospect = 56  # int | (optional)
name = 'Jane Doe'  # str | (optional)
document = '123456789'  # str | (optional)
email = 'jane.doe@example.com'  # str | (optional)
phone = '555-1234'  # str | (optional)
register_date_start = '2023-01-01T00:00:00Z'  # datetime | (optional)
register_date_end = '2023-12-31T23:59:59Z'  # datetime | (optional)
conversion_date_start = '2023-02-01T00:00:00Z'  # datetime | (optional)
conversion_date_end = '2023-11-30T23:59:59Z'  # datetime | (optional)
take = 50  # int | Total number of records to return (default is 50)
skip = 0  # int | Total number of records to skip (default is 0)
gympass_id = 'GP123456'  # str | (optional)

try:
    # Retrieve prospects
    api_response = api_instance.get_prospects(
        id_prospect=id_prospect,
        name=name,
        document=document,
        email=email,
        phone=phone,
        register_date_start=register_date_start,
        register_date_end=register_date_end,
        conversion_date_start=conversion_date_start,
        conversion_date_end=conversion_date_end,
        take=take,
        skip=skip,
        gympass_id=gympass_id
    )
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling ProspectsApi->get_prospects: {e}\n")
```

### Parameters

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **id_prospect** | `int` | Filter by prospect ID | [optional] |
| **name** | `str` | Filter by prospect name | [optional] |
| **document** | `str` | Filter by document number | [optional] |
| **email** | `str` | Filter by email address | [optional] |
| **phone** | `str` | Filter by phone number | [optional] |
| **register_date_start** | `datetime` | Start date for registration date filter | [optional] |
| **register_date_end** | `datetime` | End date for registration date filter | [optional] |
| **conversion_date_start** | `datetime` | Start date for conversion date filter | [optional] |
| **conversion_date_end** | `datetime` | End date for conversion date filter | [optional] |
| **take** | `int` | Number of records to return (max 50) | [optional] [default: 50] |
| **skip** | `int` | Number of records to skip | [optional] [default: 0] |
| **gympass_id** | `str` | Filter by Gympass ID | [optional] |

### Return Type

- `List[ProspectsResumoApiViewModel]`

### Authorization

- [Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: `text/plain`, `application/json`, `text/json`

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

---

## **add_prospects**
> `ProspectIdViewModel add_prospects(body: Optional[ProspectApiIntegracaoViewModel] = None)`

Add a new prospect to the system.

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
body = evo_client.ProspectApiIntegracaoViewModel(
    name='John',
    email='john.doe@example.com',
    lastName='Doe',
    idBranch=1,
    ddi='55',
    cellphone='91234-5678',
    birthday='1990-01-01T00:00:00Z',
    gender='M',
    visit=1,
    marketingType='Online',
    notes='Interested in premium membership.',
    currentStep='Initial Contact'
)

try:
    # Add a new prospect
    api_response = api_instance.add_prospects(body=body)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling ProspectsApi->add_prospects: {e}\n")
```

### Parameters

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **body** | `ProspectApiIntegracaoViewModel` | Details of the prospect to add | [optional] |

### Return Type

- `ProspectIdViewModel`

### Authorization

- [Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: `application/json-patch+json`, `application/json`, `text/json`, `application/*+json`
- **Accept**: `text/plain`, `application/json`, `text/json`

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

---

## **update_prospect**
> `ProspectIdViewModel update_prospect(body: Optional[ProspectApiIntegracaoAtualizacaoViewModel] = None)`

Update an existing prospect's information.

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
body = evo_client.ProspectApiIntegracaoAtualizacaoViewModel(
    idProspect=56,
    name='Jane',
    email='jane.doe@example.com',
    lastName='Doe',
    ddi='55',
    cellphone='99876-5432',
    birthday='1992-02-02T00:00:00Z',
    gender='F',
    notes='Updated contact information.',
    currentStep='Follow Up'
)

try:
    # Update prospect information
    api_response = api_instance.update_prospect(body=body)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling ProspectsApi->update_prospect: {e}\n")
```

### Parameters

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **body** | `ProspectApiIntegracaoAtualizacaoViewModel` | Updated details of the prospect | [optional] |

### Return Type

- `ProspectIdViewModel`

### Authorization

- [Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: `application/json-patch+json`, `application/json`, `text/json`, `application/*+json`
- **Accept**: `text/plain`, `application/json`, `text/json`

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

---

## **get_prospect_services**
> `List[MemberServiceViewModel] get_prospect_services(id_prospect: Optional[int] = None)`

Retrieve services associated with a specific prospect.

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
id_prospect = 56  # int | Filter by prospect ID (optional)

try:
    # Retrieve prospect services
    api_response = api_instance.get_prospect_services(id_prospect=id_prospect)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling ProspectsApi->get_prospect_services: {e}\n")
```

### Parameters

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **id_prospect** | `int` | Filter by prospect ID | [optional] |

### Return Type

- `List[MemberServiceViewModel]`

### Authorization

- [Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: Not defined
- **Accept**: `text/plain`, `application/json`, `text/json`

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

---

## **transfer_prospect**
> `None transfer_prospect(body: Optional[ProspectTransferenciaViewModel] = None)`

Transfer a prospect to another branch or representative.

### Example
```python
from __future__ import print_function
import evo_client
from evo_client.exceptions.api_exceptions import ApiException

# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
body = evo_client.ProspectTransferenciaViewModel(
    idProspect=56,
    newBranchId=2,
    newRepresentativeId=10,
    transferDate='2023-09-01T00:00:00Z',
    notes='Transferring to new branch for better service.'
)

try:
    # Transfer the prospect
    api_instance.transfer_prospect(body=body)
    print("Prospect transferred successfully.")
except ApiException as e:
    print(f"Exception when calling ProspectsApi->transfer_prospect: {e}\n")
```

### Parameters

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **body** | `ProspectTransferenciaViewModel` | Transfer details for the prospect | [optional] |

### Return Type

- `None` (empty response body)

### Authorization

- [Basic](../README.md#Basic)

### HTTP Request Headers

- **Content-Type**: `application/json-patch+json`, `application/json`, `text/json`, `application/*+json`
- **Accept**: `text/plain`, `application/json`, `text/json`

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
```
