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
from swagger_client.api.invoices_api import InvoicesApi  # noqa: E501
from swagger_client.rest import ApiException


class TestInvoicesApi(unittest.TestCase):
    """InvoicesApi unit test stubs"""

    def setUp(self):
        self.api = InvoicesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_invoices_get(self):
        """Test case for invoices_get

        Get invoices by date  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()