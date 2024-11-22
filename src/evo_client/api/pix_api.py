from typing import Optional, Union, overload
from threading import Thread

from ..core.api_client import ApiClient
from ..models.pix_payment_details_view_model import PixPaymentDetailsViewModel


class PixApi:
    """PIX API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/pix"

    @overload
    def get_qr_code(
        self, pix_receipt_id: Optional[int] = None, async_req: bool = True
    ) -> Thread: ...

    @overload
    def get_qr_code(
        self, pix_receipt_id: Optional[int] = None, async_req: bool = False
    ) -> PixPaymentDetailsViewModel: ...

    def get_qr_code(
        self, pix_receipt_id: Optional[int] = None, async_req: bool = False
    ) -> Union[PixPaymentDetailsViewModel, Thread]:
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
