from multiprocessing.pool import AsyncResult
from typing import Any, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.bank_accounts_view_model import BankAccountsViewModel


class BankAccountsApi:
    """
    Bank Accounts API client for EVO API.

    Handles operations related to bank account management.
    """

    def __init__(self, api_client: Optional[ApiClient] = None):
        """
        Initialize the Bank Accounts API client.

        Args:
            api_client: Optional API client instance. If not provided, creates a new one.
        """
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/bank-accounts"

    @overload
    def get_accounts(self, async_req: Literal[False] = False) -> AsyncResult[Any]:
        ...

    @overload
    def get_accounts(self, async_req: Literal[True] = True) -> BankAccountsViewModel:
        ...

    def get_accounts(
        self, async_req: bool = False
    ) -> Union[BankAccountsViewModel, AsyncResult[Any]]:
        """
        Get all bank accounts.

        Args:
            async_req: If True, returns a AsyncResult[Any] object for asynchronous execution.
                      If False, returns the response directly.

        Returns:
            BankAccountsViewModel containing the list of bank accounts,
            or AsyncResult[Any] if async_req is True.

        Example:
            >>> api = BankAccountsApi()
            >>> accounts = api.get_accounts()
            >>> print(accounts.accounts)
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            response_type=BankAccountsViewModel,
            async_req=async_req,
            auth_settings=["Basic"],
            _return_http_data_only=True,
            _preload_content=True,
            headers={"Accept": "application/json"},
        )
