# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from .w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel


class W12UtilsWebhookViewModel(BaseModel):
    """Model representing a webhook configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )

    IdBranch: Optional[int] = None
    eventType: Optional[str] = None
    urlCallback: Optional[str] = None
    headers: Optional[List[W12UtilsWebhookHeaderViewModel]] = Field(default=[])
    filters: Optional[List[W12UtilsWebhookFilterViewModel]] = Field(default=[])

    # Internal fields not sent to API
    id_webhook: Optional[int] = None
    id_w12: Optional[int] = None
    id_webhook_type: Optional[int] = None
    created_date: Optional[str] = None
    is_deleted: Optional[bool] = Field(default=False)
    deleted_date: Optional[str] = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, W12UtilsWebhookViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
