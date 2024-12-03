from __future__ import absolute_import

from typing import List, Optional, Dict, Any, Union, cast, TypeVar, Generic, Literal, overload
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
    
    # Configuration models
    BranchConfig,
    Address,
    BusinessHours,
    PaymentPolicy,
    GatewayConfig,
    CardFlag,
    OccupationArea,
    FAQ,
    
    # Status enums
    ActivityStatus,
    MembershipStatus,
    EntryStatus,
    EntryType,
    
    # Receivables models
    Receivable,
    ReceivableStatus,
    OverdueMember,
    
    # Sales models
    PaymentMethod,
    CardData,
    Sale,
    NewSale,
)

# External API view models
from ..models.sales_view_model import SalesViewModel
from ..models.new_sale_view_model import NewSaleViewModel
from ..models.card_data_view_model import CardDataViewModel
from ..models.e_forma_pagamento_totem import EFormaPagamentoTotem
from ..models.sales_item_view_model import SalesItemViewModel
from ..models.w12_utils_category_membership_view_model import W12UtilsCategoryMembershipViewModel
from ..models.business_hours_view_model import BusinessHoursViewModel

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

from ..models.e_tipo_gateway import ETipoGateway

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
            is_active=category_data.get('is_active', True),
            features=category_data.get('features', []),
            restrictions=category_data.get('restrictions')
        )
    except Exception as e:
        print(f"Error converting category: {str(e)}")
        return None

