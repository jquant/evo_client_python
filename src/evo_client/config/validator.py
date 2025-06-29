"""
Configuration Validator for EVO Client
======================================

Validates EVO Client configurations to catch issues early and provide
helpful feedback to users.
"""

from typing import List, Tuple
from urllib.parse import urlparse

from ..core.configuration import Configuration


class ConfigValidator:
    """Validates EVO Client configurations."""

    @classmethod
    def validate_config(
        cls, config: Configuration, strict: bool = False
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a configuration object.

        Args:
            config: Configuration to validate
            strict: Whether to apply strict validation rules

        Returns:
            Tuple of (is_valid, errors, warnings)

        Example:
            ```python
            config = ConfigBuilder.basic_auth("https://api.evo.com", "user", "pass")

            is_valid, errors, warnings = ConfigValidator.validate_config(config)

            if not is_valid:
                print("Configuration errors:")
                for error in errors:
                    print(f"  - {error}")

            if warnings:
                print("Configuration warnings:")
                for warning in warnings:
                    print(f"  - {warning}")
            ```
        """
        errors = []
        warnings = []

        # Validate host
        host_errors, host_warnings = cls._validate_host(config.host)
        errors.extend(host_errors)
        warnings.extend(host_warnings)

        # Validate authentication
        auth_errors, auth_warnings = cls._validate_authentication(config)
        errors.extend(auth_errors)
        warnings.extend(auth_warnings)

        # Validate timeouts
        timeout_errors, timeout_warnings = cls._validate_timeouts(config)
        errors.extend(timeout_errors)
        warnings.extend(timeout_warnings)

        # Validate SSL settings
        ssl_errors, ssl_warnings = cls._validate_ssl_settings(config)
        errors.extend(ssl_errors)
        warnings.extend(ssl_warnings)

        # Validate connection settings
        conn_errors, conn_warnings = cls._validate_connection_settings(config)
        errors.extend(conn_errors)
        warnings.extend(conn_warnings)

        # Strict mode additional checks
        if strict:
            strict_errors, strict_warnings = cls._validate_strict_mode(config)
            errors.extend(strict_errors)
            warnings.extend(strict_warnings)

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    @classmethod
    def _validate_host(cls, host: str) -> Tuple[List[str], List[str]]:
        """Validate host URL."""
        errors: List[str] = []
        warnings: List[str] = []

        if not host:
            errors.append("Host URL is required")
            return errors, warnings

        try:
            parsed = urlparse(host)

            if not parsed.scheme:
                errors.append("Host URL must include scheme (http:// or https://)")
            elif parsed.scheme not in ["http", "https"]:
                errors.append(
                    f"Unsupported scheme '{parsed.scheme}'. Use http or https"
                )

            if not parsed.netloc:
                errors.append("Host URL must include a valid domain")

            # Warnings for common issues
            if parsed.scheme == "http" and "localhost" not in parsed.netloc:
                warnings.append("Using HTTP instead of HTTPS for non-localhost host")

            if parsed.path and parsed.path != "/":
                warnings.append(
                    f"Host URL includes path '{parsed.path}'. Consider using base_path instead"
                )

        except Exception as e:
            errors.append(f"Invalid host URL format: {e}")

        return errors, warnings

    @classmethod
    def _validate_authentication(
        cls, config: Configuration
    ) -> Tuple[List[str], List[str]]:
        """Validate authentication settings."""
        errors = []
        warnings = []

        has_basic_auth = bool(config.username or config.password)
        has_api_key = bool(config.api_key)

        if not has_basic_auth and not has_api_key:
            errors.append(
                "No authentication configured. Set username/password or api_key"
            )

        # Basic auth validation
        if has_basic_auth:
            if not config.username:
                errors.append("Username is required when using basic authentication")
            if not config.password:
                errors.append("Password is required when using basic authentication")

            # Common username patterns for EVO
            if config.username and len(config.username) < 3:
                warnings.append(
                    "Username seems very short. EVO typically uses gym DNS names"
                )

        # API key validation
        if has_api_key:
            if "ApiKey" not in config.api_key:
                warnings.append(
                    "API key should typically be set with 'ApiKey' identifier"
                )

            for key_name, key_value in config.api_key.items():
                if not key_value or len(key_value) < 10:
                    warnings.append(f"API key '{key_name}' seems very short")

        return errors, warnings

    @classmethod
    def _validate_timeouts(cls, config: Configuration) -> Tuple[List[str], List[str]]:
        """Validate timeout settings."""
        errors = []
        warnings = []

        if config.timeout <= 0:
            errors.append("Timeout must be positive")
        elif config.timeout < 5:
            warnings.append(
                "Very short timeout (<5s) may cause issues with slower networks"
            )
        elif config.timeout > 300:
            warnings.append("Very long timeout (>5min) may cause application to hang")

        return errors, warnings

    @classmethod
    def _validate_ssl_settings(
        cls, config: Configuration
    ) -> Tuple[List[str], List[str]]:
        """Validate SSL/TLS settings."""
        errors = []
        warnings = []

        # Check SSL verification for HTTPS hosts
        if config.host and config.host.startswith("https://"):
            if not config.verify_ssl:
                warnings.append(
                    "SSL verification disabled for HTTPS host - security risk"
                )

        # Validate cert/key file pairing
        cert_file_set = config.cert_file is not None
        key_file_set = config.key_file is not None

        if cert_file_set != key_file_set:
            errors.append("cert_file and key_file must both be set or both be None")

        return errors, warnings

    @classmethod
    def _validate_connection_settings(
        cls, config: Configuration
    ) -> Tuple[List[str], List[str]]:
        """Validate connection pool and proxy settings."""
        errors = []
        warnings = []

        # Connection pool size
        if config.connection_pool_maxsize <= 0:
            errors.append("Connection pool max size must be positive")
        elif config.connection_pool_maxsize > 100:
            warnings.append(
                "Very large connection pool (>100) may consume excessive resources"
            )

        # Proxy validation
        if config.proxy:
            try:
                parsed_proxy = urlparse(config.proxy)
                if not parsed_proxy.scheme:
                    errors.append("Proxy URL must include scheme (http:// or https://)")
                if not parsed_proxy.netloc:
                    errors.append("Proxy URL must include a valid host:port")
            except Exception as e:
                errors.append(f"Invalid proxy URL: {e}")

        return errors, warnings

    @classmethod
    def _validate_strict_mode(
        cls, config: Configuration
    ) -> Tuple[List[str], List[str]]:
        """Additional validation for strict mode."""
        errors = []
        warnings = []

        # Production-ready checks
        if config.host and config.host.startswith("https://"):
            if not config.verify_ssl:
                errors.append("SSL verification must be enabled in production")

        # Strong authentication requirements
        if config.username and len(config.username) < 5:
            warnings.append("Username should be at least 5 characters for production")

        if config.password and len(config.password) < 8:
            warnings.append("Password should be at least 8 characters for production")

        return errors, warnings

    @classmethod
    def validate_for_sync(cls, config: Configuration) -> Tuple[bool, List[str]]:
        """
        Validate configuration specifically for sync client usage.

        Args:
            config: Configuration to validate

        Returns:
            Tuple of (is_valid, issues)

        Example:
            ```python
            config = ConfigBuilder.basic_auth("https://api.evo.com", "user", "pass")

            is_valid, issues = ConfigValidator.validate_for_sync(config)
            if is_valid:
                with SyncApiClient(config) as client:
                    # Safe to use
                    pass
            ```
        """
        is_valid, errors, warnings = cls.validate_config(config)

        # Sync-specific checks
        sync_issues = []
        if config.connection_pool_maxsize > 50:
            sync_issues.append(
                "Large connection pools less beneficial for sync clients"
            )

        all_issues = errors + warnings + sync_issues
        return is_valid, all_issues

    @classmethod
    def validate_for_async(cls, config: Configuration) -> Tuple[bool, List[str]]:
        """
        Validate configuration specifically for async client usage.

        Args:
            config: Configuration to validate

        Returns:
            Tuple of (is_valid, issues)

        Example:
            ```python
            config = ConfigBuilder.high_performance()
            config.username = "user"
            config.password = "pass"

            is_valid, issues = ConfigValidator.validate_for_async(config)
            if is_valid:
                async with AsyncApiClient(config) as client:
                    # Safe to use
                    pass
            ```
        """
        is_valid, errors, warnings = cls.validate_config(config)

        # Async-specific checks
        async_issues = []
        if config.connection_pool_maxsize < 5:
            async_issues.append(
                "Small connection pools may limit async concurrency benefits"
            )

        if config.timeout < 30:
            async_issues.append("Short timeouts may interrupt async operations")

        all_issues = errors + warnings + async_issues
        return is_valid, all_issues

    @classmethod
    def get_validation_report(cls, config: Configuration) -> str:
        """
        Generate a comprehensive validation report.

        Args:
            config: Configuration to validate

        Returns:
            Human-readable validation report

        Example:
            ```python
            config = ConfigBuilder.basic_auth("https://api.evo.com", "user", "pass")
            report = ConfigValidator.get_validation_report(config)
            print(report)
            ```
        """
        is_valid, errors, warnings = cls.validate_config(config)

        report_lines = [
            "🔍 EVO Client Configuration Validation Report",
            "=" * 50,
            "",
            f"📋 Overall Status: {'✅ VALID' if is_valid else '❌ INVALID'}",
            "",
        ]

        if errors:
            report_lines.extend(
                [
                    "❌ Errors (must fix):",
                    *[f"  • {error}" for error in errors],
                    "",
                ]
            )

        if warnings:
            report_lines.extend(
                [
                    "⚠️  Warnings (recommended fixes):",
                    *[f"  • {warning}" for warning in warnings],
                    "",
                ]
            )

        if not errors and not warnings:
            report_lines.extend(
                [
                    "🎉 Configuration looks great!",
                    "✅ No issues found",
                    "",
                ]
            )

        # Add configuration summary
        report_lines.extend(
            [
                "📊 Configuration Summary:",
                f"  Host: {config.host}",
                f"  Timeout: {config.timeout}s",
                f"  SSL Verification: {'✅' if config.verify_ssl else '❌'}",
                f"  Connection Pool: {config.connection_pool_maxsize}",
                f"  Authentication: {'Basic Auth' if config.username else 'API Key' if config.api_key else 'None'}",
            ]
        )

        return "\n".join(report_lines)
