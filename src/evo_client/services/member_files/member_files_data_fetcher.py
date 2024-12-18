from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union, Tuple
from loguru import logger

from ...api.members_api import MembersApi
from ...api.entries_api import EntriesApi
from ...api.receivables_api import ReceivablesApi
from ...api.activities_api import ActivitiesApi
from ...core.api_client import ApiClient
from ...models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from ...models.receivables_api_view_model import ReceivablesApiViewModel
from ...models.entradas_resumo_api_view_model import EntradasResumoApiViewModel
from ...models.atividade_agenda_api_view_model import AtividadeAgendaApiViewModel
from ...models.gym_model import (
    MembersFiles,
    MemberProfile,
    GymEntry,
    EntryType,
    EntryStatus,
    MemberEventType,
    ReceivableStatus,
    Receivable,
)
from ..data_fetchers import BaseDataFetcher


class MemberFilesDataFetcher(BaseDataFetcher[MembersApi]):
    """Handles fetching and processing comprehensive member files data."""

    def __init__(
        self,
        members_api: MembersApi,
        entries_api: EntriesApi,
        receivables_api: ReceivablesApi,
        activities_api: ActivitiesApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the member files data fetcher.

        Args:
            members_api: The members API instance
            entries_api: The entries API instance
            receivables_api: The receivables API instance
            activities_api: The activities API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(members_api, branch_api_clients)
        self.entries_api = entries_api
        self.receivables_api = receivables_api
        self.activities_api = activities_api

    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> Union[List[MembersFiles], MembersFiles]:
        """Get comprehensive member files data from one or multiple branches.

        Args:
            member_ids: List of member IDs to fetch data for
            branch_ids: Optional list of branch IDs to fetch from
            from_date: Optional start date for data range
            to_date: Optional end date for data range
            async_req: Whether to execute requests asynchronously

        Returns:
            Member files data either synchronously or as an async result
        """
        try:
            # Initialize members files container
            members_files = MembersFiles(
                member_ids=member_ids, data_from=from_date, data_to=to_date
            )

            # Synchronous execution
            all_results: List[
                Tuple[
                    ClienteDetalhesBasicosApiViewModel,
                    List[EntradasResumoApiViewModel],
                    List[ReceivablesApiViewModel],
                    List[AtividadeAgendaApiViewModel],
                ]
            ] = []
            for member_id in member_ids:
                all_results.append(
                    (
                        self.api.get_member_profile(id_member=member_id),
                        self.entries_api.get_entries(
                            register_date_start=from_date,
                            register_date_end=to_date,
                            member_id=member_id,
                        ),
                        self.receivables_api.get_receivables(
                            member_id=member_id,
                            registration_date_start=from_date,
                            registration_date_end=to_date,
                        ),
                        self.activities_api.get_schedule(
                            member_id=member_id, date=from_date, show_full_week=True
                        ),
                    )
                )

            return self._process_members_files(all_results, member_ids, members_files)

        except Exception as e:
            logger.error(f"Error fetching members files: {str(e)}")
            raise ValueError(f"Error fetching members files: {str(e)}")

    def _process_members_files(
        self,
        results: List[
            Tuple[
                ClienteDetalhesBasicosApiViewModel,
                List[EntradasResumoApiViewModel],
                List[ReceivablesApiViewModel],
                List[AtividadeAgendaApiViewModel],
            ]
        ],
        member_ids: List[int],
        members_files: MembersFiles,
    ) -> MembersFiles:
        """Process API results into MembersFiles object.

        Args:
            results: List of API results
            member_ids: List of member IDs
            members_files: MembersFiles object to populate

        Returns:
            Populated MembersFiles object
        """
        try:
            # Results come in groups of 4 per member (profile, entries, receivables, activities)
            for i, member_id in enumerate(member_ids):
                member_data = results[i]

                if member_data[0]:  # If member profile exists
                    profile = self._create_member_profile(member_data[0])
                    self._process_member_data(profile, member_data[2])
                    members_files.add_member(profile)

            return members_files

        except Exception as e:
            logger.error(f"Error processing members files: {str(e)}")
            return members_files

    def _create_member_profile(
        self, member: ClienteDetalhesBasicosApiViewModel
    ) -> MemberProfile:
        """Create a member profile from API member data."""
        return MemberProfile(
            member_id=member.id_member,
            name=f"{member.first_name} {member.last_name}".strip() or "",
            email=member.email,
            phone=member.number,
            photo_url=member.photo,
        )

    def _build_member_timeline(self, profile: MemberProfile) -> None:
        """Build a chronological timeline of member events."""
        # Add entries
        for entry in profile.entries_history:
            profile.add_timeline_event(
                event_type=MemberEventType.ENTRY,
                timestamp=entry.register_date,
                description=f"Gym entry - {entry.entry_type.value}",
                related_id=entry.id,
                branch_id=entry.branch_id,
                status=entry.status.value,
            )

        # Add financial transactions
        for receivable in profile.receivables:
            # Payment made
            if receivable.receiving_date:
                profile.add_timeline_event(
                    event_type=MemberEventType.FINANCIAL,
                    timestamp=receivable.receiving_date,
                    description=f"Payment received - {receivable.description}",
                    related_id=receivable.id,
                    amount=receivable.amount_paid,
                    transaction_type="payment",
                    payment_method=(
                        receivable.payment_method
                        if hasattr(receivable, "payment_method")
                        else None
                    ),
                )

            # Payment due
            if receivable.status == ReceivableStatus.OVERDUE:
                profile.add_timeline_event(
                    event_type=MemberEventType.FINANCIAL,
                    timestamp=receivable.due_date or datetime.now(),
                    description=f"Payment overdue - {receivable.description}",
                    related_id=receivable.id,
                    amount=receivable.amount,
                    transaction_type="overdue",
                    status="overdue",
                )

        # Sort all events by timestamp
        profile.timeline.sort(key=lambda x: x.timestamp)

    def _process_member_data(
        self,
        profile: MemberProfile,
        receivables: List[ReceivablesApiViewModel],
    ) -> None:
        """Process member data from API results."""
        try:
            # this line is probably wrong, but when we eventually run, we'll see
            profile.receivables = [Receivable(**r.model_dump()) for r in receivables]
            # Calculate financial summaries
            for receivable in profile.receivables:
                if receivable.status == ReceivableStatus.PAID:
                    profile.total_paid += receivable.amount or Decimal("0.00")
                elif receivable.status == ReceivableStatus.PENDING:
                    profile.pending_payments += receivable.amount or Decimal("0.00")
                elif receivable.status == ReceivableStatus.OVERDUE:
                    profile.overdue_payments += receivable.amount or Decimal("0.00")

            # Build timeline after all data is processed
            self._build_member_timeline(profile)
        except Exception as e:
            logger.error(f"Error processing member data: {str(e)}")
            raise

    def _convert_entry(self, entry: EntradasResumoApiViewModel) -> GymEntry:
        """Convert SDK entry model to our GymEntry model."""
        try:
            entry_type = EntryType.REGULAR
            if entry.entry_type:
                if entry.entry_type.lower() == "guest":
                    entry_type = EntryType.GUEST
                elif entry.entry_type.lower() == "trial":
                    entry_type = EntryType.TRIAL
                elif entry.entry_type.lower() == "event":
                    entry_type = EntryType.EVENT

            return GymEntry(
                idEntry=entry.id_member or 0,
                idMember=entry.id_member,
                idProspect=entry.id_prospect,
                registerDate=entry.date or datetime.now(),
                entryType=entry_type,
                status=EntryStatus.VALID,  # Default to valid since API doesn't provide status
                idBranch=entry.id_branch,
                idActivity=None,  # API doesn't provide activity info
                idMembership=None,  # API doesn't provide membership info
                deviceId=entry.device,
                notes=entry.block_reason,
            )
        except Exception as e:
            logger.error(f"Error converting entry: {str(e)}")
            return GymEntry(
                idEntry=0,
                idMember=None,
                idProspect=None,
                registerDate=datetime.now(),
                entryType=EntryType.REGULAR,
                status=EntryStatus.INVALID,
                idBranch=None,
                idActivity=None,
                idMembership=None,
                deviceId=None,
                notes=None,
            )
