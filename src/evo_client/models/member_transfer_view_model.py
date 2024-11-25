from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MemberTransferViewModel(BaseModel):
    """Member transfer model."""

    # Define fields based on ClienteTransferenciaViewModel
    member_id: Optional[int] = Field(default=None, description="idMember")
    transfer_date: Optional[datetime] = Field(default=None, description="transferDate")
    branch_from_id: Optional[int] = Field(default=None, description="idBranchFrom")
    branch_to_id: Optional[int] = Field(default=None, description="idBranchTo")
    employee_transfer_id: Optional[int] = Field(
        default=None, description="idEmployeeTransfer"
    )
