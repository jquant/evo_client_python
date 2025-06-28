"""Clean synchronous PIX API."""

from typing import Optional, cast

from ...models.pix_payment_details_view_model import PixPaymentDetailsViewModel
from .base import SyncBaseApi


class SyncPixApi(SyncBaseApi):
    """Clean synchronous PIX API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/pix"

    def get_qr_code(
        self, pix_receipt_id: Optional[int] = None
    ) -> PixPaymentDetailsViewModel:
        """
        Get PIX QR code details.

        Args:
            pix_receipt_id: PIX receipt ID to retrieve QR code for

        Returns:
            PIX payment details including QR code information

        Example:
            >>> with SyncPixApi() as api:
            ...     qr_details = api.get_qr_code(pix_receipt_id=12345)
            ...     print(f"QR Code: {qr_details.qr_code}")
            ...     print(f"PIX Key: {qr_details.pix_key}")
        """
        params = {"idRecebimentoPix": pix_receipt_id} if pix_receipt_id else {}

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/qr-code",
            method="GET",
            query_params=params,
            response_type=PixPaymentDetailsViewModel,
            auth_settings=["Basic"],
        )
        return cast(PixPaymentDetailsViewModel, result)
