# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.activities_api import ActivitiesApi  # noqa: E501
from swagger_client.rest import ApiException


class TestActivitiesApi(unittest.TestCase):
    """ActivitiesApi unit test stubs"""

    def setUp(self):
        self.api = ActivitiesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_api_v1_activities_get(self):
        """Test case for api_v1_activities_get

        Get activities  # noqa: E501
        """
        pass

    def test_api_v1_activities_schedule_detail_get(self):
        """Test case for api_v1_activities_schedule_detail_get

        Get activities schedule details  # noqa: E501
        """
        pass

    def test_api_v1_activities_schedule_enroll_post(self):
        """Test case for api_v1_activities_schedule_enroll_post

        Enroll member in activity schedule  # noqa: E501
        """
        pass

    def test_api_v1_activities_schedule_get(self):
        """Test case for api_v1_activities_schedule_get

        Get activities schedule  # noqa: E501
        """
        pass

    def test_class_post(self):
        """Test case for class_post

        Create a new experimental class and enroll the member on it  # noqa: E501
        """
        pass

    def test_status_post(self):
        """Test case for status_post

        Change status of a member in activity schedule  # noqa: E501
        """
        pass

    def test_unavailable_spots_get(self):
        """Test case for unavailable_spots_get

        List of spots that are already filled in the activity session  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
