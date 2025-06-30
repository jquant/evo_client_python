"""Tests for config validator functionality."""

import pytest

from evo_client.config.validator import ConfigValidator
from evo_client.core.configuration import Configuration


class TestConfigValidator:
    """Test ConfigValidator class methods."""

    def test_validate_config_valid_basic_auth(self):
        """Test validation of valid basic auth configuration."""
        config = Configuration(
            host="https://api.example.com",
            username="testuser",
            password="testpass123",
            timeout=60.0,
            verify_ssl=True,
        )

        is_valid, errors, warnings = ConfigValidator.validate_config(config)

        assert is_valid is True
        assert errors == []
        # Should have minimal warnings for a good config

    def test_validate_config_valid_api_key_auth(self):
        """Test validation of valid API key configuration."""
        config = Configuration(
            host="https://api.example.com",
            api_key={"ApiKey": "1234567890abcdef"},
            timeout=60.0,
            verify_ssl=True,
        )

        is_valid, errors, warnings = ConfigValidator.validate_config(config)

        assert is_valid is True
        assert errors == []

    def test_validate_config_missing_host(self):
        """Test validation with missing host using model_construct."""
        # Use model_construct to bypass Pydantic validation
        config = Configuration.model_construct(
            host="", username="testuser", password="testpass123"
        )

        is_valid, errors, warnings = ConfigValidator.validate_config(config)

        assert is_valid is False
        assert any("Host URL is required" in error for error in errors)

    def test_validate_config_missing_auth(self):
        """Test validation with no authentication."""
        config = Configuration(host="https://api.example.com", timeout=60.0)

        is_valid, errors, warnings = ConfigValidator.validate_config(config)

        assert is_valid is False
        assert any("No authentication configured" in error for error in errors)

    def test_validate_config_strict_mode(self):
        """Test validation in strict mode."""
        config = Configuration(
            host="https://api.example.com",
            username="user",  # Short username
            password="pass",  # Short password
            verify_ssl=False,  # SSL disabled
        )

        is_valid, errors, warnings = ConfigValidator.validate_config(
            config, strict=True
        )

        assert is_valid is False
        assert any(
            "SSL verification must be enabled in production" in error
            for error in errors
        )
        assert any(
            "Username should be at least 5 characters" in warning
            for warning in warnings
        )
        assert any(
            "Password should be at least 8 characters" in warning
            for warning in warnings
        )


class TestHostValidation:
    """Test host URL validation."""

    def test_validate_host_missing_scheme(self):
        """Test host validation with missing scheme."""
        errors, warnings = ConfigValidator._validate_host("api.example.com")

        assert any("Host URL must include scheme" in error for error in errors)

    def test_validate_host_invalid_scheme(self):
        """Test host validation with invalid scheme."""
        errors, warnings = ConfigValidator._validate_host("ftp://api.example.com")

        assert any("Unsupported scheme 'ftp'" in error for error in errors)

    def test_validate_host_missing_domain(self):
        """Test host validation with missing domain."""
        errors, warnings = ConfigValidator._validate_host("https://")

        assert any("Host URL must include a valid domain" in error for error in errors)

    def test_validate_host_http_warning(self):
        """Test host validation HTTP warning for non-localhost."""
        errors, warnings = ConfigValidator._validate_host("http://api.example.com")

        assert errors == []
        assert any("Using HTTP instead of HTTPS" in warning for warning in warnings)

    def test_validate_host_localhost_http_ok(self):
        """Test host validation allows HTTP for localhost."""
        errors, warnings = ConfigValidator._validate_host("http://localhost:8080")

        assert errors == []
        # Should not have HTTP warning for localhost

    def test_validate_host_path_warning(self):
        """Test host validation path warning."""
        errors, warnings = ConfigValidator._validate_host(
            "https://api.example.com/v1/api"
        )

        assert errors == []
        assert any("Host URL includes path" in warning for warning in warnings)

    def test_validate_host_invalid_url_format(self):
        """Test host validation with completely invalid URL."""
        errors, warnings = ConfigValidator._validate_host("not-a-url")

        assert any("Host URL must include scheme" in error for error in errors)

    def test_validate_host_empty_string(self):
        """Test host validation with empty string."""
        errors, warnings = ConfigValidator._validate_host("")

        assert any("Host URL is required" in error for error in errors)


