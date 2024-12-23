from datetime import datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class PaymentMethod(str, Enum):
    """Payment method enumeration"""

    CREDIT_CARD = "1"
    BOLETO = "2"
    SALE_CREDITS = "3"
    TRANSFER = "4"
    VALOR_ZERADO = "5"
    LINK_CHECKOUT = "6"
    PIX = "7"


class ActivityStatus(int, Enum):
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


class BusinessHours(BaseModel):
    """Business hours for a branch"""

    model_config = ConfigDict(populate_by_name=True)

    # API fields
    id_hour: Optional[int] = Field(default=None, alias="idHour")
    id_branch: Optional[int] = Field(default=None, alias="idBranch")
    week_day: Optional[str] = Field(default=None, alias="weekDay")
    hours_from: Optional[datetime] = Field(default=None, alias="hoursFrom")
    hours_to: Optional[datetime] = Field(default=None, alias="hoursTo")
    fl_deleted: Optional[bool] = Field(default=None, alias="flDeleted")
    id_tmp: Optional[int] = Field(default=None, alias="idTmp")
    creation_date: Optional[datetime] = Field(default=None, alias="creationDate")
    id_employee_creation: Optional[int] = Field(
        default=None, alias="idEmployeeCreation"
    )

    # Internal fields for default hours
    weekday_start: Optional[time] = Field(default=time(6, 0))  # 06:00
    weekday_end: Optional[time] = Field(default=time(23, 0))  # 23:00
    weekend_start: Optional[time] = Field(default=time(9, 0))  # 09:00
    weekend_end: Optional[time] = Field(default=time(15, 0))  # 15:00


class Address(BaseModel):
    """Physical address information"""

    model_config = ConfigDict(populate_by_name=True)

    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postal_code: str = Field(alias="postalCode")
    country: str = Field(default="Brasil")
    phone: str


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
    gateway_config: Optional[GatewayConfig] = Field(None, alias="gatewayConfig")
    occupations: List[OccupationArea] = Field(default_factory=list)
    translations: Dict[str, str] = Field(default_factory=dict)


class GymEntry(BaseModel):
    """Record of a member's entry to the gym"""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="idEntry")
    member_id: Optional[int] = Field(None, alias="idMember")
    prospect_id: Optional[int] = Field(None, alias="idProspect")
    register_date: datetime = Field(..., alias="registerDate")
    entry_type: EntryType = Field(default=EntryType.REGULAR, alias="entryType")
    status: EntryStatus = Field(default=EntryStatus.VALID)
    branch_id: Optional[int] = Field(None, alias="idBranch")
    activity_id: Optional[int] = Field(None, alias="idActivity")
    membership_id: Optional[int] = Field(None, alias="idMembership")
    device_id: Optional[str] = Field(None, alias="deviceId")
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
    end_date: Optional[datetime] = Field(None, alias="endDate")
    last_renewal_date: Optional[datetime] = Field(None, alias="lastRenewalDate")
    next_renewal_date: Optional[datetime] = Field(None, alias="nextRenewalDate")
    payment_day: int = Field(ge=1, le=31, alias="paymentDay")
    is_auto_renewal: bool = Field(default=False, alias="isAutoRenewal")
    total_value: Decimal = Field(..., alias="totalValue")
    installments: int = Field(default=1)
    branch_id: Optional[int] = Field(None, alias="idBranch")


class GymKnowledgeBase(BaseModel):
    """Complete knowledge base for a gym chain including locations, plans, and policies"""

    model_config = ConfigDict(
        populate_by_name=True,
        title="Gym Knowledge Base",
        json_schema_extra={
            "examples": [
                {
                    "name": "C4 Gym",
                    "addresses": [
                        {
                            "street": "Avenida casa grande",
                            "number": "1069",
                            "neighborhood": "vila cunha bueno",
                            "city": "São Paulo",
                            "state": "SP",
                            "postal_code": "03260-000",
                            "phone": "+55 1195091-1252",
                        }
                    ],
                    "business_hours": {
                        "weekday_start": "06:00",
                        "weekday_end": "23:00",
                        "weekend_start": "09:00",
                        "weekend_end": "15:00",
                    },
                }
            ]
        },
    )

    name: str = Field(description="Name of the gym")
    addresses: List[Address] = Field(description="List of gym locations")
    business_hours: List[BusinessHours] = Field(
        alias="businessHours", description="Standard business hours"
    )
    plans: List[GymPlan] = Field(description="Available membership plans")
    activities: List[Activity] = Field(description="Available activities and classes")
    faqs: List[FAQ] = Field(description="Frequently asked questions")
    payment_policy: PaymentPolicy = Field(
        alias="paymentPolicy", description="Payment and billing policies"
    )
    branch_config: Optional[BranchConfig] = Field(
        default=None, alias="branchConfig", description="Branch-specific configuration"
    )
    membership_categories: List[MembershipCategory] = Field(
        default_factory=list,
        alias="membershipCategories",
        description="Available membership categories",
    )
    available_services: List[MembershipService] = Field(
        default_factory=list,
        alias="availableServices",
        description="Additional services that can be added to memberships",
    )
    entries: List[GymEntry] = Field(
        default_factory=list, description="Record of gym entries"
    )


