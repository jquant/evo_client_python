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