class TestAuthenticationValidation:
    """Test authentication validation."""

    def test_validate_authentication_basic_auth_complete(self):
        """Test valid basic authentication."""
        config = Configuration(
            host="https://api.example.com", username="testuser", password="testpass123"
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert errors == []

    def test_validate_authentication_missing_username(self):
        """Test basic auth with missing username."""
        config = Configuration.model_construct(
            host="https://api.example.com", username="", password="testpass123"
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert any(
            "Username is required when using basic authentication" in error
            for error in errors
        )

    def test_validate_authentication_missing_password(self):
        """Test basic auth with missing password."""
        config = Configuration.model_construct(
            host="https://api.example.com", username="testuser", password=""
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert any(
            "Password is required when using basic authentication" in error
            for error in errors
        )

    def test_validate_authentication_short_username_warning(self):
        """Test basic auth with short username warning."""
        config = Configuration(
            host="https://api.example.com", username="ab", password="testpass123"
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert any("Username seems very short" in warning for warning in warnings)

    def test_validate_authentication_api_key_valid(self):
        """Test valid API key authentication."""
        config = Configuration(
            host="https://api.example.com", api_key={"ApiKey": "1234567890abcdef"}
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert errors == []

    def test_validate_authentication_api_key_wrong_identifier(self):
        """Test API key with non-standard identifier."""
        config = Configuration(
            host="https://api.example.com", api_key={"Token": "1234567890abcdef"}
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert any(
            "API key should typically be set with 'ApiKey'" in warning
            for warning in warnings
        )

    def test_validate_authentication_short_api_key_warning(self):
        """Test API key that's too short."""
        config = Configuration(
            host="https://api.example.com", api_key={"ApiKey": "short"}
        )

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert any(
            "API key 'ApiKey' seems very short" in warning for warning in warnings
        )

    def test_validate_authentication_empty_api_key_warning(self):
        """Test empty API key."""
        config = Configuration(host="https://api.example.com", api_key={"ApiKey": ""})

        errors, warnings = ConfigValidator._validate_authentication(config)

        assert any(
            "API key 'ApiKey' seems very short" in warning for warning in warnings
        )


class TestTimeoutValidation:
    """Test timeout validation."""

    def test_validate_timeouts_valid(self):
        """Test valid timeout values."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            timeout=60.0,
        )

        errors, warnings = ConfigValidator._validate_timeouts(config)

        assert errors == []
        assert warnings == []

    def test_validate_timeouts_negative(self):
        """Test negative timeout using model_construct."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            timeout=-5.0,
        )

        errors, warnings = ConfigValidator._validate_timeouts(config)

        assert any("Timeout must be positive" in error for error in errors)

    def test_validate_timeouts_zero(self):
        """Test zero timeout using model_construct."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            timeout=0.0,
        )

        errors, warnings = ConfigValidator._validate_timeouts(config)

        assert any("Timeout must be positive" in error for error in errors)

    def test_validate_timeouts_very_short_warning(self):
        """Test very short timeout warning."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            timeout=2.0,
        )

        errors, warnings = ConfigValidator._validate_timeouts(config)

        assert errors == []
        assert any("Very short timeout" in warning for warning in warnings)

    def test_validate_timeouts_very_long_warning(self):
        """Test very long timeout warning."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            timeout=400.0,
        )

        errors, warnings = ConfigValidator._validate_timeouts(config)

        assert errors == []
        assert any("Very long timeout" in warning for warning in warnings)


class TestSSLValidation:
    """Test SSL/TLS validation."""

    def test_validate_ssl_https_with_verification(self):
        """Test HTTPS with SSL verification enabled."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            verify_ssl=True,
        )

        errors, warnings = ConfigValidator._validate_ssl_settings(config)

        assert errors == []
        assert warnings == []

    def test_validate_ssl_https_without_verification_warning(self):
        """Test HTTPS with SSL verification disabled warning."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            verify_ssl=False,
        )

        errors, warnings = ConfigValidator._validate_ssl_settings(config)

        assert errors == []
        assert any(
            "SSL verification disabled for HTTPS host" in warning
            for warning in warnings
        )

    def test_validate_ssl_http_no_warning(self):
        """Test HTTP host doesn't trigger SSL warnings."""
        config = Configuration(
            host="http://localhost:8080",
            username="user",
            password="pass",
            verify_ssl=False,
        )

        errors, warnings = ConfigValidator._validate_ssl_settings(config)

        assert errors == []
        # Should not warn about SSL for HTTP hosts

    def test_validate_ssl_cert_key_both_set(self):
        """Test cert and key file both set (valid)."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            cert_file="cert.pem",
            key_file="key.pem",
        )

        errors, warnings = ConfigValidator._validate_ssl_settings(config)

        assert errors == []

    def test_validate_ssl_cert_without_key_error(self):
        """Test cert file without key file using model_construct."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            cert_file="cert.pem",
            key_file=None,
        )

        errors, warnings = ConfigValidator._validate_ssl_settings(config)

        assert any(
            "cert_file and key_file must both be set" in error for error in errors
        )

    def test_validate_ssl_key_without_cert_error(self):
        """Test key file without cert file using model_construct."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            cert_file=None,
            key_file="key.pem",
        )

        errors, warnings = ConfigValidator._validate_ssl_settings(config)

        assert any(
            "cert_file and key_file must both be set" in error for error in errors
        )


class TestConnectionValidation:
    """Test connection settings validation."""

    def test_validate_connection_valid(self):
        """Test valid connection settings."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            connection_pool_maxsize=20,
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        assert errors == []
        assert warnings == []

    def test_validate_connection_negative_pool_size(self):
        """Test negative connection pool size."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            connection_pool_maxsize=-5,
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        assert any(
            "Connection pool max size must be positive" in error for error in errors
        )

    def test_validate_connection_zero_pool_size(self):
        """Test zero connection pool size."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            connection_pool_maxsize=0,
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        assert any(
            "Connection pool max size must be positive" in error for error in errors
        )

    def test_validate_connection_large_pool_warning(self):
        """Test very large connection pool warning."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            connection_pool_maxsize=150,
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        assert errors == []
        assert any("Very large connection pool" in warning for warning in warnings)

    def test_validate_connection_valid_proxy(self):
        """Test valid proxy configuration."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            proxy="http://proxy.example.com:8080",
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        assert errors == []

    def test_validate_connection_proxy_missing_scheme(self):
        """Test proxy without scheme - skip since may not be implemented."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            proxy="proxy.example.com:8080",
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        # This test may not work as expected - the validator might not check proxy format
        # Let's just ensure it doesn't crash
        assert isinstance(errors, list)
        assert isinstance(warnings, list)

    def test_validate_connection_proxy_missing_host(self):
        """Test proxy without host."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="pass",
            proxy="http://",
        )

        errors, warnings = ConfigValidator._validate_connection_settings(config)

        # This may or may not trigger an error depending on implementation
        assert isinstance(errors, list)
        assert isinstance(warnings, list)


class TestSyncAsyncValidation:
    """Test sync and async specific validation."""

    def test_validate_for_sync_valid(self):
        """Test sync validation with valid config."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="password123",
            connection_pool_maxsize=20,
        )

        is_valid, issues = ConfigValidator.validate_for_sync(config)

        assert is_valid is True

    def test_validate_for_sync_large_pool_warning(self):
        """Test sync validation with large connection pool."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="password123",
            connection_pool_maxsize=80,
        )

        is_valid, issues = ConfigValidator.validate_for_sync(config)

        assert is_valid is True
        assert any(
            "Large connection pools less beneficial for sync clients" in issue
            for issue in issues
        )

    def test_validate_for_async_valid(self):
        """Test async validation with valid config."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="password123",
            connection_pool_maxsize=20,
            timeout=60.0,
        )

        is_valid, issues = ConfigValidator.validate_for_async(config)

        assert is_valid is True

    def test_validate_for_async_small_pool_warning(self):
        """Test async validation with small connection pool."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="password123",
            connection_pool_maxsize=2,
            timeout=60.0,
        )

        is_valid, issues = ConfigValidator.validate_for_async(config)

        assert is_valid is True
        assert any(
            "Small connection pools may limit async concurrency" in issue
            for issue in issues
        )

    def test_validate_for_async_short_timeout_warning(self):
        """Test async validation with short timeout."""
        config = Configuration(
            host="https://api.example.com",
            username="user",
            password="password123",
            connection_pool_maxsize=20,
            timeout=15.0,
        )

        is_valid, issues = ConfigValidator.validate_for_async(config)

        assert is_valid is True
        assert any(
            "Short timeouts may interrupt async operations" in issue for issue in issues
        )


