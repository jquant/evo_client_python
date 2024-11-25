 // Start of Selection
# evo_client.EmployeesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_employee**](EmployeesApi.md#delete_employee) | **DELETE** /api/v1/employees | Delete an employee
[**get_employees**](EmployeesApi.md#get_employees) | **GET** /api/v1/employees | Retrieve a list of employees
[**update_employee**](EmployeesApi.md#update_employee) | **POST** /api/v1/employees | Update an existing employee
[**create_employee**](EmployeesApi.md#create_employee) | **PUT** /api/v1/employees | Add a new employee

# **delete_employee**
> delete_employee(employee_id=employee_id)

Delete an employee

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
employee_id = 56  # int | ID of the employee to delete

try:
    # Delete an employee
    api_instance.delete_employee(employee_id=employee_id)
except ApiException as e:
    print("Exception when calling EmployeesApi->delete_employee: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**employee_id** | **int** | ID of the employee to delete | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_employees**
> get_employees(employee_id=employee_id, name=name, email=email, take=take, skip=skip)

Retrieve a list of employees

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
employee_id = 56  # int | (optional)
name = 'name_example'  # str | (optional)
email = 'email_example'  # str | (optional)
take = 50  # int | Total number of records to return. (optional) (default to 50)
skip = 0  # int | Total number of records to skip. (optional) (default to 0)

try:
    # Retrieve a list of employees
    api_response = api_instance.get_employees(employee_id=employee_id, name=name, email=email, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmployeesApi->get_employees: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**employee_id** | **int** | ID of the employee to filter | [optional] 
**name** | **str** | Filter by employee name | [optional] 
**email** | **str** | Filter by employee email | [optional] 
**take** | **int** | Total number of records to return. | [optional] [default to 50]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]

### Return type

[**list[FuncionariosResumoApiViewModel]**](FuncionariosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_employee**
> update_employee(body=body)

Update an existing employee

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
body = evo_client.EmployeeApiIntegracaoAtualizacaoViewModel()  # EmployeeApiIntegracaoAtualizacaoViewModel | (optional)

try:
    # Update an employee
    api_instance.update_employee(body=body)
except ApiException as e:
    print("Exception when calling EmployeesApi->update_employee: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**body** | [**EmployeeApiIntegracaoAtualizacaoViewModel**](EmployeeApiIntegracaoAtualizacaoViewModel.md) | Employee data to update | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_employee**
> create_employee(body=body)

Add a new employee

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
api_instance = evo_client.EmployeesApi(evo_client.ApiClient(configuration))
body = evo_client.EmployeeApiIntegracaoViewModel()  # EmployeeApiIntegracaoViewModel | (optional)

try:
    # Add a new employee
    api_instance.create_employee(body=body)
except ApiException as e:
    print("Exception when calling EmployeesApi->create_employee: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**body** | [**EmployeeApiIntegracaoViewModel**](EmployeeApiIntegracaoViewModel.md) | Employee data to add | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
