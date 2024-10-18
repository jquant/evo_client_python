# swagger_client.WorkoutApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_workout_put**](WorkoutApi.md#api_v1_workout_put) | **PUT** /api/v1/workout | Change data from a client&#x27;s prescribed workout
[**client_workout_get**](WorkoutApi.md#client_workout_get) | **GET** /api/v1/workout/default-client-workout | Get All Client&#x27;s or Prospect&#x27;s or Employee&#x27;s workouts
[**monthyear_professor_get**](WorkoutApi.md#monthyear_professor_get) | **GET** /api/v1/workout/workout-monthyear-professor | Get All Client&#x27;s or Prospect&#x27;s or Employee&#x27;s workouts by Month, Year or idProfessor
[**workout_get**](WorkoutApi.md#workout_get) | **GET** /api/v1/workout/default-workout | Get All default Workouts
[**workout_to_client_post**](WorkoutApi.md#workout_to_client_post) | **POST** /api/v1/workout/link-workout-to-client | Link Workout for Client

# **api_v1_workout_put**
> api_v1_workout_put(id_workout=id_workout, workout_name=workout_name, start_date=start_date, expiration_date=expiration_date, observation=observation, categories=categories, restrictions=restrictions, id_professor=id_professor, total_weeks=total_weeks, weekly_frequency=weekly_frequency)

Change data from a client's prescribed workout

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.WorkoutApi(swagger_client.ApiClient(configuration))
id_workout = 56 # int | The workout's id to be changed. (optional)
workout_name = 'workout_name_example' # str | Add a name if you want to change the current name. To keep the current name, the field must be empty. (optional)
start_date = '2013-10-20T19:20:30+01:00' # datetime | The workout's start date. (optional)
expiration_date = '2013-10-20T19:20:30+01:00' # datetime | The workout's expiration date. (optional)
observation = 'observation_example' # str |  (optional)
categories = 'categories_example' # str | You can add more than one category by separating them with commas. When adding categories, any categories already added to the workout will be replaced by the categories you add. (optional)
restrictions = 'restrictions_example' # str | You can add more than one restriction by separating them with commas. When adding restriction, any restriction already added to the workout will be replaced by the restriction you add. (optional)
id_professor = 56 # int | The ID of the professor who create the workouts. (optional)
total_weeks = 56 # int | Total number of weeks the client will do the workout. (optional)
weekly_frequency = 56 # int | The client's weekly frequency. (optional)

try:
    # Change data from a client's prescribed workout
    api_instance.api_v1_workout_put(id_workout=id_workout, workout_name=workout_name, start_date=start_date, expiration_date=expiration_date, observation=observation, categories=categories, restrictions=restrictions, id_professor=id_professor, total_weeks=total_weeks, weekly_frequency=weekly_frequency)
except ApiException as e:
    print("Exception when calling WorkoutApi->api_v1_workout_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_workout** | **int**| The workout&#x27;s id to be changed. | [optional] 
 **workout_name** | **str**| Add a name if you want to change the current name. To keep the current name, the field must be empty. | [optional] 
 **start_date** | **datetime**| The workout&#x27;s start date. | [optional] 
 **expiration_date** | **datetime**| The workout&#x27;s expiration date. | [optional] 
 **observation** | **str**|  | [optional] 
 **categories** | **str**| You can add more than one category by separating them with commas. When adding categories, any categories already added to the workout will be replaced by the categories you add. | [optional] 
 **restrictions** | **str**| You can add more than one restriction by separating them with commas. When adding restriction, any restriction already added to the workout will be replaced by the restriction you add. | [optional] 
 **id_professor** | **int**| The ID of the professor who create the workouts. | [optional] 
 **total_weeks** | **int**| Total number of weeks the client will do the workout. | [optional] 
 **weekly_frequency** | **int**| The client&#x27;s weekly frequency. | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **client_workout_get**
> client_workout_get(id_client=id_client, id_prospect=id_prospect, id_employee=id_employee, id_workout=id_workout, inactive=inactive, deleted=deleted)

Get All Client's or Prospect's or Employee's workouts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.WorkoutApi(swagger_client.ApiClient(configuration))
id_client = 56 # int | The ID of the client to get the workouts. (optional)
id_prospect = 56 # int | The ID of the prospect to get the workouts. (optional)
id_employee = 56 # int | The ID of the employee to get the workouts. (optional)
id_workout = 56 # int | The ID to get the workout. (optional)
inactive = false # bool |  (optional) (default to false)
deleted = false # bool |  (optional) (default to false)

try:
    # Get All Client's or Prospect's or Employee's workouts
    api_instance.client_workout_get(id_client=id_client, id_prospect=id_prospect, id_employee=id_employee, id_workout=id_workout, inactive=inactive, deleted=deleted)
except ApiException as e:
    print("Exception when calling WorkoutApi->client_workout_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_client** | **int**| The ID of the client to get the workouts. | [optional] 
 **id_prospect** | **int**| The ID of the prospect to get the workouts. | [optional] 
 **id_employee** | **int**| The ID of the employee to get the workouts. | [optional] 
 **id_workout** | **int**| The ID to get the workout. | [optional] 
 **inactive** | **bool**|  | [optional] [default to false]
 **deleted** | **bool**|  | [optional] [default to false]

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **monthyear_professor_get**
> monthyear_professor_get(id_professor=id_professor, month=month, year=year, skip=skip, take=take)

Get All Client's or Prospect's or Employee's workouts by Month, Year or idProfessor

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.WorkoutApi(swagger_client.ApiClient(configuration))
id_professor = 56 # int | The ID of the professor who create the workouts. (optional)
month = 56 # int | Month to get the workouts. (optional)
year = 56 # int | Year to get the workouts. (optional)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)
take = 10 # int | Total number of records to return. (Maximum of 50) (optional) (default to 10)

try:
    # Get All Client's or Prospect's or Employee's workouts by Month, Year or idProfessor
    api_instance.monthyear_professor_get(id_professor=id_professor, month=month, year=year, skip=skip, take=take)
except ApiException as e:
    print("Exception when calling WorkoutApi->monthyear_professor_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_professor** | **int**| The ID of the professor who create the workouts. | [optional] 
 **month** | **int**| Month to get the workouts. | [optional] 
 **year** | **int**| Year to get the workouts. | [optional] 
 **skip** | **int**| Total number of records to skip. | [optional] [default to 0]
 **take** | **int**| Total number of records to return. (Maximum of 50) | [optional] [default to 10]

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workout_get**
> workout_get(id_employee=id_employee, id_tag=id_tag)

Get All default Workouts

 Meaning of response objects:   - **idTreino**: The ID of the workout   - **idTreinoCopiarSerie**: The ID of the workout to copy series from (if applicable)   - **idTreinoImportarSeries**: The ID of the workout to import series from (if applicable)   - **idCliente**: The ID of the client associated with the workout (if applicable)   - **idProspect**: The ID of the prospect associated with the workout (if applicable)   - **idFuncionario**: The ID of the employee associated with the workout (if applicable)   - **nomeTreino**: Name of the workout   - **treinoPadrao**: Standard workout information (if applicable)   - **dataCriacao**: Date of creation   - **dataInicio**: Start date   - **dataValidade**: Validity date   - **observacao**: Workout observation   - **tags**: Tags associated with the workout     - **idTagTreino**: The ID of the tag associated with the workout     - **nome**: Tag name     - **idFilial**: ID of the branch (if applicable)     - **filial**: Branch information (if applicable)     - **evoTreinoTags**: Additional tag information (if applicable)   - **restricoes**: Restrictions (if applicable)   - **series**: List of workout series     - **idSerie**: The ID of the series     - **nome**: Series name     - **ordem**: Order of the series     - **observacao**: Series observation     - **itens**: List of items within the series       - **idItemSerie**: The ID of the item within the series       - **exercicio**: Exercise name       - **codigo**: Exercise code       - **repeticao**: Repetitions       - **carga**: Load or weight       - **intervalo**: Interval       - **posicao**: Position       - **vezes**: Number of times       - **observacao**: Item observation       - **ordem**: Order of the item       - **idExercicio**: ID of the exercise (if applicable)     - **sessoesConcluidas**: Number of completed sessions for the series   - **nomeProfessor**: Name of the professor   - **urlFoto**: URL of the photo (if applicable)   - **quantidadeSessoes**: Total number of sessions   - **quantidadeSemanal**: Number of weekly sessions   - **frequenciaSemana**: Weekly frequency   - **sessoesConcluidas**: Number of completed sessions   - **statusTreino**: Workout status   - **idSerieAtual**: ID of the current series (if applicable)   - **permiteImprimir**: Whether printing is allowed   - **origemEvoApp**: Whether it originated from the Evo App          Example Response      ```json   {       [           {          \"idTreino\": 67704,          \"idTreinoCopiarSerie\": 0,          \"idTreinoImportarSeries\": 0,          \"idCliente\": null,          \"idProspect\": null,          \"idFuncionario\": null,          \"nomeTreino\": \"01 Musculação Padrão (+8 de exercícios)\",          \"treinoPadrao\": null,          \"dataCriacao\": null,          \"dataInicio\": null,          \"dataValidade\": null,          \"observacao\": \"Musculação Padrão com mais de 8 exercícios (teste impressão de treinos)\",          \"tags\": [              {                   \"idTagTreino\": 117,                   \"nome\": \"Musculação\",                   \"idFilial\": 1,                   \"filial\": null,                   \"evoTreinoTags\": null              }          ],          \"restricoes\": null,          \"series\": [              {                  \"idSerie\": 148442,                  \"nome\": \"Treino 0A\",                  \"ordem\": 1,                  \"observacao\": \"Treino A\",                  \"itens\": [                      {                          \"idItemSerie\": 3340575,                          \"exercicio\": \"FLEXÃO ABERTA (A)\",                          \"codigo\": \"815\",                          \"repeticao\": \"10\",                          \"carga\": \"50\",                          \"intervalo\": \"1\",                          \"posicao\": \"2\",                          \"vezes\": \"3\",                          \"observacao\": \"ADM\",                          \"ordem\": 1,                          \"idExercicio\": null                      },                      {           \"idItemSerie\": 3340576,                          \"exercicio\": \"REMADA FECHADA MÁQUINA\",                          \"codigo\": \"555\",                          \"repeticao\": \"10\",                          \"carga\": \"50\",                          \"intervalo\": \"1\",                          \"posicao\": \"\",                          \"vezes\": \"3\",                          \"observacao\": \"\",                          \"ordem\": 2,                          \"idExercicio\": null                      }                  ],                  \"sessoesConcluidas\": 0              },              {           \"idSerie\": 148443,                  \"nome\": \"Treino 0B\",                  \"ordem\": 2,                  \"observacao\": null,                  \"itens\": [                      {          \"idItemSerie\": 3340578,                          \"exercicio\": \"LOMBAR NO GRAVITON (A)\",                          \"codigo\": \"432\",                          \"repeticao\": \"10\",                          \"carga\": \"50\",                          \"intervalo\": \"1\",                          \"posicao\": \"\",                          \"vezes\": \"3\",                          \"observacao\": \"\",                          \"ordem\": 1,                          \"idExercicio\": null                      },                      {          \"idItemSerie\": 3340579,                          \"exercicio\": \"ROSCA BARRA RETA\",                          \"codigo\": \"307\",                          \"repeticao\": \"10\",                          \"carga\": \"50\",                          \"intervalo\": \"1\",                          \"posicao\": \"\",                          \"vezes\": \"3\",                          \"observacao\": \"\",                          \"ordem\": 2,                          \"idExercicio\": null                      }                  ],                  \"sessoesConcluidas\": 0              }          ],          \"nomeProfessor\": \"SUPORTEEVO\",          \"urlFoto\": null,          \"quantidadeSessoes\": null,          \"quantidadeSemanal\": null,          \"frequenciaSemana\": null,          \"sessoesConcluidas\": 0,          \"statusTreino\": 0,          \"idSerieAtual\": null,          \"permiteImprimir\": false,          \"origemEvoApp\": false      }  ]   }   ```

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.WorkoutApi(swagger_client.ApiClient(configuration))
id_employee = 56 # int | The ID of the employee associated with the workouts. (optional)
id_tag = 56 # int | The optional ID of the tag associated with the workouts. (optional)

try:
    # Get All default Workouts
    api_instance.workout_get(id_employee=id_employee, id_tag=id_tag)
except ApiException as e:
    print("Exception when calling WorkoutApi->workout_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_employee** | **int**| The ID of the employee associated with the workouts. | [optional] 
 **id_tag** | **int**| The optional ID of the tag associated with the workouts. | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workout_to_client_post**
> bool workout_to_client_post(source_workout_id=source_workout_id, id_prescription_employee=id_prescription_employee, id_client=id_client, id_prospect=id_prospect, id_employee=id_employee, prescription_date=prescription_date)

Link Workout for Client

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.WorkoutApi(swagger_client.ApiClient(configuration))
source_workout_id = 56 # int | The ID of the source workout. (optional)
id_prescription_employee = 56 # int | The ID of the employee responsible for the prescription. (optional)
id_client = 56 # int | The ID of the client to link the workout to. (optional)
id_prospect = 56 # int | The ID of the prospect to link the workout to. (optional)
id_employee = 56 # int | The ID of the employee to link the workout to. (optional)
prescription_date = '2013-10-20T19:20:30+01:00' # datetime | Represent a date associated with a prescription yyyy-MM-dd. (optional)

try:
    # Link Workout for Client
    api_response = api_instance.workout_to_client_post(source_workout_id=source_workout_id, id_prescription_employee=id_prescription_employee, id_client=id_client, id_prospect=id_prospect, id_employee=id_employee, prescription_date=prescription_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkoutApi->workout_to_client_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **source_workout_id** | **int**| The ID of the source workout. | [optional] 
 **id_prescription_employee** | **int**| The ID of the employee responsible for the prescription. | [optional] 
 **id_client** | **int**| The ID of the client to link the workout to. | [optional] 
 **id_prospect** | **int**| The ID of the prospect to link the workout to. | [optional] 
 **id_employee** | **int**| The ID of the employee to link the workout to. | [optional] 
 **prescription_date** | **datetime**| Represent a date associated with a prescription yyyy-MM-dd. | [optional] 

### Return type

**bool**

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

