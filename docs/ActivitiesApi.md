# evo_client.ActivitiesApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_activities_get**](ActivitiesApi.md#api_v1_activities_get) | **GET** /api/v1/activities | Get activities
[**api_v1_activities_schedule_detail_get**](ActivitiesApi.md#api_v1_activities_schedule_detail_get) | **GET** /api/v1/activities/schedule/detail | Get activities schedule details
[**api_v1_activities_schedule_enroll_post**](ActivitiesApi.md#api_v1_activities_schedule_enroll_post) | **POST** /api/v1/activities/schedule/enroll | Enroll member in activity schedule
[**api_v1_activities_schedule_get**](ActivitiesApi.md#api_v1_activities_schedule_get) | **GET** /api/v1/activities/schedule | Get activities schedule
[**class_post**](ActivitiesApi.md#class_post) | **POST** /api/v1/activities/schedule/experimental-class | Create a new experimental class and enroll the member on it
[**status_post**](ActivitiesApi.md#status_post) | **POST** /api/v1/activities/schedule/enroll/change-status | Change status of a member in activity schedule
[**unavailable_spots_get**](ActivitiesApi.md#unavailable_spots_get) | **GET** /api/v1/activities/list-unavailable-spots | List of spots that are already filled in the activity session

# **api_v1_activities_get**
> list[AtividadeListApiViewModel] api_v1_activities_get(search=search, id_branch=id_branch, take=take, skip=skip)

Get activities

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
search = '' # str | Filter by activity name, group name or tags (optional)
id_branch = 56 # int | Filber by membership IdBranch (Only available when using a multilocation key, ignored otherwise) (optional)
take = 10 # int | Total number of records to return. (optional) (default to 10)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get activities
    api_response = api_instance.api_v1_activities_get(search=search, id_branch=id_branch, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->api_v1_activities_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Filter by activity name, group name or tags | [optional] 
 **id_branch** | **int**| Filber by membership IdBranch (Only available when using a multilocation key, ignored otherwise) | [optional] 
 **take** | **int**| Total number of records to return. | [optional] [default to 10]
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]

### Return type

[**list[AtividadeListApiViewModel]**](AtividadeListApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_activities_schedule_detail_get**
> AtividadeBasicoApiViewModel api_v1_activities_schedule_detail_get(id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)

Get activities schedule details

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_configuration = 56 # int | Activity IdConfiguration (Must be use combined with activityDate) (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (Must be use combined with idConfiguration) (optional)
id_activity_session = 56 # int | Activity idActivitySession (This is mandatory if IdConfiguration and activityDate are null) (optional)

try:
    # Get activities schedule details
    api_response = api_instance.api_v1_activities_schedule_detail_get(id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->api_v1_activities_schedule_detail_get: %s\n" % e)
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

# **api_v1_activities_schedule_enroll_post**
> api_v1_activities_schedule_enroll_post(id_configuration=id_configuration, activity_date=activity_date, slot_number=slot_number, id_member=id_member, id_prospect=id_prospect, origin=origin)

Enroll member in activity schedule

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_configuration = 56 # int | Activity IdConfiguration (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (optional)
slot_number = 0 # int | Slot number (only available in activites that allow spot booking) (optional) (default to 0)
id_member = 0 # int | Id Member (this is required if IdProspect is null) (optional) (default to 0)
id_prospect = 0 # int | Id Member (this is required if IdMember is null) (optional) (default to 0)
origin = evo_client.EOrigemAgendamento() # EOrigemAgendamento |  (optional)

try:
    # Enroll member in activity schedule
    api_instance.api_v1_activities_schedule_enroll_post(id_configuration=id_configuration, activity_date=activity_date, slot_number=slot_number, id_member=id_member, id_prospect=id_prospect, origin=origin)
except ApiException as e:
    print("Exception when calling ActivitiesApi->api_v1_activities_schedule_enroll_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_configuration** | **int**| Activity IdConfiguration | [optional] 
 **activity_date** | **datetime**| Activity schedule date (yyyy-MM-dd) | [optional] 
 **slot_number** | **int**| Slot number (only available in activites that allow spot booking) | [optional] [default to 0]
 **id_member** | **int**| Id Member (this is required if IdProspect is null) | [optional] [default to 0]
 **id_prospect** | **int**| Id Member (this is required if IdMember is null) | [optional] [default to 0]
 **origin** | [**EOrigemAgendamento**](.md)|  | [optional] 

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

Get activities schedule

Status:        Livre = 0,      Disponivel = 1,      Lotada = 2,      ReservaEncerrada = 3,      Restrita = 4,      Cadastrado = 5,      Finalizada = 6,      Cancelada = 7,      NaFila = 8,      LivreEncerrada = 10,      RestritaEncerrada = 11,      RestritaNaoPermiteParticipar = 12,      LotadaSemFilaEspera = 15

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_member = 0 # int | Filter by a member (optional) (default to 0)
take = 56 # int | Limit the ammount of itens returned (optional)
only_availables = false # bool | Filter by activities that are available (optional) (default to false)
_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by a specific date (optional)
show_full_week = false # bool | Show all activities in the week (Sunday to Saturday) (optional) (default to false)
id_branch = 56 # int | Filter by a different branch than the current one (optional)
id_activities = 'id_activities_example' # str | Filter by a activities ids. Inform a comma separated list Ex.: \"1,2,3\" (optional)
id_audiences = 'id_audiences_example' # str | Filter by a audiences ids. Inform a comma separated list Ex.: \"1,2,3\" (optional)
id_branch_token = 'id_branch_token_example' # str | Filter by a different branch than the current one (optional)

try:
    # Get activities schedule
    api_response = api_instance.api_v1_activities_schedule_get(id_member=id_member, take=take, only_availables=only_availables, _date=_date, show_full_week=show_full_week, id_branch=id_branch, id_activities=id_activities, id_audiences=id_audiences, id_branch_token=id_branch_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->api_v1_activities_schedule_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_member** | **int**| Filter by a member | [optional] [default to 0]
 **take** | **int**| Limit the ammount of itens returned | [optional] 
 **only_availables** | **bool**| Filter by activities that are available | [optional] [default to false]
 **_date** | **datetime**| Filter by a specific date | [optional] 
 **show_full_week** | **bool**| Show all activities in the week (Sunday to Saturday) | [optional] [default to false]
 **id_branch** | **int**| Filter by a different branch than the current one | [optional] 
 **id_activities** | **str**| Filter by a activities ids. Inform a comma separated list Ex.: \&quot;1,2,3\&quot; | [optional] 
 **id_audiences** | **str**| Filter by a audiences ids. Inform a comma separated list Ex.: \&quot;1,2,3\&quot; | [optional] 
 **id_branch_token** | **str**| Filter by a different branch than the current one | [optional] 

### Return type

[**list[AtividadeAgendaApiViewModel]**](AtividadeAgendaApiViewModel.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **class_post**
> class_post(id_prospect=id_prospect, activity_date=activity_date, activity=activity, service=service, activity_exist=activity_exist, id_branch=id_branch)

Create a new experimental class and enroll the member on it

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_prospect = 56 # int | IdProspect of who will participate from class (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date and time (yyyy-MM-dd HH:mm) (optional)
activity = 'activity_example' # str | Activity name (optional)
service = 'service_example' # str | Service that will be sold to allow the trial class (optional)
activity_exist = false # bool |  (optional) (default to false)
id_branch = 56 # int |  (optional)

try:
    # Create a new experimental class and enroll the member on it
    api_instance.class_post(id_prospect=id_prospect, activity_date=activity_date, activity=activity, service=service, activity_exist=activity_exist, id_branch=id_branch)
except ApiException as e:
    print("Exception when calling ActivitiesApi->class_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_prospect** | **int**| IdProspect of who will participate from class | [optional] 
 **activity_date** | **datetime**| Activity schedule date and time (yyyy-MM-dd HH:mm) | [optional] 
 **activity** | **str**| Activity name | [optional] 
 **service** | **str**| Service that will be sold to allow the trial class | [optional] 
 **activity_exist** | **bool**|  | [optional] [default to false]
 **id_branch** | **int**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **status_post**
> status_post(status=status, id_member=id_member, id_prospect=id_prospect, id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)

Change status of a member in activity schedule

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
status = evo_client.EStatusAtividadeSessao() # EStatusAtividadeSessao | New status to be setted (Types: Attending = 0, Absent = 1, Justified absence = 2) (optional)
id_member = 56 # int | Id Member (optional)
id_prospect = 56 # int | Id Prospect (optional)
id_configuration = 56 # int | Activity IdConfiguration - only used when idActivitySession is null) (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) - only used when idActivitySession is null) (optional)
id_activity_session = 56 # int | IdActivity Session (optional)

try:
    # Change status of a member in activity schedule
    api_instance.status_post(status=status, id_member=id_member, id_prospect=id_prospect, id_configuration=id_configuration, activity_date=activity_date, id_activity_session=id_activity_session)
except ApiException as e:
    print("Exception when calling ActivitiesApi->status_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | [**EStatusAtividadeSessao**](.md)| New status to be setted (Types: Attending &#x3D; 0, Absent &#x3D; 1, Justified absence &#x3D; 2) | [optional] 
 **id_member** | **int**| Id Member | [optional] 
 **id_prospect** | **int**| Id Prospect | [optional] 
 **id_configuration** | **int**| Activity IdConfiguration - only used when idActivitySession is null) | [optional] 
 **activity_date** | **datetime**| Activity schedule date (yyyy-MM-dd) - only used when idActivitySession is null) | [optional] 
 **id_activity_session** | **int**| IdActivity Session | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unavailable_spots_get**
> unavailable_spots_get(id_configuration=id_configuration, _date=_date)

List of spots that are already filled in the activity session

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
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
id_configuration = 56 # int | Activity IdConfiguration (optional)
_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (optional)

try:
    # List of spots that are already filled in the activity session
    api_instance.unavailable_spots_get(id_configuration=id_configuration, _date=_date)
except ApiException as e:
    print("Exception when calling ActivitiesApi->unavailable_spots_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_configuration** | **int**| Activity IdConfiguration | [optional] 
 **_date** | **datetime**| Activity schedule date (yyyy-MM-dd) | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

