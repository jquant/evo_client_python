import pytest
from pydantic import ValidationError

from evo_client.core.configuration import Configuration


@pytest.fixture
def default_configuration():
    """Create a default configuration instance."""
    return Configuration()


def test_default_configuration_initialization(default_configuration: Configuration):
    """Test initializing default configuration."""
    config = default_configuration
    assert config.host == "https://evo-integracao-api.w12app.com.br"
    assert config.timeout == 60.0
    assert config.verify_ssl is True


def test_get_api_key_with_prefix_with_credentials(default_configuration: Configuration):
    """Test getting API key with prefix."""
    default_configuration.api_key = {"ApiKey": "12345"}
    default_configuration.api_key_prefix = {"ApiKey": "Bearer"}
    api_key_with_prefix = default_configuration.get_api_key_with_prefix("ApiKey")
    assert api_key_with_prefix == "Bearer 12345"


def test_get_basic_auth_token_with_credentials(default_configuration: Configuration):
    """Test getting basic auth token."""
    default_configuration.username = "user"
    default_configuration.password = "pass"
    basic_auth = default_configuration.get_basic_auth_token()
    assert basic_auth is not None
    assert basic_auth.username == "user"
    assert basic_auth.password == "pass"


def test_get_api_key_with_prefix():
    """Test getting API key with prefix."""
    config = Configuration(
        api_key={"ApiKey": "12345"}, api_key_prefix={"ApiKey": "Bearer"}
    )
    assert config.get_api_key_with_prefix("ApiKey") == "Bearer 12345"


def test_get_basic_auth_token():
    """Test getting basic auth token."""
    config = Configuration(username="user", password="pass")
    basic_auth = config.get_basic_auth_token()
    assert basic_auth is not None
    assert basic_auth.username == "user"
    assert basic_auth.password == "pass"

    config = Configuration(username="", password="")
    assert config.get_basic_auth_token() is None


def test_refresh_api_key_hook():
    """Test refresh API key hook."""

    def refresh_api_key_hook(config):
        config.api_key = {"ApiKey": "12345"}

    config = Configuration(username="", password="")
    config.refresh_api_key_hook = refresh_api_key_hook
    assert config.get_api_key_with_prefix("ApiKey") == "12345"


def test_refresh_api_key_hook_error():
    """Test refresh API key hook error."""

    def refresh_api_key_hook(config):
        raise Exception("Error refreshing API key")

    config = Configuration(username="", password="")
    config.refresh_api_key_hook = refresh_api_key_hook
    key = config.get_api_key_with_prefix("ApiKey")
    assert key is None


def test_auth_settings(default_configuration):
    """Test getting authentication settings."""
    default_configuration.username = "user"
    default_configuration.password = "pass"
    default_configuration.api_key = {"ApiKey": "12345"}
    default_configuration.api_key_prefix = {"ApiKey": "Bearer"}
    auth_settings = default_configuration.auth_settings()

    assert "Basic" in auth_settings
    basic_auth = auth_settings["Basic"]["value"]
    assert basic_auth.username == "user"
    assert basic_auth.password == "pass"

    assert "ApiKey" in auth_settings
    assert auth_settings["ApiKey"]["value"] == "Bearer 12345"


def test_to_debug_report(default_configuration):
    """Test generating debug report."""
    debug_report = default_configuration.to_debug_report()
    assert "Python SDK Debug Report:" in debug_report
    assert "OS: " in debug_report
    assert "Python Version: " in debug_report
    assert "Version of the API: v1" in debug_report
    assert "SDK Package Version: 1.0.0" in debug_report


def test_validate_settings_invalid_host():
    """Test validation of invalid host URL."""
    with pytest.raises(ValidationError, match="Invalid host URL format"):
        Configuration(host="invalid-url")


def test_validate_settings_negative_timeout():
    """Test validation of negative timeout."""
    with pytest.raises(ValueError, match="Timeout must be positive"):
        Configuration(timeout=-1)


def test_validate_settings_cert_file_without_key_file():
    """Test validation of cert_file without key_file."""
    with pytest.raises(
        ValueError, match="key_file is required when cert_file is provided"
    ):
        Configuration(cert_file="path/to/cert.pem")


def test_validate_settings_key_file_without_cert_file():
    """Test validation of key_file without cert_file."""
    with pytest.raises(
        ValueError, match="cert_file is required when key_file is provided"
    ):
        Configuration(key_file="path/to/key.pem")


def test_validate_settings_files():
    """Test validation of cert_file and key_file."""
    config = Configuration(cert_file="path/to/cert.pem", key_file="path/to/key.pem")
    assert config.cert_file == "path/to/cert.pem"
    assert config.key_file == "path/to/key.pem"
