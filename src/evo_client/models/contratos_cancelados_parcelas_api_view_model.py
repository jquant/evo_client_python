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

from .receivables_api_sub_types_view_model import ReceivablesApiSubTypesViewModel


class ContratosCanceladosParcelasApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_receivable: Optional[int] = Field(default=None, alias="idReceivable")
    description: Optional[str] = None
    ammount: Optional[float] = None
    ammount_paid: Optional[float] = Field(default=None, alias="ammountPaid")
    current_installment: Optional[int] = Field(default=None, alias="currentInstallment")
    total_installments: Optional[int] = Field(default=None, alias="totalInstallments")
    tid: Optional[str] = None
    nsu: Optional[str] = None
    authorization: Optional[str] = None
    canceled: Optional[bool] = None
    cancellation_date: Optional[datetime] = Field(
        default=None, alias="cancellationDate"
    )
    cancellation_description: Optional[str] = Field(
        default=None, alias="cancellationDescription"
    )
    registration_date: Optional[datetime] = Field(
        default=None, alias="registrationDate"
    )
    due_date: Optional[datetime] = Field(default=None, alias="dueDate")
    receiving_date: Optional[datetime] = Field(default=None, alias="receivingDate")
    payment_type: Optional[ReceivablesApiSubTypesViewModel] = Field(
        default=None, alias="paymentType"
    )

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.model_dump(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContratosCanceladosParcelasApiViewModel):
            return False
        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
