# evo_client.EmployeesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_employees_delete**](EmployeesApi.md#api_v1_employees_delete) | **DELETE** /api/v1/employees | Delete Employees
[**api_v1_employees_get**](EmployeesApi.md#api_v1_employees_get) | **GET** /api/v1/employees | Get Employees
[**api_v1_employees_post**](EmployeesApi.md#api_v1_employees_post) | **POST** /api/v1/employees | Update Employees
[**api_v1_employees_put**](EmployeesApi.md#api_v1_employees_put) | **PUT** /api/v1/employees | Add Employees

# **api_v1_employees_delete**
> api_v1_employees_delete(id_employee=id_employee)

Delete Employees

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
id_employee = 56 # int |  (optional)

try:
    # Delete Employees
    api_instance.api_v1_employees_delete(id_employee=id_employee)
except ApiException as e:
    print("Exception when calling EmployeesApi->api_v1_employees_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_employee** | **int**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_employees_get**
> list[FuncionariosResumoApiViewModel] api_v1_employees_get(id_employee=id_employee, name=name, email=email, take=take, skip=skip)

Get Employees

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
id_employee = 56 # int |  (optional)
name = 'name_example' # str |  (optional)
email = 'email_example' # str |  (optional)
take = 50 # int | Total number of records to return. (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get Employees
    api_response = api_instance.api_v1_employees_get(id_employee=id_employee, name=name, email=email, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmployeesApi->api_v1_employees_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_employee** | **int**|  | [optional] 
 **name** | **str**|  | [optional] 
 **email** | **str**|  | [optional] 
 **take** | **int**| Total number of records to return. | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**list[FuncionariosResumoApiViewModel]**](FuncionariosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_employees_post**
> api_v1_employees_post(body=body)

Update Employees

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
body = evo_client.EmployeeApiIntegracaoAtualizacaoViewModel() # EmployeeApiIntegracaoAtualizacaoViewModel |  (optional)

try:
    # Update Employees
    api_instance.api_v1_employees_post(body=body)
except ApiException as e:
    print("Exception when calling EmployeesApi->api_v1_employees_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EmployeeApiIntegracaoAtualizacaoViewModel**](EmployeeApiIntegracaoAtualizacaoViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_employees_put**
> api_v1_employees_put(body=body)

Add Employees

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
body = evo_client.EmployeeApiIntegracaoViewModel() # EmployeeApiIntegracaoViewModel |  (optional)

try:
    # Add Employees
    api_instance.api_v1_employees_put(body=body)
except ApiException as e:
    print("Exception when calling EmployeesApi->api_v1_employees_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EmployeeApiIntegracaoViewModel**](EmployeeApiIntegracaoViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

