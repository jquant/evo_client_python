# Combined API Documentation


## ActivitiesApi

# evo_client.ActivitiesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_activities**](ActivitiesApi.md#get_activities) | **GET** /api/v1/activities | Get activities list with optional filtering
[**get_schedule_detail**](ActivitiesApi.md#get_schedule_detail) | **GET** /api/v1/activities/schedule/detail | Get activities schedule details
[**enroll**](ActivitiesApi.md#enroll) | **POST** /api/v1/activities/schedule/enroll | Enroll member in activity schedule
[**get_schedule**](ActivitiesApi.md#get_schedule) | **GET** /api/v1/activities/schedule | Get activities schedule
[**class_post**](ActivitiesApi.md#class_post) | **POST** /api/v1/activities/schedule/experimental-class | Create a new experimental class and enroll the member on it
[**status_post**](ActivitiesApi.md#status_post) | **POST** /api/v1/activities/schedule/enroll/change-status | Change status of a member in activity schedule
[**unavailable_spots_get**](ActivitiesApi.md#unavailable_spots_get) | **GET** /api/v1/activities/list-unavailable-spots | List of spots that are already filled in the activity session

# **get_activities**
> list[AtividadeListApiViewModel] get_activities(search=search, branch_id=branch_id, take=take, skip=skip)

Get activities list with optional filtering.

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))

# Optional parameters
search = ''  # str | Filter by activity name, group name or tags
branch_id = 123  # int | Filter by membership branch ID
take = 10  # int | Number of records to return
skip = 0  # int | Number of records to skip

try:
    # Get activities list
    api_response = api_instance.get_activities(
        search=search,
        branch_id=branch_id,
        take=take,
        skip=skip
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_activities: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str** | Filter by activity name, group name or tags | [optional] 
 **branch_id** | **int** | Filter by membership branch ID | [optional]
 **take** | **int** | Number of records to return | [optional]
 **skip** | **int** | Number of records to skip | [optional]

### Return type

[**list[AtividadeListApiViewModel]**](AtividadeListApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_schedule_detail**
> AtividadeBasicoApiViewModel get_schedule_detail(id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)

Get activities schedule details

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_configuration = 56 # int | Activity IdConfiguration (Must be use combined with activityDate) (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (Must be use combined with idConfiguration) (optional)
id_activity_session = 56 # int | Activity idActivitySession (This is mandatory if IdConfiguration and activityDate are null) (optional)

try:
    # Get activities schedule details
    api_response = api_instance.get_schedule_detail(id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_schedule_detail: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_configuration** | **int**| Activity IdConfiguration (Must be use combined with activityDate) | [optional] 
 **activity_date** | **datetime**| Activity schedule date (yyyy-MM-dd) (Must be use combined with idConfiguration) | [optional] 
 **id_activity_session** | **int**| Activity idActivitySession (This is mandatory if IdConfiguration and activityDate are null) | [optional] 

### Return type

[**AtividadeBasicoApiViewModel**](AtividadeBasicoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enroll**
> enroll(id_configuration=id_configuration, activity_date=activity_date, slot_number=slot_number, id_member=id_member, id_prospect=id_prospect, origin=origin)

Enroll member in activity schedule

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_configuration = 56 # int | Activity IdConfiguration (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (optional)
slot_number = 0 # int | Slot number (only available in activites that allow spot booking) (optional) (default to 0)
id_member = 0 # int | Id Member (this is required if IdProspect is null) (optional) (default to 0)
id_prospect = 0 # int | Id Member (this is required if IdMember is null) (optional) (default to 0)
origin = evo_client.EOrigemAgendamento() # EOrigemAgendamento |  (optional)

try:
    # Enroll member in activity schedule
    api_instance.enroll(id_configuration=id_configuration, activity_date=activity_date, slot_number=slot_number, id_member=id_member, id_prospect=id_prospect, origin=origin)
except ApiException as e:
    print("Exception when calling ActivitiesApi->enroll: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_configuration** | **int** | Activity IdConfiguration | [optional] 
 **activity_date** | **datetime** | Activity schedule date (yyyy-MM-dd) | [optional] 
 **slot_number** | **int** | Slot number (only available in activites that allow spot booking) | [optional] [default to 0]
 **id_member** | **int** | Id Member (this is required if IdProspect is null) | [optional] [default to 0]
 **id_prospect** | **int** | Id Member (this is required if IdMember is null) | [optional] [default to 0]
 **origin** | [**EOrigemAgendamento**](.md) |  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_activities_schedule_get**
> list[AtividadeAgendaApiViewModel] api_v1_activities_schedule_get(id_member=id_member, take=take, only_availables=only_availables, _date=_date, show_full_week=show_full_week, id_branch=id_branch, id_activities=id_activities, id_audiences=id_audiences, id_branch_token=id_branch_token)

Get activities schedule with various filtering options.

Status codes:
- 0: Free
- 1: Available  
- 2: Full
- 3: Reservation Closed
- 4: Restricted
- 5: Registered
- 6: Finished
- 7: Cancelled
- 8: In Queue
- 10: Free Closed
- 11: Restricted Closed
- 12: Restricted Not Allowed
- 15: Full No Waiting List

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))

try:
    # Get activities schedule
    api_response = api_instance.get_schedule(
        member_id=123,
        date=datetime.now(),
        branch_id=456,
        activity_ids=[1, 2, 3],
        audience_ids=[4, 5, 6],
        take=10,
        only_availables=False,
        show_full_week=False,
        branch_token="token123"
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_schedule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int** | Filter by a member | [optional]
 **date** | **datetime** | Filter by a specific date | [optional]
 **branch_id** | **int** | Filter by a different branch than the current one | [optional]
 **activity_ids** | **List[int]** | Filter by activity IDs | [optional]
 **audience_ids** | **List[int]** | Filter by audience IDs | [optional]
 **take** | **int** | Limit the amount of items returned | [optional]
 **only_availables** | **bool** | Filter by activities that are available | [optional] [default to False]
 **show_full_week** | **bool** | Show all activities in the week (Sunday to Saturday) | [optional] [default to False]
 **branch_token** | **str** | Filter by a different branch token | [optional]

### Return type

[**list[AtividadeAgendaApiViewModel]**](AtividadeAgendaApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experimental_class**
> create_experimental_class(prospect_id=prospect_id, activity_date=activity_date, activity=activity, service=service, activity_exists=activity_exists, branch_id=branch_id)

Create a new experimental class and enroll the member on it

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
prospect_id = 56 # int | IdProspect of who will participate from class (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date and time (yyyy-MM-dd HH:mm) (optional)
activity = 'activity_example' # str | Activity name (optional)
service = 'service_example' # str | Service that will be sold to allow the trial class (optional)
activity_exists = False # bool |  (optional) (default to false)
branch_id = 56 # int |  (optional)

try:
    # Create a new experimental class and enroll the member on it
    api_instance.create_experimental_class(prospect_id=prospect_id, activity_date=activity_date, activity=activity, service=service, activity_exists=activity_exists, branch_id=branch_id)
except ApiException as e:
    print("Exception when calling ActivitiesApi->create_experimental_class: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prospect_id** | **int**| IdProspect of who will participate from class | [optional] 
 **activity_date** | **datetime**| Activity schedule date and time (yyyy-MM-dd HH:mm) | [optional] 
 **activity** | **str**| Activity name | [optional] 
 **service** | **str**| Service that will be sold to allow the trial class | [optional] 
 **activity_exists** | **bool**|  | [optional] [default to false]
 **branch_id** | **int**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **change_status**
> change_status(status=status, member_id=member_id, prospect_id=prospect_id, id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)

Change status of a member in activity schedule

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
status = evo_client.EStatusAtividadeSessao() # EStatusAtividadeSessao | New status to be setted (Types: Attending = 0, Absent = 1, Justified absence = 2) (optional)
member_id = 56 # int | Id Member (optional)
prospect_id = 56 # int | Id Prospect (optional)
config_id = 56 # int | Activity IdConfiguration - only used when idActivitySession is null) (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) - only used when idActivitySession is null) (optional)
session_id = 56 # int | IdActivity Session (optional)

try:
    # Change status of a member in activity schedule
    api_instance.change_status(status=status, member_id=member_id, prospect_id=prospect_id, config_id=config_id, activity_date=activity_date, session_id=session_id)
except ApiException as e:
    print("Exception when calling ActivitiesApi->change_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | [**EStatusAtividadeSessao**](.md)| New status to be setted (Types: Attending &#x3D; 0, Absent &#x3D; 1, Justified absence &#x3D; 2) | [optional] 
 **member_id** | **int**| Id Member | [optional] 
 **prospect_id** | **int**| Id Prospect | [optional] 
 **config_id** | **int**| Activity IdConfiguration - only used when idActivitySession is null) | [optional] 
 **activity_date** | **datetime**| Activity schedule date (yyyy-MM-dd) - only used when idActivitySession is null) | [optional] 
 **session_id** | **int**| IdActivity Session | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_unavailable_spots**
> get_unavailable_spots(config_id=config_id, date=date)

List of spots that are already filled in the activity session

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
config_id = 56 # int | Activity IdConfiguration (optional)
date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (optional)

try:
    # List of spots that are already filled in the activity session
    api_instance.get_unavailable_spots(config_id=config_id, date=date)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_unavailable_spots: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **config_id** | **int**| Activity IdConfiguration | [optional] 
 **date** | **datetime**| Activity schedule date (yyyy-MM-dd) | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)



---

## BankAccountsApi

# evo_client.BankAccountsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_accounts**](BankAccountsApi.md#get_accounts) | **GET** /api/v1/bank-accounts | Get bank accounts

# **get_accounts**
> BankAccountsViewModel get_accounts()

Get bank accounts

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
api_instance = evo_client.BankAccountsApi(evo_client.ApiClient(configuration))

try:
    # Get bank accounts
    api_response = api_instance.get_accounts()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankAccountsApi->get_accounts: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BankAccountsViewModel**](BankAccountsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)



---

## ClienteEnotasRetorno

# ClienteEnotasRetorno

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id_cliente** | **int** |  | [optional] 
**tipo_pessoa** | **str** |  | [optional] 
**nome** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**cpf_cnpj** | **str** |  | [optional] 
**inscricao_municipal** | **str** |  | [optional] 
**telefone** | **str** |  | [optional] 
**endereco** | [**EnderecoEnotasRetorno**](EnderecoEnotasRetorno.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## ConfigurationApi

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


---

## EFormaContato

# EFormaContato

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EFormaPagamentoTotem

# EFormaPagamentoTotem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EOrigemAgendamento

# EOrigemAgendamento

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EStatusAtividade

# EStatusAtividade

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EStatusAtividadeSessao

# EStatusAtividadeSessao

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## ETipoContrato

# ETipoContrato

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## ETipoGateway

# ETipoGateway

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EmployeesApi

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


---

## EnderecoEnotasRetorno

# EnderecoEnotasRetorno

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pais** | **str** |  | [optional] 
**uf** | **str** |  | [optional] 
**cidade** | **str** |  | [optional] 
**logradouro** | **str** |  | [optional] 
**numero** | **str** |  | [optional] 
**complemento** | **str** |  | [optional] 
**bairro** | **str** |  | [optional] 
**cep** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EnotasRetorno

# EnotasRetorno

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**tipo** | **str** |  | [optional] 
**id_externo** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**motivo_status** | **str** |  | [optional] 
**ambiente_emissao** | **str** |  | [optional] 
**enviada_por_email** | **bool** |  | [optional] 
**data_criacao** | **datetime** |  | [optional] 
**data_ultima_alteracao** | **datetime** |  | [optional] 
**cliente** | [**ClienteEnotasRetorno**](ClienteEnotasRetorno.md) |  | [optional] 
**numero** | **str** |  | [optional] 
**codigo_verificacao** | **str** |  | [optional] 
**chave_acesso** | **str** |  | [optional] 
**data_autorizacao** | **datetime** |  | [optional] 
**link_download_pdf** | **str** |  | [optional] 
**link_download_xml** | **str** |  | [optional] 
**numero_rps** | **int** |  | [optional] 
**serie_rps** | **str** |  | [optional] 
**data_competencia_rps** | **datetime** |  | [optional] 
**servico** | [**ServicoEnotasRetorno**](ServicoEnotasRetorno.md) |  | [optional] 
**natureza_operacao** | **str** |  | [optional] 
**valor_cofins** | **float** |  | [optional] 
**valor_csll** | **float** |  | [optional] 
**valor_inss** | **float** |  | [optional] 
**valor_ir** | **float** |  | [optional] 
**valor_pis** | **float** |  | [optional] 
**deducoes** | **float** |  | [optional] 
**descontos** | **float** |  | [optional] 
**outras_retencoes** | **float** |  | [optional] 
**valor_total** | **float** |  | [optional] 
**valor_iss** | **float** |  | [optional] 
**observacoes** | **str** |  | [optional] 
**metadados** | [**MetadadosEnotasRetorno**](MetadadosEnotasRetorno.md) |  | [optional] 
**tipo_nf** | **str** |  | [optional] 
**id_filial** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## EntriesApi

# evo_client.EntriesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_entries_get**](EntriesApi.md#api_v1_entries_get) | **GET** /api/v1/entries | Get Entries

# **api_v1_entries_get**
> list[EntradasResumoApiViewModel] or AsyncResult[Any] api_v1_entries_get(register_date_start=register_date_start, register_date_end=register_date_end, take=take, skip=skip, id_entry=id_entry, id_member=id_member, async_req=async_req)

Get Entries

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
api_instance = evo_client.EntriesApi(evo_client.ApiClient(configuration))
register_date_start = '2013-10-20T19:20:30+01:00' # datetime | DateTime date start (optional)
register_date_end = '2013-10-20T19:20:30+01:00' # datetime | DateTime date end (optional)
take = 50 # int | Total number of records to return. (Maximum of 1000) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
id_entry = 0 # int | ID of the entry to return. (optional) (default to 0)
id_member = 56 # int | ID of the member to return (optional)
async_req = False # bool | Execute request asynchronously (optional)

try:
    # Get Entries
    api_response = api_instance.api_v1_entries_get(
        register_date_start=register_date_start,
        register_date_end=register_date_end,
        take=take,
        skip=skip,
        id_entry=id_entry,
        id_member=id_member,
        async_req=async_req
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EntriesApi->api_v1_entries_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
    **register_date_start** | **datetime**| DateTime date start | [optional] 
    **register_date_end** | **datetime**| DateTime date end | [optional] 
    **take** | **int**| Total number of records to return. (Maximum of 1000) | [optional] [default to 50]
    **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
    **id_entry** | **int**| ID of the entry to return. | [optional] [default to 0]
    **id_member** | **int**| ID of the member to return | [optional] 
    **async_req** | **bool**| Execute request asynchronously | [optional] [default to False]

### Return type

[**list[EntradasResumoApiViewModel]**](EntradasResumoApiViewModel.md) or **AsyncResult[Any]**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

    - **Content-Type**: Not defined
    - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


---

## HttpResponseError

# HttpResponseError

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mensagens** | **list[str]** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## InvoicesApi

 // Start of Selection
# evo_client.InvoicesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_invoices**](InvoicesApi.md#get_invoices) | **GET** /api/v1/invoices/get-invoices | Get invoices by date and filters

# **get_invoices**
> Union[EnotasRetorno, AsyncResult[Any]] get_invoices(issue_date_start=issue_date_start, issue_date_end=issue_date_end, competency_date_start=competency_date_start, competency_date_end=competency_date_end, send_date_start=send_date_start, send_date_end=send_date_end, take=take, skip=skip, member_id=member_id, status_invoice=status_invoice, types_invoice=types_invoice, async_req=async_req)

Get invoices by date and various filters.

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
api_instance = evo_client.InvoicesApi(evo_client.ApiClient(configuration))
issue_date_start = '2023-01-01T00:00:00+00:00'  # datetime | Filter by the invoice issuance start date (yyyy-mm-dd) (optional)
issue_date_end = '2023-12-31T23:59:59+00:00'    # datetime | Filter by the invoice issuance end date (yyyy-mm-dd) (optional)
competency_date_start = '2023-01-01T00:00:00+00:00'  # datetime | Filter by competency start date (yyyy-mm-dd) (optional)
competency_date_end = '2023-12-31T23:59:59+00:00'    # datetime | Filter by competency end date (yyyy-mm-dd) (optional)
send_date_start = '2023-01-01T00:00:00+00:00'        # datetime | Filter by the invoice sending start date (yyyy-mm-dd) (optional)
send_date_end = '2023-12-31T23:59:59+00:00'          # datetime | Filter by the invoice sending end date (yyyy-mm-dd) (optional)
take = 25                                           # int | Total number of records to return. (Maximum of 250) (optional, default to 25)
skip = 0                                            # int | Total number of records to skip. (optional, default to 0)
member_id = 56                                      # int | Filter by a member ID (optional)
status_invoice = [evro_client.InvoiceStatus.ISSUED, evro_client.InvoiceStatus.CANCELED]  # List[InvoiceStatus] | Filter by a list of invoice statuses (optional)
types_invoice = [evro_client.InvoiceType.NFSE, evro_client.InvoiceType.NFE]                # List[InvoiceType] | Filter by a list of invoice types (optional)
async_req = False                                   # bool | Execute request asynchronously (optional)

try:
    # Get invoices by date and filters
    api_response = api_instance.get_invoices(
        issue_date_start=issue_date_start,
        issue_date_end=issue_date_end,
        competency_date_start=competency_date_start,
        competency_date_end=competency_date_end,
        send_date_start=send_date_start,
        send_date_end=send_date_end,
        take=take,
        skip=skip,
        member_id=member_id,
        status_invoice=status_invoice,
        types_invoice=types_invoice,
        async_req=async_req
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvoicesApi->get_invoices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_date_start** | **datetime** | Filter by the invoice issuance start date (yyyy-mm-dd) | [optional] 
 **issue_date_end** | **datetime** | Filter by the invoice issuance end date (yyyy-mm-dd) | [optional] 
 **competency_date_start** | **datetime** | Filter by competency start date (yyyy-mm-dd) | [optional] 
 **competency_date_end** | **datetime** | Filter by competency end date (yyyy-mm-dd) | [optional] 
 **send_date_start** | **datetime** | Filter by the invoice sending start date (yyyy-mm-dd) | [optional] 
 **send_date_end** | **datetime** | Filter by the invoice sending end date (yyyy-mm-dd) | [optional] 
 **take** | **int** | Total number of records to return. (Maximum of 250) | [optional] [default to 25]
 **skip** | **int** | Total number of records to skip. | [optional] [default to 0]
 **member_id** | **int** | Filter by a member ID | [optional] 
 **status_invoice** | **List[InvoiceStatus]** | Filter by a list of invoice statuses. Status options: 1 - Issued, 2 - With error, 3 - Canceled | [optional] 
 **types_invoice** | **List[InvoiceType]** | Filter by a list of invoice types. Type options: 1 - NFSe, 2 - NFe, 3 - NFCe | [optional] 
 **async_req** | **bool** | Execute request asynchronously | [optional] 

### Return type

[**Union[EnotasRetorno, AsyncResult[Any]]**](EnotasRetorno.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


---

## ManagmentApi

# evo_client.ManagementApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_active_clients**](ManagmentApi.md#get_active_clients) | **GET** /api/v1/management/activeclients | Get active Clients
[**get_prospects**](ManagmentApi.md#get_prospects) | **GET** /api/v1/management/prospects | Get Prospects
[**get_non_renewed_clients**](ManagmentApi.md#get_non_renewed_clients) | **GET** /api/v1/management/not-renewed | Get non-renewed Clients

# **get_active_clients**
> list[ClientesAtivosViewModel] get_active_clients()

Get active Clients

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
api_instance = evo_client.ManagementApi(evo_client.ApiClient(configuration))

try:
    # Get active Clients
    api_response = api_instance.get_active_clients()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagementApi->get_active_clients: %s\n" % e)
```

### Parameters
This endpoint does not need any parameters.

### Return type

[**list[ClientesAtivosViewModel]**](ClientesAtivosViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_prospects**
> list[SpsRelProspectsCadastradosConvertidos] get_prospects(dt_start=dt_start, dt_end=dt_end)

Get Prospects

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
api_instance = evo_client.ManagementApi(evo_client.ApiClient(configuration))
dt_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
dt_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

try:
    # Get Prospects
    api_response = api_instance.get_prospects(dt_start=dt_start, dt_end=dt_end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagementApi->get_prospects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**dt_start** | **datetime**| Start date filter | [optional] 
**dt_end** | **datetime**| End date filter | [optional] 

### Return type

[**list[SpsRelProspectsCadastradosConvertidos]**](SpsRelProspectsCadastradosConvertidos.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_non_renewed_clients**
> list[ContratoNaoRenovadosViewModel] get_non_renewed_clients(dt_start=dt_start, dt_end=dt_end)

Get non-renewed Clients

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
api_instance = evo_client.ManagementApi(evo_client.ApiClient(configuration))
dt_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
dt_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

try:
    # Get non-renewed Clients
    api_response = api_instance.get_non_renewed_clients(dt_start=dt_start, dt_end=dt_end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManagementApi->get_non_renewed_clients: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**dt_start** | **datetime**| Start date filter | [optional] 
**dt_end** | **datetime**| End date filter | [optional] 

### Return type

[**list[ContratoNaoRenovadosViewModel]**](ContratoNaoRenovadosViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


---

## MemberMembershipApi

# evo_client.MemberMembershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_membership**](MemberMembershipApi.md#cancel_membership) | **POST** /api/v1/membermembership/cancellation | Cancel MemberMembership
[**get_canceled_memberships**](MemberMembershipApi.md#get_canceled_memberships) | **GET** /api/v2/membermembership | Get summary of canceled MemberMemberships

# **cancel_membership**
> cancel_membership(id_member_membership=id_member_membership, id_member_branch=id_member_branch, cancellation_date=cancellation_date, reason_cancellation=reason_cancellation, notice_cancellaton=notice_cancellaton, cancel_future_releases=cancel_future_releases, cancel_future_sessions=cancel_future_sessions, convert_credit_days=convert_credit_days, schedule_cancellation=schedule_cancellation, schedule_cancellation_date=schedule_cancellation_date, add_fine=add_fine, value_fine=value_fine)

Cancel MemberMembership

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
api_instance = evo_client.MemberMembershipApi(evo_client.ApiClient(configuration))
id_member_membership = 56 # int | Id MemberMembership (optional)
id_member_branch = 56 # int | Id Member Branch of Cancellation (optional)
cancellation_date = '2013-10-20T19:20:30+01:00' # datetime | Date of cancellation (optional)
reason_cancellation = 'reason_cancellation_example' # str | Reason of Cancellation (optional)
notice_cancellaton = '' # str | Notes of Cancellation (optional)
cancel_future_releases = False # bool | If 'true' all the releases will be canceled (optional) (default to false)
cancel_future_sessions = False # bool | If 'true' all the sessions will be canceled (optional) (default to false)
convert_credit_days = False # bool | Convert all remaining credits and days to use (optional) (default to false)
schedule_cancellation = False # bool | Activate or deactivate schedule cancellation date (optional) (default to false)
schedule_cancellation_date = '2013-10-20T19:20:30+01:00' # datetime | Date of Cancellation if ScheduleCancellation = 'true' (optional)
add_fine = False # bool | Activate or deactivate Fine (optional) (default to false)
value_fine = 1.2 # float | Value of Fine, to use param AddFine must have activated (optional)

try:
    # Cancel MemberMembership
    api_instance.cancel_membership(id_member_membership=id_member_membership, id_member_branch=id_member_branch, cancellation_date=cancellation_date, reason_cancellation=reason_cancellation, notice_cancellaton=notice_cancellaton, cancel_future_releases=cancel_future_releases, cancel_future_sessions=cancel_future_sessions, convert_credit_days=convert_credit_days, schedule_cancellation=schedule_cancellation, schedule_cancellation_date=schedule_cancellation_date, add_fine=add_fine, value_fine=value_fine)
except ApiException as e:
    print("Exception when calling MemberMembershipApi->cancel_membership: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member_membership** | **int**| Id MemberMembership | [optional] 
 **id_member_branch** | **int**| Id Member Branch of Cancellation | [optional] 
 **cancellation_date** | **datetime**| Date of cancellation | [optional] 
 **reason_cancellation** | **str**| Reason of Cancellation | [optional] 
 **notice_cancellaton** | **str**| Notes of Cancellation | [optional] 
 **cancel_future_releases** | **bool**| If &#x27;true&#x27; all the releases will be canceled | [optional] [default to false]
 **cancel_future_sessions** | **bool**| If &#x27;true&#x27; all the sessions will be canceled | [optional] [default to false]
 **convert_credit_days** | **bool**| Convert all remaining credits and days to use | [optional] [default to false]
 **schedule_cancellation** | **bool**| Activate or deactivate schedule cancellation date | [optional] [default to false]
 **schedule_cancellation_date** | **datetime**| Date of Cancellation if ScheduleCancellation &#x3D; &#x27;true&#x27; | [optional] 
 **add_fine** | **bool**| Activate or deactivate Fine | [optional] [default to false]
 **value_fine** | **float**| Value of Fine, to use param AddFine must have activated | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_canceled_memberships**
> list[ContratosCanceladosResumoApiViewModel] get_canceled_memberships(id_member=id_member, id_membership=id_membership, member_name=member_name, register_date_start=register_date_start, register_date_end=register_date_end, cancel_date_start=cancel_date_start, cancel_date_end=cancel_date_end, show_transfers=show_transfers, show_aggregators=show_aggregators, show_vips=show_vips, contract_type=contract_type, take=take, skip=skip)

Get summary of canceled MemberMemberships

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
api_instance = evo_client.MemberMembershipApi(evo_client.ApiClient(configuration))
id_member = 56 # int |  (optional)
id_membership = 56 # int |  (optional)
member_name = 'member_name_example' # str |  (optional)
register_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
register_date_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
cancel_date_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
cancel_date_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
show_transfers = False # bool | Show transferred contracts. (optional) (default to false)
show_aggregators = False # bool | Show aggregators contracts. (optional) (default to false)
show_vips = False # bool | Show VIP category contracts. (optional) (default to false)
contract_type = 'contract_type_example' # str | Filter by a comma separated list of types of contract. types: 1 - Common, 3 - Plan extension, 4 - Locking extension, 5 - Monthly recurring, 6 - Recurring monthly with validity, 7 - Monthly recurring with automatic renewal, 8 - Additional dependent, 9 - Annual with a specific end, 10 - Additional contract (optional)
take = 25 # int | Total number of records to return. (Maximum of 25) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get summary of canceled MemberMemberships
    api_response = api_instance.get_canceled_memberships(id_member=id_member, id_membership=id_membership, member_name=member_name, register_date_start=register_date_start, register_date_end=register_date_end, cancel_date_start=cancel_date_start, cancel_date_end=cancel_date_end, show_transfers=show_transfers, show_aggregators=show_aggregators, show_vips=show_vips, contract_type=contract_type, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MemberMembershipApi->get_canceled_memberships: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**|  | [optional] 
 **id_membership** | **int**|  | [optional] 
 **member_name** | **str**|  | [optional] 
 **register_date_start** | **datetime**|  | [optional] 
 **register_date_end** | **datetime**|  | [optional] 
 **cancel_date_start** | **datetime**|  | [optional] 
 **cancel_date_end** | **datetime**|  | [optional] 
 **show_transfers** | **bool**| Show transferred contracts. | [optional] [default to false]
 **show_aggregators** | **bool**| Show aggregators contracts. | [optional] [default to false]
 **show_vips** | **bool**| Show VIP category contracts. | [optional] [default to false]
 **contract_type** | **str**| Filter by a comma separated list of types of contract. types: 1 - Common, 3 - Plan extension, 4 - Locking extension, 5 - Monthly recurring, 6 - Recurring monthly with validity, 7 - Monthly recurring with automatic renewal, 8 - Additional dependent, 9 - Annual with a specific end, 10 - Additional contract | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 25) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[list[ContratosCanceladosResumoApiViewModel]](ContratosCanceladosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
# End of Selection
```


---

## MembersApi

# evo_client.MembersApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authenticate_member**](MembersApi.md#authenticate_member) | **POST** /api/v1/members/auth | Authenticate member
[**get_basic_info**](MembersApi.md#get_basic_info) | **GET** /api/v1/members/basic | Get basic member information
[**get_fitcoins**](MembersApi.md#get_fitcoins) | **GET** /api/v1/members/fitcoins | Get member fitcoins
[**update_fitcoins**](MembersApi.md#update_fitcoins) | **PUT** /api/v1/members/fitcoins | Update member fitcoins
[**get_members**](MembersApi.md#get_members) | **GET** /api/v1/members | Get members list
[**update_member_card**](MembersApi.md#update_member_card) | **PUT** /api/v1/members/{idMember}/card | Update member card number
[**get_member_profile**](MembersApi.md#get_member_profile) | **GET** /api/v1/members/{idMember} | Get member profile
[**reset_password**](MembersApi.md#reset_password) | **GET** /api/v1/members/resetPassword | Get password reset link
[**get_member_services**](MembersApi.md#get_member_services) | **GET** /api/v1/members/services | Get member services
[**transfer_member**](MembersApi.md#transfer_member) | **POST** /api/v1/members/transfer | Transfer member to another branch
[**update_member_data**](MembersApi.md#update_member_data) | **PATCH** /api/v1/members/update-member-data/{idMember} | Update basic member data

# **authenticate_member**
> MemberAuthenticateViewModel authenticate_member(email: str, password: str, change_password: bool = False, async_req: bool = False)

Authenticate member.

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Authenticate member
    response = api_instance.authenticate_member(
        email="user@example.com",
        password="password123",
        change_password=False
    )
    print(response)
except Exception as e:
    print(f"Exception when calling authenticate_member: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**email** | **str** | Member email | 
**password** | **str** | Member password |
**change_password** | **bool** | True if password needs to be changed | [optional] [default to False]
**async_req** | **bool** | Execute request asynchronously | [optional] [default to False]

### Return type

[**MemberAuthenticateViewModel**](MemberAuthenticateViewModel.md)

# **get_basic_info**
> MembersBasicApiViewModel get_basic_info(email: str, document: str, phone: str, id_member: int, take: int = 50, skip: int = 0)

Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.
    response = api_instance.get_basic_info(
        email="user@example.com",
        document="1234567890",
        phone="1112341234",
        id_member=56
    )
    print(response)
except Exception as e:
    print(f"Exception when calling get_basic_info: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**email** | **str** | Filter by a member e-mail | 
**document** | **str** | Filter by a member document | 
**phone** | **str** | Filter by a member telephone or cellphone Ex.:1112341234 | 
**id_member** | **int** | Filter by member id | 
**take** | **int** | Total number of records to return. (Maximum of 50) | [optional] [default to 50]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]

### Return type

[**MembersBasicApiViewModel**](MembersBasicApiViewModel.md)

# **get_fitcoins**
> void get_fitcoins(id_member: int)

Get member fitcoins

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get member fitcoins
    api_instance.get_fitcoins(id_member=56)
except Exception as e:
    print(f"Exception when calling get_fitcoins: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Id Member | 

### Return type

void (empty response body)

# **update_fitcoins**
> void update_fitcoins(id_member: int, type: int, fitcoin: int, reason: str)

Update member fitcoins

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Update member fitcoins
    api_instance.update_fitcoins(
        id_member=56,
        type=1,
        fitcoin=56,
        reason="Reason for adding fitcoins"
    )
except Exception as e:
    print(f"Exception when calling update_fitcoins: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Id Member | 
**type** | **int** | 1 - Add Fitcoins, 2 - Remove Fitcoins | 
**fitcoin** | **int** | Quantity add/remove fitcoin | 
**reason** | **str** | Reason add/remove fitcoin | 

### Return type

void (empty response body)

# **get_members**
> MembersApiViewModel get_members(name: str, email: str, document: str, phone: str, conversion_date_start: datetime, conversion_date_end: datetime, register_date_start: datetime, register_date_end: datetime, membership_start_date_start: datetime, membership_start_date_end: datetime, membership_cancel_date_start: datetime, membership_cancel_date_end: datetime, status: int, token_gympass: str, take: int = 50, skip: int = 0, ids_members: str = None, only_personal: bool = False, personal_type: int = None, show_activity_data: bool = False)

Get members

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get members
    response = api_instance.get_members(
        name="John Doe",
        email="john@example.com",
        document="1234567890",
        phone="1112341234",
        conversion_date_start="2013-10-20T19:20:30+01:00",
        conversion_date_end="2013-10-20T19:20:30+01:00",
        register_date_start="2013-10-20T19:20:30+01:00",
        register_date_end="2013-10-20T19:20:30+01:00",
        membership_start_date_start="2013-10-20T19:20:30+01:00",
        membership_start_date_end="2013-10-20T19:20:30+01:00",
        membership_cancel_date_start="2013-10-20T19:20:30+01:00",
        membership_cancel_date_end="2013-10-20T19:20:30+01:00",
        status=1,
        token_gympass="gympass123",
        take=50,
        skip=0,
        ids_members="1,2,3",
        only_personal=False,
        personal_type=1,
        show_activity_data=False
    )
    print(response)
except Exception as e:
    print(f"Exception when calling get_members: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**name** | **str** | Filter by members name | 
**email** | **str** | Filter by a member e-mail | 
**document** | **str** | Filter by a member document | 
**phone** | **str** | Filter by a member telephone or cellphone Ex.:1112341234 | 
**conversion_date_start** | **datetime** | Filter by a member conversion date starting in: (yyyy-mm-dd) | 
**conversion_date_end** | **datetime** | Filter by a member conversion date ending in: (yyyy-mm-dd) | 
**register_date_start** | **datetime** | Filter by a member register date starting in: (yyyy-mm-dd) | 
**register_date_end** | **datetime** | Filter by a member register date ending in: (yyyy-mm-dd) | 
**membership_start_date_start** | **datetime** | Filter by a membership start date from: (yyyy-mm-dd) | 
**membership_start_date_end** | **datetime** | Filter by a membership start date to: (yyyy-mm-dd) | 
**membership_cancel_date_start** | **datetime** | Filter by a membership cancel date from: (yyyy-mm-dd) | 
**membership_cancel_date_end** | **datetime** | Filter by a membership cancel date to: (yyyy-mm-dd) | 
**status** | **int** | Filter by a member state: 1 - Active (Suspendeds and Vips included), 2 - Inactive | 
**token_gympass** | **str** | Filter by the member gympass token gympass | 
**take** | **int** | Total number of records to return. (Maximum of 50) | [optional] [default to 50]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]
**ids_members** | **str** | Filter by member ids. Add member ids separated by comma. Example: 1,2,3 | [optional]
**only_personal** | **bool** | Show only personal trainers | [optional] [default to False]
**personal_type** | **int** | Filter by personal type: 1 - Internal, 2 - External | [optional]
**show_activity_data** | **bool** |  | [optional] [default to False]

### Return type

[**MembersApiViewModel**](MembersApiViewModel.md)

# **update_member_card**
> void update_member_card(id_member: int, card_number: str)

Update member card number

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Update member card number
    api_instance.update_member_card(
        id_member=56,
        card_number="1234567890"
    )
except Exception as e:
    print(f"Exception when calling update_member_card: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by a member | 
**card_number** | **str** | Card number | [optional]

### Return type

void (empty response body)

# **get_member_profile**
> ClienteDetalhesBasicosApiViewModel get_member_profile(id_member: int)

Get member profile

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get member profile
    response = api_instance.get_member_profile(id_member=56)
    print(response)
except Exception as e:
    print(f"Exception when calling get_member_profile: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by a member | 

### Return type

[**ClienteDetalhesBasicosApiViewModel**](ClienteDetalhesBasicosApiViewModel.md)

# **reset_password**
> MemberAuthenticateViewModel reset_password(sign_in: bool, user: str)

Get password reset link

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get password reset link
    response = api_instance.reset_password(
        sign_in=True,
        user="1234567890"
    )
    print(response)
except Exception as e:
    print(f"Exception when calling reset_password: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**sign_in** | **bool** | Check true if after change password you want sign in | [optional]
**user** | **str** | Filter by CPF, idMember or e-mail | 

### Return type

[**MemberAuthenticateViewModel**](MemberAuthenticateViewModel.md)

# **get_member_services**
> list[MemberServiceViewModel] get_member_services(id_member: int)

Get member services

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Get member services
    response = api_instance.get_member_services(id_member=56)
    print(response)
except Exception as e:
    print(f"Exception when calling get_member_services: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** | Filter by member id | 

### Return type

[**list[MemberServiceViewModel]**](MemberServiceViewModel.md)

# **transfer_member**
> void transfer_member(body: ClienteTransferenciaViewModel)

Transfer member to another branch

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Transfer member to another branch
    api_instance.transfer_member(body=ClienteTransferenciaViewModel())
except Exception as e:
    print(f"Exception when calling transfer_member: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**body** | [**ClienteTransferenciaViewModel**](ClienteTransferenciaViewModel.md) |  | 

### Return type

void (empty response body)

# **update_member_data**
> bool update_member_data(id_member: int, body: MemberDataViewModel)

Update basic member data

Example body                     Body           {              {                  \"idContactType\": 1, { 1 = Telephone, 2 = Cellphone}              }              \"gender\": \"string\", { \"M\" = Male, \"F\" = Female, \"P\" = Other }              \"idState\": 0 {1 = AC, 2 = AL, 3 = AP, 4 = AM, 5 = BA, 6 = CE, 7 = DF, 8 = ES, 9 = GO, 10 = MA, 11 = MT, 12 = MS, 13 = MG, 14 = PA, 15 = PB, 16 = PR, 17 = PE, 18 = PI, 19 = RJ, 20 = RN, 21 = RS, 22 = RO, 23 = RR, 24 = SC, 25 = SP, 26 = SE, 27 = TO}            }

### Example
```python
from evo_client import MembersApi

# Configure HTTP basic authorization
api_instance = MembersApi()

try:
    # Update basic member data
    response = api_instance.update_member_data(
        id_member=56,
        body=MemberDataViewModel()
    )
    print(response)
except Exception as e:
    print(f"Exception when calling update_member_data: {e}")
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id_member** | **int** |  | 
**body** | [**MemberDataViewModel**](MemberDataViewModel.md) |  | [optional]

### Return type

**bool**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)



---

## MembershipApi

# evo_client.MembershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_categories**](MembershipApi.md#get_categories) | **GET** /api/v1/membership/category | Get Membership Categories
[**get_memberships**](MembershipApi.md#get_memberships) | **GET** /api/v1/membership | Get Memberships

# **get_categories**
> list[W12UtilsCategoryMembershipViewModel] get_categories()

Get Membership Categories

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
api_instance = evo_client.MembershipApi(evo_client.ApiClient(configuration))

try:
    # Get Membership Categories
    api_response = api_instance.get_categories()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipApi->get_categories: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[W12UtilsCategoryMembershipViewModel]**](W12UtilsCategoryMembershipViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_memberships**
> list[ContratosResumoApiViewModel] get_memberships(membership_id=membership_id, name=name, branch_id=branch_id, take=take, skip=skip, active=active)

Get Memberships

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
api_instance = evo_client.MembershipApi(evo_client.ApiClient(configuration))
membership_id = 56 # int | Filter by membership ID (optional)
name = 'name_example' # str |  (optional)
branch_id = 56 # int | Filter by branch ID (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25 # int | Total number of records to return. (Maximum of 50) (optional) (default to 25)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
active = True # bool | Filter by active/inactive memberships (optional)

try:
    # Get Memberships
    api_response = api_instance.get_memberships(membership_id=membership_id, name=name, branch_id=branch_id, take=take, skip=skip, active=active)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipApi->get_memberships: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **membership_id** | **int**| Filter by membership ID | [optional] 
 **name** | **str**|  | [optional] 
 **branch_id** | **int**| Filter by branch ID (Only available when using a multilocation key, ignored otherwise) | [optional] 
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 25]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **active** | **bool**| Filter by active/inactive memberships | [optional] 

### Return type

[**list[ContratosResumoApiViewModel]**](ContratosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
# End of Selection
```


---

## MetadadosEnotasRetorno

# MetadadosEnotasRetorno

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## NotificationsApi

# evo_client.NotificationsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_notification**](NotificationsApi.md#create_notification) | **POST** /api/v1/notifications | Insert a member notification

# **create_notification**
> create_notification(notification=notification)

Insert a member notification

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

# create an instance of the API class
api_instance = evo_client.NotificationsApi(evo_client.ApiClient(configuration))
notification = evo_client.NotificationApiViewModel() # NotificationApiViewModel |  (optional)

try:
    # Insert a member notification
    api_instance.create_notification(notification=notification)
except ApiException as e:
    print("Exception when calling NotificationsApi->create_notification: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification** | [**NotificationApiViewModel**](NotificationApiViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# End of Selection
```


---

## PartnershipApi

# evo_client.PartnershipApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

## Methods

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_partnerships**](PartnershipApi.md#get_partnerships) | **GET** /api/v1/partnership | Get partnerships

## **get_partnerships**
> list[ConveniosApiViewModel] get_partnerships(status=status, description=description, dt_created=dt_created)

Get partnerships

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
api_instance = evo_client.PartnershipApi(evo_client.ApiClient(configuration))
status = 56 # int | Filter by status: 0 Both, 1 Active, 2 Inactive (optional)
description = 'description_example' # str | Filter by Partnership name (optional)
dt_created = '2013-10-20T19:20:30+01:00' # datetime | Filter by registration date (optional)

try:
    # Get partnerships
    api_response = api_instance.get_partnerships(status=status, description=description, dt_created=dt_created)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PartnershipApi->get_partnerships: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **int**| Filter by status: 0 Both, 1 Active, 2 Inactive | [optional] 
 **description** | **str**| Filter by Partnership name | [optional] 
 **dt_created** | **datetime**| Filter by registration date | [optional] 

### Return type

[**list[ConveniosApiViewModel]**](ConveniosApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
# End of Selection
```


---

## PayablesApi

# evo_client.PayablesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_cost_centers**](PayablesApi.md#get_cost_centers) | **GET** /api/v1/costcenter | Get Cost Centers
[**get_payables**](PayablesApi.md#get_payables) | **GET** /api/v1/payables | Retrieve payables

# **get_cost_centers**
> CostCenterApiViewModel get_cost_centers(take: int = 50, skip: int = 0, async_req: bool = False)

Get Cost Centers with pagination.

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
api_instance = evo_client.PayablesApi(evo_client.ApiClient(configuration))
take = 50 # int | Total number of records to return. (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get Cost Centers
    api_response = api_instance.get_cost_centers(take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayablesApi->get_cost_centers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **take** | **int**| Total number of records to return. | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**CostCenterApiViewModel**](CostCenterApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_payables**
> PayablesApiViewModel get_payables(description: str = None, date_input_start: datetime = None, date_input_end: datetime = None, due_date_start: datetime = None, due_date_end: datetime = None, date_payment_start: datetime = None, date_payment_end: datetime = None, competence_start: datetime = None, competence_end: datetime = None, bank_account: str = None, amount_start: float = None, amount_end: float = None, account_status: str = None, take: int = 50, skip: int = 0, async_req: bool = False)

Retrieve payables with optional filtering.

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
api_instance = evo_client.PayablesApi(evo_client.ApiClient(configuration))
description = 'description_example' # str | Filter by account description (optional)
date_input_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by input of the account starting on a date (yyyy-mm-dd) (optional)
date_input_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by input of the account ending on a date (yyyy-mm-dd) (optional)
due_date_start = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account starting on a date (yyyy-mm-dd) (optional)
due_date_end = '2013-10-20T19:20:30+01:00' # datetime | Filter by due of the account ending on a date (yyyy-mm-dd) (optional)
date_payment_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
date_payment_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
competence_start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
competence_end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
bank_account = 'bank_account_example' # str | Filter by bank account id. The bank account id can be obtained from the BankAccounts API. Accounts can be concatenated with a comma to search, for example (2,215), in which case it will return payments from bank accounts 2 and 215. (optional)
amount_start = 1.2 # float | Filter by minimum amount (optional)
amount_end = 1.2 # float | Filter by maximum amount (optional)
account_status = 'account_status_example' # str | Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Paid, 3 - Canceled (optional)
take = 50 # int | Total number of records to return. (Maximum of 50) (optional) (default to 50)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Retrieve payables
    api_response = api_instance.get_payables(description=description, date_input_start=date_input_start, date_input_end=date_input_end, due_date_start=due_date_start, due_date_end=due_date_end, date_payment_start=date_payment_start, date_payment_end=date_payment_end, competence_start=competence_start, competence_end=competence_end, bank_account=bank_account, amount_start=amount_start, amount_end=amount_end, account_status=account_status, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayablesApi->get_payables: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **description** | **str**| Filter by account description | [optional]
 **date_input_start** | **datetime**| Filter by input of the account starting on a date (yyyy-mm-dd) | [optional]
 **date_input_end** | **datetime**| Filter by input of the account ending on a date (yyyy-mm-dd) | [optional]
 **due_date_start** | **datetime**| Filter by due of the account starting on a date (yyyy-mm-dd) | [optional]
 **due_date_end** | **datetime**| Filter by due of the account ending on a date (yyyy-mm-dd) | [optional]
 **date_payment_start** | **datetime**|  | [optional]
 **date_payment_end** | **datetime**|  | [optional]
 **competence_start** | **datetime**|  | [optional]
 **competence_end** | **datetime**|  | [optional]
 **bank_account** | **str**| Filter by bank account id. The bank account id can be obtained from the BankAccounts API. Accounts can be concatenated with a comma to search, for example (2,215), in which case it will return payments from bank accounts 2 and 215. | [optional]
 **amount_start** | **float**| Filter by minimum amount | [optional]
 **amount_end** | **float**| Filter by maximum amount | [optional]
 **account_status** | **str**| Filter by a comma separated list of status ids. Status: 1 - Opened, 2 - Paid, 3 - Canceled | [optional]
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 50]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**PayablesApiViewModel**](PayablesApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
# End of Selection
```


---

## PixApi

# evo_client.PixApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_qr_code**](PixApi.md#get_qr_code) | **GET** /api/v1/pix/qr-code | Get QR code

# **get_qr_code**
> PixPaymentDetailsViewModel get_qr_code(pix_receipt_id=pix_receipt_id)

Get QR code

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
api_instance = evo_client.PixApi(evo_client.ApiClient(configuration))
pix_receipt_id = 56 # int |  (optional)

try:
    # Get QR code
    api_response = api_instance.get_qr_code(pix_receipt_id=pix_receipt_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PixApi->get_qr_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pix_receipt_id** | **int**| PIX receipt ID | [optional] 

### Return type

[**PixPaymentDetailsViewModel**](PixPaymentDetailsViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# End of Selection
```


---

## ProspectsApi

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


---

## ReceivablesApi

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


---

## ReceivablesCreditDetails

# ReceivablesCreditDetails

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id_credit** | **int** |  | [optional] 
**id_cancelation_credit** | **int** |  | [optional] 
**id_branch_origin** | **int** |  | [optional] 
**ammount** | **float** |  | [optional] 
**branch_document** | **str** |  | [optional] 
**id_sale_origin** | **int** |  | [optional] 
**id_receivable_origin** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## SalesApi

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


---

## ServiceApi

# evo_client.ServiceApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_services**](ServiceApi.md#get_services) | **GET** /api/v1/service | Get Services

# **get_services**
> list[ServicosResumoApiViewModel] get_services(service_id=service_id, name=name, branch_id=branch_id, take=take, skip=skip, active=active)

Get Services

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
api_instance = evo_client.ServiceApi(evo_client.ApiClient(configuration))
service_id = 56  # int | Filter by Service Id (optional)
name = 'name_example'  # str |  (optional)
branch_id = 56  # int | Filter by service branch ID (Only available when using a multilocation key, ignored otherwise) (optional)
take = 25  # int | Total number of records to return. (Maximum of 50) (optional) (default to 25)
skip = 0  # int | Total number of records to skip. (optional) (default to 0)
active = True  # bool | Filter by active/inactive services (optional)

try:
    # Get Services
    api_response = api_instance.get_services(
        service_id=service_id,
        name=name,
        branch_id=branch_id,
        take=take,
        skip=skip,
        active=active
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceApi->get_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**service_id** | **int** | Filter by Service Id | [optional] 
**name** | **str** |  | [optional] 
**branch_id** | **int** | Filter by service branch ID (Only available when using a multilocation key, ignored otherwise) | [optional] 
**take** | **int** | Total number of records to return. (Maximum of 50) | [optional] [default to 25]
**skip** | **int** | Total number of records to skip. | [optional] [default to 0]
**active** | **bool** | Filter by active/inactive services | [optional] 

### Return type

[**list[ServicosResumoApiViewModel]**](ServicosResumoApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)




---

## ServicoEnotasRetorno

# ServicoEnotasRetorno

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**descricao** | **str** |  | [optional] 
**aliquota_iss** | **float** |  | [optional] 
**iss_retido_fonte** | **bool** |  | [optional] 
**codigo_servico_municipio** | **str** |  | [optional] 
**item_lista_servico_lc116** | **str** |  | [optional] 
**cnae** | **str** |  | [optional] 
**municipio_prestacao_servico** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## SpsRelProspectsCadastradosConvertidos

# SpsRelProspectsCadastradosConvertidos

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id_filial** | **int** |  | [optional] 
**nome_filial** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**id_prospect** | **int** |  | [optional] 
**nome** | **str** |  | [optional] 
**dt_cadastro** | **datetime** |  | [optional] 
**primeira_visita** | **str** |  | [optional] 
**convertido_por** | **str** |  | [optional] 
**dt_conversao** | **datetime** |  | [optional] 
**id_cliente** | **int** |  | [optional] 
**descricao** | **str** |  | [optional] 
**primeiro_contrato** | **str** |  | [optional] 
**apelido** | **str** |  | [optional] 
**marketing** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



---

## StatesApi

# evo_client.StatesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_states**](StatesApi.md#get_states) | **GET** /api/v1/states | Retrieve a list of available states/provinces

# **get_states**
> get_states(async_req=False)

### Description

Retrieve a list of available states or provinces.

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
api_instance = evo_client.StatesApi(evo_client.ApiClient(configuration))

try:
    # Retrieve list of states
    api_response = api_instance.get_states(async_req=False)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatesApi->get_states: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**async_req** | **bool** | Execute request asynchronously | [optional] [default to False]

### Return type

**list[State]** – A list of state objects containing details such as:
- State ID
- State name
- State abbreviation
- Country information

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


---

## VoucherApi

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


---

## WebhookApi

# evo_client.WebhookApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_webhook**](WebhookApi.md#delete_webhook) | **DELETE** /api/v1/webhook | Remove a specific webhook by ID
[**get_webhooks**](WebhookApi.md#get_webhooks) | **GET** /api/v1/webhook | List all webhooks created
[**create_webhook**](WebhookApi.md#create_webhook) | **POST** /api/v1/webhook | Add a new webhook

# **delete_webhook**
> delete_webhook(webhook_id)

Remove a specific webhook by ID

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
api_instance = evo_client.WebhookApi(evo_client.ApiClient(configuration))
webhook_id = 56 # int | Webhook ID (required)

try:
    # Remove a specific webhook by ID
    api_instance.delete_webhook(webhook_id=webhook_id)
except ApiException as e:
    print("Exception when calling WebhookApi->delete_webhook: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**webhook_id** | **int** | Webhook ID | [required] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_webhooks**
> get_webhooks()

List all webhooks created

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
api_instance = evo_client.WebhookApi(evo_client.ApiClient(configuration))

try:
    # List all webhooks created
    webhooks = api_instance.get_webhooks()
    pprint(webhooks)
except ApiException as e:
    print("Exception when calling WebhookApi->get_webhooks: %s\n" % e)
```

### Parameters
This endpoint does not require any parameters.

### Return type

List of [**W12UtilsWebhookViewModel**](W12UtilsWebhookViewModel.md) objects

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_webhook**
> create_webhook(body=body)

Add a new webhook

Create webhooks so EVO will notify outside systems every time a certain event occurs. Headers and filters are optional; filters are only available for webhooks of type 'NewSale' and won't be stored for other event types.

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
api_instance = evo_client.WebhookApi(evo_client.ApiClient(configuration))
body = evo_client.W12UtilsWebhookViewModel() # W12UtilsWebhookViewModel | (optional)

try:
    # Add a new webhook
    api_instance.create_webhook(body=body)
except ApiException as e:
    print("Exception when calling WebhookApi->create_webhook: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**body** | [**W12UtilsWebhookViewModel**](W12UtilsWebhookViewModel.md) | Webhook configuration details | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


---

## WorkoutApi

# evo_client.WorkoutApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**update_workout**](WorkoutApi.md#update_workout) | **PUT** /api/v2/workout | Update a client's prescribed workout details
[**get_client_workouts**](WorkoutApi.md#get_client_workouts) | **GET** /api/v2/workouts/client | Retrieve all workouts for a specific client, prospect, or employee
[**get_professor_workouts_by_date**](WorkoutApi.md#get_professor_workouts_by_date) | **GET** /api/v2/workouts/professor/date | Retrieve workouts by professor, month, and year with pagination
[**list_default_workouts**](WorkoutApi.md#list_default_workouts) | **GET** /api/v2/workouts/default | Retrieve all default workouts
[**link_workout_to_client**](WorkoutApi.md#link_workout_to_client) | **POST** /api/v2/workouts/link | Associate a workout with a client

# **update_workout**
> update_workout(workout_id, name=None, start_date=None, end_date=None, notes=None, categories=None, restrictions=None, professor_id=None, duration_weeks=None, weekly_frequency=None)

Update a client's prescribed workout details.

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
api_instance = evo_client.WorkoutApi(evo_client.ApiClient(configuration))
workout_id = 56 # int | The ID of the workout to update.
name = 'Advanced Workout Plan' # str | New name for the workout.
start_date = '2024-01-01T08:00:00Z' # datetime | New start date for the workout.
end_date = '2024-06-01T08:00:00Z' # datetime | New expiration date for the workout.
notes = 'Updated to include advanced exercises.' # str | Additional notes.
categories = 'Strength,Endurance' # str | Comma-separated categories.
restrictions = 'None' # str | Comma-separated restrictions.
professor_id = 78 # int | ID of the professor creating the workout.
duration_weeks = 12 # int | Total number of weeks.
weekly_frequency = 5 # int | Number of sessions per week.

try:
    # Update a client's prescribed workout
    api_instance.update_workout(workout_id=workout_id, name=name, start_date=start_date, end_date=end_date, notes=notes, categories=categories, restrictions=restrictions, professor_id=professor_id, duration_weeks=duration_weeks, weekly_frequency=weekly_frequency)
except ApiException as e:
    print("Exception when calling WorkoutApi->update_workout: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**workout_id** | **int**| The ID of the workout to update. | [required]
**name** | **str**| New name for the workout. | [optional]
**start_date** | **datetime**| New start date for the workout. | [optional]
**end_date** | **datetime**| New expiration date for the workout. | [optional]
**notes** | **str**| Additional notes. | [optional]
**categories** | **str**| Comma-separated categories. | [optional]
**restrictions** | **str**| Comma-separated restrictions. | [optional]
**professor_id** | **int**| ID of the professor creating the workout. | [optional]
**duration_weeks** | **int**| Total number of weeks. | [optional]
**weekly_frequency** | **int**| Number of sessions per week. | [optional]

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_client_workouts**
> get_client_workouts(client_id=None, prospect_id=None, employee_id=None, workout_id=None, is_active=False, is_deleted=False)

Retrieve all workouts for a specific client, prospect, or employee.

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
api_instance = evo_client.WorkoutApi(evo_client.ApiClient(configuration))
client_id = 123 # int | The ID of the client to retrieve workouts for.
prospect_id = None # int | The ID of the prospect to retrieve workouts for.
employee_id = None # int | The ID of the employee to retrieve workouts for.
workout_id = None # int | Specific workout ID to retrieve.
is_active = True # bool | Filter active workouts.
is_deleted = False # bool | Filter deleted workouts.

try:
    # Retrieve all workouts for a client, prospect, or employee
    api_response = api_instance.get_client_workouts(client_id=client_id, prospect_id=prospect_id, employee_id=employee_id, workout_id=workout_id, is_active=is_active, is_deleted=is_deleted)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkoutApi->get_client_workouts: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**client_id** | **int**| The ID of the client to retrieve workouts for. | [optional]
**prospect_id** | **int**| The ID of the prospect to retrieve workouts for. | [optional]
**employee_id** | **int**| The ID of the employee to retrieve workouts for. | [optional]
**workout_id** | **int**| Specific workout ID to retrieve. | [optional]
**is_active** | **bool**| Filter active workouts. | [optional] [default to False]
**is_deleted** | **bool**| Filter deleted workouts. | [optional] [default to False]

### Return type

List of **Workout** objects

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_professor_workouts_by_date**
> get_professor_workouts_by_date(professor_id, month=None, year=None, offset=0, limit=20)

Retrieve workouts by professor, month, and year with pagination.

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
api_instance = evo_client.WorkoutApi(evo_client.ApiClient(configuration))
professor_id = 45 # int | The ID of the professor.
month = 5 # int | The month to filter workouts by.
year = 2024 # int | The year to filter workouts by.
offset = 0 # int | Number of records to skip.
limit = 25 # int | Number of records to retrieve (max 50).

try:
    # Retrieve workouts by professor, month, and year with pagination
    api_response = api_instance.get_professor_workouts_by_date(professor_id=professor_id, month=month, year=year, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkoutApi->get_professor_workouts_by_date: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**professor_id** | **int**| The ID of the professor to filter workouts by. | [required]
**month** | **int**| The month to filter workouts by. | [optional]
**year** | **int**| The year to filter workouts by. | [optional]
**offset** | **int**| Number of records to skip for pagination. | [optional] [default to 0]
**limit** | **int**| Number of records to retrieve (maximum of 50). | [optional] [default to 20]

### Return type

List of **Workout** objects with pagination metadata

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_default_workouts**
> list_default_workouts(employee_id=None, tag_id=None)

Retrieve all default workouts.

   Meaning of response objects:
   - **workout_id**: The ID of the workout
   - **source_workout_id**: The ID of the workout to copy series from (if applicable)
   - **import_series_workout_id**: The ID of the workout to import series from (if applicable)
   - **client_id**: The ID of the client associated with the workout (if applicable)
   - **prospect_id**: The ID of the prospect associated with the workout (if applicable)
   - **employee_id**: The ID of the employee associated with the workout (if applicable)
   - **workout_name**: Name of the workout
   - **is_standard**: Standard workout information (if applicable)
   - **creation_date**: Date of creation
   - **start_date**: Start date
   - **validity_date**: Validity date
   - **notes**: Workout notes
   - **tags**: Tags associated with the workout
     - **tag_id**: The ID of the tag associated with the workout
     - **name**: Tag name
     - **branch_id**: ID of the branch (if applicable)
     - **branch**: Branch information (if applicable)
     - **additional_tags**: Additional tag information (if applicable)
   - **restrictions**: Restrictions (if applicable)
   - **series**: List of workout series
     - **series_id**: The ID of the series
     - **series_name**: Series name
     - **order**: Order of the series
     - **observations**: Series observations
     - **items**: List of items within the series
       - **item_id**: The ID of the item within the series
       - **exercise**: Exercise name
       - **code**: Exercise code
       - **repetitions**: Number of repetitions
       - **weight**: Load or weight
       - **interval**: Interval between sets
       - **position**: Position
       - **sets**: Number of sets
       - **item_notes**: Item observations
       - **order**: Order of the item
       - **exercise_id**: ID of the exercise (if applicable)
     - **completed_sessions**: Number of completed sessions for the series
   - **professor_name**: Name of the professor
   - **photo_url**: URL of the photo (if applicable)
   - **total_sessions**: Total number of sessions
   - **weekly_sessions**: Number of weekly sessions
   - **weekly_frequency**: Weekly frequency
   - **completed_sessions**: Number of completed sessions
   - **workout_status**: Workout status
   - **current_series_id**: ID of the current series (if applicable)
   - **can_print**: Whether printing is allowed
   - **is_from_evo_app**: Whether it originated from the Evo App

### Example Response
```json
{
    "workouts": [
        {
            "workout_id": 67704,
            "source_workout_id": 0,
            "import_series_workout_id": 0,
            "client_id": null,
            "prospect_id": null,
            "employee_id": null,
            "workout_name": "01 Musculação Padrão (+8 de exercícios)",
            "is_standard": null,
            "creation_date": null,
            "start_date": null,
            "validity_date": null,
            "notes": "Musculação Padrão com mais de 8 exercícios (teste impressão de treinos)",
            "tags": [
                {
                    "tag_id": 117,
                    "name": "Musculação",
                    "branch_id": 1,
                    "branch": null,
                    "additional_tags": null
                }
            ],
            "restrictions": null,
            "series": [
                {
                    "series_id": 148442,
                    "series_name": "Treino 0A",
                    "order": 1,
                    "observations": "Treino A",
                    "items": [
                        {
                            "item_id": 3340575,
                            "exercise": "FLEXÃO ABERTA (A)",
                            "code": "815",
                            "repetitions": "10",
                            "weight": "50",
                            "interval": "1",
                            "position": "2",
                            "sets": "3",
                            "item_notes": "ADM",
                            "order": 1,
                            "exercise_id": null
                        },
                        {
                            "item_id": 3340576,
                            "exercise": "REMADA FECHADA MÁQUINA",
                            "code": "555",
                            "repetitions": "10",
                            "weight": "50",
                            "interval": "1",
                            "position": "",
                            "sets": "3",
                            "item_notes": "",
                            "order": 2,
                            "exercise_id": null
                        }
                    ],
                    "completed_sessions": 0
                },
                {
                    "series_id": 148443,
                    "series_name": "Treino 0B",
                    "order": 2,
                    "observations": null,
                    "items": [
                        {
                            "item_id": 3340578,
                            "exercise": "LOMBAR NO GRAVITON (A)",
                            "code": "432",
                            "repetitions": "10",
                            "weight": "50",
                            "interval": "1",
                            "position": "",
                            "sets": "3",
                            "item_notes": "",
                            "order": 1,
                            "exercise_id": null
                        },
                        {
                            "item_id": 3340579,
                            "exercise": "ROSCA BARRA RETA",
                            "code": "307",
                            "repetitions": "10",
                            "weight": "50",
                            "interval": "1",
                            "position": "",
                            "sets": "3",
                            "item_notes": "",
                            "order": 2,
                            "exercise_id": null
                        }
                    ],
                    "completed_sessions": 0
                }
            ],
            "professor_name": "SUPORTEEVO",
            "photo_url": null,
            "total_sessions": null,
            "weekly_sessions": null,
            "weekly_frequency": null,
            "completed_sessions": 0,
            "workout_status": 0,
            "current_series_id": null,
            "can_print": false,
            "is_from_evo_app": false
        }
    ]
}
```

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
api_instance = evo_client.WorkoutApi(evo_client.ApiClient(configuration))
employee_id = 56 # int | The ID of the employee associated with the workouts. (optional)
tag_id = 56 # int | The optional ID of the tag associated with the workouts. (optional)

try:
    # Retrieve all default workouts
    api_response = api_instance.list_default_workouts(employee_id=employee_id, tag_id=tag_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkoutApi->list_default_workouts: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**employee_id** | **int**| The ID of the employee associated with the workouts. | [optional]
**tag_id** | **int**| The optional ID of the tag associated with the workouts. | [optional]

### Return type

List of **Workout** objects

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **link_workout_to_client**
> link_workout_to_client(source_workout_id, prescribing_employee_id=None, client_id=None, prospect_id=None, employee_id=None, prescription_date=None)

Associate a workout with a client.

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
api_instance = evo_client.WorkoutApi(evo_client.ApiClient(configuration))
source_workout_id = 56 # int | The ID of the source workout.
prescribing_employee_id = 78 # int | The ID of the employee responsible for the prescription.
client_id = 123 # int | The ID of the client to link the workout to.
prospect_id = None # int | The ID of the prospect to link the workout to.
employee_id = None # int | The ID of the employee to link the workout to.
prescription_date = datetime.strptime('2024-01-15', '%Y-%m-%d') # datetime | The date of the prescription.

try:
    # Associate a workout with a client
    api_response = api_instance.link_workout_to_client(
        source_workout_id=source_workout_id,
        prescribing_employee_id=prescribing_employee_id,
        client_id=client_id,
        prospect_id=prospect_id,
        employee_id=employee_id,
        prescription_date=prescription_date
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkoutApi->link_workout_to_client: %s\n" % e)
```

### Parameters

Name | Type | Description | Notes
------------- | ------------- | ------------- | -------------
**source_workout_id** | **int**| The ID of the source workout. | [required]
**prescribing_employee_id** | **int**| The ID of the employee responsible for the prescription. | [optional]
**client_id** | **int**| The ID of the client to link the workout to. | [optional]
**prospect_id** | **int**| The ID of the prospect to link the workout to. | [optional]
**employee_id** | **int**| The ID of the employee to link the workout to. | [optional]
**prescription_date** | **datetime**| The date of the prescription in YYYY-MM-DD format. | [optional]

### Return type

**bool**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


---
