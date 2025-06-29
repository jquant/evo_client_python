# /src/evo_client/models/gym_model.py

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field

from .atividade_list_api_view_model import AtividadeListApiViewModel
from .configuracao_api_view_model import ConfiguracaoApiViewModel
from .contratos_resumo_api_view_model import ContratosResumoApiViewModel
from .receivables_api_view_model import ReceivablesApiViewModel
from .servicos_resumo_api_view_model import ServicosResumoApiViewModel
from .w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)


class PaymentMethod(IntEnum):
    """Payment method enumeration"""

    CREDIT_CARD = 1
    BOLETO = 2
    SALE_CREDITS = 3
    TRANSFER = 4
    VALOR_ZERADO = 5
    LINK_CHECKOUT = 6
    PIX = 7


class ActivityStatus(IntEnum):
    """Status of a membership"""

    FREE = 0
    AVAILABLE = 1
    FULL = 2
    RESERVATION_CLOSED = 3
    RESTRICTED = 4
    REGISTERED = 5
    FINISHED = 6
    CANCELLED = 7
    IN_QUEUE = 8
    FREE_CLOSED = 10
    RESTRICTED_CLOSED = 11
    RESTRICTED_NOT_ALLOWED = 12
    FULL_NO_WAITING_LIST = 15


class MembershipStatus(str, Enum):
    """Status of a membership"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    PENDING = "pending"


class EntryStatus(str, Enum):
    """Status of a gym entry"""

    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    CANCELLED = "cancelled"


class EntryType(str, Enum):
    """Type of gym entry"""

    REGULAR = "regular"
    GUEST = "guest"
    TRIAL = "trial"
    EVENT = "event"


class Address(BaseModel):
    """Physical address information"""

    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    phone: Optional[str] = None


class BusinessHours(BaseModel):
    """Business hours information"""

    weekDay: str
    hoursFrom: str
    hoursTo: str


class GymUnitKnowledgeBase(BaseModel):
    """Knowledge base for a specific gym unit"""

    model_config = ConfigDict(populate_by_name=True)

    branch_id: int = Field(description="Unit identifier")
    name: str = Field(description="Name of the gym unit")
    address: Address = Field(description="Physical location")
    business_hours: List[BusinessHours] = Field(
        alias="businessHours", description="Standard business hours"
    )
    activities: List[AtividadeListApiViewModel] = Field(
        description="Available activities and classes"
    )
    available_services: List[ServicosResumoApiViewModel] = Field(
        alias="availableServices",
        description="Additional services that can be added to memberships",
    )
    plans: List[ContratosResumoApiViewModel] = Field(
        description="Available membership plans"
    )
    payment_policy: Dict = Field(
        default_factory=dict,
        alias="paymentPolicy",
        description="Payment and billing policies",
    )
    membership_categories: List[W12UtilsCategoryMembershipViewModel] = Field(
        default_factory=list,
        alias="membershipCategories",
        description="Available membership categories",
    )
    branch_config: ConfiguracaoApiViewModel = Field(
        alias="branchConfig", description="Branch-specific configuration"
    )


class GymKnowledgeBase(BaseModel):
    """Complete knowledge base for the entire gym chain"""

    model_config = ConfigDict(
        populate_by_name=True,
        title="Gym Knowledge Base",
    )

    name: str = Field(description="Name of the gym chain")
    units: List[GymUnitKnowledgeBase] = Field(description="List of gym units")
    faqs: List[Dict] = Field(
        default_factory=list, description="Frequently asked questions"
    )


class Activity(BaseModel):
    """Activity or class information"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    description: str
    max_capacity: int = Field(alias="maxCapacity")
    requires_reservation: bool = Field(default=False, alias="requiresReservation")
    duration_minutes: int = Field(alias="durationMinutes")
    instructor: Optional[str] = None
    schedule: Dict[str, List[time]]  # Day of week -> list of times
    status: ActivityStatus = Field(default=ActivityStatus.AVAILABLE)
    photo: Optional[str] = None
    color: Optional[str] = None
    activity_group: Optional[str] = Field(alias="activityGroup")
    show_on_mobile: Optional[bool] = Field(default=True, alias="showOnMobile")
    show_on_website: Optional[bool] = Field(default=True, alias="showOnWebsite")
    audience: List[str] = Field(default_factory=list)
    instructor_photo: Optional[str] = Field(alias="instructorPhoto")
    area: Optional[str] = None
    branch_name: Optional[str] = Field(alias="branchName")
    allow_choosing_spot: Optional[bool] = Field(
        default=False, alias="allowChoosingSpot"
    )
    spots: Optional[List[Dict[str, Union[int, bool, str]]]] = None  # Spot reservations
    session_details: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, alias="sessionDetails"
    )  # Schedule details


