"""Tests for the GymApi class."""

from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, PropertyMock, patch

import pytest

from evo_client.api.gym_api import GymApi
from evo_client.exceptions.api_exceptions import ApiException
from evo_client.models.gym_model import (
    GymKnowledgeBase,
    GymOperatingData,
    GymPlan,
    MembershipCategory,
    MembershipContract,
    OverdueMember,
    Receivable,
    ReceivableStatus,
)


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("evo_client.api.gym_api.ApiClient") as mock:
        mock.call_api = Mock()
        yield mock


@pytest.fixture
def mock_membership_api():
    """Create a mock membership API."""
    with patch("evo_client.api.membership_api.MembershipApi") as mock:
        yield mock


@pytest.fixture
def mock_configuration_api():
    """Create a mock configuration API."""
    with patch("evo_client.api.configuration_api.ConfigurationApi") as mock:
        yield mock


@pytest.fixture
def mock_managment_api():
    """Create a mock managment API."""
    with patch("evo_client.api.managment_api.ManagementApi") as mock:
        yield mock


@pytest.fixture
def mock_prospects_api():
    """Create a mock prospects API."""
    with patch("evo_client.api.prospects_api.ProspectsApi") as mock:
        yield mock


@pytest.fixture
def mock_receivables_api():
    """Create a mock receivables API."""
    with patch("evo_client.api.receivables_api.ReceivablesApi") as mock:
        yield mock


@pytest.fixture
def mock_entries_api():
    """Create a mock entries API."""
    with patch("evo_client.api.entries_api.EntriesApi") as mock:
        mock.get_entries = Mock()
        mock.get_member_entries = Mock()
        mock.get_entry_by_id = Mock()
        yield mock


@pytest.fixture
def gym_api(
    mock_api_client,
    mock_membership_api,
    mock_configuration_api,
    mock_managment_api,
    mock_prospects_api,
    mock_receivables_api,
    mock_entries_api,
):
    """Create a GymApi instance for testing with mocked dependencies."""
    with patch(
        "evo_client.api.gym_api.MembershipApi", return_value=mock_membership_api
    ), patch(
        "evo_client.api.gym_api.ConfigurationApi", return_value=mock_configuration_api
    ), patch(
        "evo_client.api.gym_api.ManagementApi", return_value=mock_managment_api
    ), patch(
        "evo_client.api.gym_api.ProspectsApi", return_value=mock_prospects_api
    ), patch(
        "evo_client.api.gym_api.ReceivablesApi", return_value=mock_receivables_api
    ), patch(
        "evo_client.api.gym_api.EntriesApi", return_value=mock_entries_api
    ):
        return GymApi(api_client=mock_api_client())


def test_get_contracts_basic(gym_api: GymApi, mock_membership_api: Mock):
    """Test getting contracts with basic parameters."""
    # Mock data
    mock_membership = Mock()
    type(mock_membership).id_member_membership = PropertyMock(return_value=1)
    type(mock_membership).id_member = PropertyMock(return_value=100)
    type(mock_membership).name_membership = PropertyMock(return_value="Basic Plan")
    type(mock_membership).value_next_month = PropertyMock(return_value=99.99)
    type(mock_membership).id_category_membership = PropertyMock(return_value=1)
    type(mock_membership).description = PropertyMock(return_value="")
    type(mock_membership).differentials = PropertyMock(return_value=[])
    type(mock_membership).duration = PropertyMock(return_value=12)
    type(mock_membership).access_branches = PropertyMock(return_value=False)
    type(mock_membership).max_amount_installments = PropertyMock(return_value=1)
    type(mock_membership).inactive = PropertyMock(return_value=False)
    mock_membership_api.get_memberships.return_value = [mock_membership]

    # Call the method
    result = gym_api.get_contracts(async_req=False)

    # Verify the result
    assert isinstance(result, list)
    assert len(result) == 1
    contract = result[0]
    assert isinstance(contract, MembershipContract)
    assert contract.id == 1
    assert contract.member_id == 100
    assert isinstance(contract.plan, GymPlan)
    assert contract.plan.name == "Basic Plan"
    assert contract.plan.price == Decimal("99.99")
    assert isinstance(contract.category, MembershipCategory)
    assert contract.category.id == 1

    # Verify the mock was called correctly
    mock_membership_api.get_memberships.assert_called_once_with(
        id_membership=None,
        id_branch=None,
        active=True,
        take=50,
        skip=0,
        async_req=False,
    )


