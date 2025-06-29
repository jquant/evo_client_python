"""Synchronous API classes."""

from .activities_api import SyncActivitiesApi
from .bank_accounts_api import SyncBankAccountsApi
from .base import SyncBaseApi
from .voucher_api import SyncVoucherApi
from .member_membership_api import SyncMemberMembershipApi
from .workout_api import SyncWorkoutApi
from .employees_api import SyncEmployeesApi
from .configuration_api import SyncConfigurationApi
from .entries_api import SyncEntriesApi
from .invoices_api import SyncInvoicesApi
from .management_api import SyncManagementApi
from .members_api import SyncMembersApi
from .membership_api import SyncMembershipApi
from .notifications_api import SyncNotificationsApi
from .partnership_api import SyncPartnershipApi
from .payables_api import SyncPayablesApi
from .pix_api import SyncPixApi
from .prospects_api import SyncProspectsApi
from .receivables_api import SyncReceivablesApi
from .sales_api import SyncSalesApi
from .service_api import SyncServiceApi
from .states_api import SyncStatesApi
from .webhook_api import SyncWebhookApi

__all__ = [
    "SyncBaseApi",
    "SyncMembersApi",
    "SyncSalesApi",
    "SyncActivitiesApi",
    "SyncMembershipApi",
    "SyncReceivablesApi",
    "SyncPayablesApi",
    "SyncEntriesApi",
    "SyncProspectsApi",
    "SyncInvoicesApi",
    "SyncPixApi",
    "SyncBankAccountsApi",
    "SyncVoucherApi",
    "SyncMemberMembershipApi",
    "SyncWorkoutApi",
    "SyncEmployeesApi",
    "SyncConfigurationApi",
    "SyncStatesApi",
    "SyncServiceApi",
    "SyncManagementApi",
    "SyncNotificationsApi",
    "SyncWebhookApi",
    "SyncPartnershipApi",
]
