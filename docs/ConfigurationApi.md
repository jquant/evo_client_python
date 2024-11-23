# evo_client.ConfigurationApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_gateway_config**](ConfigurationApi.md#get_gateway_config) | **GET** /api/v1/configuration/gateway | Get gateway configurations
[**get_branch_config**](ConfigurationApi.md#get_branch_config) | **GET** /api/v1/configuration | Get branch configurations
[**get_occupations**](ConfigurationApi.md#get_occupations) | **GET** /api/v1/configuration/occupation | Get Occupation
[**get_card_flags**](ConfigurationApi.md#get_card_flags) | **GET** /api/v1/configuration/card-flags | Get card flags
[**get_translations**](ConfigurationApi.md#get_translations) | **GET** /api/v1/configuration/card-translation | Get card translations

# **get_gateway_config**
> EmpresasFiliaisGatewayViewModel get_gateway_config(async_req: bool = False)

Get gateway configurations

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

# Create an instance of the API class
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get gateway configurations
    api_response = api_instance.get_gateway_config()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_gateway_config: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional]

### Return type

[**EmpresasFiliaisGatewayViewModel**](EmpresasFiliaisGatewayViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_branch_config**
> ConfiguracaoApiViewModel get_branch_config(async_req: bool = False)

Get branch configurations

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

# Create an instance of the API class
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get branch configurations
    api_response = api_instance.get_branch_config()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_branch_config: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional]

### Return type

[**ConfiguracaoApiViewModel**](ConfiguracaoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_occupations**
> list[EmpresasFiliaisOcupacaoViewModel] get_occupations(async_req: bool = True)

Get Occupation

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

# Create an instance of the API class
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get Occupation
    api_response = api_instance.get_occupations()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_occupations: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional]

### Return type

[**list[EmpresasFiliaisOcupacaoViewModel]**](EmpresasFiliaisOcupacaoViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_card_flags**
> list[BandeirasBasicoViewModel] get_card_flags(async_req: bool = False)

Get card flags

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

# Create an instance of the API class
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get card flags
    api_response = api_instance.get_card_flags()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_card_flags: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional]

### Return type

[**list[BandeirasBasicoViewModel]**](BandeirasBasicoViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_translations**
> dict get_translations(async_req: bool = False)

Get card translations

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

# Create an instance of the API class
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get card translations
    api_response = api_instance.get_translations()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_translations: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional]

### Return type

**dict**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