def test_get_contracts_with_member_id(gym_api: GymApi, mock_membership_api: Mock):
    """Test getting contracts for a specific member."""
    # Mock data
    mock_membership = Mock()
    type(mock_membership).id_member_membership = PropertyMock(return_value=1)
    type(mock_membership).id_member = PropertyMock(return_value=100)
    type(mock_membership).name_membership = PropertyMock(return_value="Premium Plan")
    type(mock_membership).value_next_month = PropertyMock(return_value=199.99)
    type(mock_membership).id_category_membership = PropertyMock(return_value=2)
    type(mock_membership).description = PropertyMock(return_value="")
    type(mock_membership).differentials = PropertyMock(return_value=[])
    type(mock_membership).duration = PropertyMock(return_value=12)
    type(mock_membership).access_branches = PropertyMock(return_value=False)
    type(mock_membership).max_amount_installments = PropertyMock(return_value=1)
    type(mock_membership).inactive = PropertyMock(return_value=False)
    mock_membership_api.get_memberships.return_value = [mock_membership]

    # Call the method
    result = gym_api.get_contracts(member_id=100, async_req=False)

    # Verify the result
    assert len(result) == 1
    contract = result[0]
    assert contract.member_id == 100
    assert contract.plan.name == "Premium Plan"

    # Verify the mock was called correctly
    mock_membership_api.get_memberships.assert_called_once_with(
        id_membership=100, id_branch=None, active=True, take=50, skip=0, async_req=False
    )


def test_get_contracts_empty(gym_api: GymApi, mock_membership_api: Mock):
    """Test getting contracts when no contracts exist."""
    mock_membership_api.get_memberships.return_value = []

    result = gym_api.get_contracts(async_req=False)

    assert isinstance(result, list)
    assert len(result) == 0

    # Verify the mock was called correctly
    mock_membership_api.get_memberships.assert_called_once_with(
        id_membership=None,
        id_branch=None,
        active=True,
        take=50,
        skip=0,
        async_req=False,
    )


def test_get_contracts_error_handling(gym_api: GymApi, mock_membership_api: Mock):
    """Test error handling when getting contracts."""
    mock_membership_api.get_memberships.side_effect = ApiException(
        status=404, reason="Not Found"
    )

    result = gym_api.get_contracts(async_req=False)

    assert isinstance(result, list)
    assert len(result) == 0

    # Verify the mock was called correctly
    mock_membership_api.get_memberships.assert_called_once_with(
        id_membership=None,
        id_branch=None,
        active=True,
        take=50,
        skip=0,
        async_req=False,
    )


def test_convert_receivable(gym_api: GymApi):
    """Test converting receivable model."""
    mock_receivable = Mock()
    type(mock_receivable).idReceivable = PropertyMock(return_value=1)
    type(mock_receivable).description = PropertyMock(return_value="Monthly fee")
    type(mock_receivable).ammount = PropertyMock(return_value=99.99)
    type(mock_receivable).ammountPaid = PropertyMock(return_value=50.00)
    type(mock_receivable).dueDate = PropertyMock(return_value=datetime.now())
    type(mock_receivable).receivingDate = PropertyMock(return_value=None)
    type(mock_receivable).status = PropertyMock(
        return_value=Mock(value=ReceivableStatus.PAID.value)
    )
    type(mock_receivable).idMemberPayer = PropertyMock(return_value=100)
    type(mock_receivable).payerName = PropertyMock(return_value="John Doe")
    type(mock_receivable).idBranchMember = PropertyMock(return_value=1)
    type(mock_receivable).currentInstallment = PropertyMock(return_value=1)
    type(mock_receivable).totalInstallments = PropertyMock(return_value=12)

    result = gym_api._convert_receivable(mock_receivable)

    assert isinstance(result, Receivable)
    assert result.id == 1
    assert result.description == "Monthly fee"
    assert result.amount == Decimal("99.99")
    assert result.amount_paid == Decimal("50.00")
    assert result.status == ReceivableStatus.PAID
    assert result.member_id == 100
    assert result.member_name == "John Doe"
    assert result.current_installment == 1
    assert result.total_installments == 12


