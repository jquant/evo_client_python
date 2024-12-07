from __future__ import absolute_import

import asyncio
from typing import List, Optional, Dict, Any, Union, cast, TypeVar, Generic, Literal, overload, Callable
from datetime import datetime, time, timedelta
from multiprocessing.pool import AsyncResult, Pool
from decimal import Decimal
from loguru import logger

from ..core.api_client import ApiClient
from ..core.configuration import Configuration
from ..exceptions.api_exceptions import ApiException

# Models from gym_model
from ..models.gym_model import (
    # Core models
    GymKnowledgeBase,
    MembershipContract,
    GymPlan,
    Activity,
    MembershipCategory,
    MembershipService,
    GymOperatingData,
    GymEntry,
    MembersFiles,
    MemberProfile,
    MemberEventType,
    PaymentMethod,
    MembershipStatus,
    
    # Configuration models
    BranchConfig,
    Address,
    BusinessHours,
    PaymentPolicy,
    GatewayConfig,
    OccupationArea,
    
    # Status enums
    ActivityStatus,
    EntryStatus,
    EntryType,
    
    # Receivables models
    Receivable,
    ReceivableStatus,
    OverdueMember,
    
    # Sales models
    Sale,
    NewSale,
)

# External API view models
from ..models.sales_view_model import SalesViewModel
from ..models.new_sale_view_model import NewSaleViewModel
from ..models.card_data_view_model import CardDataViewModel
from ..models.e_forma_pagamento_totem import EFormaPagamentoTotem
from ..models.sales_item_view_model import SalesItemViewModel

# API clients
from ..api.configuration_api import ConfigurationApi
from ..api.activities_api import ActivitiesApi
from ..api.membership_api import MembershipApi
from ..api.entries_api import EntriesApi
from ..api.member_membership_api import MemberMembershipApi
from ..api.workout_api import WorkoutApi
from ..api.service_api import ServiceApi
from ..api.employees_api import EmployeesApi
from ..api.receivables_api import ReceivablesApi
from ..api.sales_api import SalesApi
from ..api.managment_api import ManagementApi
from ..api.members_api import MembersApi
from ..api.prospects_api import ProspectsApi
from ..api.webhook_api import WebhookApi
from ..models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from ..models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from ..models.entradas_resumo_api_view_model import EntradasResumoApiViewModel as EntriesApiViewModel

T = TypeVar('T')

class TypedAsyncResult(AsyncResult, Generic[T]):
    """Type-safe wrapper for AsyncResult."""
    def get(self) -> T:
        return super().get()

def create_async_result(pool: Pool, callback: Any, error_callback: Any) -> TypedAsyncResult[Any]:
    """Create a typed AsyncResult."""
    return cast(TypedAsyncResult[Any], AsyncResult(pool=pool, callback=callback, error_callback=error_callback))

def _convert_category(category_data: Dict[str, Any]) -> Optional[MembershipCategory]:
    """Convert category data to MembershipCategory model."""
    try:
        return MembershipCategory(
            id=category_data.get('id', 0),
            name=category_data.get('name', 'Standard'),
            description=category_data.get('description'),
            isActive=category_data.get('is_active', True),
            features=category_data.get('features', []),
            restrictions=category_data.get('restrictions')
        )
    except Exception as e:
        print(f"Error converting category: {str(e)}")
        return None

