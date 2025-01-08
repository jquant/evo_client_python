from datetime import datetime, timedelta
from typing import Optional
from decimal import Decimal
import asyncio

from evo_client.core.configuration import Configuration
from evo_client.core.api_client import ApiClient
from evo_client.api.gym_api import GymApi
from evo_client.models.gym_model import GymOperatingData


async def fetch_operating_data(
    username: str,
    password: str,
    host: str = "https://evo-integracao-api.w12app.com.br",
    branch_id: Optional[int] = None,
    days: int = 30,
) -> GymOperatingData:
    """Fetch operating data from the EVO API.

    Args:
        username: API username
        password: API password
        host: API host URL
        branch_id: Optional branch ID to filter data
        days: Number of days to fetch data for

    Returns:
        GymOperatingData object containing metrics and data
    """
    # Initialize API client
    configuration = Configuration()
    configuration.username = username
    configuration.password = password
    configuration.host = host

    api_client = ApiClient(configuration=configuration)
    gym_api = GymApi(api_client=api_client)

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    try:
        # Fetch operating data
        operating_data = await gym_api.get_operating_data(
            from_date=start_date,
            to_date=end_date,
            branch_ids=[str(branch_id)] if branch_id is not None else None,
            async_req=False,
        )

        # If we get a list of branch data, aggregate the metrics
        if isinstance(operating_data, list):
            # Create aggregated data object
            aggregated = GymOperatingData(data_from=start_date, data_to=end_date)

            # Aggregate metrics
            aggregated.total_active_members = sum(
                d.total_active_members for d in operating_data
            )
            aggregated.total_churned_members = sum(
                d.total_churned_members for d in operating_data
            )
            aggregated.mrr = (
                Decimal(str(sum(d.mrr for d in operating_data)))
                if operating_data
                else Decimal("0")
            )
            if operating_data:
                avg_churn = sum(d.churn_rate for d in operating_data) / Decimal(
                    str(len(operating_data))
                )
                aggregated.churn_rate = avg_churn
            else:
                aggregated.churn_rate = Decimal("0")

            # Combine lists
            aggregated.active_members = [
                m for d in operating_data for m in d.active_members
            ]
            aggregated.active_contracts = [
                c for d in operating_data for c in d.active_contracts
            ]
            aggregated.prospects = [p for d in operating_data for p in d.prospects]
            aggregated.non_renewed_members = [
                m for d in operating_data for m in d.non_renewed_members
            ]
            aggregated.receivables = [r for d in operating_data for r in d.receivables]
            aggregated.recent_entries = [
                e for d in operating_data for e in d.recent_entries
            ]

            return aggregated

        return operating_data

    except Exception as e:
        print(f"Error fetching operating data: {str(e)}")
        raise


async def main():
    # Example usage
    username = "your_username"
    password = "your_password"
    branch_id = 1  # Optional: specify branch ID

    try:
        data = await fetch_operating_data(
            username=username, password=password, branch_id=branch_id
        )

        # Print some metrics
        print(f"Active members: {data.total_active_members}")
        print(f"MRR: ${data.mrr}")
        print(f"Churn rate: {data.churn_rate}%")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