def test_get_gym_knowledge_base(gym_api: GymApi, mock_configuration_api: Mock):
    """Test getting gym knowledge base."""
    # Mock configuration API
    mock_config = Mock()
    type(mock_config).id_branch = PropertyMock(return_value=1)
    type(mock_config).name = PropertyMock(return_value="Test Gym")
    type(mock_config).internal_name = PropertyMock(return_value="Test Gym")
    type(mock_config).cnpj = PropertyMock(return_value="12345678901234")
    type(mock_config).telephone = PropertyMock(return_value="123-456-7890")
    type(mock_config).address = PropertyMock(return_value="123 Main St")
    type(mock_config).number = PropertyMock(return_value="1")
    type(mock_config).neighborhood = PropertyMock(return_value="Downtown")
    type(mock_config).city = PropertyMock(return_value="Test City")
    type(mock_config).state = PropertyMock(return_value="TS")
    type(mock_config).zip_code = PropertyMock(return_value="12345")

    # Mock business hours
    mock_business_hour = Mock()
    type(mock_business_hour).id_hour = PropertyMock(return_value=1)
    type(mock_business_hour).id_branch = PropertyMock(return_value=1)
    type(mock_business_hour).week_day = PropertyMock(return_value="Monday")
    type(mock_business_hour).hours_from = PropertyMock(
        return_value=datetime(2024, 1, 1, 6, 0)
    )
    type(mock_business_hour).hours_to = PropertyMock(
        return_value=datetime(2024, 1, 1, 22, 0)
    )
    type(mock_business_hour).fl_deleted = PropertyMock(return_value=False)
    type(mock_business_hour).id_tmp = PropertyMock(return_value=None)
    type(mock_business_hour).creation_date = PropertyMock(return_value=None)
    type(mock_business_hour).id_employee_creation = PropertyMock(return_value=None)

    # Set business hours on config
    type(mock_config).business_hours = PropertyMock(return_value=[mock_business_hour])

    # Mock gateway config
    mock_gateway = Mock()
    type(mock_gateway).tipo_gateway = PropertyMock(return_value=Mock(value="PAGARME"))
    mock_configuration_api.get_gateway_config = Mock(return_value=mock_gateway)

    # Set up the mocks
    mock_configuration_api.get_branch_config = Mock(return_value=[mock_config])
    mock_configuration_api.get_business_hours = Mock(return_value=[mock_business_hour])

    # Call API
    result = gym_api.get_gym_knowledge_base(branch_id=1, async_req=False)

    # Verify response
    assert isinstance(result, GymKnowledgeBase)
    assert result.branch_config is not None
    assert result.branch_config.name == "Test Gym"
    assert result.branch_config.address is not None
    assert result.branch_config.address.street == "123 Main St"
    assert result.branch_config.address.number == "1"
    assert result.branch_config.address.neighborhood == "Downtown"
    assert result.branch_config.address.city == "Test City"
    assert result.branch_config.address.state == "TS"
    assert result.branch_config.address.postal_code == "12345"
    assert result.branch_config.address.country == "Brasil"
    assert result.branch_config.address.phone == "123-456-7890"

    # Verify business hours
    assert len(result.branch_config.business_hours) == 1
    business_hour = result.branch_config.business_hours[0]
    assert business_hour.week_day == "Monday"
    assert business_hour.hours_from == datetime(2024, 1, 1, 6, 0)
    assert business_hour.hours_to == datetime(2024, 1, 1, 22, 0)

    # Verify gateway config
    assert result.branch_config.gateway_config is not None
    assert result.branch_config.gateway_config.type == "PAGARME"


