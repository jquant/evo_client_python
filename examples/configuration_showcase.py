#!/usr/bin/env python3
"""
🎊 EVO Client Configuration Helpers Showcase
============================================

This example demonstrates the powerful configuration helpers introduced in
Phase 4.2, making EVO Client setup effortless and error-free.

✅ Environment Variable Loading
✅ Factory Methods & Presets
✅ Configuration Validation
✅ Error Prevention & Helpful Messages
✅ Works with Both Sync & Async Clients

Usage:
    python examples/configuration_showcase.py
"""

import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

print("🎊 EVO Client Configuration Helpers Showcase")
print("=" * 55)
print()

# =============================================================================
# 🎯 EXAMPLE 1: Environment-Based Configuration (Recommended)
# =============================================================================

print("1️⃣ Environment-Based Configuration (Recommended)")
print("-" * 50)

from evo_client.config import ConfigBuilder, EnvConfigLoader

# Show current environment variables
current_env = EnvConfigLoader.check_env_vars()
if current_env:
    print("✅ Found environment variables:")
    for var, value in current_env.items():
        print(
            f"   {var} = {value[:20]}..." if len(value) > 20 else f"   {var} = {value}"
        )
else:
    print("ℹ️  No EVO_* environment variables found")

print("\n📄 Example .env file content:")
print("-" * 30)
example_env = EnvConfigLoader.get_example_env_file()
print(example_env[:300] + "..." if len(example_env) > 300 else example_env)

# Try to load from environment (will work if vars are set)
try:
    config = ConfigBuilder.from_env(required_vars=False)
    print("\n✅ Configuration loaded from environment!")
    print(f"   Host: {config.host}")
    print(f"   Username: {config.username}")
except Exception as e:
    print(f"\nℹ️  Environment config demo: {e}")

print()

# =============================================================================
# 🎯 EXAMPLE 2: Configuration Presets (Instant Setup)
# =============================================================================

print("2️⃣ Configuration Presets (Instant Setup)")
print("-" * 42)

from evo_client.config import ConfigPresets

# List all available presets
presets = ConfigPresets.list_presets()
print("📋 Available presets:")
for name, description in presets.items():
    print(f"   • {name}: {description}")

print("\n🚀 Creating preset configurations:")

# Development preset
dev_config = ConfigPresets.gym_development()
print(f"✅ Development: {dev_config.host} (SSL: {dev_config.verify_ssl})")

# Production preset
prod_config = ConfigPresets.gym_production()
print(f"✅ Production: {prod_config.host} (SSL: {dev_config.verify_ssl})")

# High performance preset
perf_config = ConfigPresets.high_performance()
print(
    f"✅ High Performance: Connection pool size = {perf_config.connection_pool_maxsize}"
)

# Low latency preset
latency_config = ConfigPresets.low_latency()
print(f"✅ Low Latency: Timeout = {latency_config.timeout}s")

print()

# =============================================================================
# 🎯 EXAMPLE 3: Factory Methods (Easy Creation)
# =============================================================================

print("3️⃣ Factory Methods (Easy Creation)")
print("-" * 35)

# Basic authentication
print("🔑 Basic Authentication:")
basic_config = ConfigBuilder.basic_auth(
    host="https://evo-integracao-api.w12app.com.br",
    username="demo_gym",
    password="demo_secret",
)
print(f"✅ Created: {basic_config.host} with basic auth")

# API key authentication
print("\n🗝️  API Key Authentication:")
api_config = ConfigBuilder.api_key_auth(
    host="https://evo-integracao-api.w12app.com.br", api_key="demo_api_key_12345"
)
print(f"✅ Created: {api_config.host} with API key auth")

# Development configuration
print("\n🛠️  Development Configuration:")
dev_config = ConfigBuilder.development()
print(f"✅ Created: {dev_config.host} (dev-friendly settings)")

# Production configuration
print("\n🏭 Production Configuration:")
prod_config = ConfigBuilder.production(
    host="https://api.evo.com", username="production_user", password="secure_password"
)
print(f"✅ Created: {prod_config.host} (production-optimized)")

print()

# =============================================================================
# 🎯 EXAMPLE 4: Configuration Validation (Error Prevention)
# =============================================================================

print("4️⃣ Configuration Validation (Error Prevention)")
print("-" * 48)

from evo_client.config import ConfigValidator

# Create a problematic configuration for demonstration
print("🔍 Testing configuration validation...")

