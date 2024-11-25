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