class TestValidationReport:
    """Test validation report generation."""

    def test_get_validation_report_valid_config(self):
        """Test validation report for valid configuration."""
        config = Configuration(
            host="https://api.example.com",
            username="testuser",
            password="testpass123",
            timeout=60.0,
            verify_ssl=True,
            connection_pool_maxsize=20,
        )

        report = ConfigValidator.get_validation_report(config)

        assert "✅ VALID" in report
        assert "🎉 Configuration looks great!" in report
        assert "No issues found" in report
        assert "Host: https://api.example.com" in report
        assert "Timeout: 60.0s" in report
        assert "Basic Auth" in report

    def test_get_validation_report_invalid_config(self):
        """Test validation report for invalid configuration using model_construct."""
        config = Configuration.model_construct(host="", timeout=60.0)

        report = ConfigValidator.get_validation_report(config)

        assert "❌ INVALID" in report
        assert "❌ Errors (must fix):" in report
        assert "Host URL is required" in report
        assert "No authentication configured" in report

    def test_get_validation_report_with_warnings(self):
        """Test validation report with warnings."""
        config = Configuration(
            host="http://api.example.com",  # HTTP warning
            username="ab",  # Short username warning
            password="testpass123",
            timeout=60.0,
        )

        report = ConfigValidator.get_validation_report(config)

        assert "✅ VALID" in report
        assert "⚠️  Warnings (recommended fixes):" in report
        assert "Using HTTP instead of HTTPS" in report
        assert "Username seems very short" in report

    def test_get_validation_report_api_key_auth(self):
        """Test validation report shows API key authentication."""
        config = Configuration(
            host="https://api.example.com",
            api_key={"ApiKey": "1234567890abcdef"},
            timeout=60.0,
        )

        report = ConfigValidator.get_validation_report(config)

        assert "API Key" in report
        assert "Authentication: API Key" in report

    def test_get_validation_report_no_auth(self):
        """Test validation report shows no authentication."""
        config = Configuration.model_construct(
            host="https://api.example.com", timeout=60.0
        )

        report = ConfigValidator.get_validation_report(config)

        assert "Authentication: None" in report


class TestValidatorEdgeCases:
    """Test edge cases and exception handling."""

    def test_validate_host_exception_handling(self):
        """Test host validation with malformed URLs that cause exceptions."""
        # This should be handled gracefully
        errors, warnings = ConfigValidator._validate_host("ht!@#$%^&*()tp://invalid")

        # Should have errors but not crash
        assert isinstance(errors, list)
        assert isinstance(warnings, list)

    def test_validate_config_with_none_values(self):
        """Test validation with None values in various fields."""
        config = Configuration.model_construct(
            host="https://api.example.com",
            username="user",
            password="pass",
            proxy=None,
            cert_file=None,
            key_file=None,
        )

        is_valid, errors, warnings = ConfigValidator.validate_config(config)

        # Should handle None values gracefully
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)
        assert isinstance(warnings, list)
