from enum import Enum
from typing import Optional, Dict, List
from pydantic import AnyHttpUrl

from .w12_utils_webhook_view_model import W12UtilsWebhookViewModel
from .w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from .w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel


class WebhookEventType(str, Enum):
    """Types of events that can trigger a webhook."""

    # Core events
    ENTRIES = "entries"
    MEMBERS = "members"
    CONTRACTS = "contracts"
    PAYMENTS = "payments"
    ACTIVITIES = "activities"
    PROSPECTS = "prospects"
    RECEIVABLES = "receivables"
    INVOICES = "invoices"


class WebhookHeader(W12UtilsWebhookHeaderViewModel):
    """Enhanced webhook header model with validation."""

    @classmethod
    def create_secret_key(cls, secret: str) -> "WebhookHeader":
        """Create a header with a secret key.

        Args:
            secret: The secret key value

        Returns:
            WebhookHeader: A header configured with the secret key
        """
        return cls(nome="chave", valor=secret)


class WebhookFilter(W12UtilsWebhookFilterViewModel):
    """Enhanced webhook filter model."""

    @classmethod
    def create_branch_filter(cls, branch_id: int) -> "WebhookFilter":
        """Create a filter for a specific branch.

        Args:
            branch_id: The branch ID to filter

        Returns:
            WebhookFilter: A filter configured for the branch
        """
        return cls(filterType="branch", value=str(branch_id))


class Webhook(W12UtilsWebhookViewModel):
    """Enhanced webhook configuration model.

    Example:
        {
            "idBranch": 1,
            "eventType": "entries",
            "urlCallback": "https://my-webhook-handler.com/evo-events",
            "headers": [
                {"nome": "chave", "valor": "my-secret-key"}
            ],
            "filters": [
                {"filterType": "branch", "value": "1"}
            ]
        }
    """

    def __init__(self, **data):
        """Initialize webhook with enhanced validation."""
        # Convert string URL to AnyHttpUrl for validation
        if "urlCallback" in data and isinstance(data["urlCallback"], str):
            data["urlCallback"] = AnyHttpUrl(data["urlCallback"])
        super().__init__(**data)

    @classmethod
    def create(
        cls,
        url: str,
        event_type: WebhookEventType,
        branch_id: int,
        secret_key: Optional[str] = None,
        additional_headers: Optional[List[WebhookHeader]] = None,
        additional_filters: Optional[List[WebhookFilter]] = None,
    ) -> "Webhook":
        """Create a new webhook configuration.

        Args:
            url: The webhook callback URL
            event_type: Type of events to subscribe to
            branch_id: Branch ID for the webhook
            secret_key: Optional secret key for webhook validation
            additional_headers: Optional additional headers to include
            additional_filters: Optional additional filters to apply

        Returns:
            Webhook: A configured webhook instance
        """
        headers = additional_headers or []
        if secret_key:
            headers.append(WebhookHeader.create_secret_key(secret_key))

        filters = additional_filters or []
        filters.append(WebhookFilter.create_branch_filter(branch_id))

        return cls(
            idBranch=branch_id,
            eventType=event_type.value,
            urlCallback=url,
            headers=headers,
            filters=filters,
        )

    def get_secret_key(self) -> Optional[str]:
        """Get the configured secret key if any.

        Returns:
            Optional[str]: The secret key if configured, None otherwise
        """
        if not self.headers:
            return None

        for header in self.headers:
            if header.nome == "chave":
                return header.valor
        return None

    def validate_request(
        self, request_headers: Dict[str, str], event_type: str
    ) -> bool:
        """Validate an incoming webhook request.

        Args:
            request_headers: The headers from the incoming request
            event_type: The event type from the request

        Returns:
            bool: True if the request is valid, False otherwise
        """
        # Validate event type
        if event_type != self.event_type:
            return False

        # Validate secret key if configured
        secret_key = self.get_secret_key()
        if secret_key:
            request_key = request_headers.get("chave")
            if not request_key or request_key != secret_key:
                return False

        return True