class MembershipCategory(BaseModel):
    """Category of membership"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    description: Optional[str] = None
    is_active: bool = Field(default=True, alias="isActive")
    features: List[str] = Field(default_factory=list)
    restrictions: Optional[List[str]] = None


class MembershipService(BaseModel):
    """Additional services included in membership"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    description: str
    price: Decimal
    is_recurring: bool = Field(default=True, alias="isRecurring")
    duration_days: Optional[int] = Field(alias="durationDays")


class GymPlan(BaseModel):
    """Membership plan information"""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., alias="nameMembership")
    price: Decimal = Field(..., alias="value")
    description: str
    features: List[str]
    minimum_commitment_months: int = Field(..., alias="duration")
    enrollment_fee: Optional[Decimal] = None
    annual_fee: Optional[Decimal] = None
    cancellation_notice_days: int = Field(default=30)
    payment_methods: List[PaymentMethod]
    multi_unit_access: bool = Field(default=False, alias="accessBranches")
    allowed_branch_ids: List[int] = Field(
        default_factory=list, alias="allowedBranchIds"
    )
    home_branch_required: bool = Field(default=True, alias="homeBranchRequired")
    max_branch_visits_per_month: Optional[int] = Field(
        default=None, alias="maxBranchVisitsPerMonth"
    )
    category: Optional[MembershipCategory] = None
    available_services: List[MembershipService] = Field(default_factory=list)
    max_installments: int = Field(default=1, alias="maxAmountInstallments")
    is_active: bool = Field(default=True, alias="isActive")


class FAQ(BaseModel):
    """Frequently asked question"""

    model_config = ConfigDict(populate_by_name=True)

    question: str
    answer: str


class PaymentPolicy(BaseModel):
    """Payment and billing policies"""

    model_config = ConfigDict(populate_by_name=True)

    active_member_discount: Optional[int] = Field(
        default=30, alias="activeMemberDiscount"
    )  # 30% discount
    inactive_member_discount: Optional[int] = Field(
        default=50, alias="inactiveMemberDiscount"
    )  # 50% discount
    accepted_payment_methods: List[PaymentMethod] = Field(
        alias="acceptedPaymentMethods"
    )
    pix_key: Optional[str] = Field(alias="pixKey")
    installment_available: bool = Field(default=False, alias="installmentAvailable")
    cancellation_fee_percentage: Optional[int] = Field(
        default=10, alias="cancellationFeePercentage"
    )  # 10% of remaining commitment


class CardFlag(BaseModel):
    """Card flag/brand information"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    code: str
    is_active: bool = Field(default=True, alias="isActive")


class GatewayConfig(BaseModel):
    """Payment gateway configuration"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    type: str
    merchant_id: Optional[str] = Field(alias="merchantId")
    merchant_key: Optional[str] = Field(alias="merchantKey")
    is_active: bool = Field(default=True, alias="isActive")
    accepted_flags: List[CardFlag] = Field(default_factory=list, alias="acceptedFlags")


class OccupationArea(BaseModel):
    """Occupation/Professional area information"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    description: Optional[str] = None
    is_active: bool = Field(default=True, alias="isActive")


class BranchConfig(BaseModel):
    """Branch-specific configuration"""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="idBranch")
    name: str
    trading_name: str = Field(..., alias="tradingName")
    document: str  # CNPJ
    phone: str
    email: str
    address: Address
    business_hours: List[BusinessHours] = Field(..., alias="businessHours")
    gateway_config: Optional[GatewayConfig] = Field(default=None, alias="gatewayConfig")
    occupations: List[OccupationArea] = Field(default_factory=list)
    translations: Dict[str, str] = Field(default_factory=dict)
    parent_branch_id: Optional[int] = Field(default=None, alias="parentBranchId")
    child_branch_ids: List[int] = Field(default_factory=list, alias="childBranchIds")
    is_main_branch: bool = Field(default=False, alias="isMainBranch")
    allowed_access_branch_ids: List[int] = Field(
        default_factory=list, alias="allowedAccessBranchIds"
    )


class GymEntry(BaseModel):
    """Record of a member's entry to the gym"""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="idEntry")
    member_id: Optional[int] = Field(default=None, alias="idMember")
    prospect_id: Optional[int] = Field(default=None, alias="idProspect")
    register_date: datetime = Field(..., alias="registerDate")
    entry_type: EntryType = Field(default=EntryType.REGULAR, alias="entryType")
    status: EntryStatus = Field(default=EntryStatus.VALID)
    branch_id: Optional[int] = Field(default=None, alias="idBranch")
    activity_id: Optional[int] = Field(default=None, alias="idActivity")
    membership_id: Optional[int] = Field(default=None, alias="idMembership")
    device_id: Optional[str] = Field(default=None, alias="deviceId")
    notes: Optional[str]


