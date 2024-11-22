# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from .receivables_api_sub_types_view_model import ReceivablesApiSubTypesViewModel
from .receivables_invoice_api_view_model import ReceivablesInvoiceApiViewModel
from .log_tef_api_view_model import LogTefApiViewModel
from .receivables_credit_details import ReceivablesCreditDetails


class ReceivablesApiViewModel(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    id_receivable: Optional[int] = Field(default=None, alias="idReceivable")
    description: Optional[str] = None
    registration_date: Optional[datetime] = Field(
        default=None, alias="registrationDate"
    )
    due_date: Optional[datetime] = Field(default=None, alias="dueDate")
    receiving_date: Optional[datetime] = Field(default=None, alias="receivingDate")
    competence_date: Optional[datetime] = Field(default=None, alias="competenceDate")
    cancellation_date: Optional[datetime] = Field(
        default=None, alias="cancellationDate"
    )
    ammount: Optional[float] = None
    ammount_paid: Optional[float] = Field(default=None, alias="ammountPaid")
    status: Optional[ReceivablesApiSubTypesViewModel] = None
    current_installment: Optional[int] = Field(default=None, alias="currentInstallment")
    total_installments: Optional[int] = Field(default=None, alias="totalInstallments")
    authorization: Optional[str] = None
    payer_name: Optional[str] = Field(default=None, alias="payerName")
    id_member_payer: Optional[int] = Field(default=None, alias="idMemberPayer")
    id_prospect_payer: Optional[int] = Field(default=None, alias="idProspectPayer")
    id_branch_member: Optional[int] = Field(default=None, alias="idBranchMember")
    id_sale: Optional[int] = Field(default=None, alias="idSale")
    bank_account: Optional[ReceivablesApiSubTypesViewModel] = Field(
        default=None, alias="bankAccount"
    )
    payment_type: Optional[ReceivablesApiSubTypesViewModel] = Field(
        default=None, alias="paymentType"
    )
    invoice_details: Optional[List[ReceivablesInvoiceApiViewModel]] = Field(
        default=None, alias="invoiceDetails"
    )
    fees: Optional[float] = None
    conciliated: Optional[bool] = None
    log_tef: Optional[LogTefApiViewModel] = Field(default=None, alias="logTef")
    tid: Optional[str] = None
    nsu: Optional[str] = None
    update_date: Optional[datetime] = Field(default=None, alias="updateDate")
    charge_date: Optional[datetime] = Field(default=None, alias="chargeDate")
    id_receivable_from: Optional[int] = Field(default=None, alias="idReceivableFrom")
    card_acquirer: Optional[str] = Field(default=None, alias="cardAcquirer")
    card_flag: Optional[str] = Field(default=None, alias="cardFlag")
    credit_details: Optional[List[ReceivablesCreditDetails]] = Field(
        default=None, alias="creditDetails"
    )
    cancellation_description: Optional[str] = Field(
        default=None, alias="cancellationDescription"
    )
    source: Optional[str] = None
    sale_date: Optional[datetime] = Field(default=None, alias="saleDate")

    class Config:
        populate_by_name = True
        validate_assignment = True

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
        if not isinstance(other, ReceivablesApiViewModel):
            return False

        return self.model_dump() == other.model_dump()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
