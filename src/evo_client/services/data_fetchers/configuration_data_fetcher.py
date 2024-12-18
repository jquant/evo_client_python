# /src/evo_client/services/data_fetchers/configuration_data_fetcher.py
from typing import List, Dict, Optional
import logging

from evo_client.api.configuration_api import ConfigurationApi
from evo_client.core.api_client import ApiClient
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.configuracao_api_view_model import ConfiguracaoApiViewModel
from . import BaseDataFetcher

logger = logging.getLogger(__name__)


class ConfigurationDataFetcher(BaseDataFetcher[ConfigurationApi]):
    """Handles fetching and processing branch configuration-related data."""

    def __init__(
        self,
        configuration_api: ConfigurationApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the configuration data fetcher.

        Args:
            configuration_api: The configuration API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(configuration_api, branch_api_clients)

    def fetch_branch_configurations(self) -> List[ConfiguracaoApiViewModel]:
        """Fetch branch configurations.

        Returns:
            List[ConfiguracaoApiViewModel]: List of branch configurations
        """
        try:
            configs = []

            # Get configurations from default client
            result: List[ConfiguracaoApiViewModel] = self.api.get_branch_config()
            if result:
                # Only include configs for branches we have clients for
                branch_ids = self.get_available_branch_ids()
                configs.extend(
                    [
                        config
                        for config in result
                        if not branch_ids or (config.id_branch in branch_ids)
                    ]
                )

            # Get configurations from branch clients
            for branch_id in self.get_available_branch_ids():
                branch_api = self.get_branch_api(branch_id, ConfigurationApi)
                if branch_api:
                    try:
                        branch_result = branch_api.get_branch_config()
                        if branch_result:
                            if isinstance(branch_result, list):
                                configs.extend(branch_result)
                            else:
                                configs.append(branch_result)
                    except Exception as e:
                        logger.warning(
                            f"Failed to fetch config for branch {branch_id}: {e}"
                        )

            # Remove duplicates based on branch ID
            seen_branches = set()
            unique_configs = []
            for config in configs:
                if config.id_branch and config.id_branch not in seen_branches:
                    seen_branches.add(config.id_branch)
                    unique_configs.append(config)

            return unique_configs

        except Exception as e:
            logger.error(f"Error fetching branch configurations: {str(e)}")
            raise

    def validate_and_cache_configurations(self) -> List[ConfiguracaoApiViewModel]:
        """Validate credentials and cache branch configurations.

        Returns:
            List[ConfiguracaoApiViewModel]: List of validated branch configurations

        Raises:
            ValueError: If no valid configurations are found
            ApiException: If authentication fails
        """
        try:
            # Fetch configurations using existing method
            configs = self.fetch_branch_configurations()

            if not configs:
                raise ValueError("No branch configurations found - check credentials")

            # Cache configurations in API client
            if hasattr(self.api.api_client, "configuration"):
                self.api.api_client.configuration.branch_configs = configs

            # Log successful validation
            branch_summary = [
                f"{c.id_branch}:{c.name}" for c in configs if c.id_branch and c.name
            ]
            logger.info(
                f"Validated configurations for {len(configs)} branches: "
                f"{', '.join(branch_summary)}"
            )

            return configs

        except ApiException as e:
            if e.status == 401:
                raise ValueError("Invalid credentials") from e
            raise