class MembershipContract(BaseModel):
    """Detailed membership contract information"""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="idMemberMembership")
    member_id: int = Field(..., alias="idMember")
    plan: "GymPlan"  # Forward reference
    category: Optional[MembershipCategory] = None
    status: MembershipStatus = Field(default=MembershipStatus.PENDING)
    start_date: datetime = Field(..., alias="startDate")
    end_date: Optional[datetime] = Field(default=None, alias="endDate")
    last_renewal_date: Optional[datetime] = Field(default=None, alias="lastRenewalDate")
    next_renewal_date: Optional[datetime] = Field(default=None, alias="nextRenewalDate")
    payment_day: int = Field(ge=1, le=31, alias="paymentDay")
    is_auto_renewal: bool = Field(default=False, alias="isAutoRenewal")
    total_value: Decimal = Field(..., alias="totalValue")
    installments: int = Field(default=1)
    branch_id: Optional[int] = Field(default=None, alias="idBranch")


class ReceivableStatus(str, Enum):
    """Status of a receivable"""

    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Receivable(BaseModel):
    """Financial receivable record"""

    model_config = ConfigDict(populate_by_name=True)

    # Core fields
    id: int
    description: Optional[str] = None
    amount: Decimal
    amount_paid: Optional[Decimal] = None
    status: ReceivableStatus = Field(default=ReceivableStatus.PENDING)
    payment_method: Optional[PaymentMethod] = None
    payment_types: Optional[str] = None
    account_status: Optional[str] = None

    # Date fields
    registration_date: Optional[datetime] = Field(
        default=None, alias="registrationDate"
    )
    due_date: Optional[datetime] = Field(default=None, alias="dueDate")
    receiving_date: Optional[datetime] = Field(default=None, alias="receivingDate")
    competence_date: Optional[datetime] = Field(default=None, alias="competenceDate")
    cancellation_date: Optional[datetime] = Field(
        default=None, alias="cancellationDate"
    )
    charge_date: Optional[datetime] = Field(default=None, alias="chargeDate")
    update_date: Optional[datetime] = Field(default=None, alias="updateDate")
    invoice_date: Optional[datetime] = Field(default=None, alias="invoiceDate")
    invoice_canceled_date: Optional[datetime] = Field(
        default=None, alias="invoiceCanceledDate"
    )
    sale_date: Optional[datetime] = Field(default=None, alias="saleDate")

    # Related IDs
    member_id: Optional[int] = Field(default=None, alias="memberId")
    member_name: Optional[str] = Field(default=None, alias="memberName")
    employee_id: Optional[int] = Field(default=None, alias="employeeId")
    employee_name: Optional[str] = Field(default=None, alias="employeeName")
    branch_id: Optional[int] = Field(default=None, alias="branchId")
    sale_id: Optional[int] = Field(default=None, alias="saleId")
    receivable_id: Optional[int] = Field(default=None, alias="receivableId")

    # Installment info
    current_installment: Optional[int] = Field(default=None, alias="currentInstallment")
    total_installments: Optional[int] = Field(default=None, alias="totalInstallments")

    def is_installment(self) -> bool:
        """Check if this receivable is part of an installment plan."""
        return self.total_installments is not None and self.total_installments > 1

    @classmethod
    def get_date_range_filters(cls) -> Dict[str, Tuple[str, str]]:
        """Get mapping of date range filter fields."""
        return {
            "registration_date": ("registration_date_start", "registration_date_end"),
            "due_date": ("due_date_start", "due_date_end"),
            "receiving_date": ("receiving_date_start", "receiving_date_end"),
            "competence_date": ("competence_date_start", "competence_date_end"),
            "cancellation_date": ("cancellation_date_start", "cancellation_date_end"),
            "charge_date": ("charge_date_start", "charge_date_end"),
            "update_date": ("update_date_start", "update_date_end"),
            "invoice_date": ("invoice_date_start", "invoice_date_end"),
            "invoice_canceled_date": (
                "invoice_canceled_date_start",
                "invoice_canceled_date_end",
            ),
            "sale_date": ("sale_date_start", "sale_date_end"),
        }

    @classmethod
    def get_amount_range_filters(cls) -> Tuple[str, str]:
        """Get amount range filter field names."""
        return ("amount_start", "amount_end")


class OverdueMember(BaseModel):
    """Member with overdue payments"""

    id: int
    member_id: int
    name: str
    branch_id: Optional[int] = None
    total_overdue: Decimal
    overdue_since: datetime
    last_payment_date: Optional[datetime] = None
    overdue_receivables: List[ReceivablesApiViewModel] = Field(default_factory=list)


class CardData(BaseModel):
    """Card payment data"""

    model_config = ConfigDict(populate_by_name=True)

    card_number: str = Field(..., alias="cardNumber")
    holder_name: str = Field(..., alias="holderName")
    expiration_month: int = Field(..., alias="expirationMonth")
    expiration_year: int = Field(..., alias="expirationYear")
    security_code: str = Field(..., alias="securityCode")
    brand: Optional[str] = None


