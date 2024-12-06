from datetime import datetime
from multiprocessing.pool import AsyncResult
from pathlib import Path
from typing import cast, Optional

from evo_client.api.gym_api import GymApi
from evo_client.core.api_client import ApiClient
from evo_client.core.configuration import Configuration
from evo_client.models.gym_model import GymKnowledgeBase

def test_gym_connection(
    username: str,
    password: str,
    host: str = "https://evo-integracao-api.w12app.com.br",
    branch_id: Optional[int] = None,
    save_config: bool = True
) -> GymKnowledgeBase:
    """
    Test connection to a gym's EVO API and fetch its configuration.
    
    Args:
        username: API username/login
        password: API password
        host: API host URL (default: https://evo-integracao-api.w12app.com.br)
        branch_id: Optional branch ID to fetch specific branch info
        save_config: Whether to save the fetched configuration to a file
    
    Returns:
        GymKnowledgeBase: The complete gym configuration
    """
    print(f"\n=== Testing Connection to {host} ===")
    
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
    
    try:
        print("\nFetching gym knowledge base...")
        result = gym_api.get_gym_knowledge_base(
            branch_ids=[str(branch_id)] if branch_id is not None else None,
            include_activity_details=True
        )
        
        # Handle async result if necessary
        gym_kb: GymKnowledgeBase
        if isinstance(result, AsyncResult):
            gym_kb = cast(GymKnowledgeBase, result.get())
        else:
            gym_kb = cast(GymKnowledgeBase, result)
        
        print("\n=== Connection Successful! ===")
        print(f"Gym Name: {gym_kb.name}")
        print(f"Number of Locations: {len(gym_kb.addresses)}")
        print(f"Number of Plans: {len(gym_kb.plans)}")
        print(f"Number of Activities: {len(gym_kb.activities)}")
        
        if save_config:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            branch_suffix = f"_branch_{branch_id}" if branch_id else ""
            output_file = f"gym_config{branch_suffix}_{timestamp}.json"
            
            # Save configuration
            print(f"\nSaving configuration to {output_file}...")
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json_data = gym_kb.model_dump_json(
                    indent=2,
                    exclude_none=True,
                    by_alias=True
                )
                f.write(json_data)
            print("Configuration saved successfully!")
        
        return gym_kb
    
    except Exception as e:
        print("\n=== Connection Failed! ===")
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    import os
    
    # Get credentials from environment variables
    username = "redfit"
    password = "D180781C-E858-4482-9EF9-13BF9F2DCA4F"
    host = os.getenv('EVO_API_HOST', 'https://evo-integracao-api.w12app.com.br')
    
    if not username or not password:
        raise ValueError("EVO_USERNAME and EVO_PASSWORD environment variables must be set")
    
    assert username is not None
    assert password is not None
    
    try:
        gym_kb = test_gym_connection(
            username=username,
            password=password,
            host=host,
            branch_id=1,  # Optional: specify branch ID
            save_config=True  # Save configuration to file
        )
        
        # You can now use gym_kb to access all gym information
        print("\n=== Example Data ===")
        
        # Print locations
        print("\nLocations:")
        for address in gym_kb.addresses:
            print(f"- {address.street}, {address.city}, {address.state}")
        
        # Print plans
        print("\nMembership Plans:")
        for plan in gym_kb.plans:
            print(f"- {plan.name}: ${plan.price}/month")
        
        # Print activities
        print("\nActivities:")
        for activity in gym_kb.activities:
            print(f"- {activity.name} (max {activity.max_capacity} people)")
        
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        print("Please check your credentials and try again.") 