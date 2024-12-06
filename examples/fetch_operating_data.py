from datetime import datetime, timedelta
from typing import Optional

from evo_client.core.configuration import Configuration
from evo_client.core.api_client import ApiClient
from evo_client.api.gym_api import GymApi
from evo_client.models.gym_model import GymOperatingData

def fetch_operating_data(
    username: str,
    password: str,
    host: str = "https://evo-integracao-api.w12app.com.br",
    branch_id: Optional[int] = None,
    days: int = 30
) -> GymOperatingData:
    """
    Fetch operating data from a gym's EVO API.
    
    Args:
        username: API username/login
        password: API password
        host: API host URL (default: https://evo-integracao-api.w12app.com.br)
        branch_id: Optional branch ID to fetch specific branch info
        days: Number of days of history to fetch (default: 30)
    
    Returns:
        GymOperatingData: The gym's operating data
    """
    print(f"\n=== Fetching Operating Data from {host} ===")
    
    # Initialize configuration with authentication
    config = Configuration(
        username=username,
        password=password,
        host=host
    )
    
    # Initialize API client with configuration
    api_client = ApiClient(configuration=config)
    
    # Initialize gym API with the authenticated client
    gym_api = GymApi(api_client=api_client)
    
    # Set date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        # Fetch operating data
        operating_data = gym_api.get_operating_data(
            from_date=start_date,
            to_date=end_date,
            branch_ids=[str(branch_id)] if branch_id is not None else None,
            async_req=False
        )
        
        # Print summary
        print("\n=== Gym Operating Data Summary ===")
        print(f"Active Members: {len(operating_data.active_members)}")
        print(f"Active Contracts: {len(operating_data.active_contracts)}")
        print(f"Recent Entries: {len(operating_data.recent_entries)}")
        print(f"Monthly Recurring Revenue: ${operating_data.mrr:.2f}")
        print(f"Churn Rate: {operating_data.churn_rate:.1f}%")
        
        # Print financial metrics
        print("\n=== Financial Metrics ===")
        total_receivables = sum(r.amount for r in operating_data.receivables)
        total_overdue = sum(r.amount for r in operating_data.receivables if r.status == "overdue")
        print(f"Total Receivables: ${total_receivables:.2f}")
        print(f"Total Overdue: ${total_overdue:.2f}")
        print(f"Overdue Members: {len(operating_data.overdue_members)}")
        
        return operating_data
        
    except Exception as e:
        print(f"Error fetching operating data: {str(e)}")
        raise

if __name__ == "__main__":
    import os
    
    # Get credentials from environment variables
    username = os.getenv('EVO_USERNAME')
    password = os.getenv('EVO_PASSWORD')
    host = os.getenv('EVO_API_HOST', 'https://evo-integracao-api.w12app.com.br')
    
    if not username or not password:
        raise ValueError("EVO_USERNAME and EVO_PASSWORD environment variables must be set")
    
    assert username is not None
    assert password is not None
        
    fetch_operating_data(
        username=username,
        password=password,
        host=host
    ) 