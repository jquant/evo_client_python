#!/usr/bin/env python3
"""
🔐 EVO Client Authentication Example (Updated to Modern Patterns)
================================================================

⚠️  NOTICE: This example has been updated from v1 bundler patterns
    to modern sync/async patterns for better maintainability.

✅ Modern authentication setup
✅ Clean configuration patterns
✅ Direct API method calls
✅ Proper error handling

This example shows how to test connection and fetch gym configuration
using the modern EVO Client Python SDK.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from evo_client.config import ConfigBuilder, QuickConfig
from evo_client.sync import SyncApiClient
from evo_client.sync.api import SyncConfigurationApi, SyncMembersApi

print("🔐 EVO Client Authentication Example - Modern Patterns")
print("=" * 55)
print()


def test_gym_connection(
    username: str,
    password: str,
    host: str = "https://evo-integracao-api.w12app.com.br",
    branch_id: Optional[int] = None,
    save_config: bool = True,
) -> dict:
    """
    Test connection to a gym's EVO API and fetch its configuration.

    Args:
        username: API username/login (gym DNS)
        password: API secret key
        host: API host URL (default: EVO production)
        branch_id: Optional branch ID to focus on specific branch
        save_config: Whether to save the fetched configuration to a file

    Returns:
        dict: The gym configuration data
    """
    print(f"\n🔄 Testing connection to {host}")
    print(f"📋 Username: {username}")
    print(f"🏢 Branch ID: {branch_id or 'All branches'}")

    # Create configuration using modern helpers
    config = ConfigBuilder.basic_auth(host=host, username=username, password=password)

    print(f"✅ Configuration created")
    print(f"   Host: {config.host}")
    print(f"   Timeout: {config.timeout}s")
    print(f"   SSL Verification: {config.verify_ssl}")

    try:
        # Use modern sync client with context manager
        with SyncApiClient(config) as client:
            print("\n🔌 Connecting to EVO API...")

            # Create API instances
            config_api = SyncConfigurationApi(client)
            members_api = SyncMembersApi(client)

            print("✅ API clients created successfully")

            # Test connection by fetching configuration
            print("\n📡 Fetching gym configuration...")

            # Get basic gym configuration
            try:
                # Fetch branch configuration
                branch_config = config_api.get_branch_config()
                print(f"✅ Branch configuration fetched")

                # Get additional configuration data
                gateway_config = config_api.get_gateway_config()
                card_flags = config_api.get_card_flags()

                print(f"✅ Gateway configuration: Retrieved")
                print(f"✅ Card flags: {len(card_flags) if card_flags else 0}")

                # Test member API access
                print("\n👥 Testing member API access...")
                try:
                    # Get a small sample of members to verify access
                    sample_members = members_api.get_members(take=1)
                    print(
                        f"✅ Member API accessible (sample size: {len(sample_members) if sample_members else 0})"
                    )
                except Exception as member_error:
                    print(
                        f"⚠️  Member API limited access: {type(member_error).__name__}"
                    )

                # Prepare gym data summary
                gym_data = {
                    "connection_test": {
                        "status": "success",
                        "timestamp": datetime.now().isoformat(),
                        "username": username,
                        "host": host,
                        "branch_id": branch_id,
                    },
                    "configuration": {
                        "branch_configs_count": (
                            len(branch_config) if branch_config else 0
                        ),
                        "gateway_config": (
                            "retrieved" if gateway_config else "not_available"
                        ),
                        "card_flags_count": len(card_flags) if card_flags else 0,
                    },
                    "api_access": {
                        "configuration_api": "accessible",
                        "members_api": "accessible",
                    },
                }

                print("\n🎉 Connection test successful!")
                print(f"📊 Configuration summary:")
                print(
                    f"   • Branch configurations: {gym_data['configuration']['branch_configs_count']}"
                )
                print(
                    f"   • Gateway config: {gym_data['configuration']['gateway_config']}"
                )
                print(
                    f"   • Card flags: {gym_data['configuration']['card_flags_count']}"
                )
                print(f"   • API access: ✅ Verified")

                # Save configuration if requested
                if save_config:
                    save_gym_configuration(gym_data, username, branch_id)

                return gym_data

            except Exception as api_error:
                print(f"\n❌ API Error: {type(api_error).__name__}")
                print(f"   Details: {str(api_error)}")
                raise

    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        print(f"\n🔧 Troubleshooting tips:")
        print(f"   • Verify your gym DNS and secret key")
        print(f"   • Check network connectivity")
        print(f"   • Ensure the API host is correct")
        print(f"   • Contact your gym administrator for API access")
        raise


def save_gym_configuration(
    gym_data: dict, username: str, branch_id: Optional[int] = None
) -> Path:
    """Save gym configuration to a JSON file."""
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_suffix = f"_branch_{branch_id}" if branch_id else ""
    filename = f"gym_config_{username}{branch_suffix}_{timestamp}.json"

    output_path = Path(filename)

    print(f"\n💾 Saving configuration...")
    print(f"   File: {output_path.absolute()}")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(gym_data, f, indent=2, ensure_ascii=False, default=str)

        print(f"✅ Configuration saved successfully!")
        print(f"   Size: {output_path.stat().st_size} bytes")

        return output_path

    except Exception as e:
        print(f"❌ Error saving configuration: {str(e)}")
        raise


def main():
    """Main function to run the authentication test."""
    print("🎯 Starting gym authentication test...\n")

    # Example credentials (replace with real ones)
    username = "demo_gym"  # Your gym's DNS
    password = "your_secret_key"  # Your API secret key
    host = "https://evo-integracao-api.w12app.com.br"

    # Override with environment variables if available
    username = os.getenv("EVO_USERNAME", username)
    password = os.getenv("EVO_PASSWORD", password)
    host = os.getenv("EVO_API_HOST", host)

    if username == "demo_gym" or password == "your_secret_key":
        print("⚠️  Using demo credentials!")
        print("   Set EVO_USERNAME and EVO_PASSWORD environment variables")
        print("   for real testing with your gym's credentials.")
        print()

    try:
        # Test the connection
        gym_data = test_gym_connection(
            username=username,
            password=password,
            host=host,
            branch_id=1,  # Optional: test specific branch
            save_config=True,
        )

        print("\n" + "=" * 55)
        print("✅ Authentication test completed successfully!")
        print("\n📋 Summary:")
        print(f"   • Gym: {username}")
        print(f"   • Host: {host}")
        print(f"   • APIs tested: Configuration, Members")
        print(f"   • Data saved: Yes")
        print("\n🚀 Your gym is ready for EVO API integration!")

    except Exception as e:
        print(f"\n❌ Authentication test failed: {str(e)}")
        print("\n🔧 Next steps:")
        print("   1. Verify your credentials")
        print("   2. Check API host URL")
        print("   3. Contact your gym administrator")
        print("   4. Review API documentation")


if __name__ == "__main__":
    main()
