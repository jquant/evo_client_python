Configuration API
===============

The Configuration API enables you to manage system settings, preferences, and integration configurations for your gym management system.

Key Features
-----------

* Centralized configuration management
* Environment-specific settings
* Secure credential storage
* Dynamic configuration updates
* Configuration validation
* Version control and history
* Bulk configuration operations
* Configuration inheritance
* Override management

Models
------

.. module:: evo_client.models

.. autoclass:: SystemSettingsModel
   :members:
   :undoc-members:
   :show-inheritance:

   .. py:attribute:: business_hours
      :type: Dict[str, Dict[str, str]]

      Business hours configuration for each day of the week.
      Format: ``{"day": {"open": "HH:MM", "close": "HH:MM"}}``

   .. py:attribute:: timezone
      :type: str

      IANA timezone identifier (e.g., "America/New_York")

   .. py:attribute:: default_language
      :type: str

      ISO language code (e.g., "en-US")

.. autoclass:: NotificationSettingsModel
   :members:
   :undoc-members:
   :show-inheritance:

   .. py:attribute:: enabled
      :type: bool

      Master switch for notifications

   .. py:attribute:: providers
      :type: Dict[str, Dict[str, Any]]

      Configuration for notification providers (SMTP, SMS, etc.)

   .. py:attribute:: templates
      :type: Dict[str, Dict[str, str]]

      Notification templates configuration

.. autoclass:: IntegrationConfigModel
   :members:
   :undoc-members:
   :show-inheritance:

API Methods
----------

.. module:: evo_client.api

.. autoclass:: ConfigurationApi
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: update_system_settings
      :return: SystemSettingsModel
      :raises: ValueError, ApiException

   .. automethod:: update_notification_settings
      :return: None
      :raises: ApiException

   .. automethod:: update_integration_config
      :return: None
      :raises: ApiException

Usage Examples
-------------

System Settings Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.api import ConfigurationApi
    from evo_client.models import SystemSettingsModel
    from evo_client.exceptions import ApiException

    config_api = ConfigurationApi()

    try:
        # Get current system settings
        settings = config_api.get_system_settings()
        
        # Update business hours
        settings.business_hours = {
            "monday": {"open": "06:00", "close": "22:00"},
            "tuesday": {"open": "06:00", "close": "22:00"},
            # ... other days
        }
        settings.timezone = "America/New_York"
        settings.default_language = "en-US"
        
        # Update settings
        updated_settings = config_api.update_system_settings(settings)
        
    except ValueError as e:
        print(f"Invalid settings data: {e}")
    except ApiException as e:
        if e.status == 400:
            print("Invalid configuration format")
        elif e.status == 403:
            print("Insufficient permissions to modify settings")
        else:
            print(f"API error: {e.status} - {e.reason}")

Notification Configuration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from evo_client.models import NotificationSettingsModel

    try:
        # Configure email notifications
        email_settings = NotificationSettingsModel(
            enabled=True,
            providers={
                "smtp": {
                    "host": "smtp.example.com",
                    "port": 587,
                    "use_tls": True,
                    "username": "${SMTP_USERNAME}"  # Use environment variable
                }
            },
            templates={
                "welcome": {
                    "subject": "Welcome to Our Gym!",
                    "template_id": "welcome_template_01"
                }
            }
        )
        
        # Update notification settings
        config_api.update_notification_settings(email_settings)
        
    except ApiException as e:
        if e.status == 400:
            print("Invalid notification configuration")
        elif e.status == 401:
            print("Authentication failed")
        else:
            print(f"API error: {e.status} - {e.reason}")

Error Handling
------------

The Configuration API uses standard HTTP status codes:

- 400: Invalid configuration format or validation failed
- 401: Authentication failed
- 403: Insufficient permissions to modify settings
- 404: Configuration not found
- 409: Configuration conflict
- 500: Internal server error

All errors are wrapped in :class:`~evo_client.exceptions.ApiException` with detailed error messages.

Security Considerations
--------------------

1. **Sensitive Data**:
   - Never hardcode credentials in configuration
   - Use environment variables for sensitive values
   - Encrypt sensitive configuration values

2. **Access Control**:
   - Configuration changes require appropriate permissions
   - Audit logs track all configuration changes
   - Some settings may require additional verification

Best Practices
------------

1. **Secure Credential Storage**

Always use secure methods for storing sensitive configuration:

.. code-block:: python

    from evo_client.utils.security import encrypt_credentials
    
    def secure_integration_config():
        # Encrypt sensitive credentials
        encrypted_creds = encrypt_credentials({
            "api_key": "your_api_key",
            "client_secret": "your_client_secret"
        })
        
        # Store encrypted configuration
        config = IntegrationConfigModel(
            provider="payment_gateway",
            credentials=encrypted_creds
        )
        config_api.update_integration_config(config)

2. **Configuration Validation**

Always validate configurations before applying:

.. code-block:: python

    def validate_configuration(config: Dict[str, Any]) -> bool:
        try:
            # Validate configuration
            validation = config_api.validate_configuration(config)
            
            if not validation.is_valid:
                print("Validation errors:")
                for error in validation.errors:
                    print(f"- {error}")
                return False
                
            return True
            
        except ApiException as e:
            print(f"Validation error: {e}")
            return False

3. **Environment Management**

Manage configurations across different environments:

.. code-block:: python

    def manage_environment_config():
        # Load environment-specific configuration
        env = os.getenv("ENVIRONMENT", "development")
        config = config_api.get_environment_config(env)
        
        # Apply environment overrides
        config.update({
            "debug_mode": env == "development",
            "log_level": "DEBUG" if env == "development" else "INFO"
        })
        
        # Update environment configuration
        config_api.update_environment_config(env, config)