class Sale(BaseModel):
    """Sale information"""

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = None
    idBranch: Optional[int] = None
    idMember: Optional[int] = None
    idService: Optional[int] = None
    serviceValue: Decimal
    payment_method: PaymentMethod
    totalInstallments: int = Field(default=1)
    createdAt: datetime
    status: str = Field(default="active")


class NewSale(BaseModel):
    """New sale request"""

    model_config = ConfigDict(populate_by_name=True)

    branch_id: int = Field(..., alias="idBranch")
    member_id: int = Field(..., alias="idMember")
    service_id: Optional[int] = Field(default=None, alias="idService")
    service_value: Decimal = Field(..., alias="serviceValue")
    payment_method: PaymentMethod
    total_installments: int = Field(default=1, alias="totalInstallments")
    card_data: Optional[CardData] = Field(default=None, alias="cardData")


class RevenueBreakdown(BaseModel):
    """Detailed breakdown of revenue sources"""

    model_config = ConfigDict(populate_by_name=True)

    membership_revenue: Decimal = Field(default=Decimal("0.00"))
    class_revenue: Decimal = Field(default=Decimal("0.00"))
    additional_services: Decimal = Field(default=Decimal("0.00"))
    guest_passes: Decimal = Field(default=Decimal("0.00"))
    pt_sessions: Decimal = Field(default=Decimal("0.00"))
    retail: Decimal = Field(default=Decimal("0.00"))

    @property
    def total_revenue(self) -> Decimal:
        """Calculate total revenue from all sources"""
        return (
            self.membership_revenue
            + self.class_revenue
            + self.additional_services
            + self.guest_passes
            + self.pt_sessions
            + self.retail
        )


class CapacityMetrics(BaseModel):
    """Facility utilization and capacity metrics"""

    model_config = ConfigDict(populate_by_name=True)

    peak_hours_utilization: Decimal = Field(default=Decimal("0.00"))
    off_peak_utilization: Decimal = Field(default=Decimal("0.00"))
    class_fill_rate: Decimal = Field(default=Decimal("0.00"))
    equipment_usage_rate: Optional[Decimal] = None
    max_capacity: int = Field(default=0)
    average_daily_visits: Decimal = Field(default=Decimal("0.00"))
    busiest_day_visits: int = Field(default=0)
    quietest_day_visits: int = Field(default=0)


class MemberSegment(BaseModel):
    """Member segment analytics"""

    model_config = ConfigDict(populate_by_name=True)

    segment_name: str
    member_count: int = Field(default=0)
    average_revenue: Decimal = Field(default=Decimal("0.00"))
    retention_rate: Decimal = Field(default=Decimal("0.00"))
    visit_frequency: Decimal = Field(default=Decimal("0.00"))
    average_membership_duration: Decimal = Field(default=Decimal("0.00"))
    member_ids: List[int] = Field(default_factory=list)


