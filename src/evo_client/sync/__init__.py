"""Clean synchronous EVO Client implementation."""

# Import all sync API classes for easy access
from .api import (
    SyncActivitiesApi,
    SyncBankAccountsApi,
    SyncVoucherApi,
    SyncWorkoutApi,
    SyncConfigurationApi,
    SyncEmployeesApi,
    SyncEntriesApi,
    SyncInvoicesApi,
    SyncManagementApi,
    SyncMemberMembershipApi,
    SyncMembersApi,
    SyncMembershipApi,
    SyncNotificationsApi,
    SyncPartnershipApi,
    SyncPayablesApi,
    SyncPixApi,
    SyncProspectsApi,
    SyncReceivablesApi,
    SyncSalesApi,
    SyncServiceApi,
    SyncStatesApi,
    SyncWebhookApi,
)
from .api.base import SyncBaseApi
from .core.api_client import SyncApiClient
from .core.request_handler import SyncRequestHandler

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
