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
from evo_client.rest import ApiException
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