class GymApi:
    """Gym API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        if api_client is None:
            configuration = Configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
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
        self._pool = Pool(processes=1)  # Single process pool for async operations

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, '_pool'):
            self._pool.close()
            self._pool.join()

    def _convert_receivable(self, receivable: Any) -> Receivable:
        """Convert SDK receivable model to our model."""
        status = ReceivableStatus.PENDING
        if receivable.status:
            if receivable.status.value == "1":  # Assuming 1 is paid
                status = ReceivableStatus.PAID
            elif receivable.status.value == "2":  # Assuming 2 is overdue
                status = ReceivableStatus.OVERDUE
            elif receivable.status.value == "3":  # Assuming 3 is cancelled
                status = ReceivableStatus.CANCELLED

        return Receivable(
            id=receivable.id_receivable or 0,
            description=receivable.description or "",
            amount=Decimal(str(receivable.ammount or 0)),
            amount_paid=Decimal(str(receivable.ammount_paid or 0)) if receivable.ammount_paid else None,
            due_date=receivable.due_date or datetime.now(),
            receiving_date=receivable.receiving_date,
            status=status,
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
        """
        Get membership contracts for a member or branch.
        
        Args:
            member_id: Optional ID of a specific member
            branch_id: Optional ID of a specific branch
            active_only: Whether to return only active contracts
            async_req: If True, returns AsyncResult
            
        Returns:
            List[MembershipContract]: List of membership contracts
        """
        try:
            # Get memberships using the membership API
            memberships_result = self.membership_api.get_memberships(
                branch_id=branch_id,
                active=active_only,
                async_req=True if async_req else False  # type: ignore
            )
            
            if isinstance(memberships_result, AsyncResult):
                def convert_result(result: Any) -> List[MembershipContract]:
                    if isinstance(result, list):
                        return self._convert_memberships_to_contracts(result, member_id)
                    return []

                async_result = create_async_result(
                    pool=self._pool,
                    callback=convert_result,
                    error_callback=lambda e: []
                )
                return cast(TypedAsyncResult[List[MembershipContract]], async_result)
            
            if memberships_result is None:
                return []
                
            return self._convert_memberships_to_contracts(memberships_result, member_id)
            
        except Exception as e:
            print(f"Error fetching contracts: {str(e)}")
            return []

    def _convert_memberships_to_contracts(self, memberships: List[Any], member_id: Optional[int] = None) -> List[MembershipContract]:
        """Convert SDK membership models to our contract models."""
        contracts = []
        for membership in memberships:
            try:
                category = _convert_category({
                    'id': membership.id_category_membership or 0,
                    'name': "Standard",  # Default value
                    'description': None,
                    'is_active': True,
                    'features': [],
                    'restrictions': None,
                })
                
                contract = MembershipContract(
                    idMemberMembership=membership.id_member_membership or 0,
                    idMember=membership.id_member or 0,
                    plan=GymPlan(
                        nameMembership=membership.name or "",
                        value=Decimal(str(membership.value_next_month or 0)),
                        description="",  # Not available in this model
                        features=[],  # Not available in this model
                        duration=1,  # Default value
                        enrollment_fee=None,
                        annual_fee=None,
                        cancellation_notice_days=30,
                        payment_methods=[PaymentMethod.CREDIT_CARD],
                        accessBranches=False,  # Not available in this model
                        category=category,
                        available_services=[],
                        maxAmountInstallments=1,  # Not available in this model
                        isActive=membership.membership_status == "Active"
                    ),
                    category=category,
                    status=MembershipStatus(membership.membership_status.lower()) if membership.membership_status else MembershipStatus.PENDING,
                    startDate=membership.start_date or datetime.now(),
                    endDate=membership.end_date,
                    lastRenewalDate=membership.sale_date,
                    nextRenewalDate=membership.next_charge,
                    paymentDay=membership.payment_day or 1,
                    isAutoRenewal=False,  # Not available in this model
                    totalValue=Decimal(str(membership.value_next_month or 0)),
                    installments=1,  # Not available in this model
                    idBranch=None  # Not available in this model
                )
                contracts.append(contract)
            except Exception as e:
                print(f"Error converting membership {membership}: {str(e)}")
                continue
        return contracts

    def get_gym_knowledge_base(
        self,
        branch_id: Optional[int] = None,
        include_activity_details: bool = False,
        async_req: bool = False
    ) -> Union[GymKnowledgeBase, TypedAsyncResult[GymKnowledgeBase]]:
        """
        Get complete knowledge base for a gym chain or specific branch by aggregating data from various APIs
        
        Args:
            branch_id: Optional ID of a specific branch
            include_activity_details: Whether to include detailed activity information (schedules, spots, etc.)
            async_req: If True, returns AsyncResult
            
        Returns:
            GymKnowledgeBase: Complete knowledge base including locations, plans, and policies
        """
        try:
            # Get basic configuration
            logger.info(f"Fetching gym configuration for branch_id={branch_id}")
            config_result = self.configuration_api.get_branch_config(
                async_req=True if async_req else False  # type: ignore
            )

            # Handle async result
            if isinstance(config_result, AsyncResult):
                logger.debug("Got async result, waiting for completion...")
                config_result = config_result.get()

            # Extract configuration from response
            config = None
            try:
                # Log the raw response for debugging
                logger.debug(f"Raw API response: {config_result}")
                logger.debug(f"Response type: {type(config_result)}")

                # If it's a list, extract the first item or matching branch
                if isinstance(config_result, list):
                    logger.info(f"Got list response with {len(config_result)} items")
                    if branch_id is not None:
                        logger.debug(f"Looking for branch_id={branch_id} in response")
                        config = next(
                            (cfg for cfg in config_result if getattr(cfg, 'id_branch', None) == branch_id),
                            config_result[0] if config_result else None
                        )
                        if config:
                            logger.info(f"Found matching branch configuration for branch_id={branch_id}")
                        else:
                            logger.warning(f"Branch {branch_id} not found, using first available")
                    else:
                        logger.info("No branch_id specified, using first configuration")
                        config = config_result[0] if config_result else None
                else:
                    # If it's a single item, use it directly
                    logger.info("Got single item response")
                    config = config_result

                if config:
                    logger.debug(f"Selected configuration: id_branch={getattr(config, 'id_branch', None)}, name={getattr(config, 'name', None)}")
                else:
                    logger.warning("No valid configuration found")

            except Exception as e:
                logger.error(f"Error processing configuration: {str(e)}")
                config = None

            if config is None:
                logger.warning("Creating empty knowledge base due to missing configuration")
                return self._create_empty_knowledge_base()

            # Create knowledge base from the selected configuration
            logger.info("Creating knowledge base from configuration")
            gym_kb = self._create_knowledge_base(config, branch_id, async_req)

            # Populate additional data if not async
            if not async_req:
                logger.info("Populating additional data")
                gym_kb = self._populate_activities(gym_kb, branch_id, include_activity_details)
                gym_kb = self._populate_memberships(gym_kb, branch_id)
                gym_kb = self._populate_gateway_config(gym_kb)
                gym_kb = self._populate_occupations(gym_kb)

            logger.info("Successfully created gym knowledge base")
            return gym_kb
            
        except Exception as e:
            logger.exception(f"Error fetching complete gym knowledge base: {str(e)}")
            return self._create_empty_knowledge_base()

    def _create_empty_knowledge_base(self) -> GymKnowledgeBase:
        """Create an empty knowledge base with default values."""
        return GymKnowledgeBase(
            name="Unknown",
            addresses=[],
            business_hours=[],
            activities=[],
            plans=[],
            faqs=[],
            membership_categories=[],
            available_services=[],
            payment_policy=PaymentPolicy(
                active_member_discount=30,
                inactive_member_discount=50,
                accepted_payment_methods=[
                    PaymentMethod.CREDIT_CARD,
                    PaymentMethod.DEBIT_CARD,
                    PaymentMethod.PIX
                ],
                pix_key=None,
                installment_available=True,
                cancellation_fee_percentage=10
            )
        )

    def _create_knowledge_base(self, config: Any, branch_id: Optional[int] = None, async_req: bool = False) -> GymKnowledgeBase:
        """Create a knowledge base from configuration data."""
        # Handle business hours
        business_hours = config.business_hours
        if isinstance(business_hours, AsyncResult):
            business_hours = business_hours.get()
        if not isinstance(business_hours, list):
            business_hours = []

        gym_kb = GymKnowledgeBase(
            name=config.name or "",
            addresses=[
                Address(
                    street=config.address or "",
                    number=config.number or "",
                    neighborhood=config.neighborhood or "",
                    city=config.city or "",
                    state=config.state or "",
                    postal_code=config.zip_code or "",
                    country="Brasil",  # Default for this SDK
                    phone=config.telephone or ""
                )
            ],
            business_hours=[
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
            membership_categories=[],  # Will be populated later
            available_services=[],  # Will be populated later
            payment_policy=PaymentPolicy(
                active_member_discount=30,  # Default values since not in SDK
                inactive_member_discount=50,
                accepted_payment_methods=[
                    PaymentMethod.CREDIT_CARD,
                    PaymentMethod.DEBIT_CARD,
                    PaymentMethod.PIX
                ],
                pix_key=None,
                installment_available=True,
                cancellation_fee_percentage=10
            ),
            branch_config=BranchConfig(
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
                    postal_code=config.zip_code or "",
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
                translations={}  # Default empty translations
            )
        )

        # Populate additional data if not async
        if not async_req:
            gym_kb = self._populate_activities(gym_kb, branch_id)
            gym_kb = self._populate_memberships(gym_kb, branch_id)
            gym_kb = self._populate_gateway_config(gym_kb)
            gym_kb = self._populate_occupations(gym_kb)
        
        return gym_kb

    def _populate_activities(self, gym_kb: GymKnowledgeBase, branch_id: Optional[int] = None, include_details: bool = False) -> GymKnowledgeBase:
        """Populate activities data in the knowledge base."""
        try:
            # Get basic activity list
            activities_result = self.activities_api.get_activities(branch_id=branch_id)
            employees_result = self.employees_api.get_employees()

            # Handle async results
            activities = activities_result.get() if isinstance(activities_result, AsyncResult) else activities_result
            employees = employees_result.get() if isinstance(employees_result, AsyncResult) else employees_result

            if not isinstance(activities, list) or not isinstance(employees, list):
                return gym_kb

            # Get schedule for all activities if details are requested
            schedule_result = None
            activity_schedules = {}
            if include_details:
                schedule_result = self.activities_api.get_schedule(
                    branch_id=branch_id,
                    date=datetime.now(),
                    show_full_week=True
                )
                schedule = schedule_result.get() if isinstance(schedule_result, AsyncResult) else schedule_result

                # Create a mapping of activity schedules by activity ID
                if isinstance(schedule, list):
                    for session in schedule:
                        # Access id_activity through model fields
                        activity_id = getattr(session, 'id_activity', None)
                        if activity_id is not None:
                            if activity_id not in activity_schedules:
                                activity_schedules[activity_id] = []
                            activity_schedules[activity_id].append(session)

            # Create activities with enhanced information
            gym_kb.activities = [
                Activity(
                    id=act.id_activity or 0,
                    name=act.name or "",
                    description=act.description or "",
                    max_capacity=act.total_records or 0,
                    requires_reservation=True,  # Default to requiring reservation
                    duration_minutes=60,  # Default duration since not in API model
                    instructor=next(
                        (emp.name for emp in employees if emp.id_employee == act.id_activity),
                        None
                    ),
                    schedule=activity_schedules.get(act.id_activity, {}) if include_details else {},
                    status=ActivityStatus.AVAILABLE,  # Default to available
                    photo=act.photo,  # Add photo if available
                    color=act.color,  # Add color if available
                    activity_group=act.activity_group,  # Add group if available
                    show_on_mobile=act.show_on_mobile,  # Add mobile visibility
                    show_on_website=act.show_on_website,  # Add website visibility
                    audience=[  # Add audience information
                        str(audience.nome)  # Convert to string to handle None values
                        for audience in (act.audience or [])
                        if hasattr(audience, 'nome') and audience.nome is not None
                    ],
                    session_details=activity_schedules.get(act.id_activity, []) if include_details else []
                ) for act in activities
            ]
        except Exception as e:
            logger.exception(f"Error populating activities: {str(e)}")
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
                    id=cat.id_category_membership or 0,
                    name=cat.name or "Standard",
                    description="",  # Default empty description
                    is_active=True,  # Default to active
                    features=[],  # Default empty features
                    restrictions=None  # Default no restrictions
                ) for cat in categories
            ]

            # Create a mapping of category names to categories for easy lookup
            category_map = {cat.name.lower(): cat for cat in gym_kb.membership_categories}

            # Then populate plans with their categories
            gym_kb.plans = [
                GymPlan(
                    nameMembership=plan.name_membership or "",
                    value=Decimal(str(plan.value or 0)),
                    description=plan.description or "",
                    features=[d.title for d in (plan.differentials or []) if d.title],
                    duration=plan.duration or 1,
                    enrollment_fee=None,
                    annual_fee=None,
                    cancellation_notice_days=plan.min_period_stay_membership or 30,
                    payment_methods=[PaymentMethod.CREDIT_CARD],
                    accessBranches=bool(plan.access_branches),
                    category=category_map.get((plan.membership_type or "").lower(), MembershipCategory(
                        id=0,
                        name="Standard",
                        description="",
                        is_active=True,
                        features=[],
                        restrictions=None
                    )),
                    available_services=[],
                    maxAmountInstallments=plan.max_amount_installments or 1,
                    isActive=not plan.inactive
                ) for plan in memberships
            ]

            # Finally, populate available services
            gym_kb.available_services = [
                MembershipService(
                    id=service.id_service or 0,
                    name=service.name_service or "",
                    description=service.online_sales_observations or "",
                    price=Decimal(str(service.value or 0)),
                    is_recurring=False,  # Not available in API model
                    duration_days=30  # Default value
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
                        merchant_id="",  # Not available in API model
                        merchant_key="",  # Not available in API model
                        is_active=True,  # Default to active
                        accepted_flags=flags
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
                        is_active=True  # Not available in SDK model
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
                memberId=member_id,
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
        member_map: Dict[int, List[Receivable]] = {}
        overdue_members: List[OverdueMember] = []

        # Group receivables by member
        for receivable in receivables:
            if receivable.member_id:
                if receivable.member_id not in member_map:
                    member_map[receivable.member_id] = []
                member_map[receivable.member_id].append(receivable)

        # Create OverdueMember objects
        for member_id, member_receivables in member_map.items():
            # Sort receivables by due date
            member_receivables.sort(key=lambda r: r.due_date)
            
            # Calculate total overdue amount
            total_overdue = sum((r.amount - (r.amount_paid or Decimal(0))) for r in member_receivables)
            
            # Get the earliest overdue date
            overdue_since = member_receivables[0].due_date if member_receivables else datetime.now()
            
            # Get the last payment date
            last_payment = None
            for r in reversed(member_receivables):
                if r.receiving_date:
                    last_payment = r.receiving_date
                    break
            
            overdue_members.append(OverdueMember(
                id=member_id,
                member_id=member_id,
                name=member_receivables[0].member_name or "Unknown",
                branch_id=member_receivables[0].branch_id,
                total_overdue=Decimal(str(total_overdue or 0)),
                overdue_since=overdue_since,
                last_payment_date=last_payment,
                overdue_receivables=member_receivables
            ))
        
        # Sort by total overdue amount descending
        overdue_members.sort(key=lambda m: m.total_overdue, reverse=True)
        return overdue_members

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
        branch_id: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> GymOperatingData:
        ...

    @overload
    def get_operating_data(
        self,
        branch_id: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> TypedAsyncResult[GymOperatingData]:
        ...

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

    def _aggregate_operating_data(
        self,
        results: List[Any],
        from_date: Optional[datetime],
        to_date: Optional[datetime]
    ) -> GymOperatingData:
        """Aggregate async results into a single GymOperatingData object."""
        operating_data = GymOperatingData(
            data_from=from_date,
            data_to=to_date
        )
        
        try:
            # Unpack results in the same order they were requested
            active_members, contracts, prospects, non_renewed, receivables, entries = results
            
            if active_members:
                operating_data.active_members = [m.to_dict() for m in active_members]
            
            if contracts:
                operating_data.active_contracts = contracts
            
            if prospects:
                operating_data.prospects = [p.to_dict() for p in prospects]
            
            if non_renewed:
                operating_data.non_renewed_members = [m.to_dict() for m in non_renewed]
            
            if receivables:
                operating_data.receivables = [self._convert_receivable(r) for r in receivables]
            
            if entries:
                operating_data.recent_entries = [self._convert_entry(e) for e in entries]
            
            # Calculate metrics after all data is aggregated
            operating_data.calculate_metrics()
                
        except Exception as e:
            logger.error(f"Error aggregating operating data: {str(e)}")
            
        return operating_data

    def get_operating_data(
        self,
        branch_id: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[GymOperatingData, TypedAsyncResult[GymOperatingData]]:
        """
        Get operational data for a gym branch.
        
        This method aggregates various operational data like active members,
        prospects, receivables, etc. into a single GymOperatingData object.
        It also calculates key metrics like MRR and Churn Rate for the period.
        
        Args:
            branch_id: Optional ID of a specific branch
            from_date: Optional start date for time-based data
            to_date: Optional end date for time-based data
            async_req: If True, returns AsyncResult
            
        Returns:
            GymOperatingData: Aggregated operational data with calculated metrics,
                            or AsyncResult if async_req=True
        """
        try:
            if async_req:
                # Start all async requests
                results = [
                    self.management_api.get_active_clients(async_req=True),
                    self.get_contracts(branch_id=branch_id, active_only=True, async_req=True),
                    self.management_api.get_prospects(
                        dt_start=from_date,
                        dt_end=to_date,
                        async_req=True
                    ),
                    self.management_api.get_non_renewed_clients(
                        dt_start=from_date,
                        dt_end=to_date,
                        async_req=True
                    ),
                    self.receivables_api.get_receivables(
                        registration_date_start=from_date,
                        registration_date_end=to_date,
                        take=50,
                        skip=0,
                        async_req=True
                    ),
                    self.entries_api.get_entries(
                        register_date_start=from_date,
                        register_date_end=to_date,
                        take=1000,
                        skip=0,
                        entry_id=None,
                        member_id=None,
                        async_req=True
                    )
                ]
                
                # Create async result that will aggregate all data
                async_result = create_async_result(
                    pool=self._pool,
                    callback=lambda _: self._aggregate_operating_data([r.get() for r in results], from_date, to_date),
                    error_callback=lambda e: GymOperatingData(data_from=from_date, data_to=to_date)
                )
                
                return cast(TypedAsyncResult[GymOperatingData], async_result)
            
            # Synchronous execution
            operating_data = GymOperatingData(
                data_from=from_date,
                data_to=to_date
            )
            
            # Get active members and contracts
            active_members = self.management_api.get_active_clients(async_req=False)
            if active_members:
                operating_data.active_members = [m.to_dict() for m in active_members]
            
            contracts = self.get_contracts(branch_id=branch_id, active_only=True, async_req=False)
            if contracts:
                operating_data.active_contracts = contracts
            
            # Get prospects and non-renewed members
            prospects = self.management_api.get_prospects(
                dt_start=from_date,
                dt_end=to_date,
                async_req=False
            )
            if prospects:
                operating_data.prospects = [p.to_dict() for p in prospects]
            
            non_renewed = self.management_api.get_non_renewed_clients(
                dt_start=from_date,
                dt_end=to_date,
                async_req=False
            )
            if non_renewed:
                operating_data.non_renewed_members = [m.to_dict() for m in non_renewed]
            
            # Get receivables and overdue members
            receivables = self.receivables_api.get_receivables(
                registration_date_start=from_date,
                registration_date_end=to_date,
                take=50,
                skip=0,
                async_req=False
            )
            if receivables:
                operating_data.receivables = [self._convert_receivable(r) for r in receivables]
            
            # Get recent entries
            entries = self.entries_api.get_entries(
                register_date_start=from_date,
                register_date_end=to_date,
                take=1000,
                skip=0,
                entry_id=None,
                member_id=None,
                async_req=False
            )
            if entries:
                operating_data.recent_entries = [self._convert_entry(e) for e in entries]
            
            # Calculate metrics after all data is loaded
            operating_data.calculate_metrics()
            
            return operating_data
            
        except Exception as e:
            logger.error(f"Error fetching operating data: {str(e)}")
            return GymOperatingData(data_from=from_date, data_to=to_date)

    @overload
    def get_members_files(
        self,
        member_ids: List[int],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> MembersFiles:
        ...

    @overload
    def get_members_files(
        self,
        member_ids: List[int],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> TypedAsyncResult[MembersFiles]:
        ...

    def get_members_files(
        self,
        member_ids: List[int],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[MembersFiles, TypedAsyncResult[MembersFiles]]:
        """
        Get comprehensive data about specified members.
        
        This method fetches all available data about the specified members,
        including their complete history of interactions with the gym.
        
        Args:
            member_ids: List of member IDs to analyze
            from_date: Optional start date for historical data
            to_date: Optional end date for historical data
            async_req: If True, returns AsyncResult
            
        Returns:
            MembersFiles: Comprehensive member data and metrics,
                         or AsyncResult if async_req=True
        """
        try:
            members_files = MembersFiles(
                member_ids=member_ids,
                data_from=from_date,
                data_to=to_date
            )
            
            if async_req:
                # Start all async requests for each member
                async_results = []
                for member_id in member_ids:
                    # Basic member info
                    async_results.append(self.members_api.get_member_profile(
                        id_member=member_id,
                        async_req=True
                    ))
                    
                    # Contracts
                    async_results.append(self.get_contracts(
                        member_id=member_id,
                        active_only=False,
                        async_req=True
                    ))
                    
                    # Entries
                    async_results.append(self.entries_api.get_entries(
                        register_date_start=from_date,
                        register_date_end=to_date,
                        member_id=member_id,
                        async_req=True
                    ))
                    
                    # Receivables
                    async_results.append(self.receivables_api.get_receivables(
                        member_id=member_id,
                        registration_date_start=from_date,
                        registration_date_end=to_date,
                        async_req=True
                    ))
                    
                    # Activity sessions
                    async_results.append(self.activities_api.get_schedule(
                        member_id=member_id,
                        date=from_date,
                        show_full_week=True,
                        async_req=True
                    ))
                
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
            for member_id in member_ids:
                # Get member profile
                member = self.members_api.get_member_profile(
                    id_member=member_id,
                    async_req=False
                )
                
                if member:
                    profile = self._create_member_profile(member)
                    
                    # Get contracts
                    contracts = self.get_contracts(
                        member_id=member_id,
                        active_only=False,
                        async_req=False
                    )
                    if contracts:
                        profile.contracts_history = contracts
                        # Find current contract
                        active_contracts = [c for c in contracts if c.status == MembershipStatus.ACTIVE]
                        if active_contracts:
                            profile.current_contract = active_contracts[0]
                            profile.is_active = True
                    
                    # Get entries
                    entries = self.entries_api.get_entries(
                        register_date_start=from_date,
                        register_date_end=to_date,
                        member_id=member_id,
                        async_req=False
                    )
                    if entries:
                        profile.entries_history = [self._convert_entry(e) for e in entries]
                        profile.total_entries = len(profile.entries_history)
                        if profile.entries_history:
                            profile.last_entry = profile.entries_history[-1]
                    
                    # Get receivables
                    receivables = self.receivables_api.get_receivables(
                        member_id=member_id,
                        registration_date_start=from_date,
                        registration_date_end=to_date,
                        async_req=False
                    )
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
                    
                    # Get activity sessions
                    sessions = self.activities_api.get_schedule(
                        member_id=member_id,
                        date=from_date,
                        show_full_week=True,
                        async_req=False
                    )
                    if sessions:
                        profile.total_classes_attended = len(sessions)
                        # Track favorite activities
                        activity_counts: Dict[str, int] = {}
                        for session in sessions:
                            activity_name = getattr(session, 'activity_name', None)
                            if activity_name:
                                activity_counts[activity_name] = activity_counts.get(activity_name, 0) + 1
                        profile.favorite_activities = sorted(
                            activity_counts.keys(),
                            key=lambda x: activity_counts[x],
                            reverse=True
                        )[:5]  # Top 5 activities
                    
                    # Build timeline
                    self._build_member_timeline(profile)
                    
                    # Add profile to collection
                    members_files.add_member(profile)
            
            return members_files
            
        except Exception as e:
            logger.error(f"Error fetching members files: {str(e)}")
            return members_files

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