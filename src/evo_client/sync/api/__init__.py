"""Synchronous API classes."""

from .base import SyncBaseApi
from .members_api import SyncMembersApi
from .sales_api import SyncSalesApi
from .activities_api import SyncActivitiesApi
from .membership_api import SyncMembershipApi
from .receivables_api import SyncReceivablesApi
from .payables_api import SyncPayablesApi
from .entries_api import SyncEntriesApi
from .prospects_api import SyncProspectsApi
from .invoices_api import SyncInvoicesApi
from .pix_api import SyncPixApi
from .bank_accounts_api import SyncBankAccountsApi
from .voucher_api import SyncVoucherApi
from .member_membership_api import SyncMemberMembershipApi
from .workout_api import SyncWorkoutApi
from .employees_api import SyncEmployeesApi
from .configuration_api import SyncConfigurationApi
from .states_api import SyncStatesApi
from .service_api import SyncServiceApi
from .management_api import SyncManagementApi
from .notifications_api import SyncNotificationsApi
from .webhook_api import SyncWebhookApi
from .partnership_api import SyncPartnershipApi

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
