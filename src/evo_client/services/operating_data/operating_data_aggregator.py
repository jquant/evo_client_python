from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

from evo_client.models.members_api_view_model import MembersApiViewModel
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel


@dataclass
class GymOperatingData:
    """Represents aggregated operating data for a gym."""
    total_active_members: int
    total_mrr: float
    member_status_distribution: Dict[str, int]
    collection_date: datetime


class OperatingDataAggregator:
    """Aggregates raw data into meaningful operating metrics."""
    
    def aggregate_member_data(self, members: List[MembersApiViewModel]) -> GymOperatingData:
        """
        Aggregate member data into operating metrics.
        
        Args:
            members: List of member data from the API
            
        Returns:
            GymOperatingData with computed metrics
        """
        total_active = len([m for m in members if m.status == "active"])
        status_dist = self._compute_status_distribution(members)
        
        return GymOperatingData(
            total_active_members=total_active,
            total_mrr=0.0,  # TODO: Implement MRR calculation
            member_status_distribution=status_dist,
            collection_date=datetime.now()
        )
    
    def _compute_status_distribution(self, members: List[MembersApiViewModel]) -> Dict[str, int]:
        """Compute the distribution of member statuses."""
        distribution = {}
        for member in members:
            status = member.status or "unknown"
            distribution[status] = distribution.get(status, 0) + 1
        return distribution 