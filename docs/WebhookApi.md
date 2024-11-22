# evo_client.WebhookApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_webhook_delete**](WebhookApi.md#api_v1_webhook_delete) | **DELETE** /api/v1/webhook | Remove a specific webhook by id
[**api_v1_webhook_get**](WebhookApi.md#api_v1_webhook_get) | **GET** /api/v1/webhook | List all webhooks created
[**api_v1_webhook_post**](WebhookApi.md#api_v1_webhook_post) | **POST** /api/v1/webhook | Add new webhook

# **api_v1_webhook_delete**
> api_v1_webhook_delete(id_webhook=id_webhook)

Remove a specific webhook by id

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
api_instance = evo_client.WebhookApi(evo_client.ApiClient(configuration))
id_webhook = 56 # int | Webhook id (optional)

try:
    # Remove a specific webhook by id
    api_instance.api_v1_webhook_delete(id_webhook=id_webhook)
except ApiException as e:
    print("Exception when calling WebhookApi->api_v1_webhook_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_webhook** | **int**| Webhook id | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_webhook_get**
> api_v1_webhook_get()

List all webhooks created

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
api_instance = evo_client.WebhookApi(evo_client.ApiClient(configuration))

try:
    # List all webhooks created
    api_instance.api_v1_webhook_get()
except ApiException as e:
    print("Exception when calling WebhookApi->api_v1_webhook_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_webhook_post**
> api_v1_webhook_post(body=body)

Add new webhook

Create webhooks so EVO will notify outside systems every time a certain event happens:  headers is optional*  filters are optional, filters are only available for webhooks of type 'NewSale' and won't be stored for other event types      POST      {         \"IdBranch\": \"Branch number that webhook will be registered (Only available when using a multilocation key, ignored otherwise)\"         \"eventType\": \"Type: String. Specifies the type of event that will trigger this webhook. Available Types: 'NewSale', 'CreateMember', 'AlterMember', 'EndedSessionActivity', 'ClearedDebt', 'AlterReceivables', 'Freeze', 'RecurrentSale', 'entries', 'ActivityEnroll', 'SalesItensUpdated', 'CreateMembership',  'AlterMembership', 'CreateService', 'AlterService', 'CreateProduct', 'AlterProduct'\",         \"urlCallback\": \"Type: String. Url that will be called after the event. The API that will receive the request must accept the type POST and the content in the following format\",         \"headers\": [              {\"name\": \"Type: string\", \"value\": \"Type string\"}          ],          \"filters\": [              {                  \"FilterType\": \"Type: string. Specifies the filter that will be executed. Available Types: 'SaleItemDescription',                  \"Value\": \"Type: string. String that will be used to filter\"              }          ]      }                    POST       {         \"IdW12\": \"Type: Int. Unique gym ID\",         \"IdBranch\": \"Type: Int. Branch number\",         \"IdRecord\": \"Type: Int. Generate resource primary key\",         \"EventType\": \"Type: String. Webhook event type. Ex: 'NewSale'\"      }

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
api_instance = evo_client.WebhookApi(evo_client.ApiClient(configuration))
body = evo_client.W12UtilsWebhookViewModel() # W12UtilsWebhookViewModel |  (optional)

try:
    # Add new webhook
    api_instance.api_v1_webhook_post(body=body)
except ApiException as e:
    print("Exception when calling WebhookApi->api_v1_webhook_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**W12UtilsWebhookViewModel**](W12UtilsWebhookViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

