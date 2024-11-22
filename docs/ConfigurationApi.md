# evo_client.ConfigurationApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_configuration_gateway_get**](ConfigurationApi.md#api_v1_configuration_gateway_get) | **GET** /api/v1/configuration/gateway | Get gateway configurations
[**api_v1_configuration_get**](ConfigurationApi.md#api_v1_configuration_get) | **GET** /api/v1/configuration | Get branch configurations
[**api_v1_configuration_occupation_get**](ConfigurationApi.md#api_v1_configuration_occupation_get) | **GET** /api/v1/configuration/occupation | Get Occupation
[**flags_get**](ConfigurationApi.md#flags_get) | **GET** /api/v1/configuration/card-flags | Get card flag
[**translation_get**](ConfigurationApi.md#translation_get) | **GET** /api/v1/configuration/card-translation | Get card translation

# **api_v1_configuration_gateway_get**
> EmpresasFiliaisGatewayViewModel api_v1_configuration_gateway_get()

Get gateway configurations

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
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get gateway configurations
    api_response = api_instance.api_v1_configuration_gateway_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->api_v1_configuration_gateway_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**EmpresasFiliaisGatewayViewModel**](EmpresasFiliaisGatewayViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_configuration_get**
> ConfiguracaoApiViewModel api_v1_configuration_get()

Get branch configurations

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
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get branch configurations
    api_response = api_instance.api_v1_configuration_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->api_v1_configuration_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ConfiguracaoApiViewModel**](ConfiguracaoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_configuration_occupation_get**
> list[EmpresasFiliaisOcupacaoViewModel] api_v1_configuration_occupation_get()

Get Occupation

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
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get Occupation
    api_response = api_instance.api_v1_configuration_occupation_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->api_v1_configuration_occupation_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[EmpresasFiliaisOcupacaoViewModel]**](EmpresasFiliaisOcupacaoViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **flags_get**
> list[BandeirasBasicoViewModel] flags_get()

Get card flag

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
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get card flag
    api_response = api_instance.flags_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->flags_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[BandeirasBasicoViewModel]**](BandeirasBasicoViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **translation_get**
> object translation_get()

Get card translation

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
api_instance = evo_client.ConfigurationApi(evo_client.ApiClient(configuration))

try:
    # Get card translation
    api_response = api_instance.translation_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->translation_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