def test_get_operating_data(
    gym_api: GymApi,
    mock_managment_api: Mock,
    mock_membership_api: Mock,
    mock_prospects_api: Mock,
    mock_receivables_api: Mock,
    mock_entries_api: Mock,
):
    """Test getting gym operating data."""
    # Mock active members
    mock_member = Mock()
    type(mock_member).id = PropertyMock(return_value=1)
    type(mock_member).name = PropertyMock(return_value="John Doe")
    type(mock_member).to_dict = Mock(return_value={"id": 1, "name": "John Doe"})
    mock_managment_api.get_active_clients = Mock(return_value=[mock_member])

    # Mock active contracts
    mock_membership = Mock()
    type(mock_membership).id_member_membership = PropertyMock(return_value=1)
    type(mock_membership).id_member = PropertyMock(return_value=100)
    type(mock_membership).name_membership = PropertyMock(return_value="Basic Plan")
    type(mock_membership).value_next_month = PropertyMock(return_value=99.99)
    type(mock_membership).description = PropertyMock(return_value="")
    type(mock_membership).differentials = PropertyMock(return_value=[])
    type(mock_membership).duration = PropertyMock(return_value=12)
    type(mock_membership).access_branches = PropertyMock(return_value=False)
    type(mock_membership).max_amount_installments = PropertyMock(return_value=1)
    type(mock_membership).inactive = PropertyMock(return_value=False)
    type(mock_membership).id_category_membership = PropertyMock(return_value=1)
    mock_membership_api.get_memberships = Mock(return_value=[mock_membership])

    # Mock prospects
    mock_prospects_api.get_prospects = Mock(return_value=[])

    # Mock non-renewed members
    mock_managment_api.get_non_renewed_clients = Mock(return_value=[])

    # Mock receivables
    mock_receivables_api.get_receivables = Mock(return_value=[])

    # Mock entries
    mock_entries_api.get_entries = Mock(return_value=[])

    # Call API
    result = gym_api.get_operating_data(async_req=False)

    # Verify response
    assert isinstance(result, GymOperatingData)
    assert len(result.active_members) == 1
    assert result.active_members[0]["id"] == 1
    assert result.active_members[0]["name"] == "John Doe"
    assert len(result.active_contracts) == 1
    assert result.total_active_members == 1
    assert result.total_churned_members == 0
    assert result.mrr == Decimal("99.99")
    assert result.churn_rate == Decimal("0.00")


def test_get_overdue_members(gym_api: GymApi, mock_receivables_api: Mock):
    """Test getting overdue members."""
    # Mock receivables API
    mock_receivable = Mock()
    type(mock_receivable).idReceivable = PropertyMock(return_value=1)
    type(mock_receivable).description = PropertyMock(return_value="Monthly fee")
    type(mock_receivable).ammount = PropertyMock(return_value=199.99)
    type(mock_receivable).ammountPaid = PropertyMock(return_value=0.00)
    type(mock_receivable).dueDate = PropertyMock(return_value=datetime(2024, 1, 1))
    type(mock_receivable).receivingDate = PropertyMock(return_value=None)
    type(mock_receivable).status = PropertyMock(
        return_value=Mock(value=ReceivableStatus.OVERDUE.value)
    )
    type(mock_receivable).idMemberPayer = PropertyMock(return_value=100)
    type(mock_receivable).payerName = PropertyMock(return_value="John Doe")
    type(mock_receivable).idBranchMember = PropertyMock(return_value=1)
    type(mock_receivable).currentInstallment = PropertyMock(return_value=1)
    type(mock_receivable).totalInstallments = PropertyMock(return_value=12)
    mock_receivables_api.get_receivables = Mock(return_value=[mock_receivable])

    # Call API
    result = gym_api.get_overdue_members(async_req=False)

    # Verify response
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], OverdueMember)
    assert result[0].member_id == 100
    assert result[0].name == "John Doe"
    assert result[0].total_overdue == Decimal("199.99")
    assert result[0].overdue_since == datetime(2024, 1, 1)
    assert len(result[0].overdue_receivables) == 1
