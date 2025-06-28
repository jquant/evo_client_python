"""
🎊 EVO Client Configuration Helpers
==================================

This module provides easy-to-use configuration helpers for both sync and async
EVO Client implementations.

✅ **Environment Variable Loading**: Automatic config from environment
✅ **Factory Methods**: Pre-configured setups for common use cases
✅ **Shared Configuration**: Works seamlessly with both sync and async clients
✅ **Validation**: Built-in validation and error handling

Usage Examples:
    ```python
    # Easy environment-based configuration
    from evo_client.config import ConfigBuilder

    config = ConfigBuilder.from_env()

    # Use with sync client
    from evo_client.sync import SyncApiClient
    with SyncApiClient(config) as client:
        # Ready to use!
        pass

    # Use with async client
    from evo_client.aio import AsyncApiClient
    async with AsyncApiClient(config) as client:
        # Ready to use!
        pass
    ```
"""

from .builder import ConfigBuilder, QuickConfig
from .env_loader import EnvConfigLoader
from .presets import ConfigPresets
from .validator import ConfigValidator

__all__ = [
    "ConfigBuilder",
    "QuickConfig",
    "EnvConfigLoader",
    "ConfigPresets",
    "ConfigValidator",
]
