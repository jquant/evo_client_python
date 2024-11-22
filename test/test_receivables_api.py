# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import evo_client
from evo_client.api.receivables_api import ReceivablesApi  # noqa: E501
from evo_client.rest import ApiException


class TestReceivablesApi(unittest.TestCase):
    """ReceivablesApi unit test stubs"""

    def setUp(self):
        self.api = ReceivablesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_api_v1_receivables_get(self):
        """Test case for api_v1_receivables_get

        Get receivables  # noqa: E501
        """
        pass

    def test_api_v1_revenuecenter_get(self):
        """Test case for api_v1_revenuecenter_get

        Get Cost Center  # noqa: E501
        """
        pass

    def test_received_put(self):
        """Test case for received_put"""
        pass


if __name__ == "__main__":
    unittest.main()
