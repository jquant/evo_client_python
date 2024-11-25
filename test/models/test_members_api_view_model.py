# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

from datetime import datetime

import pytest

from evo_client.models.member_membership_api_view_model import (
    MemberMembershipApiViewModel,
)
from evo_client.models.member_responsible_view_model import MemberResponsibleViewModel
from evo_client.models.members_api_view_model import MembersApiViewModel
from evo_client.models.telefone_api_view_model import TelefoneApiViewModel


@pytest.fixture
def members_api_view_model():
    return MembersApiViewModel(
        idMember=1,
        firstName="John",
        lastName="Doe",
        registerDate=datetime(2023, 1, 1),
        idBranch=101,
        branchName="Main Branch",
        accessBlocked=False,
        gender="Male",
        birthDate=datetime(1990, 5, 20),
        accessCardNumber="1234567890",
        membershipStatus="Active",
        penalized=False,
        status="Active",
        contacts=[TelefoneApiViewModel(idPhone=123456789)],
        memberships=[MemberMembershipApiViewModel(idMembership=1)],
        lastAccessDate=datetime(2023, 10, 1),
        idEmployeeConsultant=201,
        nameEmployeeConsultant="Jane Smith",
        idEmployeeInstructor=202,
        nameEmployeeInstructor="Mike Johnson",
        idEmployeePersonalTrainer=203,
        nameEmployeePersonalTrainer="Emily Davis",
        photoUrl="https://example.com/photo.jpg",
        idMemberMigration="MIG123",
        responsibles=[MemberResponsibleViewModel()],
        gympassId="GYMPASS123",
        personalTrainer=True,
        personalType="TypeA",
    )


def test_members_api_view_model_creation(members_api_view_model):
    """Test creating a MembersApiViewModel instance"""
    model = members_api_view_model
    assert isinstance(model, MembersApiViewModel)
    assert model.id_member == 1
    assert model.first_name == "John"
    assert model.last_name == "Doe"
    assert model.register_date == datetime(2023, 1, 1)
    assert model.id_branch == 101
    assert model.branch_name == "Main Branch"
    assert model.access_blocked is False
    assert model.gender == "Male"
    assert model.birth_date == datetime(1990, 5, 20)
    assert model.access_card_number == "1234567890"
    assert model.membership_status == "Active"
    assert model.penalized is False
    assert model.status == "Active"
    assert model.contacts is not None
    assert model.memberships is not None
    assert model.last_access_date == datetime(2023, 10, 1)
    assert model.id_employee_consultant == 201
    assert model.name_employee_consultant == "Jane Smith"
    assert model.id_employee_instructor == 202
    assert model.name_employee_instructor == "Mike Johnson"
    assert model.id_employee_personal_trainer == 203
    assert model.name_employee_personal_trainer == "Emily Davis"
    assert model.photo_url == "https://example.com/photo.jpg"
    assert model.id_member_migration == "MIG123"
    assert model.responsibles is not None
    assert model.gympass_id == "GYMPASS123"
    assert model.personal_trainer is True
    assert model.personal_type == "TypeA"


def test_members_api_view_model_to_dict(members_api_view_model):
    """Test converting MembersApiViewModel to dictionary"""
    model_dict = members_api_view_model.to_dict()

    assert isinstance(model_dict, dict)
    assert model_dict["idMember"] == 1
    assert model_dict["firstName"] == "John"
    assert model_dict["lastName"] == "Doe"
    assert model_dict["registerDate"] == "2023-01-01T00:00:00"
    assert model_dict["idBranch"] == 101
    assert model_dict["branchName"] == "Main Branch"
    assert model_dict["accessBlocked"] is False
    assert model_dict["gender"] == "Male"
    assert model_dict["birthDate"] == "1990-05-20T00:00:00"
    assert model_dict["accessCardNumber"] == "1234567890"
    assert model_dict["membershipStatus"] == "Active"
    assert model_dict["penalized"] is False
    assert model_dict["status"] == "Active"
    assert model_dict["contacts"] is not None
    assert model_dict["memberships"] is not None
    assert model_dict["lastAccessDate"] == "2023-10-01T00:00:00"
    assert model_dict["idEmployeeConsultant"] == 201
    assert model_dict["nameEmployeeConsultant"] == "Jane Smith"
    assert model_dict["idEmployeeInstructor"] == 202
    assert model_dict["nameEmployeeInstructor"] == "Mike Johnson"
    assert model_dict["idEmployeePersonalTrainer"] == 203
    assert model_dict["nameEmployeePersonalTrainer"] == "Emily Davis"
    assert model_dict["photoUrl"] == "https://example.com/photo.jpg"
    assert model_dict["idMemberMigration"] == "MIG123"
    assert model_dict["responsibles"] is not None
    assert model_dict["gympassId"] == "GYMPASS123"
    assert model_dict["personalTrainer"] is True
    assert model_dict["personalType"] == "TypeA"


def test_members_api_view_model_equality(members_api_view_model):
    """Test equality comparison of MembersApiViewModel instances"""
    same_model = MembersApiViewModel(
        idMember=1,
        firstName="John",
        lastName="Doe",
        registerDate=datetime(2023, 1, 1),
        idBranch=101,
        branchName="Main Branch",
        accessBlocked=False,
        gender="Male",
        birthDate=datetime(1990, 5, 20),
        accessCardNumber="1234567890",
        membershipStatus="Active",
        penalized=False,
        status="Active",
        contacts=[TelefoneApiViewModel(idPhone=123456789)],
        memberships=[MemberMembershipApiViewModel(idMembership=1)],
        lastAccessDate=datetime(2023, 10, 1),
        idEmployeeConsultant=201,
        nameEmployeeConsultant="Jane Smith",
        idEmployeeInstructor=202,
        nameEmployeeInstructor="Mike Johnson",
        idEmployeePersonalTrainer=203,
        nameEmployeePersonalTrainer="Emily Davis",
        photoUrl="https://example.com/photo.jpg",
        idMemberMigration="MIG123",
        responsibles=[MemberResponsibleViewModel()],
        gympassId="GYMPASS123",
        personalTrainer=True,
        personalType="TypeA",
    )

    different_model = MembersApiViewModel(
        idMember=2,
        firstName="Jane",
        lastName="Smith",
        registerDate=datetime(2023, 2, 1),
        idBranch=102,
        branchName="Secondary Branch",
        accessBlocked=True,
        gender="Female",
        birthDate=datetime(1992, 6, 15),
        accessCardNumber="0987654321",
        membershipStatus="Inactive",
        penalized=True,
        status="Inactive",
        contacts=[TelefoneApiViewModel()],
        memberships=[MemberMembershipApiViewModel()],
        lastAccessDate=datetime(2023, 11, 1),
        idEmployeeConsultant=204,
        nameEmployeeConsultant="Michael Brown",
        idEmployeeInstructor=205,
        nameEmployeeInstructor="Sarah Wilson",
        idEmployeePersonalTrainer=206,
        nameEmployeePersonalTrainer="Chris Evans",
        photoUrl="https://example.com/photo2.jpg",
        idMemberMigration="MIG456",
        responsibles=[MemberResponsibleViewModel()],
        gympassId="GYMPASS456",
        personalTrainer=False,
        personalType="TypeB",
    )

    assert members_api_view_model == same_model
    assert members_api_view_model != different_model
    assert members_api_view_model != 1
