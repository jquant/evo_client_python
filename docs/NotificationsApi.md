# evo_client.NotificationsApi

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_notifications_post**](NotificationsApi.md#api_v1_notifications_post) | **POST** /api/v1/notifications | Insert a member notification

# **api_v1_notifications_post**
> api_v1_notifications_post(body=body)

Insert a member notification

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
api_instance = evo_client.NotificationsApi(evo_client.ApiClient(configuration))
body = evo_client.NotificationApiViewModel() # NotificationApiViewModel |  (optional)

try:
    # Insert a member notification
    api_instance.api_v1_notifications_post(body=body)
except ApiException as e:
    print("Exception when calling NotificationsApi->api_v1_notifications_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NotificationApiViewModel**](NotificationApiViewModel.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