class ReceivableStatus(str, Enum):
    """Status of a receivable"""

    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Receivable(BaseModel):
    """Financial receivable record"""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    description: str
    amount: Decimal
    amount_paid: Optional[Decimal] = None
    due_date: datetime
    receiving_date: Optional[datetime] = None
    status: ReceivableStatus = Field(default=ReceivableStatus.PENDING)
    payment_method: Optional[PaymentMethod] = None

    # Member info
    member_id: Optional[int] = None
    member_name: Optional[str] = None

    # Additional details
    branch_id: Optional[int] = None
    current_installment: Optional[int] = None
    total_installments: Optional[int] = None

    def is_installment(self) -> bool:
        """Check if this receivable is part of an installment plan."""
        return self.total_installments is not None and self.total_installments > 1


class OverdueMember(BaseModel):
    """Member with overdue payments"""

    id: int
    member_id: int
    name: str
    branch_id: Optional[int] = None
    total_overdue: Decimal
    overdue_since: datetime
    last_payment_date: Optional[datetime] = None
    overdue_receivables: List[Receivable] = Field(default_factory=list)


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
    service_id: Optional[int] = Field(None, alias="idService")
    service_value: Decimal = Field(..., alias="serviceValue")
    payment_method: PaymentMethod
    total_installments: int = Field(default=1, alias="totalInstallments")
    card_data: Optional[CardData] = Field(None, alias="cardData")


class GymOperatingData(BaseModel):
    """Dynamic operational data for a gym branch.

    This model contains all the dynamic/operational data about members, entries,
    receivables, etc. This is separate from GymKnowledgeBase which contains
    static configuration data.
    """

    model_config = ConfigDict(populate_by_name=True)

    # Active members data
    active_members: List[Dict[str, Any]] = Field(default_factory=list)
    active_contracts: List[MembershipContract] = Field(default_factory=list)

    # Prospects and leads
    prospects: List[Dict[str, Any]] = Field(default_factory=list)
    non_renewed_members: List[Dict[str, Any]] = Field(default_factory=list)

    # Financial data
    receivables: List[Receivable] = Field(default_factory=list)
    overdue_members: List[OverdueMember] = Field(default_factory=list)

    # Access control
    recent_entries: List[GymEntry] = Field(default_factory=list)

    # Time filters
    data_from: Optional[datetime] = Field(default=None)
    data_to: Optional[datetime] = Field(default=None)

    # Financial metrics
    mrr: Decimal = Field(
        default=Decimal("0.00"), description="Monthly Recurring Revenue in the period"
    )
    churn_rate: Decimal = Field(
        default=Decimal("0.00"), description="Churn Rate percentage in the period"
    )
    total_active_members: int = Field(
        default=0, description="Total number of active members in the period"
    )
    total_churned_members: int = Field(
        default=0, description="Total number of churned members in the period"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return self.model_dump(by_alias=True)

    def calculate_metrics(self) -> None:
        """Calculate financial and operational metrics."""
        # Calculate total active members
        self.total_active_members = len(self.active_members)

        # Calculate MRR from active contracts
        total_mrr = Decimal("0.00")
        for contract in self.active_contracts:
            if contract.total_value:
                # Convert annual/quarterly values to monthly
                if contract.plan and contract.plan.minimum_commitment_months:
                    monthly_value = Decimal(str(contract.total_value)) / Decimal(
                        str(contract.plan.minimum_commitment_months)
                    )
                    total_mrr += monthly_value
        self.mrr = total_mrr

        # Calculate churn rate
        self.total_churned_members = len(self.non_renewed_members)
        if self.total_active_members > 0:
            self.churn_rate = (
                Decimal(str(self.total_churned_members))
                / Decimal(str(self.total_active_members))
            ) * Decimal("100")
        else:
            self.churn_rate = Decimal("0.00")


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
        activity_counts = {}
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
