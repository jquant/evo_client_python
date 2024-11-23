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
from evo_client.rest import ApiException
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
from evo_client.rest import ApiException
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
from evo_client.rest import ApiException
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
