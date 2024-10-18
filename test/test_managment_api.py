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
from swagger_client.api.managment_api import ManagmentApi  # noqa: E501
from swagger_client.rest import ApiException


class TestManagmentApi(unittest.TestCase):
    """ManagmentApi unit test stubs"""

    def setUp(self):
        self.api = ManagmentApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_api_v1_managment_activeclients_get(self):
        """Test case for api_v1_managment_activeclients_get

        Get active Clients  # noqa: E501
        """
        pass

    def test_api_v1_managment_prospects_get(self):
        """Test case for api_v1_managment_prospects_get

        Get Prospects  # noqa: E501
        """
        pass

    def test_renewed_get(self):
        """Test case for renewed_get

        Get non-renewed Clients  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()