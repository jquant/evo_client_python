# /src/evo_client/services/data_fetchers/configuration_data_fetcher.py
from typing import List

from loguru import logger

from ...exceptions.api_exceptions import ApiException
from ...models.configuracao_api_view_model import ConfiguracaoApiViewModel
from ...sync.api.configuration_api import SyncConfigurationApi
from . import BaseDataFetcher


class ConfigurationDataFetcher(BaseDataFetcher):
    """Handles fetching and processing branch configuration-related data."""

    def fetch_branch_configurations(self) -> List[ConfiguracaoApiViewModel]:
        """Fetch branch configurations.

        Returns:
            List[ConfiguracaoApiViewModel]: List of branch configurations
        """
        try:
            configs: List[ConfiguracaoApiViewModel] = []
            # Get configurations from branch clients
            for branch_id in self.get_available_branch_ids():
                branch_api = SyncConfigurationApi(
                    api_client=self.get_branch_api(branch_id)
                )
                if branch_api:
                    try:
                        branch_result = branch_api.get_branch_config()
                        if branch_result:
                            configs.extend(branch_result)
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
            raise ValueError(f"Error fetching branch configurations: {str(e)}")

    def validate_and_cache_configurations(self) -> List[ConfiguracaoApiViewModel]:
        """Validate credentials and cache branch configurations.w

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
            raise ValueError(f"Error validating and caching configurations: {str(e)}")
