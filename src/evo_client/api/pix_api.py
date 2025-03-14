from multiprocessing.pool import AsyncResult
from typing import Any, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.pix_payment_details_view_model import PixPaymentDetailsViewModel
from .base import BaseApi


class PixApi(BaseApi):
    """PIX API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = "/api/v1/pix"

    @overload
    def get_qr_code(
        self,
        pix_receipt_id: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> PixPaymentDetailsViewModel:
        ...

    @overload
    def get_qr_code(
        self, pix_receipt_id: Optional[int] = None, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    def get_qr_code(
        self, pix_receipt_id: Optional[int] = None, async_req: bool = False
    ) -> Union[PixPaymentDetailsViewModel, AsyncResult[Any]]:
        """
        Get PIX QR code details.

        Args:
            pix_receipt_id: PIX receipt ID
            async_req: Execute request asynchronously

        Returns:
            PIX payment details including QR code
        """
        params = {"idRecebimentoPix": pix_receipt_id} if pix_receipt_id else {}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/qr-code",
            method="GET",
            query_params=params,
            response_type=PixPaymentDetailsViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )
