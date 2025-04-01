# coding: utf-8

"""
EVO API

Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

OpenAPI spec version: v1

Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from enum import IntEnum


class EFormaContato(IntEnum):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    _1 = 1
    _2 = 2
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _10 = 10
    _11 = 11
    _12 = 12

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.value

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EFormaContato):
            return False

        return self.value == other.value

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
