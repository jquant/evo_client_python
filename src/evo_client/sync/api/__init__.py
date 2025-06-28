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
]
