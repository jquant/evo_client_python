"""Tests for MemberDataFetcher."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from src.evo_client.models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from src.evo_client.models.members_api_view_model import MembersApiViewModel
from src.evo_client.services.data_fetchers import (
    BaseDataFetcher,
    BranchApiClientManager,
)
from src.evo_client.services.data_fetchers.member_data_fetcher import MemberDataFetcher


class TestMemberDataFetcher:
    """Test suite for MemberDataFetcher class."""

    @pytest.fixture
    def mock_client_manager(self):
        """Create a mock client manager for testing."""
        mock_manager = Mock(spec=BranchApiClientManager)
        mock_manager.branch_api_clients = {"1": Mock(), "2": Mock(), "3": Mock()}
        mock_manager.branch_ids = [1, 2, 3]
        return mock_manager

    @pytest.fixture
    def member_fetcher(self, mock_client_manager):
        """Create a MemberDataFetcher instance for testing."""
        return MemberDataFetcher(mock_client_manager)

    def test_inheritance(self, member_fetcher):
        """Test that MemberDataFetcher inherits from BaseDataFetcher."""
        assert isinstance(member_fetcher, BaseDataFetcher)

    def test_fetch_member_by_id_success_specific_branch(
        self, member_fetcher, mock_client_manager
    ):
        """Test successful fetch of member by ID from specific branch."""
        # Setup mock data
        member_id = "12345"
        branch_id = 1
        expected_member = ClienteDetalhesBasicosApiViewModel(
            idMember=12345,
            firstName="Test",
            lastName="Member",
            email="test@example.com",
        )

        # Mock the API client and method
        mock_api_client = Mock()
        mock_members_api = Mock()
        mock_members_api.get_member_profile.return_value = expected_member

        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_sync_api.return_value = mock_members_api
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1, 2, 3])

            result = member_fetcher.fetch_member_by_id(member_id, branch_id)

        assert result == expected_member
        mock_members_api.get_member_profile.assert_called_once_with(id_member=12345)

    def test_fetch_member_by_id_search_all_branches(
        self, member_fetcher, mock_client_manager
    ):
        """Test fetching member by ID when searching across all branches."""
        member_id = "12345"
        expected_member = ClienteDetalhesBasicosApiViewModel(
            idMember=12345,
            firstName="Test",
            lastName="Member",
            email="test@example.com",
        )

        # Mock API to return None for first branch, member for second branch
        mock_api_client = Mock()
        mock_members_api_1 = Mock()
        mock_members_api_1.get_member_profile.return_value = None
        mock_members_api_2 = Mock()
        mock_members_api_2.get_member_profile.return_value = expected_member

        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_sync_api.side_effect = [mock_members_api_1, mock_members_api_2]
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1, 2])

            result = member_fetcher.fetch_member_by_id(member_id)

        assert result == expected_member
        assert mock_members_api_1.get_member_profile.call_count == 1
        assert mock_members_api_2.get_member_profile.call_count == 1

    def test_fetch_member_by_id_not_found(self, member_fetcher, mock_client_manager):
        """Test fetch member by ID when member is not found in any branch."""
        member_id = "99999"

        mock_api_client = Mock()
        mock_members_api = Mock()
        mock_members_api.get_member_profile.return_value = None

        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_sync_api.return_value = mock_members_api
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1, 2])

            result = member_fetcher.fetch_member_by_id(member_id)

        assert result is None

    def test_fetch_member_by_id_exception_handling(
        self, member_fetcher, mock_client_manager
    ):
        """Test exception handling in fetch_member_by_id."""
        member_id = "12345"

        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_sync_api.side_effect = Exception("API Error")
            member_fetcher.get_branch_api = Mock(return_value=Mock())
            member_fetcher.get_available_branch_ids = Mock(return_value=[1])

            with patch(
                "src.evo_client.services.data_fetchers.member_data_fetcher.logger"
            ) as mock_logger:
                with pytest.raises(ValueError) as exc_info:
                    member_fetcher.fetch_member_by_id(member_id)

                assert f"Error fetching member {member_id}" in str(exc_info.value)
                mock_logger.error.assert_called()

    def test_fetch_member_by_id_branch_exception_warning(
        self, member_fetcher, mock_client_manager
    ):
        """Test that exceptions from individual branches are logged as warnings."""
        member_id = "12345"
        expected_member = ClienteDetalhesBasicosApiViewModel(
            idMember=12345,
            firstName="Test",
            lastName="Member",
            email="test@example.com",
        )

        # First branch throws exception, second returns member
        mock_api_client = Mock()
        mock_members_api_1 = Mock()
        mock_members_api_1.get_member_profile.side_effect = Exception("Branch 1 error")
        mock_members_api_2 = Mock()
        mock_members_api_2.get_member_profile.return_value = expected_member

        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api, patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.logger"
        ) as mock_logger:
            mock_sync_api.side_effect = [mock_members_api_1, mock_members_api_2]
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1, 2])

            result = member_fetcher.fetch_member_by_id(member_id)

        assert result == expected_member
        mock_logger.warning.assert_called_once()

    def test_fetch_members_success(self, member_fetcher, mock_client_manager):
        """Test successful fetch of members with filters."""
        # Setup test data
        member1 = MembersApiViewModel(idMember=1, firstName="Member", lastName="1")
        member2 = MembersApiViewModel(idMember=2, firstName="Member", lastName="2")
        member3 = MembersApiViewModel(idMember=3, firstName="Member", lastName="3")

        # Mock paginated API call to return different members for each branch
        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.paginated_api_call"
        ) as mock_paginated, patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_paginated.side_effect = [
                [member1],  # Branch 1
                [member2],  # Branch 2
                [member3],  # Branch 3
            ]

            mock_api_client = Mock()
            mock_members_api = Mock()
            mock_sync_api.return_value = mock_members_api
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1, 2, 3])

            # Call with some filters
            result = member_fetcher.fetch_members(
                name="Test", email="test@example.com", status=1
            )

        assert len(result) == 3
        assert member1 in result
        assert member2 in result
        assert member3 in result

        # Verify paginated_api_call was called for each branch
        assert mock_paginated.call_count == 3

    def test_fetch_members_all_parameters(self, member_fetcher, mock_client_manager):
        """Test fetch_members with all possible parameters."""
        test_datetime = datetime(2023, 1, 1)

        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.paginated_api_call"
        ) as mock_paginated, patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_paginated.return_value = []
            mock_api_client = Mock()
            mock_members_api = Mock()
            mock_sync_api.return_value = mock_members_api
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1])

            # Call with all parameters
            result = member_fetcher.fetch_members(
                name="Test Name",
                email="test@example.com",
                document="123456789",
                phone="555-1234",
                conversion_date_start=test_datetime,
                conversion_date_end=test_datetime,
                register_date_start=test_datetime,
                register_date_end=test_datetime,
                membership_start_date_start=test_datetime,
                membership_start_date_end=test_datetime,
                membership_cancel_date_start=test_datetime,
                membership_cancel_date_end=test_datetime,
                status=1,
                token_gympass="token123",
                ids_members="1,2,3",
                only_personal=True,
                personal_type=1,
                show_activity_data=True,
            )

        # Verify all parameters were passed to paginated_api_call
        mock_paginated.assert_called_with(
            api_func=mock_members_api.get_members,
            branch_id="1",
            name="Test Name",
            email="test@example.com",
            document="123456789",
            phone="555-1234",
            conversion_date_start=test_datetime,
            conversion_date_end=test_datetime,
            register_date_start=test_datetime,
            register_date_end=test_datetime,
            membership_start_date_start=test_datetime,
            membership_start_date_end=test_datetime,
            membership_cancel_date_start=test_datetime,
            membership_cancel_date_end=test_datetime,
            status=1,
            token_gympass="token123",
            ids_members="1,2,3",
            only_personal=True,
            personal_type=1,
            show_activity_data=True,
        )

    def test_fetch_members_no_branches(self, member_fetcher, mock_client_manager):
        """Test fetch_members when no branches are available."""
        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.paginated_api_call"
        ) as mock_paginated:
            member_fetcher.get_available_branch_ids = Mock(return_value=[])

            result = member_fetcher.fetch_members()

        assert result == []
        mock_paginated.assert_not_called()

    def test_fetch_members_exception_handling(
        self, member_fetcher, mock_client_manager
    ):
        """Test exception handling in fetch_members."""
        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.paginated_api_call"
        ) as mock_paginated, patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_paginated.side_effect = Exception("Pagination error")
            mock_api_client = Mock()
            mock_members_api = Mock()
            mock_sync_api.return_value = mock_members_api
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1])

            with patch(
                "src.evo_client.services.data_fetchers.member_data_fetcher.logger"
            ) as mock_logger:
                with pytest.raises(ValueError) as exc_info:
                    member_fetcher.fetch_members()

                assert "Error fetching members" in str(exc_info.value)
                mock_logger.error.assert_called()

    def test_fetch_members_none_api_client(self, member_fetcher, mock_client_manager):
        """Test fetch_members when API client is None for a branch."""
        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.paginated_api_call"
        ) as mock_paginated, patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_sync_api.return_value = None  # Simulate None API client
            member_fetcher.get_branch_api = Mock(return_value=Mock())
            member_fetcher.get_available_branch_ids = Mock(return_value=[1])

            result = member_fetcher.fetch_members()

        # Should return empty list when no valid API clients
        assert result == []
        mock_paginated.assert_not_called()

    def test_fetch_members_empty_results(self, member_fetcher, mock_client_manager):
        """Test fetch_members when paginated_api_call returns empty results."""
        with patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.paginated_api_call"
        ) as mock_paginated, patch(
            "src.evo_client.services.data_fetchers.member_data_fetcher.SyncMembersApi"
        ) as mock_sync_api:
            mock_paginated.return_value = []
            mock_api_client = Mock()
            mock_members_api = Mock()
            mock_sync_api.return_value = mock_members_api
            member_fetcher.get_branch_api = Mock(return_value=mock_api_client)
            member_fetcher.get_available_branch_ids = Mock(return_value=[1, 2])

            result = member_fetcher.fetch_members()

        assert result == []
        assert mock_paginated.call_count == 2  # Called for both branches
