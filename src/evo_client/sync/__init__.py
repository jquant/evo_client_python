"""Clean synchronous EVO Client implementation."""

from .core.api_client import SyncApiClient
from .core.request_handler import SyncRequestHandler
from .api.base import SyncBaseApi

# Import all sync API classes for easy access
from .api import (
    SyncMembersApi,
    SyncSalesApi,
    SyncActivitiesApi,
    SyncMembershipApi,
    SyncReceivablesApi,
    SyncPayablesApi,
    SyncEntriesApi,
    SyncProspectsApi,
    SyncInvoicesApi,
    SyncPixApi,
    SyncBankAccountsApi,
    SyncVoucherApi,
    SyncMemberMembershipApi,
    SyncWorkoutApi,
    SyncEmployeesApi,
    SyncConfigurationApi,
    SyncStatesApi,
    SyncServiceApi,
    SyncManagementApi,
    SyncNotificationsApi,
    SyncWebhookApi,
    SyncPartnershipApi,
)

__all__ = [
    # Core components
    "SyncApiClient",
    "SyncRequestHandler",
    "SyncBaseApi",
    # All API classes
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
