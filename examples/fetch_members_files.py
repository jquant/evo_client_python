from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from evo_client.core.configuration import Configuration
from evo_client.core.api_client import ApiClient
from evo_client.services.gym_api import GymApi
from evo_client.models.gym_model import MembershipStatus, MembersFiles


def fetch_members_files(
    username: str,
    password: str,
    member_ids: List[int],
    host: str = "https://evo-integracao-api.w12app.com.br",
    days: int = 30,
) -> MembersFiles:
    """
    Fetch members files from a gym's EVO API.

    Args:
        username: API username/login
        password: API password
        member_ids: List of member IDs to analyze
        host: API host URL (default: https://evo-integracao-api.w12app.com.br)
        days: Number of days of history to fetch (default: 30)

    Returns:
        MembersFiles: The gym's members files data
    """
    print(f"\n=== Fetching Members Files from {host} ===")
    print(f"Fetching data for {len(member_ids)} members")

    # Initialize configuration with authentication
    config = Configuration(username=username, password=password, host=host)

    # Initialize API client with configuration
    api_client = ApiClient(configuration=config)

    # Initialize gym API with the authenticated client
    gym_api = GymApi(api_client=api_client)

    # Set date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    try:
        # Fetch members files
        members_files = gym_api.get_members_files(
            member_ids=member_ids,
            from_date=start_date,
            to_date=end_date,
            async_req=False,
        )

        # Print summary
        print("\n=== Members Files Summary ===")
        print(f"Total Members: {members_files.total_members}")
        print(f"Active Members: {members_files.active_members}")

        # Print financial metrics
        print("\n=== Financial Metrics ===")
        total_revenue = Decimal("0.00")
        total_pending = Decimal("0.00")

        for member in members_files.members.values():
            if member.current_contract:
                total_revenue += member.total_paid
            total_pending += member.pending_payments

        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Total Pending: ${total_pending:.2f}")

        # Print member status distribution
        print("\n=== Member Status Distribution ===")
        status_counts = {status: 0 for status in MembershipStatus}
        for member in members_files.members.values():
            status_counts[member.status] += 1

        for status, count in status_counts.items():
            if count > 0:
                print(f"{status.value}: {count}")

        # Print timeline summary
        print("\n=== Timeline Summary ===")
        total_events = sum(len(m.timeline) for m in members_files.members.values())
        print(f"Total Timeline Events: {total_events}")

        # Print activity summary
        print("\n=== Activity Summary ===")
        total_entries = sum(m.total_entries for m in members_files.members.values())
        total_classes = sum(
            m.total_classes_attended for m in members_files.members.values()
        )
        print(f"Total Gym Entries: {total_entries}")
        print(f"Total Classes Attended: {total_classes}")

        return members_files

    except Exception as e:
        print(f"Error fetching members files: {str(e)}")
        raise


if __name__ == "__main__":
    import os

    # Get credentials from environment variables
    username = os.getenv("EVO_USERNAME")
    password = os.getenv("EVO_PASSWORD")
    host = os.getenv("EVO_API_HOST", "https://evo-integracao-api.w12app.com.br")

    if not username or not password:
        raise ValueError(
            "EVO_USERNAME and EVO_PASSWORD environment variables must be set"
        )

    # Example member IDs - replace with actual IDs
    member_ids = [1234, 5678]  # Replace with real member IDs

    fetch_members_files(
        username=username,  # type: ignore
        password=password,  # type: ignore
        member_ids=member_ids,
        host=host,
    )