class GymApi:
    """Gym API client for EVO API."""

    def __init__(
        self,
        api_client: Optional[ApiClient] = None,
        branch_credentials: Optional[List[Dict[str, str]]] = None
    ):
        """Initialize the GymApi with optional multi-branch support.
        
        Args:
            api_client: Optional API client. If not provided, a default one will be created.
            branch_credentials: Optional list of branch credentials in the format:
                [
                    {
                        "username": "branch1_user",
                        "password": "branch1_pass",
                        "branch_id": "1"
                    },
                    ...
                ]
        """
        self.branch_api_clients: Dict[str, ApiClient] = {}
        
        if branch_credentials:
            # Create API clients for each branch
            for cred in branch_credentials:
                branch_config = Configuration()
                branch_config.username = cred['username']
                branch_config.password = cred['password']
                self.branch_api_clients[cred['branch_id']] = ApiClient(configuration=branch_config)
            
            # Use the first branch's credentials for the default client if no specific client is provided
            if api_client is None and self.branch_api_clients:
                first_branch_id = next(iter(self.branch_api_clients))
                self.default_api_client = self.branch_api_clients[first_branch_id]
            else:
                self.default_api_client = api_client
        else:
            # Set up default client
            if api_client is None:
                configuration = Configuration()
                api_client = ApiClient(configuration=configuration)
            self.default_api_client = api_client
        
        # Initialize APIs with default client
        self._init_apis(self.default_api_client)
        self._pool = Pool(processes=1)  # Single process pool for async operations

    def _init_apis(self, api_client: Optional[ApiClient]):
        """Initialize API instances with the given client."""
        if api_client:
            self.configuration_api = ConfigurationApi(api_client)
            self.activities_api = ActivitiesApi(api_client)
            self.membership_api = MembershipApi(api_client)
            self.entries_api = EntriesApi(api_client)
            self.member_membership_api = MemberMembershipApi(api_client)
            self.workout_api = WorkoutApi(api_client)
            self.service_api = ServiceApi(api_client)
            self.employees_api = EmployeesApi(api_client)
            self.receivables_api = ReceivablesApi(api_client)
            self.sales_api = SalesApi(api_client)
            self.management_api = ManagementApi(api_client)
            self.members_api = MembersApi(api_client)
            self.prospects_api = ProspectsApi(api_client)
            self.webhook_api = WebhookApi(api_client)

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, '_pool'):
            self._pool.close()
            self._pool.join()

    def _convert_receivable(self, receivable: Any) -> Receivable:
        """Convert API receivable model to internal model."""
        return Receivable(
            id=receivable.id_receivable,
            description=receivable.description,
            amount=Decimal(str(receivable.ammount)) if receivable.ammount is not None else Decimal('0.00'),
            amount_paid=Decimal(str(receivable.ammount_paid)) if receivable.ammount_paid is not None else Decimal('0.00'),
            due_date=receivable.due_date,
            receiving_date=receivable.receiving_date,
            status=ReceivableStatus(receivable.status.value) if receivable.status else ReceivableStatus.PENDING,
            member_id=receivable.id_member_payer,
            member_name=receivable.payer_name,
            branch_id=receivable.id_branch_member,
            current_installment=receivable.current_installment,
            total_installments=receivable.total_installments
        )

    @overload
    def get_contracts(
        self,
        member_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        active_only: bool = True,
        async_req: Literal[False] = False,
    ) -> List[MembershipContract]:
        ...

    @overload
    def get_contracts(
        self,
        member_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        active_only: bool = True,
        async_req: Literal[True] = True,
    ) -> TypedAsyncResult[List[MembershipContract]]:
        ...

    def get_contracts(
        self,
        member_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        active_only: bool = True,
        async_req: bool = False,
    ) -> Union[List[MembershipContract], TypedAsyncResult[List[MembershipContract]]]:
        """Get membership contracts."""
        try:
            # Get memberships from API
            memberships = self.membership_api.get_memberships(
                membership_id=None,  # This should be None as we're filtering by member_id
                name=None,
                branch_id=branch_id,
                take=50,  # Maximum allowed
                skip=0,
                active=active_only,
                async_req=True if async_req else False  # type: ignore
            )

            # Handle async result
            if isinstance(memberships, AsyncResult):
                memberships = memberships.get()

            # Filter by member_id if provided
            if member_id is not None:
                memberships = [m for m in memberships if m.id_member == member_id]

            # Convert to contracts
            contracts = []
            for membership in memberships:
                plan = GymPlan(
                    nameMembership=membership.name_membership or "",
                    value=Decimal(str(membership.value)) if membership.value is not None else Decimal('0.00'),
                    description=membership.description or "",
                    features=[d.title for d in membership.differentials] if membership.differentials else [],
                    duration=membership.duration or 12,
                    payment_methods=[PaymentMethod.CREDIT_CARD],
                    accessBranches=bool(membership.access_branches),
                    maxAmountInstallments=membership.max_amount_installments or 1,
                    isActive=not membership.inactive,
                    enrollment_fee=None,
                    annual_fee=None,
                    cancellation_notice_days=membership.min_period_stay_membership or 30,
                    category=None,
                    available_services=[]
                )

                category = MembershipCategory(
                    id=membership.id_membership or 0,
                    name=membership.membership_type or "",
                    description=membership.description or "",
                    isActive=not membership.inactive,
                    features=[],  # Not available in API response
                    restrictions=None  # Not available in API response
                )

                contract = MembershipContract(
                    idMemberMembership=membership.id_membership or 0,
                    idMember=member_id or 0,
                    plan=plan,
                    category=category,
                    status=MembershipStatus.ACTIVE if not membership.inactive else MembershipStatus.INACTIVE,
                    startDate=datetime.now(),  # Not available in API response
                    endDate=None,  # Not available in API response
                    lastRenewalDate=None,  # Not available in API response
                    nextRenewalDate=None,  # Not available in API response
                    paymentDay=1,  # Default value
                    totalValue=Decimal(str(membership.value)) if membership.value is not None else Decimal('0.00'),
                    idBranch=membership.id_branch
                )
                contracts.append(contract)

            return contracts

        except ApiException as e:
            logger.error(f"API error getting contracts: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error getting contracts: {str(e)}")
            return []

    def get_gym_knowledge_base(
        self,
        branch_ids: Optional[List[str]] = None,
        include_activity_details: bool = False,
        async_req: bool = False
    ) -> Union[List[GymKnowledgeBase], GymKnowledgeBase, TypedAsyncResult[List[GymKnowledgeBase]], TypedAsyncResult[GymKnowledgeBase]]:
        """Get gym knowledge base for one or multiple branches."""
        if not branch_ids or not self.branch_api_clients or not any(bid in self.branch_api_clients for bid in branch_ids):
            # Use default client implementation
            try:
                # Get configuration data
                config = self.configuration_api.get_branch_config(async_req=False)
                
                # Create base knowledge base from configuration
                gym_kb = self._create_knowledge_base(config[0] if config else None, None)
                
                # If not async, populate all data
                if not async_req:
                    gym_kb = self._populate_activities(gym_kb, None, include_activity_details)
                    gym_kb = self._populate_memberships(gym_kb, None)
                    gym_kb = self._populate_gateway_config(gym_kb)
                    gym_kb = self._populate_occupations(gym_kb)
                    return gym_kb
                else:
                    # Create async result that will process all data
                    async_result = create_async_result(
                        pool=self._pool,
                        callback=lambda x: self._create_knowledge_base(x[0], None),
                        error_callback=lambda e: logger.error(f"Error in async knowledge base creation: {str(e)}")
                    )
                    return cast(TypedAsyncResult[GymKnowledgeBase], async_result)
            except Exception as e:
                logger.error(f"Error getting gym knowledge base: {str(e)}")
                return self._create_empty_knowledge_base()
        
        branch_ids = branch_ids or list(self.branch_api_clients.keys())
        results = []
        
        for branch_id in branch_ids:
            if branch_id in self.branch_api_clients:
                # Create temporary GymApi instance with branch client
                branch_api = GymApi(api_client=self.branch_api_clients[branch_id])
                result = branch_api.get_gym_knowledge_base(
                    async_req=True,  # Always async for parallel processing
                    include_activity_details=include_activity_details
                )
                results.append(result)
        
        if async_req:
            async_result = self._pool.map_async(lambda r: r.get() if isinstance(r, AsyncResult) else r, results)
            return cast(TypedAsyncResult[List[GymKnowledgeBase]], async_result)
        
        # Wait for all results
        knowledge_bases = [r.get() if isinstance(r, AsyncResult) else r for r in results]
        return knowledge_bases if len(knowledge_bases) > 1 else knowledge_bases[0]

    def _create_empty_knowledge_base(self) -> GymKnowledgeBase:
        """Create an empty knowledge base with default values."""
        return GymKnowledgeBase(
            name="Unknown",
            addresses=[],
            businessHours=[],
            activities=[],
            plans=[],
            faqs=[],
            membershipCategories=[],
            availableServices=[],
            paymentPolicy=PaymentPolicy(
                activeMemberDiscount=30,
                inactiveMemberDiscount=50,
                acceptedPaymentMethods=[
                    PaymentMethod.CREDIT_CARD,
                    PaymentMethod.TRANSFER,
                    PaymentMethod.PIX
                ],
                pixKey=None,
                installmentAvailable=True,
                cancellationFeePercentage=10
            )
        )

    def _create_knowledge_base(self, config: Any, branch_id: Optional[int] = None, async_req: bool = False, include_activity_details: bool = False) -> GymKnowledgeBase:
        """Create a GymKnowledgeBase instance from configuration."""
        try:
            business_hours = getattr(config, 'business_hours', [])
            
            return GymKnowledgeBase(
                name=config.name or "",
                addresses=[
                    Address(
                        street=config.address or "",
                        number=config.number or "",
                        neighborhood=config.neighborhood or "",
                        city=config.city or "",
                        state=config.state or "",
                        postalCode=config.zip_code or "",
                        country="Brasil",
                        phone=config.telephone or ""
                    )
                ],
                businessHours=[
                    BusinessHours(
                        idHour=bh.id_hour or None,
                        idBranch=bh.id_branch or None,
                        weekDay=bh.week_day or None,
                        hoursFrom=bh.hours_from or None,
                        hoursTo=bh.hours_to or None,
                        flDeleted=bh.fl_deleted or None,
                        idTmp=bh.id_tmp or None,
                        creationDate=bh.creation_date or None,
                        idEmployeeCreation=bh.id_employee_creation or None,
                        weekday_start=time(6, 0),
                        weekday_end=time(23, 0),
                        weekend_start=time(9, 0),
                        weekend_end=time(15, 0)
                    ) for bh in business_hours
                ],
                activities=[],  # Will be populated later
                plans=[],  # Will be populated later
                faqs=[],  # Will be populated later
                membershipCategories=[],  # Will be populated later
                availableServices=[],  # Will be populated later
                paymentPolicy=PaymentPolicy(
                    activeMemberDiscount=30,  # Default values since not in SDK
                    inactiveMemberDiscount=50,
                    acceptedPaymentMethods=[
                        PaymentMethod.CREDIT_CARD,
                        PaymentMethod.PIX,
                        PaymentMethod.TRANSFER
                    ],
                    pixKey=None,
                    installmentAvailable=True,
                    cancellationFeePercentage=10
                ),
                branchConfig=BranchConfig(
                    idBranch=config.id_branch or 0,
                    name=config.name or "",
                    tradingName=config.internal_name or "",
                    document=config.cnpj or "",
                    phone=config.telephone or "",
                    email="",  # Not available in SDK
                    address=Address(
                        street=config.address or "",
                        number=config.number or "",
                        neighborhood=config.neighborhood or "",
                        city=config.city or "",
                        state=config.state or "",
                        postalCode=config.zip_code or "",
                        country="Brasil",
                        phone=config.telephone or ""
                    ),
                    businessHours=[
                        BusinessHours(
                            idHour=bh.id_hour or None,
                            idBranch=bh.id_branch or None,
                            weekDay=bh.week_day or None,
                            hoursFrom=bh.hours_from or None,
                            hoursTo=bh.hours_to or None,
                            flDeleted=bh.fl_deleted or None,
                            idTmp=bh.id_tmp or None,
                            creationDate=bh.creation_date or None,
                            idEmployeeCreation=bh.id_employee_creation or None,
                            weekday_start=time(6, 0),
                            weekday_end=time(23, 0),
                            weekend_start=time(9, 0),
                            weekend_end=time(15, 0)
                        ) for bh in business_hours
                    ],
                    gatewayConfig=None,  # Will be populated later
                    occupations=[],  # Will be populated later
                    translations={},  # Default empty translations
                    parentBranchId=getattr(config, 'parent_branch_id', None),
                    childBranchIds=getattr(config, 'child_branch_ids', []) or [],
                    isMainBranch=getattr(config, 'is_main_branch', False),
                    allowedAccessBranchIds=getattr(config, 'allowed_access_branch_ids', []) or []
                )
            )
        except Exception as e:
            logger.error(f"Error creating knowledge base: {str(e)}")
            return self._create_empty_knowledge_base()

    def _populate_activities(self, gym_kb: GymKnowledgeBase, branch_id: Optional[int] = None, include_details: bool = False) -> GymKnowledgeBase:
        """Populate activities in the knowledge base."""
        try:
            # Get activities and employees
            activities = self.activities_api.get_activities(branch_id=branch_id, async_req=False)
            employees = self.employees_api.get_employees(
                employee_id=None,
                name=None,
                email=None,
                take=None,
                skip=None,
                async_req=False
            )

            # Get activity schedules if needed
            activity_schedules = {}
            if include_details:
                for act in activities:
                    try:
                        # Get basic schedule first
                        schedules = self.activities_api.get_schedule(
                            member_id=None,
                            date=datetime.now(),
                            branch_id=branch_id,
                            activity_ids=[act.id_activity] if act.id_activity is not None else None,
                            audience_ids=None,
                            take=None,
                            only_availables=False,
                            show_full_week=False,
                            branch_token=None,
                            async_req=False
                        )
                        
                        if schedules:
                            # Convert list of schedules to dictionary by weekday
                            schedule_dict = {}
                            for schedule in schedules:
                                try:
                                    config_id = getattr(schedule, "idConfiguration", None)
                                    activity_date = getattr(schedule, "date", None) or datetime.now()
                                    session_id = getattr(schedule, "idActivitySession", None)

                                    if session_id:
                                        # If we have a session ID, use that
                                        detail = self.activities_api.get_schedule_detail(
                                            config_id=None,
                                            activity_date=None,
                                            session_id=session_id,
                                            async_req=False
                                        )
                                    elif config_id:
                                        # Otherwise use config_id and activity_date
                                        detail = self.activities_api.get_schedule_detail(
                                            config_id=config_id,
                                            activity_date=activity_date,
                                            session_id=None,
                                            async_req=False
                                        )
                                    else:
                                        # Skip if we don't have either required combination
                                        continue
                                    
                                    if detail and detail.week_day is not None:
                                        weekday = str(detail.week_day)
                                        if weekday not in schedule_dict:
                                            schedule_dict[weekday] = []
                                        if detail.date:
                                            schedule_dict[weekday].append(detail.date.time())
                                except Exception as e:
                                    logger.warning(f"Error getting schedule detail: {str(e)}")
                                    continue
                        
                        activity_schedules[act.id_activity] = schedule_dict
                    except Exception as e:
                        logger.warning(f"Error getting schedule for activity {act.id_activity}: {str(e)}")
                        continue

            # Create activities with enhanced information
            gym_kb.activities = [
                Activity(
                    id=act.id_activity or 0,
                    name=act.name or "",
                    description=act.description or "",
                    maxCapacity=act.total_records or 0,
                    requiresReservation=True,  # Default to requiring reservation
                    durationMinutes=60,  # Default duration since not in API model
                    instructor=next(
                        (emp.name for emp in employees if emp.id_employee == act.id_activity),
                        None
                    ),
                    schedule=activity_schedules.get(act.id_activity, {}),  # Use converted dictionary
                    status=ActivityStatus.AVAILABLE,  # Default to available
                    photo=act.photo,  # Add photo if available
                    color=act.color,  # Add color if available
                    activityGroup=act.activity_group,  # Add group if available
                    showOnMobile=act.show_on_mobile,  # Add mobile visibility
                    showOnWebsite=act.show_on_website,  # Add website visibility
                    audience=[  # Add audience information
                        str(audience.nome)  # Convert to string to handle None values
                        for audience in (act.audience or [])
                        if hasattr(audience, 'nome') and audience.nome is not None
                    ],
                    instructorPhoto=next(
                        (emp.photo_url for emp in employees if emp.id_employee == act.id_activity),
                        None
                    ),
                    area=getattr(act, 'area', None),
                    branchName=next(
                        (emp.name for emp in employees if emp.id_employee == act.id_activity),
                        None
                    ),
                    allowChoosingSpot=getattr(act, 'allow_choosing_spot', False),
                    spots=getattr(act, 'spots', None),
                    sessionDetails=[]  # Skip session details for now to avoid status conversion issues
                ) for act in activities
            ]

            return gym_kb
        except Exception as e:
            logger.error(f"Error populating activities: {str(e)}")
            return gym_kb

    def _populate_memberships(
        self,
        gym_kb: GymKnowledgeBase,
        branch_id: Optional[int] = None,
        async_req: bool = False
    ) -> GymKnowledgeBase:
        """Populate membership plans and categories."""
        try:
            # Fetch memberships, categories, and services
            memberships_result = self.membership_api.get_memberships(
                branch_id=branch_id,
                active=True,  # Only get active memberships
                async_req=True if async_req else False  # type: ignore
            )
            categories_result = self.membership_api.get_categories(
                async_req=True if async_req else False  # type: ignore
            )
            services_result = self.service_api.get_services(
                branch_id=branch_id,
                async_req=True if async_req else False  # type: ignore
            )

            # Handle async results
            memberships = memberships_result.get() if isinstance(memberships_result, AsyncResult) else memberships_result
            categories = categories_result.get() if isinstance(categories_result, AsyncResult) else categories_result
            services = services_result.get() if isinstance(services_result, AsyncResult) else services_result

            if not isinstance(memberships, list) or not isinstance(categories, list) or not isinstance(services, list):
                logger.warning("Invalid response type for memberships, categories, or services")
                return gym_kb

            # First populate categories with default values for missing fields
            gym_kb.membership_categories = [
                MembershipCategory(
                    id=cat.id_category_membership,
                    name=cat.name or "",
                    description="",  # Default empty description
                    isActive=True,  # Default to active
                    features=[],  # Default empty features
                    restrictions=None  # Default no restrictions
                ) for cat in categories
            ]

            # Create a mapping of category names to categories for easy lookup
            category_map = {cat.name.lower(): cat for cat in gym_kb.membership_categories}

            # Then populate plans with their categories and multi-unit access details
            gym_kb.plans = [
                GymPlan(
                    nameMembership=plan.name_membership or "",
                    value=Decimal(str(plan.value or 0)),
                    description=plan.description or "",
                    features=[d.title for d in (plan.differentials or []) if d.title],
                    duration=plan.duration or 12,
                    payment_methods=[PaymentMethod.CREDIT_CARD],
                    accessBranches=bool(plan.access_branches),
                    maxAmountInstallments=plan.max_amount_installments or 1,
                    isActive=not plan.inactive,
                    enrollment_fee=None,
                    annual_fee=None,
                    cancellation_notice_days=plan.min_period_stay_membership or 30,
                    category=category_map.get((plan.membership_type or "").lower()) if plan.membership_type else MembershipCategory(
                        id=0,
                        name="Standard",
                        description="",
                        isActive=True,
                        features=[],
                        restrictions=None
                    ),
                    available_services=[]
                ) for plan in memberships
            ]

            # Finally, populate available services
            gym_kb.available_services = [
                MembershipService(
                    id=service.id_service or 0,
                    name=service.name_service or "",
                    description=service.online_sales_observations or "",
                    price=Decimal(str(service.value or 0)),
                    isRecurring=False,  # Not available in API model
                    durationDays=30  # Default value
                ) for service in services
            ]

            return gym_kb
        except Exception as e:
            logger.exception(f"Error populating memberships: {str(e)}")
            return gym_kb

    def _populate_gateway_config(self, gym_kb: GymKnowledgeBase) -> GymKnowledgeBase:
        """Populate gateway configuration in the knowledge base."""
        try:
            gateway_result = self.configuration_api.get_gateway_config()
            gateway_config = gateway_result.get() if isinstance(gateway_result, AsyncResult) else gateway_result

            if gateway_config and gym_kb.branch_config:
                flags = []  # Card flags will be populated from a different endpoint
                try:
                    # Convert tipo_gateway enum to string
                    gateway_type = str(gateway_config.tipo_gateway.value) if gateway_config.tipo_gateway else "0"
                    
                    # Update branch config with gateway info
                    gym_kb.branch_config.gateway_config = GatewayConfig(
                        id=1,  # Default ID since not in API model
                        name="Payment Gateway",  # Default name
                        type=gateway_type,
                        merchantId="",  # Not available in API model
                        merchantKey="",  # Not available in API model
                        isActive=True,  # Default to active
                        acceptedFlags=flags
                    )
                except Exception as e:
                    print(f"Error populating gateway config: {str(e)}")
            return gym_kb
        except Exception as e:
            print(f"Error fetching gateway config: {str(e)}")
            return gym_kb

    def _populate_occupations(self, gym_kb: GymKnowledgeBase) -> GymKnowledgeBase:
        """Populate occupation areas in the knowledge base."""
        try:
            occupations_result = self.configuration_api.get_occupations()
            occupation_areas = occupations_result.get() if isinstance(occupations_result, AsyncResult) else occupations_result

            if not isinstance(occupation_areas, list):
                return gym_kb

            if gym_kb.branch_config:
                gym_kb.branch_config.occupations = [
                    OccupationArea(
                        id=occ.id_branch or 0,
                        name=occ.name or "Unknown",  # Convert None to default string
                        description=f"Max Occupation: {occ.max_occupation or 0}, Current: {occ.occupation or 0}",
                        isActive=True  # Not available in SDK model
                    ) for occ in occupation_areas
                    if hasattr(occ, 'id_branch') and hasattr(occ, 'name')  # Only include if required fields exist
                ]
        except Exception as e:
            print(f"Error populating occupations: {str(e)}")
        return gym_kb

    def get_receivables(
        self,
        member_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[ReceivableStatus] = None,
        async_req: bool = False
    ) -> Union[List[Receivable], TypedAsyncResult[List[Receivable]]]:
        """
        Get receivables filtered by member, branch, date range, and status.
        
        Args:
            member_id: Optional ID of a specific member
            branch_id: Optional ID of a specific branch
            start_date: Optional start date for filtering receivables
            end_date: Optional end date for filtering receivables
            status: Optional status to filter by
            async_req: If True, returns AsyncResult
            
        Returns:
            List[Receivable]: List of receivables matching the filters
        """
        try:
            # Convert status to SDK format
            account_status = None
            if status:
                if status == ReceivableStatus.PAID:
                    account_status = "1"
                elif status == ReceivableStatus.OVERDUE:
                    account_status = "2"
                elif status == ReceivableStatus.CANCELLED:
                    account_status = "3"

            receivables_result = self.receivables_api.get_receivables(
                member_id=member_id,
                due_date_start=start_date,
                due_date_end=end_date,
                account_status=account_status,
                async_req=True if async_req else False  # type: ignore
            )

            if isinstance(receivables_result, AsyncResult):
                def convert_result(result: Any) -> List[Receivable]:
                    if isinstance(result, list):
                        return [self._convert_receivable(r) for r in result]
                    return []

                async_result = create_async_result(
                    pool=self._pool,
                    callback=convert_result,
                    error_callback=lambda e: []
                )
                return cast(TypedAsyncResult[List[Receivable]], async_result)

            # Handle SDK response
            if receivables_result is None:
                return []
            
            if not isinstance(receivables_result, list):
                try:
                    # Try to convert to list if it's an iterable
                    receivables_list = list(receivables_result)
                except (TypeError, ValueError):
                    return []
            else:
                receivables_list = receivables_result

            return [self._convert_receivable(r) for r in receivables_list]

        except Exception as e:
            print(f"Error fetching receivables: {str(e)}")
            return []

    def get_overdue_members(
        self,
        branch_id: Optional[int] = None,
        min_days_overdue: int = 1,
        async_req: bool = False
    ) -> Union[List[OverdueMember], TypedAsyncResult[List[OverdueMember]]]:
        """
        Get members with overdue payments.
        
        Args:
            branch_id: Optional ID of a specific branch
            min_days_overdue: Minimum number of days overdue (default: 1)
            async_req: If True, returns AsyncResult
            
        Returns:
            List[OverdueMember]: List of members with overdue payments
        """
        try:
            end_date = datetime.now() - timedelta(days=min_days_overdue)
            receivables_result = self.get_receivables(
                branch_id=branch_id,
                end_date=end_date,
                status=ReceivableStatus.OVERDUE,
                async_req=async_req
            )

            if isinstance(receivables_result, AsyncResult):
                def convert_result(result: List[Receivable]) -> List[OverdueMember]:
                    return self._group_overdue_receivables(result)

                async_result = create_async_result(
                    pool=self._pool,
                    callback=convert_result,
                    error_callback=lambda e: []
                )
                return cast(TypedAsyncResult[List[OverdueMember]], async_result)

            return self._group_overdue_receivables(receivables_result)

        except Exception as e:
            print(f"Error fetching overdue members: {str(e)}")
            return []

    def _group_overdue_receivables(self, receivables: List[Receivable]) -> List[OverdueMember]:
        """Group overdue receivables by member."""
        member_map: Dict[int, OverdueMember] = {}
        
        for receivable in receivables:
            if receivable.member_id and receivable.member_id not in member_map:
                member_map[receivable.member_id] = OverdueMember(
                    id=receivable.member_id,
                    name=receivable.member_name or "Unknown",
                    member_id=receivable.member_id,
                    total_overdue=Decimal('0.00'),
                    overdue_since=receivable.due_date or datetime.now(),
                    overdue_receivables=[],
                    branch_id=receivable.branch_id,
                    last_payment_date=None
                )
            
            if receivable.member_id:
                member = member_map[receivable.member_id]
                member.total_overdue += receivable.amount - (receivable.amount_paid or Decimal('0.00'))
                member.overdue_receivables.append(receivable)
        
        return list(member_map.values())

    def _convert_sale(self, sale_vm: SalesViewModel) -> Sale:
        """Convert SDK sale model to our Sale model."""
        # Get the first sale item which contains service details
        sale_item = sale_vm.sale_itens[0].itens[0] if sale_vm.sale_itens and sale_vm.sale_itens[0].itens else None
        
        # Get payment type from sale item or default to CREDIT_CARD
        payment_type = None
        if sale_item and isinstance(sale_item, SalesItemViewModel):
            payment_type = str(sale_item.type) if sale_item.type is not None else None
        
        return Sale(
            id=sale_vm.id_sale,
            idBranch=sale_vm.id_branch,
            idMember=sale_vm.id_member,
            idService=sale_item.id_membership if sale_item else None,
            serviceValue=Decimal(str(sale_item.service_value)) if sale_item and sale_item.service_value else Decimal("0"),
            payment_method=PaymentMethod(payment_type) if payment_type else PaymentMethod.CREDIT_CARD,
            totalInstallments=getattr(sale_item, "installments_count", 1) if sale_item else 1,
            createdAt=sale_vm.sale_date or datetime.now(),
            status="active" if not sale_vm.removed else "cancelled"
        )

    def get_sale(self, sale_id: int) -> Sale:
        """Get a sale by its ID."""
        sale_vm = cast(SalesViewModel, self.sales_api.get_sale_by_id(sale_id, async_req=False))
        return self._convert_sale(sale_vm)

    def create_sale(self, sale: NewSale) -> Sale:
        """Create a new sale."""
        # Convert the sale model to view model
        sale_vm = NewSaleViewModel(
            idBranch=sale.branch_id,
            idMembership=sale.service_id,
            idService=sale.service_id,
            serviceValue=float(sale.service_value) if sale.service_value else None,
            idMember=sale.member_id,
            payment=EFormaPagamentoTotem(sale.payment_method.value),
            typePayment=sale.payment_method.value,
            totalInstallments=sale.total_installments,
            cardData=CardDataViewModel(**sale.card_data.model_dump(by_alias=True)) if sale.card_data else None,
        )

        # Create the sale
        result = cast(NewSaleViewModel, self.sales_api.create_sale(sale_vm, async_req=False))
        if result and result.id_membership:
            # After creating the sale, fetch its details using the membership ID
            created_sale = cast(SalesViewModel, self.sales_api.get_sale_by_id(int(result.id_membership), async_req=False))
            return self._convert_sale(created_sale)
        raise ValueError("Failed to create sale: missing sale ID in response")

    def get_sales(
        self,
        *,  # Force keyword arguments
        id_member: Optional[int] = None,
        date_sale_start: Optional[datetime] = None,
        date_sale_end: Optional[datetime] = None,
        payment_type: Optional[str] = None,
        show_receivables: Optional[bool] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> List[Sale]:
        """Get sales with optional filters.
        
        Args:
            id_member: Filter by member ID
            date_sale_start: Start date for filtering sales
            date_sale_end: End date for filtering sales
            payment_type: Filter by payment type
            show_receivables: Whether to include receivables
            take: Number of records to take
            skip: Number of records to skip
            async_req: Whether to make the request asynchronously
        """
        try:
            sales_vm = cast(List[SalesViewModel], self.sales_api.get_sales(
                member_id=id_member,
                date_sale_start=date_sale_start,
                date_sale_end=date_sale_end,
                show_receivables=show_receivables,
                take=take,
                skip=skip,
                async_req=True if async_req else False  # type: ignore
            ))
            
            return [
                self._convert_sale(sale) for sale in sales_vm
                if sale and sale.sale_itens and sale.sale_itens[0].itens and
                isinstance(sale.sale_itens[0].itens[0], SalesItemViewModel) and
                sale.sale_itens[0].itens[0].service_value is not None
            ]
        except Exception as e:
            print(f"Error getting sales: {str(e)}")
            return []

    @overload
    def get_operating_data(
        self,
        branch_ids: Optional[List[str]] = None,
        days: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> Union[GymOperatingData, List[GymOperatingData]]:
        ...

    @overload
    def get_operating_data(
        self,
        branch_ids: Optional[List[str]] = None,
        days: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> TypedAsyncResult[Union[GymOperatingData, List[GymOperatingData]]]:
        ...

    def get_operating_data(
        self,
        branch_ids: Optional[List[str]] = None,
        days: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[GymOperatingData, List[GymOperatingData], TypedAsyncResult[Union[GymOperatingData, List[GymOperatingData]]]]:
        """Get operating data for one or multiple branches."""
        # Calculate date range if not provided
        if from_date is None or to_date is None:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days if days is not None else 30)
        
        # Helper function to safely execute API calls
        def safe_api_call(func: Callable, *args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except ApiException as e:
                logger.warning(f"API call failed for {func.__name__}: {str(e)}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                return []

        if not branch_ids and not self.branch_api_clients:
            try:
                logger.debug("Starting API calls for operating data")
                start_time = datetime.now()
                
                if async_req:
                    # Async execution with error handling
                    logger.debug("Fetching active clients...")
                    active_members_result = safe_api_call(
                        self.management_api.get_active_clients,
                        async_req=True
                    )
                    
                    logger.debug("Fetching active contracts...")
                    active_contracts_result = safe_api_call(
                        self.get_contracts,
                        active_only=True,
                        async_req=True
                    )
                    
                    logger.debug("Fetching prospects...")
                    prospects_result = safe_api_call(
                        self.prospects_api.get_prospects,
                        register_date_start=from_date,
                        register_date_end=to_date,
                        async_req=True
                    )
                    
                    logger.debug("Fetching non-renewed clients...")
                    non_renewed_result = safe_api_call(
                        self.management_api.get_non_renewed_clients,
                        dt_start=from_date,
                        dt_end=to_date,
                        async_req=True
                    )
                    
                    logger.debug("Fetching receivables...")
                    receivables_result = safe_api_call(
                        self.receivables_api.get_receivables,
                        registration_date_start=from_date,
                        registration_date_end=to_date,
                        async_req=True
                    )
                    
                    logger.debug("Fetching entries...")
                    entries_result = safe_api_call(
                        self.entries_api.get_entries,
                        register_date_start=from_date,
                        register_date_end=to_date,
                        async_req=True
                    )
                    
                    logger.debug("Waiting for all API calls to complete...")
                    
                    # Safely get results
                    def safe_get(result):
                        try:
                            if isinstance(result, AsyncResult):
                                return result.get()
                            return result
                        except Exception:
                            return []

                    results = [
                        safe_get(active_members_result),
                        safe_get(active_contracts_result),
                        safe_get(prospects_result),
                        safe_get(non_renewed_result),
                        safe_get(receivables_result),
                        safe_get(entries_result)
                    ]
                    
                else:
                    # Synchronous execution with error handling
                    logger.debug("Fetching active clients...")
                    active_members = safe_api_call(
                        self.management_api.get_active_clients,
                        async_req=False
                    )
                    
                    logger.debug("Fetching active contracts...")
                    active_contracts = safe_api_call(
                        self.get_contracts,
                        active_only=True,
                        async_req=False
                    )
                    
                    logger.debug("Fetching prospects...")
                    prospects = safe_api_call(
                        self.prospects_api.get_prospects,
                        register_date_start=from_date,
                        register_date_end=to_date,
                        async_req=False
                    )
                    
                    logger.debug("Fetching non-renewed clients...")
                    non_renewed = safe_api_call(
                        self.management_api.get_non_renewed_clients,
                        dt_start=from_date,
                        dt_end=to_date,
                        async_req=False
                    )
                    
                    logger.debug("Fetching receivables...")
                    receivables = safe_api_call(
                        self.receivables_api.get_receivables,
                        registration_date_start=from_date,
                        registration_date_end=to_date,
                        async_req=False
                    )
                    
                    logger.debug("Fetching entries...")
                    entries = safe_api_call(
                        self.entries_api.get_entries,
                        register_date_start=from_date,
                        register_date_end=to_date,
                        async_req=False
                    )
                    
                    results = [active_members, active_contracts, prospects, non_renewed, receivables, entries]
                
                # Process results
                data = self._aggregate_operating_data(results, from_date, to_date)
                
                elapsed_time = (datetime.now() - start_time).total_seconds()
                logger.debug(f"All API calls completed in {elapsed_time:.2f}s")
                return data

            except Exception as e:
                logger.error(f"Error getting operating data: {str(e)}")
                return GymOperatingData(data_from=from_date, data_to=to_date)
        
        # Handle multi-branch requests
        branch_ids = branch_ids or list(self.branch_api_clients.keys())
        results = []
        
        for branch_id in branch_ids:
            if branch_id in self.branch_api_clients:
                try:
                    branch_api = GymApi(api_client=self.branch_api_clients[branch_id])
                    result = branch_api.get_operating_data(
                        days=days,
                        from_date=from_date,
                        to_date=to_date,
                        async_req=True
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error getting data for branch {branch_id}: {str(e)}")
                    results.append(GymOperatingData(data_from=from_date, data_to=to_date))
        
        if async_req:
            async_result = self._pool.map_async(lambda r: r.get() if isinstance(r, AsyncResult) else r, results)
            return cast(TypedAsyncResult[Union[GymOperatingData, List[GymOperatingData]]], async_result)
        
        operating_data = [r.get() if isinstance(r, AsyncResult) else r for r in results]
        return operating_data if len(operating_data) > 1 else operating_data[0]

    def _aggregate_operating_data(
        self,
        results: List[Any],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> GymOperatingData:
        """Aggregate results from multiple API calls into GymOperatingData."""
        logger.debug("Starting data aggregation")
        start_time = datetime.now()
        
        try:
            # Convert API results to appropriate formats
            def to_dict(obj: Any) -> Dict[str, Any]:
                """Convert API object to dictionary."""
                if isinstance(obj, dict):
                    return obj
                return {k: getattr(obj, k, None) for k in dir(obj) 
                    if not k.startswith('_') and not callable(getattr(obj, k))}

            # Extract and convert results with debug logging
            active_members = [m for m in (results[0] or []) if m is not None]
            active_contracts = [c for c in (results[1] or []) if c is not None]
            prospects = [to_dict(p) for p in (results[2] or []) if p is not None]
            non_renewed = [to_dict(m) for m in (results[3] or []) if m is not None]
            receivables = [r for r in (results[4] or []) if r is not None]
            entries = [e for e in (results[5] or []) if e is not None]

            logger.debug(f"Raw members: {len(active_members)}")
            logger.debug(f"Raw contracts: {len(active_contracts)}")
            logger.debug(f"Raw prospects: {len(prospects)}")
            logger.debug(f"Raw non-renewed: {len(non_renewed)}")
            logger.debug(f"Raw receivables: {len(receivables)}")
            logger.debug(f"Raw entries: {len(entries)}")

            # Convert entries to GymEntry objects
            converted_entries = []
            valid_entries = 0
            for entry in entries:
                try:
                    entry_dict = to_dict(entry)
                    entry_action = entry_dict.get('entry_action', '').lower()
                    
                    # Only count valid entries
                    if entry_action == 'entry' and not entry_dict.get('block_reason'):
                        valid_entries += 1
                    
                    converted_entry = GymEntry(
                        idEntry=entry_dict.get('id', 0),
                        idMember=entry_dict.get('id_member'),
                        idProspect=entry_dict.get('id_prospect'),
                        registerDate=entry_dict.get('date', datetime.now()),
                        entryType=EntryType.REGULAR,
                        status=EntryStatus.VALID if entry_action == 'entry' else EntryStatus.INVALID,
                        idBranch=entry_dict.get('id_branch'),
                        idActivity=None,
                        idMembership=None,
                        deviceId=entry_dict.get('device'),
                        notes=entry_dict.get('block_reason', '')
                    )
                    converted_entries.append(converted_entry)
                except Exception as e:
                    logger.warning(f"Error converting entry: {str(e)}")
                    continue

            # Convert receivables to our model
            converted_receivables = []
            total_mrr = Decimal('0.00')
            monthly_payments = set()  # Track unique monthly payments
            
            for receivable in receivables:
                try:
                    rec_dict = to_dict(receivable)
                    status = ReceivableStatus.PENDING
                    
                    # Get status object
                    status_obj = rec_dict.get('status', {})
                    if isinstance(status_obj, dict):
                        status_name = status_obj.get('name', '').lower()
                    else:
                        status_name = getattr(status_obj, 'name', '').lower()
                    
                    # Map status
                    if status_name == 'received':
                        status = ReceivableStatus.PAID
                    elif status_name == 'expired':
                        status = ReceivableStatus.OVERDUE
                    elif status_name == 'canceled':
                        status = ReceivableStatus.CANCELLED

                    # Get amounts safely
                    amount = Decimal(str(rec_dict.get('ammount', 0)))
                    amount_paid = None
                    if rec_dict.get('ammount_paid') is not None:
                        amount_paid = Decimal(str(rec_dict['ammount_paid']))

                    # Calculate MRR from unique monthly payments
                    description = rec_dict.get('description', '').lower()
                    member_id = rec_dict.get('id_member_payer')
                    if (
                        status == ReceivableStatus.PAID and
                        ('mensalidade' in description or 'monthly' in description) and
                        member_id and
                        (member_id, amount) not in monthly_payments
                    ):
                        total_mrr += amount
                        monthly_payments.add((member_id, amount))
                        logger.debug(f"Added to MRR: ${amount} for member {member_id}")

                    converted_receivable = Receivable(
                        id=rec_dict.get('id_receivable', 0),
                        description=rec_dict.get('description', ''),
                        amount=amount,
                        amount_paid=amount_paid,
                        due_date=rec_dict.get('due_date') or datetime.now(),
                        receiving_date=rec_dict.get('receiving_date'),
                        status=status,
                        member_id=member_id,
                        member_name=rec_dict.get('payer_name'),
                        branch_id=rec_dict.get('id_branch_member'),
                        current_installment=rec_dict.get('current_installment'),
                        total_installments=rec_dict.get('total_installments')
                    )
                    converted_receivables.append(converted_receivable)
                except Exception as e:
                    logger.warning(f"Error converting receivable: {str(e)}")
                    continue

            # Get unique active member count from contracts
            unique_active_members = set()
            for contract in active_contracts:
                if contract and hasattr(contract, 'idMember'):
                    unique_active_members.add(contract.idMember)
            
            active_member_count = len(unique_active_members)
            logger.debug(f"Unique active members from contracts: {active_member_count}")

            # Create and populate GymOperatingData
            data = GymOperatingData(
                active_members=list(dict.fromkeys(active_members)),  # Remove duplicates
                active_contracts=active_contracts,
                prospects=prospects,
                non_renewed_members=non_renewed,
                receivables=converted_receivables,
                recent_entries=converted_entries,
                data_from=from_date,
                data_to=to_date
            )

            # Calculate metrics
            data.total_active_members = active_member_count
            data.total_churned_members = len(non_renewed)
            data.mrr = total_mrr

            # Calculate churn rate
            if data.total_active_members > 0:
                data.churn_rate = (Decimal(str(data.total_churned_members)) / 
                                Decimal(str(data.total_active_members))) * Decimal('100')
            
            # Calculate cross-branch metrics
            if data.total_active_members > 0:
                member_home_branches = {}
                cross_branch_entries = []
                
                # Get home branches from contracts
                for contract in active_contracts:
                    if hasattr(contract, 'idMember') and hasattr(contract, 'idBranch'):
                        member_home_branches[contract.idMember] = contract.idBranch
                
                # Identify cross-branch entries
                for entry in converted_entries:
                    if (entry.member_id and entry.branch_id and 
                        entry.member_id in member_home_branches and 
                        entry.branch_id != member_home_branches[entry.member_id]):
                        cross_branch_entries.append(entry)
                
                data.cross_branch_entries = cross_branch_entries
                
                # Calculate multi-unit percentage from contracts
                multi_unit_members = sum(
                    1 for c in active_contracts 
                    if hasattr(c, 'plan') and 
                    getattr(c.plan, 'access_branches', False)
                )
                
                if data.total_active_members > 0:
                    data.multi_unit_member_percentage = (
                        Decimal(str(multi_unit_members)) / 
                        Decimal(str(data.total_active_members))
                    ) * Decimal('100')

            logger.debug(f"Final metrics:")
            logger.debug(f"Total active members: {data.total_active_members}")
            logger.debug(f"Total churned members: {data.total_churned_members}")
            logger.debug(f"MRR: ${data.mrr}")
            logger.debug(f"Churn rate: {data.churn_rate}%")

            elapsed_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"Data aggregation completed in {elapsed_time:.2f}s")
            return data
            
        except Exception as e:
            logger.error(f"Error during data aggregation: {str(e)}")
            logger.exception("Full traceback:")
            return GymOperatingData(
                active_members=[],
                active_contracts=[],
                prospects=[],
                non_renewed_members=[],
                receivables=[],
                recent_entries=[],
                data_from=from_date,
                data_to=to_date
            )

    @overload
    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> MembersFiles:
        ...

    @overload
    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> TypedAsyncResult[MembersFiles]:
        ...

    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[MembersFiles], MembersFiles, TypedAsyncResult[List[MembersFiles]], TypedAsyncResult[MembersFiles]]:
        """Get members files from one or multiple branches."""
        if not branch_ids and not self.branch_api_clients:
            # Use default client implementation
            members_files = MembersFiles(
                member_ids=member_ids,
                data_from=from_date,
                data_to=to_date
            )
            
            try:
                if async_req:
                    # Start all async requests for each member
                    async_results = []
                    for member_id in member_ids:
                        async_results.extend([
                            self.members_api.get_member_profile(id_member=member_id, async_req=True),
                            self.get_contracts(member_id=member_id, active_only=False, async_req=True),
                            self.entries_api.get_entries(
                                register_date_start=from_date,
                                register_date_end=to_date,
                                member_id=member_id,
                                async_req=True
                            ),
                            self.receivables_api.get_receivables(
                                member_id=member_id,
                                registration_date_start=from_date,
                                registration_date_end=to_date,
                                async_req=True
                            ),
                            self.activities_api.get_schedule(
                                member_id=member_id,
                                date=from_date,
                                show_full_week=True,
                                async_req=True
                            )
                        ])
                    
                    # Create async result that will process all data
                    async_result = create_async_result(
                        pool=self._pool,
                        callback=lambda _: self._process_members_files(
                            [r.get() for r in async_results],
                            member_ids,
                            members_files
                        ),
                        error_callback=lambda e: members_files
                    )
                    return cast(TypedAsyncResult[MembersFiles], async_result)
                
                # Synchronous execution
                all_results = []
                for member_id in member_ids:
                    all_results.extend([
                        self.members_api.get_member_profile(id_member=member_id, async_req=False),
                        self.get_contracts(member_id=member_id, active_only=False, async_req=False),
                        self.entries_api.get_entries(
                            register_date_start=from_date,
                            register_date_end=to_date,
                            member_id=member_id,
                            async_req=False
                        ),
                        self.receivables_api.get_receivables(
                            member_id=member_id,
                            registration_date_start=from_date,
                            registration_date_end=to_date,
                            async_req=False
                        ),
                        self.activities_api.get_schedule(
                            member_id=member_id,
                            date=from_date,
                            show_full_week=True,
                            async_req=False
                        )
                    ])
                return self._process_members_files(all_results, member_ids, members_files)
            except Exception as e:
                logger.error(f"Error fetching members files: {str(e)}")
                return members_files
        
        branch_ids = branch_ids or list(self.branch_api_clients.keys())
        results = []
        
        for branch_id in branch_ids:
            if branch_id in self.branch_api_clients:
                # Create temporary GymApi instance with branch client
                branch_api = GymApi(api_client=self.branch_api_clients[branch_id])
                result = branch_api.get_members_files(
                    member_ids=member_ids,
                    from_date=from_date,
                    to_date=to_date,
                    async_req=True  # Always async for parallel processing
                )
                results.append(result)
        
        if async_req:
            async_result = self._pool.map_async(lambda r: r.get() if isinstance(r, AsyncResult) else r, results)
            return cast(TypedAsyncResult[List[MembersFiles]], async_result)
        
        # Wait for all results
        members_files = [r.get() if isinstance(r, AsyncResult) else r for r in results]
        return members_files if len(members_files) > 1 else members_files[0]

    def _create_member_profile(self, member: Any) -> MemberProfile:
        """Create a member profile from API member data."""
        return MemberProfile(
            member_id=member.id_member,
            name=member.name or "",
            email=member.email,
            phone=member.phone,
            photo_url=member.photo_url
        )

    def _build_member_timeline(self, profile: MemberProfile) -> None:
        """Build a chronological timeline of member events."""
        # Add entries
        for entry in profile.entries_history:
            profile.add_timeline_event(
                event_type=MemberEventType.ENTRY,
                timestamp=entry.register_date,
                description=f"Gym entry - {entry.entry_type.value}",
                related_id=entry.id,
                branch_id=entry.branch_id,
                status=entry.status.value
            )
            
        # Add financial transactions
        for receivable in profile.receivables:
            # Payment made
            if receivable.receiving_date:
                profile.add_timeline_event(
                    event_type=MemberEventType.FINANCIAL,
                    timestamp=receivable.receiving_date,
                    description=f"Payment received - {receivable.description}",
                    related_id=receivable.id,
                    amount=receivable.amount_paid,
                    transaction_type="payment",
                    payment_method=receivable.payment_method if hasattr(receivable, 'payment_method') else None
                )
            
            # Payment due
            if receivable.status == ReceivableStatus.OVERDUE:
                profile.add_timeline_event(
                    event_type=MemberEventType.FINANCIAL,
                    timestamp=receivable.due_date,
                    description=f"Payment overdue - {receivable.description}",
                    related_id=receivable.id,
                    amount=receivable.amount,
                    transaction_type="overdue",
                    status="overdue"
                )
            
        # Sort all events by timestamp
        profile.timeline.sort(key=lambda x: x.timestamp)

    def _process_members_files(
        self,
        results: List[Any],
        member_ids: List[int],
        members_files: MembersFiles
    ) -> MembersFiles:
        """Process async results into MembersFiles object."""
        try:
            # Results come in groups of 5 per member (member, contracts, entries, receivables, sessions)
            results_per_member = 5
            for i, member_id in enumerate(member_ids):
                base_idx = i * results_per_member
                member = results[base_idx]
                
                if member:
                    profile = self._create_member_profile(member)
                    
                    # Process contracts
                    contracts = results[base_idx + 1]
                    if contracts:
                        profile.contracts_history = contracts
                        active_contracts = [c for c in contracts if c.status == MembershipStatus.ACTIVE]
                        if active_contracts:
                            profile.current_contract = active_contracts[0]
                            profile.is_active = True
                    
                    # Process entries
                    entries = results[base_idx + 2]
                    if entries:
                        profile.entries_history = [self._convert_entry(e) for e in entries]
                        profile.total_entries = len(profile.entries_history)
                        if profile.entries_history:
                            profile.last_entry = profile.entries_history[-1]
                    
                    # Process receivables
                    receivables = results[base_idx + 3]
                    if receivables:
                        profile.receivables = [self._convert_receivable(r) for r in receivables]
                        # Calculate financial summaries
                        for receivable in profile.receivables:
                            if receivable.status == ReceivableStatus.PAID:
                                profile.total_paid += receivable.amount or Decimal('0.00')
                            elif receivable.status == ReceivableStatus.PENDING:
                                profile.pending_payments += receivable.amount or Decimal('0.00')
                            elif receivable.status == ReceivableStatus.OVERDUE:
                                profile.overdue_payments += receivable.amount or Decimal('0.00')
                    
                    # Process activity sessions
                    sessions = results[base_idx + 4]
                    if sessions:
                        profile.total_classes_attended = len(sessions)
                        activity_counts: Dict[str, int] = {}
                        for session in sessions:
                            activity_name = getattr(session, 'activity_name', None)
                            if activity_name:
                                activity_counts[activity_name] = activity_counts.get(activity_name, 0) + 1
                        profile.favorite_activities = sorted(
                            activity_counts.keys(),
                            key=lambda x: activity_counts[x],
                            reverse=True
                        )[:5]
                    
                    # Build timeline
                    self._build_member_timeline(profile)
                    
                    # Add profile to collection
                    members_files.add_member(profile)
            
        except Exception as e:
            logger.error(f"Error processing members files: {str(e)}")
            
        return members_files

    def _process_member_data(self, profile: MemberProfile, results: List[Any]) -> None:
        """Process member data from API results."""
        try:
            # Process receivables
            receivables = results[3] if len(results) > 3 else None
            if receivables:
                profile.receivables = [self._convert_receivable(r) for r in receivables]
                # Calculate financial summaries
                for receivable in profile.receivables:
                    if receivable.status == ReceivableStatus.PAID:
                        profile.total_paid += receivable.amount or Decimal('0.00')
                    elif receivable.status == ReceivableStatus.PENDING:
                        profile.pending_payments += receivable.amount or Decimal('0.00')
                    elif receivable.status == ReceivableStatus.OVERDUE:
                        profile.overdue_payments += receivable.amount or Decimal('0.00')

            # Build timeline after all data is processed
            self._build_member_timeline(profile)
        except Exception as e:
            logger.error(f"Error processing member data: {str(e)}")
            raise

    def _convert_entry(self, entry: Any) -> GymEntry:
        """Convert SDK entry model to our GymEntry model."""
        try:
            entry_type = EntryType.REGULAR
            if entry.entry_type:
                if entry.entry_type.lower() == "guest":
                    entry_type = EntryType.GUEST
                elif entry.entry_type.lower() == "trial":
                    entry_type = EntryType.TRIAL
                elif entry.entry_type.lower() == "event":
                    entry_type = EntryType.EVENT

            return GymEntry(
                idEntry=entry.id or 0,
                idMember=entry.id_member,
                idProspect=entry.id_prospect,
                registerDate=entry.date or datetime.now(),
                entryType=entry_type,
                status=EntryStatus.VALID,  # Default to valid since API doesn't provide status
                idBranch=entry.id_branch,
                idActivity=None,  # API doesn't provide activity info
                idMembership=None,  # API doesn't provide membership info
                deviceId=entry.device,
                notes=entry.block_reason
            )
        except Exception as e:
            logger.error(f"Error converting entry: {str(e)}")
            return GymEntry(
                idEntry=0,
                idMember=None,
                idProspect=None,
                registerDate=datetime.now(),
                entryType=EntryType.REGULAR,
                status=EntryStatus.INVALID,
                idBranch=None,
                idActivity=None,
                idMembership=None,
                deviceId=None,
                notes=None
            )

    async def _handle_rate_limit(self, delay: float = 1.5):
        """Handle rate limiting with exponential backoff."""
        await asyncio.sleep(delay)

    async def _delete_webhook_with_retry(self, webhook_api: WebhookApi, webhook_id: int, max_retries: int = 3, base_delay: float = 1.5) -> bool:
        """Delete webhook with retry logic."""
        for attempt in range(max_retries):
            try:
                response = webhook_api.delete_webhook(webhook_id, async_req=False)
                # If response is boolean, use it directly
                if isinstance(response, bool):
                    if response:
                        logger.debug(f"Successfully deleted webhook {webhook_id}")
                        await self._handle_rate_limit()
                        return True
                    else:
                        logger.error(f"Failed to delete webhook {webhook_id}")
                        return False
                
                # Otherwise try to get success from response data
                success = getattr(response, 'data', None)
                if success:
                    logger.debug(f"Successfully deleted webhook {webhook_id}")
                    await self._handle_rate_limit()
                    return True
                
                logger.error(f"Failed to delete webhook {webhook_id}")
                
            except Exception as e:
                if "429" in str(e):  # Rate limit error
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit, waiting {delay} seconds before retry")
                    await asyncio.sleep(delay)
                    continue
                logger.error(f"Error deleting webhook {webhook_id}: {str(e)}")
            
            await self._handle_rate_limit()  # Wait between attempts
        
        return False

    async def manage_webhooks(
        self,
        url_callback: str,
        branch_ids: Optional[List[str]] = None,
        event_types: Optional[List[str]] = None,
        headers: Optional[List[Dict[str, str]]] = None,
        filters: Optional[List[Dict[str, str]]] = None,
        unsubscribe: bool = False,
        async_req: bool = False,
    ) -> Union[bool, TypedAsyncResult[bool]]:
        """Manage webhook subscriptions."""
        try:
            logger.debug(f"Managing webhooks for URL: {url_callback}")
            logger.debug(f"Branch IDs: {branch_ids}")
            logger.debug(f"Event types: {event_types}")
            logger.debug(f"Operation: {'unsubscribe' if unsubscribe else 'subscribe'}")

            # Log available branch credentials
            logger.debug("Available branch credentials:")
            for branch_id, client in self.branch_api_clients.items():
                if client and client.configuration:
                    logger.debug(f"  Branch {branch_id}: {client.configuration.username}")

            # Define all possible event types
            all_event_types = [
                "NewSale",
                "CreateMember",
                "AlterMember",
                "EndedSessionActivity",
                "ClearedDebt",
                "AlterReceivables",
                "Freeze",
                "RecurrentSale",
                "entries",
                "ActivityEnroll",
                "SalesItensUpdated",
                "CreateMembership",
                "AlterMembership",
                "CreateService",
                "AlterService",
                "CreateProduct",
                "AlterProduct"
            ]
            event_types = event_types or all_event_types
            logger.debug(f"Using event types: {event_types}")

            # Convert headers and filters to view models
            webhook_headers = [
                W12UtilsWebhookHeaderViewModel(nome=h["nome"], valor=h["valor"])
                for h in (headers or [])
            ] or [W12UtilsWebhookHeaderViewModel(nome="Content-Type", valor="application/json")]
            logger.debug(f"Using headers: {webhook_headers}")

            webhook_filters = [
                W12UtilsWebhookFilterViewModel(filterType=f["filterType"], value=f["value"])
                for f in (filters or [])
            ] or [W12UtilsWebhookFilterViewModel(filterType="All", value="*")]
            logger.debug(f"Using filters: {webhook_filters}")

            # Handle unsubscribe
            if unsubscribe:
                logger.debug("Getting existing webhooks for unsubscribe")
                if branch_ids:
                    # Get webhooks for each branch
                    for branch_id in branch_ids:
                        if branch_id in self.branch_api_clients:
                            logger.debug(f"Getting webhooks for branch {branch_id}")
                            branch_webhook_api = WebhookApi(self.branch_api_clients[branch_id])
                            existing_webhooks = branch_webhook_api.get_webhooks(async_req=False)
                            logger.debug(f"Found webhooks for branch {branch_id}: {existing_webhooks}")
                            await self._handle_rate_limit()
                            
                            for webhook in existing_webhooks:
                                webhook_id = webhook.get('idWebhook')
                                webhook_url = webhook.get('urlCallback')
                                webhook_event = webhook.get('tipoEvento')
                                webhook_branch = webhook.get('idFilial')
                                
                                logger.debug(f"Checking webhook: ID={webhook_id}, URL={webhook_url}, Event={webhook_event}, Branch={webhook_branch}")
                                
                                if webhook_id and (
                                    webhook_url == url_callback and 
                                    webhook_event in event_types and
                                    str(webhook_branch) == branch_id
                                ):
                                    success = await self._delete_webhook_with_retry(branch_webhook_api, webhook_id)
                                    if not success:
                                        continue  # Try next webhook
                else:
                    # Get webhooks using default client
                    if self.default_api_client:
                        existing_webhooks = self.webhook_api.get_webhooks(async_req=False)
                        logger.debug(f"Found webhooks: {existing_webhooks}")
                        await self._handle_rate_limit()
                        
                        for webhook in existing_webhooks:
                            webhook_id = webhook.get('idWebhook')
                            webhook_url = webhook.get('urlCallback')
                            webhook_event = webhook.get('tipoEvento')
                            
                            logger.debug(f"Checking webhook: ID={webhook_id}, URL={webhook_url}, Event={webhook_event}")
                            
                            if webhook_id and webhook_url == url_callback and webhook_event in event_types:
                                success = await self._delete_webhook_with_retry(self.webhook_api, webhook_id)
                                if not success:
                                    continue  # Try next webhook
                return True

            # Handle subscribe
            if branch_ids:
                # Create webhooks for each branch and event type
                for branch_id in branch_ids:
                    logger.debug(f"Processing branch {branch_id}")
                    # Get branch-specific API client
                    if branch_id in self.branch_api_clients and self.branch_api_clients[branch_id]:
                        client = self.branch_api_clients[branch_id]
                        if client.configuration:
                            logger.debug(f"Using branch-specific client for branch {branch_id}")
                            logger.debug(f"Branch {branch_id} username: {client.configuration.username}")
                            webhook_api = WebhookApi(client)
                        else:
                            logger.warning(f"No configuration for branch {branch_id}, using default client")
                            webhook_api = WebhookApi(self.default_api_client) if self.default_api_client else None
                    else:
                        logger.warning(f"No credentials found for branch {branch_id}, using default client")
                        webhook_api = WebhookApi(self.default_api_client) if self.default_api_client else None

                    if webhook_api:
                        for event_type in event_types:
                            logger.debug(f"Creating webhook for branch {branch_id}, event {event_type}")
                            try:
                                success = webhook_api.create_webhook(
                                    event_type=event_type,
                                    url_callback=url_callback,
                                    branch_id=int(branch_id),
                                    headers=webhook_headers,
                                    filters=webhook_filters if event_type == "NewSale" else None,
                                    async_req=False
                                )
                                if not success:
                                    logger.error(f"Failed to create webhook for branch {branch_id}, event {event_type}")
                                    return False
                                logger.debug(f"Successfully created webhook for branch {branch_id}, event {event_type}")
                                await self._handle_rate_limit()
                            except Exception as e:
                                if "429" in str(e):  # Rate limit error
                                    logger.warning("Rate limit hit, retrying with longer delay")
                                    await self._handle_rate_limit(3.0)  # Longer delay on rate limit
                                    continue
                                logger.error(f"Error creating webhook: {str(e)}")
                                return False
            else:
                # Create webhooks for each event type without branch ID
                if self.default_api_client:
                    logger.debug("Using default client for webhook creation")
                    if self.default_api_client.configuration:
                        logger.debug(f"Default client username: {self.default_api_client.configuration.username}")
                    
                    for event_type in event_types:
                        logger.debug(f"Creating webhook for event {event_type}")
                        try:
                            success = self.webhook_api.create_webhook(
                                event_type=event_type,
                                url_callback=url_callback,
                                headers=webhook_headers,
                                filters=webhook_filters if event_type == "NewSale" else None,
                                async_req=False
                            )
                            if not success:
                                logger.error(f"Failed to create webhook for event {event_type}")
                                return False
                            logger.debug(f"Successfully created webhook for event {event_type}")
                            await self._handle_rate_limit()
                        except Exception as e:
                            if "429" in str(e):  # Rate limit error
                                logger.warning("Rate limit hit, retrying with longer delay")
                                await self._handle_rate_limit(3.0)  # Longer delay on rate limit
                                continue
                            logger.error(f"Error creating webhook: {str(e)}")
                            return False

            return True

        except Exception as e:
            logger.error(f"Error managing webhooks: {str(e)}")
            logger.exception("Full traceback:")
            return False