class GymOperatingData(BaseModel):
    """Enhanced operational data metrics for a gym branch."""

    model_config = ConfigDict(populate_by_name=True)
    logger: ClassVar = logger

    # Branch Information
    branch_id: Optional[str] = Field(
        default=None, description="ID of the branch this data belongs to"
    )
    branch_name: Optional[str] = Field(default=None, description="Name of the branch")

    # Base Data Collections
    active_members: List[Dict[str, Any]] = Field(default_factory=list)
    active_contracts: List["MembershipContract"] = Field(default_factory=list)
    prospects: List[Dict[str, Any]] = Field(default_factory=list)
    non_renewed_members: List[Dict[str, Any]] = Field(default_factory=list)
    receivables: List["Receivable"] = Field(default_factory=list)
    overdue_members: List["OverdueMember"] = Field(default_factory=list)
    recent_entries: List["GymEntry"] = Field(default_factory=list)
    cross_branch_entries: List["GymEntry"] = Field(default_factory=list)

    # Time Filters
    data_from: Optional[datetime] = Field(default=None)
    data_to: Optional[datetime] = Field(default=None)

    # Core Financial Metrics
    mrr: Decimal = Field(
        default=Decimal("0.00"), description="Monthly Recurring Revenue in the period"
    )
    arr: Decimal = Field(
        default=Decimal("0.00"), description="Annualized Recurring Revenue"
    )
    revenue_breakdown: RevenueBreakdown = Field(default_factory=RevenueBreakdown)
    average_revenue_per_member: Decimal = Field(default=Decimal("0.00"))
    lifetime_value: Decimal = Field(default=Decimal("0.00"))
    grr: Decimal = Field(default=Decimal("0.00"), description="Gross Revenue Retention")
    nrr: Decimal = Field(default=Decimal("0.00"), description="Net Revenue Retention")

    # Membership Metrics
    total_active_members: int = Field(default=0)
    total_churned_members: int = Field(default=0)
    churn_rate: Decimal = Field(default=Decimal("0.00"))
    retention_rate: Decimal = Field(default=Decimal("0.00"))
    membership_growth_rate: Decimal = Field(default=Decimal("0.00"))
    member_segments: Dict[str, MemberSegment] = Field(default_factory=dict)

    # Multi-Unit Metrics
    cross_branch_revenue: Decimal = Field(
        default=Decimal("0.00"), description="Revenue from cross-branch visits"
    )
    multi_unit_member_percentage: Decimal = Field(
        default=Decimal("0.00"),
        description="Percentage of members with multi-unit access",
    )

    # Capacity and Utilization
    capacity_metrics: CapacityMetrics = Field(default_factory=CapacityMetrics)

    # Member Engagement
    class_attendance_rate: Decimal = Field(default=Decimal("0.00"))
    member_satisfaction_score: Optional[Decimal] = None
    average_visits_per_member: Decimal = Field(default=Decimal("0.00"))

    # Campaign and Discount Metrics
    discount_effectiveness: Optional[str] = Field(
        default=None, description="Impact of discount campaigns on ARPU"
    )
    campaign_effectiveness: Optional[str] = Field(
        default=None, description="Impact of marketing campaigns on member reactivation"
    )

    total_prospects: int = Field(default=0)
    total_paid: Decimal = Field(default=Decimal("0.00"))
    total_pending: Decimal = Field(default=Decimal("0.00"))
    total_overdue: Decimal = Field(default=Decimal("0.00"))

    def __init__(self, **data):
        """Initialize GymOperatingData with logging."""
        self.logger.debug("Initializing GymOperatingData")
        start_time = datetime.now()
        super().__init__(**data)
        self.logger.debug(
            "GymOperatingData initialized in {}s",
            (datetime.now() - start_time).total_seconds(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        self.logger.debug("Converting GymOperatingData to dictionary")
        start_time = datetime.now()
        result = self.model_dump(by_alias=True)
        self.logger.debug(
            "Conversion completed in {}s", (datetime.now() - start_time).total_seconds()
        )
        return result

    def _segment_members(self) -> None:
        """Segment members based on behavior and value."""
        self.logger.debug("Segmenting members")

        segments = {
            "premium": MemberSegment(segment_name="Premium"),
            "regular": MemberSegment(segment_name="Regular"),
            "at_risk": MemberSegment(segment_name="At Risk"),
            "inactive": MemberSegment(segment_name="Inactive"),
        }

        for member in self.active_members:
            member_id = member.get("id")
            if not member_id:
                continue

            # Calculate member metrics
            visit_count = len(
                [e for e in self.recent_entries if e.member_id == member_id]
            )
            revenue = sum(
                r.amount for r in self.receivables if r.member_id == member_id
            )

            # Determine segment
            if visit_count == 0:
                segment = segments["inactive"]
            elif visit_count < 4:
                segment = segments["at_risk"]
            elif revenue > 1000:
                segment = segments["premium"]
            else:
                segment = segments["regular"]

            # Update segment metrics
            segment.member_count += 1
            segment.member_ids.append(member_id)
            if segment.member_count > 0:
                segment.average_revenue = (
                    segment.average_revenue * (segment.member_count - 1) + revenue
                ) / segment.member_count

        self.member_segments = segments

    def _analyze_capacity(self) -> None:
        """Analyze facility capacity and utilization."""
        self.logger.debug("Analyzing capacity metrics")

        if not self.recent_entries:
            return

        # Group entries by day
        daily_visits: Dict[date, List[GymEntry]] = {}
        peak_hours_entries = []
        off_peak_entries = []

        for entry in self.recent_entries:
            # Daily grouping
            entry_date = entry.register_date.date()
            if entry_date not in daily_visits:
                daily_visits[entry_date] = []
            daily_visits[entry_date].append(entry)

            # Peak vs off-peak
            hour = entry.register_date.hour
            if 6 <= hour <= 9 or 17 <= hour <= 20:  # Peak hours
                peak_hours_entries.append(entry)
            else:
                off_peak_entries.append(entry)

        # Calculate metrics
        total_days = len(daily_visits)
        if total_days > 0:
            self.capacity_metrics.average_daily_visits = Decimal(
                str(len(self.recent_entries) / total_days)
            )
            self.capacity_metrics.busiest_day_visits = max(
                len(visits) for visits in daily_visits.values()
            )
            self.capacity_metrics.quietest_day_visits = min(
                len(visits) for visits in daily_visits.values()
            )

            # Utilization rates
            if self.capacity_metrics.max_capacity > 0:
                self.capacity_metrics.peak_hours_utilization = Decimal(
                    str(
                        len(peak_hours_entries)
                        / (self.capacity_metrics.max_capacity * total_days)
                    )
                ) * Decimal("100")
                self.capacity_metrics.off_peak_utilization = Decimal(
                    str(
                        len(off_peak_entries)
                        / (self.capacity_metrics.max_capacity * total_days)
                    )
                ) * Decimal("100")

    def _analyze_revenue(self) -> None:
        """Analyze revenue streams."""
        self.logger.debug("Analyzing revenue streams")

        # Reset revenue breakdown
        self.revenue_breakdown = RevenueBreakdown()

        # Analyze receivables
        for receivable in self.receivables:
            if not receivable.amount:
                continue

            # Categorize revenue based on description or other attributes
            description = (
                receivable.description.lower() if receivable.description else ""
            )
            amount = receivable.amount

            if "membership" in description:
                self.revenue_breakdown.membership_revenue += amount
            elif "class" in description:
                self.revenue_breakdown.class_revenue += amount
            elif "personal training" in description:
                self.revenue_breakdown.pt_sessions += amount
            elif "guest" in description:
                self.revenue_breakdown.guest_passes += amount
            elif "retail" in description:
                self.revenue_breakdown.retail += amount
            else:
                self.revenue_breakdown.additional_services += amount

    def calculate_metrics(self) -> None:
        """Calculate all financial and operational metrics."""
        self.logger.info("Starting metrics calculation")
        start_time = datetime.now()

        # Calculate total active members
        self.logger.debug("Calculating active members count")
        self.total_active_members = len(self.active_members)
        self.logger.info("Total active members: {}", self.total_active_members)

        # Calculate MRR from active contracts
        self.logger.debug("Calculating Monthly Recurring Revenue")
        total_mrr = Decimal("0.00")
        contract_count = 0
        for contract in self.active_contracts:
            if contract.total_value:
                # Convert annual/quarterly values to monthly
                if contract.plan and contract.plan.minimum_commitment_months:
                    monthly_value = Decimal(str(contract.total_value)) / Decimal(
                        str(contract.plan.minimum_commitment_months)
                    )
                    total_mrr += monthly_value
                    contract_count += 1

        self.mrr = total_mrr
        self.arr = self.mrr * Decimal("12")

        if self.total_active_members > 0:
            self.average_revenue_per_member = self.mrr / Decimal(
                str(self.total_active_members)
            )

        self.logger.info(
            "Calculated MRR: ${:.2f} from {} contracts", self.mrr, contract_count
        )

        # Calculate churn and retention
        self.logger.debug("Calculating churn metrics")
        self.total_churned_members = len(self.non_renewed_members)
        if self.total_active_members > 0:
            self.churn_rate = (
                Decimal(str(self.total_churned_members))
                / Decimal(str(self.total_active_members))
            ) * Decimal("100")
            self.retention_rate = Decimal("100") - self.churn_rate

        self.logger.info(
            "Churn rate: {:.2f}% ({} churned members)",
            self.churn_rate,
            self.total_churned_members,
        )

        # Calculate membership growth rate
        if self.data_from:
            initial_members = len(
                [
                    m
                    for m in self.active_members
                    if m.get("join_date") and m["join_date"] <= self.data_from
                ]
            )
            if initial_members > 0:
                growth = self.total_active_members - initial_members
                self.membership_growth_rate = (
                    Decimal(str(growth)) / Decimal(str(initial_members))
                ) * Decimal("100")

        # Calculate multi-unit metrics
        self.logger.debug("Calculating multi-unit metrics")
        multi_unit_members = sum(
            1 for m in self.active_members if m.get("access_branches", False)
        )
        if self.total_active_members > 0:
            self.multi_unit_member_percentage = (
                Decimal(str(multi_unit_members))
                / Decimal(str(self.total_active_members))
            ) * Decimal("100")

        self.logger.info(
            "Multi-unit member percentage: {:.2f}%", self.multi_unit_member_percentage
        )

        # Calculate engagement metrics
        if self.total_active_members > 0:
            self.average_visits_per_member = Decimal(
                str(len(self.recent_entries))
            ) / Decimal(str(self.total_active_members))

        # Run detailed analysis
        self._segment_members()
        self._analyze_capacity()
        self._analyze_revenue()

        # Calculate lifetime value
        if self.total_active_members > 0 and self.retention_rate > 0:
            avg_monthly_revenue = self.average_revenue_per_member
            churn_rate_decimal = self.churn_rate / Decimal("100")
            if churn_rate_decimal > 0:
                self.lifetime_value = avg_monthly_revenue / churn_rate_decimal

        elapsed_time = (datetime.now() - start_time).total_seconds()
        self.logger.info("Metrics calculation completed in {:.2f}s", elapsed_time)

    def get_membership_trends(self) -> Dict[str, Any]:
        """Calculate membership trends over time."""
        if not self.data_from or not self.data_to:
            return {}

        trends: Dict[str, Dict[str, int | Decimal]] = {
            "new_members_by_month": {},
            "churned_members_by_month": {},
            "net_growth_by_month": {},
            "mrr_by_month": {},
        }

        current_date = self.data_from
        while current_date <= self.data_to:
            month_key = current_date.strftime("%Y-%m")

            # New members this month
            new_members = len(
                [
                    m
                    for m in self.active_members
                    if m.get("join_date")
                    and m["join_date"].strftime("%Y-%m") == month_key
                ]
            )
            trends["new_members_by_month"][month_key] = new_members

            # Churned members this month
            churned_members = len(
                [
                    m
                    for m in self.non_renewed_members
                    if m.get("cancellation_date")
                    and m["cancellation_date"].strftime("%Y-%m") == month_key
                ]
            )
            trends["churned_members_by_month"][month_key] = churned_members

            # Net growth
            trends["net_growth_by_month"][month_key] = new_members - churned_members

            # MRR for the month
            month_mrr = sum(
                Decimal(str(c.total_value))
                / Decimal(str(c.plan.minimum_commitment_months))
                for c in self.active_contracts
                if (
                    c.start_date
                    and c.start_date.strftime("%Y-%m") <= month_key
                    and (not c.end_date or c.end_date.strftime("%Y-%m") > month_key)
                )
            )
            trends["mrr_by_month"][month_key] = month_mrr

            # Move to next month
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(
                day=1
            )

        return trends

    def get_revenue_summary(self) -> Dict[str, Decimal]:
        """Get a summary of all revenue metrics."""
        return {
            "mrr": self.mrr,
            "arr": self.arr,
            "average_revenue_per_member": self.average_revenue_per_member,
            "lifetime_value": self.lifetime_value,
            "cross_branch_revenue": self.cross_branch_revenue,
            "membership_revenue": self.revenue_breakdown.membership_revenue,
            "class_revenue": self.revenue_breakdown.class_revenue,
            "additional_services": self.revenue_breakdown.additional_services,
            "pt_sessions": self.revenue_breakdown.pt_sessions,
            "guest_passes": self.revenue_breakdown.guest_passes,
            "retail": self.revenue_breakdown.retail,
            "total_revenue": self.revenue_breakdown.total_revenue,
        }

    def get_membership_summary(self) -> Dict[str, Any]:
        """Get a summary of all membership metrics."""
        return {
            "total_active_members": self.total_active_members,
            "total_churned_members": self.total_churned_members,
            "churn_rate": self.churn_rate,
            "retention_rate": self.retention_rate,
            "growth_rate": self.membership_growth_rate,
            "multi_unit_percentage": self.multi_unit_member_percentage,
            "average_visits_per_member": self.average_visits_per_member,
            "segments": {
                name: {
                    "count": segment.member_count,
                    "average_revenue": segment.average_revenue,
                    "retention_rate": segment.retention_rate,
                }
                for name, segment in self.member_segments.items()
            },
        }

    def get_capacity_summary(self) -> Dict[str, Any]:
        """Get a summary of all capacity metrics."""
        return {
            "peak_hours_utilization": self.capacity_metrics.peak_hours_utilization,
            "off_peak_utilization": self.capacity_metrics.off_peak_utilization,
            "class_fill_rate": self.capacity_metrics.class_fill_rate,
            "average_daily_visits": self.capacity_metrics.average_daily_visits,
            "busiest_day_visits": self.capacity_metrics.busiest_day_visits,
            "quietest_day_visits": self.capacity_metrics.quietest_day_visits,
        }

    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report of all metrics."""
        return {
            "time_period": {
                "from": self.data_from.isoformat() if self.data_from else None,
                "to": self.data_to.isoformat() if self.data_to else None,
            },
            "revenue": self.get_revenue_summary(),
            "membership": self.get_membership_summary(),
            "capacity": self.get_capacity_summary(),
            "trends": self.get_membership_trends(),
        }


class MemberEventType(str, Enum):
    """Types of events in a member's timeline"""

    ENTRY = "entry"  # Gym entry/exit events
    MEMBERSHIP = "membership"  # Membership changes
    ACTIVITY = "activity"  # Activity participation
    FINANCIAL = "financial"  # Financial transactions
    PROFILE = "profile"  # Profile updates


class MemberTimelineEvent(BaseModel):
    """A single event in a member's timeline"""

    model_config = ConfigDict(populate_by_name=True)

    event_type: MemberEventType
    timestamp: datetime
    description: str
    related_id: Optional[int] = None
    branch_id: Optional[int] = None
    status: Optional[str] = None
    amount: Optional[Decimal] = None  # For financial transactions
    transaction_type: Optional[str] = None  # payment, refund, etc.
    payment_method: Optional[PaymentMethod] = None


class MemberProfile(BaseModel):
    """Complete member profile including history and timeline"""

    model_config = ConfigDict(populate_by_name=True)

    # Basic info
    id: int = Field(alias="member_id")
    member_id: int  # Will be set from id in __init__
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None

    # Status and dates
    status: MembershipStatus = Field(default=MembershipStatus.PENDING)
    is_active: bool = Field(default=False)
    join_date: Optional[datetime] = None
    last_visit_date: Optional[datetime] = None

    # Membership
    current_contract: Optional[MembershipContract] = None

    # Activity summary
    total_entries: int = Field(default=0)
    total_classes_attended: int = Field(default=0)
    favorite_activities: List[str] = Field(default_factory=list)
    last_entry: Optional[GymEntry] = None

    # Financial summary
    total_paid: Decimal = Field(default=Decimal("0.00"))
    pending_payments: Decimal = Field(default=Decimal("0.00"))
    overdue_payments: Decimal = Field(default=Decimal("0.00"))

    # History
    entries_history: List[GymEntry] = Field(default_factory=list)
    contracts_history: List[MembershipContract] = Field(default_factory=list)
    activities_history: List[Dict[str, Any]] = Field(default_factory=list)
    receivables: List[Receivable] = Field(default_factory=list)

    # Timeline
    timeline: List[MemberTimelineEvent] = Field(default_factory=list)

    def __init__(self, **data):
        # Ensure id is present
        if "id" not in data and "member_id" in data:
            data["id"] = data["member_id"]

        super().__init__(**data)

        # Always set member_id from id
        self.member_id = self.id

        # Set is_active based on status
        self.is_active = self.status == MembershipStatus.ACTIVE

        # Find current contract
        now = datetime.now()
        active_contracts = [
            contract
            for contract in self.contracts_history
            if (
                contract.start_date
                and contract.start_date <= now
                and (not contract.end_date or contract.end_date > now)
                and contract.status == MembershipStatus.ACTIVE
            )
        ]
        self.current_contract = active_contracts[0] if active_contracts else None

        # Update activity summary
        self.total_entries = len(self.entries_history)
        self.total_classes_attended = len(
            [a for a in self.activities_history if a.get("status") == "attended"]
        )
        self.last_entry = self.entries_history[-1] if self.entries_history else None

        # Calculate favorite activities
        activity_counts: Dict[str, int] = {}
        for activity in self.activities_history:
            name = activity.get("name", "")
            if name:
                activity_counts[name] = activity_counts.get(name, 0) + 1
        self.favorite_activities = sorted(
            activity_counts.keys(), key=lambda x: activity_counts[x], reverse=True
        )[
            :5
        ]  # Top 5 most attended activities

    def add_timeline_event(
        self,
        event_type: MemberEventType,
        timestamp: datetime,
        description: str,
        related_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        status: Optional[str] = None,
        amount: Optional[Decimal] = None,
        transaction_type: Optional[str] = None,
        payment_method: Optional[PaymentMethod] = None,
    ) -> None:
        """Add an event to the member's timeline."""
        self.timeline.append(
            MemberTimelineEvent(
                event_type=event_type,
                timestamp=timestamp,
                description=description,
                related_id=related_id,
                branch_id=branch_id,
                status=status,
                amount=amount,
                transaction_type=transaction_type,
                payment_method=payment_method,
            )
        )


class MembersFiles(BaseModel):
    """Comprehensive data about a list of members.

    This model contains all available data about specified members,
    including their complete history of interactions with the gym.
    """

    model_config = ConfigDict(populate_by_name=True)

    # Input parameters
    member_ids: List[int] = Field(..., description="List of member IDs to analyze")
    data_from: Optional[datetime] = Field(default=None)
    data_to: Optional[datetime] = Field(default=None)

    # Member data
    members: Dict[int, MemberProfile] = Field(
        default_factory=dict, description="Member profiles indexed by member ID"
    )

    # Aggregated metrics
    total_members: int = Field(default=0)
    active_members: int = Field(default=0)
    total_revenue: Decimal = Field(default=Decimal("0.00"))
    average_lifetime: Decimal = Field(default=Decimal("0.00"))  # In months

    def add_member(self, profile: MemberProfile) -> None:
        """Add a member profile to the collection."""
        self.members[profile.member_id] = profile
        self._update_metrics()

    def _update_metrics(self) -> None:
        """Update aggregated metrics based on member data."""
        self.total_members = len(self.members)
        self.active_members = sum(1 for m in self.members.values() if m.is_active)

        # Calculate total revenue using Decimal
        total = Decimal("0.00")
        for member in self.members.values():
            total += member.total_paid
        self.total_revenue = total

        # Calculate average lifetime
        total_months = Decimal("0.00")
        for member in self.members.values():
            if member.contracts_history:
                # Sum up months from all contracts
                for contract in member.contracts_history:
                    if contract.start_date:
                        end_date = contract.end_date or datetime.now()
                        months = (end_date - contract.start_date).days / Decimal(
                            "30.44"
                        )  # Average month length
                        total_months += Decimal(str(months))

        if self.total_members > 0:
            self.average_lifetime = total_months / Decimal(str(self.total_members))
        else:
            self.average_lifetime = Decimal("0.00")


# At the end, update forward references
MembershipContract.model_rebuild()
