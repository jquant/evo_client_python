"""Common API response models for various endpoints."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StateResponse(BaseModel):
    """State/Province response model."""

    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    code: Optional[str] = None
    country_id: Optional[int] = Field(default=None, alias="countryId")
    country_name: Optional[str] = Field(default=None, alias="countryName")
    active: Optional[bool] = None

    model_config = ConfigDict(populate_by_name=True)


class NotificationCreateResponse(BaseModel):
    """Response model for notification creation."""

    success: bool
    notification_id: Optional[int] = Field(default=None, alias="notificationId")
    message: Optional[str] = None
    sent_at: Optional[datetime] = Field(default=None, alias="sentAt")
    delivery_status: Optional[str] = Field(default=None, alias="deliveryStatus")
    errors: Optional[List[str]] = None

    model_config = ConfigDict(populate_by_name=True)


class WebhookResponse(BaseModel):
    """Webhook configuration response model."""

    id: Optional[int] = Field(default=None, alias="idWebhook")
    event_type: Optional[str] = Field(default=None, alias="eventType")
    url_callback: Optional[str] = Field(default=None, alias="urlCallback")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    branch_name: Optional[str] = Field(default=None, alias="branchName")
    active: Optional[bool] = None
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    last_triggered: Optional[datetime] = Field(default=None, alias="lastTriggered")
    success_count: Optional[int] = Field(default=None, alias="successCount")
    failure_count: Optional[int] = Field(default=None, alias="failureCount")
    headers: Optional[List[Dict[str, Any]]] = None
    filters: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(populate_by_name=True)


class ApiOperationResponse(BaseModel):
    """Generic API operation response."""

    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True)


class MemberServiceResponse(BaseModel):
    """Member service response model."""

    id: Optional[int] = None
    member_id: Optional[int] = Field(default=None, alias="memberId")
    service_name: Optional[str] = Field(default=None, alias="serviceName")
    service_type: Optional[str] = Field(default=None, alias="serviceType")
    start_date: Optional[datetime] = Field(default=None, alias="startDate")
    end_date: Optional[datetime] = Field(default=None, alias="endDate")
    price: Optional[float] = None
    currency: Optional[str] = None
    active: Optional[bool] = None
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)


class EmployeeOperationResponse(BaseModel):
    """Response model for employee operations (create, update, delete)."""

    success: bool
    employee_id: Optional[int] = Field(default=None, alias="employeeId")
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    operation_type: Optional[str] = Field(
        default=None, alias="operationType"
    )  # "create", "update", "delete"

    model_config = ConfigDict(populate_by_name=True)


class ActivityOperationResponse(BaseModel):
    """Response model for activity operations."""

    success: bool
    activity_session_id: Optional[int] = Field(default=None, alias="activitySessionId")
    member_id: Optional[int] = Field(default=None, alias="memberId")
    prospect_id: Optional[int] = Field(default=None, alias="prospectId")
    status: Optional[str] = None  # "Attending", "Absent", "Justified absence"
    message: Optional[str] = None
    errors: Optional[List[str]] = None

    model_config = ConfigDict(populate_by_name=True)
