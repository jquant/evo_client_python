"""Clean asynchronous Bank Accounts API."""

from typing import cast

from ...models.bank_accounts_view_model import BankAccountsViewModel
from .base import AsyncBaseApi


class AsyncBankAccountsApi(AsyncBaseApi):
    """Clean asynchronous Bank Accounts API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/bank-accounts"

    async def get_accounts(self) -> BankAccountsViewModel:
        """
        Get all bank accounts.

        Returns:
            Bank accounts view model containing all available accounts

        Example:
            >>> async with AsyncBankAccountsApi() as api:
            ...     accounts = await api.get_accounts()
            ...     for account in accounts.accounts:
            ...         print(f"Account: {account.bank_name} - {account.account_number}")
        """
        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            response_type=BankAccountsViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(BankAccountsViewModel, result)
