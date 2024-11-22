# evo_client.ProspectsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_prospects_get**](ProspectsApi.md#api_v1_prospects_get) | **GET** /api/v1/prospects | Get prospects
[**api_v1_prospects_post**](ProspectsApi.md#api_v1_prospects_post) | **POST** /api/v1/prospects | Add prospects
[**api_v1_prospects_put**](ProspectsApi.md#api_v1_prospects_put) | **PUT** /api/v1/prospects | Update prospect
[**api_v1_prospects_services_get**](ProspectsApi.md#api_v1_prospects_services_get) | **GET** /api/v1/prospects/services | Get prospect services
[**api_v1_prospects_transfer_post**](ProspectsApi.md#api_v1_prospects_transfer_post) | **POST** /api/v1/prospects/transfer | 

# **api_v1_prospects_get**
> list[ProspectsResumoApiViewModel] api_v1_prospects_get(id_prospect=id_prospect, name=name, document=document, email=email, phone=phone, register_date_start=register_date_start, register_date_end=register_date_end, conversion_date_start=conversion_date_start, conversion_date_end=conversion_date_end, take=take, skip=skip, gympass_id=gympass_id)

Get prospects

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
id_prospect = 56 # int |  (optional)
name = 'name_example' # str |  (optional)
document = 'document_example' # str |  (optional)
email = 'email_example' # str |  (optional)
phone = 'phone_example' # str |  (optional)
register_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
register_date_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
conversion_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
conversion_date_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
gympass_id = '' # str |  (optional)

try:
    # Get prospects
    api_response = api_instance.api_v1_prospects_get(id_prospect=id_prospect, name=name, document=document, email=email, phone=phone, register_date_start=register_date_start, register_date_end=register_date_end, conversion_date_start=conversion_date_start, conversion_date_end=conversion_date_end, take=take, skip=skip, gympass_id=gympass_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProspectsApi->api_v1_prospects_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_prospect** | **int**|  | [optional] 
 **name** | **str**|  | [optional] 
 **document** | **str**|  | [optional] 
 **email** | **str**|  | [optional] 
 **phone** | **str**|  | [optional] 
 **register_date_start** | **datetime**|  | [optional] 
 **register_date_end** | **datetime**|  | [optional] 
 **conversion_date_start** | **datetime**|  | [optional] 
 **conversion_date_end** | **datetime**|  | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **gympass_id** | **str**|  | [optional] 

### Return type

[**list[ProspectsResumoApiViewModel]**](ProspectsResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_prospects_post**
> ProspectIdViewModel api_v1_prospects_post(body=body)

Add prospects

Example body                     Body           {             name(string, required - First Name of the prospect),             email(string, required - E-mail of the prospect),             lastName(string, optional - Last Name of the prospect),             idBranch(int, optional - Branch of the prospect),             ddi(string, optional - Cellphone DDI),             cellphone(string, optional - Cellphone of the prospect),             birthday(DateTime, optional - Birthday of the prospect),             gender(string, optional - Gender of the prospect) { \"M\" = Male, \"F\" = Female, \"P\" = Other },             visit(integer, optional - Origin of the visit of the prospect) { Personal = 1, Email = 2, Telephone = 3, Other = 4 },              marketingType(string, optional - Type of marketing where the prospect met the gym ),             notes(string, optional - Free field for prospect notes),             currentStep(string, optional - Current step in the process for converting the prospect),            }

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
body = evo_client.ProspectApiIntegracaoViewModel() # ProspectApiIntegracaoViewModel |  (optional)

try:
    # Add prospects
    api_response = api_instance.api_v1_prospects_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProspectsApi->api_v1_prospects_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProspectApiIntegracaoViewModel**](ProspectApiIntegracaoViewModel.md)|  | [optional] 

### Return type

[**ProspectIdViewModel**](ProspectIdViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_prospects_put**
> ProspectIdViewModel api_v1_prospects_put(body=body)

Update prospect

Example body                     Body           {             idProspect(int, required - Id of the Prospect),              name(string, required - First Name of the prospect),             email(string, required - E-mail of the prospect),             lastName(string, optional - Last Name of the prospect),             ddi(string, optional - Cellphone DDI),             cellphone(string, optional - Cellphone of the prospect),             birthday(DateTime, optional - Birthday of the prospect),             gender(string, optional - Gender of the prospect) { \"M\" = Male, \"F\" = Female, \"P\" = Other },                            notes(string, optional - Free field for prospect notes),             currentStep(string, optional - Current step in the process for converting the prospect),            }

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
body = evo_client.ProspectApiIntegracaoAtualizacaoViewModel() # ProspectApiIntegracaoAtualizacaoViewModel |  (optional)

try:
    # Update prospect
    api_response = api_instance.api_v1_prospects_put(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProspectsApi->api_v1_prospects_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProspectApiIntegracaoAtualizacaoViewModel**](ProspectApiIntegracaoAtualizacaoViewModel.md)|  | [optional] 

### Return type

[**ProspectIdViewModel**](ProspectIdViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_prospects_services_get**
> list[MemberServiceViewModel] api_v1_prospects_services_get(id_prospect=id_prospect)

Get prospect services

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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
id_prospect = 56 # int | Filter by prospect id (optional)

try:
    # Get prospect services
    api_response = api_instance.api_v1_prospects_services_get(id_prospect=id_prospect)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProspectsApi->api_v1_prospects_services_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_prospect** | **int**| Filter by prospect id | [optional] 

### Return type

[**list[MemberServiceViewModel]**](MemberServiceViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_prospects_transfer_post**
> api_v1_prospects_transfer_post(body=body)



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
api_instance = evo_client.ProspectsApi(evo_client.ApiClient(configuration))
body = evo_client.ProspectTransferenciaViewModel() # ProspectTransferenciaViewModel |  (optional)

try:
    api_instance.api_v1_prospects_transfer_post(body=body)
except ApiException as e:
    print("Exception when calling ProspectsApi->api_v1_prospects_transfer_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProspectTransferenciaViewModel**](ProspectTransferenciaViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

