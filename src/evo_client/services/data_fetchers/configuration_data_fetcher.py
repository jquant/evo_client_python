# /src/evo_client/services/data_fetchers/configuration_data_fetcher.py
from typing import List, Dict, Optional
import logging

from evo_client.api.configuration_api import ConfigurationApi
from evo_client.core.api_client import ApiClient
from evo_client.models.configuracao_api_view_model import ConfiguracaoApiViewModel
from . import BaseDataFetcher

logger = logging.getLogger(__name__)


class ConfigurationDataFetcher(BaseDataFetcher):
    """Handles fetching and processing branch configuration-related data."""
    
    def __init__(self, configuration_api: ConfigurationApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(configuration_api, branch_api_clients)
    
    def fetch_branch_configurations(
        self,
    ) -> List[ConfiguracaoApiViewModel]:
        """Fetch branch configurations.

        Returns:
            List[ConfiguracaoApiViewModel]: List of branch configurations
        """
        try:
            configs = []
            
            # Get configurations from default client
            result: List[ConfiguracaoApiViewModel] = self.api.get_branch_config()
            if result:
                configs.extend(result)
            
            # Get configurations from branch clients
            if self.branch_api_clients:
                for branch_id, branch_client in self.branch_api_clients.items():
                    try:
                        branch_result = ConfigurationApi(branch_client).get_branch_config()
                        if branch_result:
                            if isinstance(branch_result, list):
                                configs.extend(branch_result)
                            else:
                                configs.append(branch_result)
                    except Exception as e:
                        logger.warning(f"Failed to fetch config for branch {branch_id}: {e}")
            
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
