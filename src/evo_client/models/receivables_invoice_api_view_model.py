# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReceivablesInvoiceApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    invoice_number: Optional[str] = Field(default=None, alias="invoiceNumber")
    issued_amount: Optional[float] = Field(default=None, alias="issuedAmount")
    status: Optional[str] = None
    send_date: Optional[datetime] = Field(default=None, alias="sendDate")
    canceled_date: Optional[datetime] = Field(default=None, alias="canceledDate")
    url_pdf: Optional[str] = Field(default=None, alias="urlPdf")
    id_invoice_type: Optional[int] = Field(default=None, alias="idInvoiceType")
    invoice_type: Optional[str] = Field(default=None, alias="invoiceType")

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ReceivablesInvoiceApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