# Good configuration
good_config = ConfigBuilder.basic_auth(
    host="https://evo-integracao-api.w12app.com.br",
    username="valid_gym_dns",
    password="secure_password_123",
)

is_valid, errors, warnings = ConfigValidator.validate_config(good_config)
print(f"\n✅ Good config validation: {'VALID' if is_valid else 'INVALID'}")
if warnings:
    print("⚠️  Warnings:")
    for warning in warnings[:2]:  # Show first 2 warnings
        print(f"   • {warning}")

# Problematic configuration
print("\n🚨 Testing with problematic config...")
bad_config = ConfigBuilder.basic_auth(
    host="http://api.evo.com",  # HTTP instead of HTTPS
    username="x",  # Too short
    password="123",  # Too short
)
bad_config.verify_ssl = False

is_valid, errors, warnings = ConfigValidator.validate_config(bad_config)
print(f"❌ Bad config validation: {'VALID' if is_valid else 'INVALID'}")
if errors:
    print("❌ Errors:")
    for error in errors[:2]:  # Show first 2 errors
        print(f"   • {error}")
if warnings:
    print("⚠️  Warnings:")
    for warning in warnings[:2]:  # Show first 2 warnings
        print(f"   • {warning}")

print()

# =============================================================================
# 🎯 EXAMPLE 5: Validation Reports (Human-Readable)
# =============================================================================

print("5️⃣ Validation Reports (Human-Readable)")
print("-" * 40)

print("📋 Generating validation report...")
report = ConfigValidator.get_validation_report(good_config)
print("\n" + report[:400] + "..." if len(report) > 400 else report)

print()

# =============================================================================
# 🎯 EXAMPLE 6: Sync/Async Specific Validation
# =============================================================================

print("6️⃣ Sync/Async Specific Validation")
print("-" * 36)

# Validate for sync usage
sync_valid, sync_issues = ConfigValidator.validate_for_sync(perf_config)
print(f"🔄 Sync validation: {'VALID' if sync_valid else 'INVALID'}")
if sync_issues:
    print("📝 Sync-specific notes:")
    for issue in sync_issues[:2]:
        print(f"   • {issue}")

# Validate for async usage
async_valid, async_issues = ConfigValidator.validate_for_async(latency_config)
print(f"\n⚡ Async validation: {'VALID' if async_valid else 'INVALID'}")
if async_issues:
    print("📝 Async-specific notes:")
    for issue in async_issues[:2]:
        print(f"   • {issue}")

print()

# =============================================================================
# 🎯 EXAMPLE 7: Integration with Clients
# =============================================================================

print("7️⃣ Integration with Sync & Async Clients")
print("-" * 42)

from evo_client import SyncApiClient, AsyncApiClient

# Using configuration with sync client
print("🔄 Using config with SyncApiClient:")
try:
    with SyncApiClient(good_config) as sync_client:
        print("✅ SyncApiClient created successfully")
        print(f"   Host: {sync_client.configuration.host}")
        print(f"   Username: {sync_client.configuration.username}")
except Exception as e:
    print(f"⚠️  Demo mode: {type(e).__name__}")

# Using configuration with async client
print("\n⚡ Using config with AsyncApiClient:")
import asyncio


async def demo_async_config():
    try:
        async with AsyncApiClient(good_config) as async_client:
            print("✅ AsyncApiClient created successfully")
            print(f"   Host: {async_client.configuration.host}")
            print(f"   Username: {async_client.configuration.username}")
    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")


try:
    asyncio.run(demo_async_config())
except Exception as e:
    print(f"⚠️  Demo mode: {type(e).__name__}")

print()

# =============================================================================
# 🎯 KEY BENEFITS SUMMARY
# =============================================================================

print("8️⃣ Key Benefits Summary")
print("-" * 25)

benefits = [
    "✅ One-line configuration: ConfigBuilder.from_env()",
    "✅ Environment variable automation with validation",
    "✅ 7 preset configurations for common scenarios",
    "✅ Factory methods for different auth types",
    "✅ Configuration validation with helpful error messages",
    "✅ Sync/async specific validation rules",
    "✅ Human-readable validation reports",
    "✅ Seamless integration with both client types",
    "✅ Error prevention catches issues early",
    "✅ Example .env file generation",
]

for benefit in benefits:
    print(f"  {benefit}")

print()
print("🎉 Configuration Helpers Showcase Complete!")
print("Phase 4.2 has revolutionized EVO Client configuration! 🚀")
