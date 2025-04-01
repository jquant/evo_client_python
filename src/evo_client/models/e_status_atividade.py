# coding: utf-8

"""
EVO API

Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

OpenAPI spec version: v1

Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from enum import Enum
from typing import Union


class EStatusAtividade(int, Enum):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15
    _NA = "NA"

    @classmethod
    def _missing_(cls, value: Union[str, int]) -> "EStatusAtividade":
        """Handle both string and integer inputs."""
        if isinstance(value, int):
            value = str(value)
        for member in cls:
            if member.value == value:
                return member
        return cls._NA

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.value

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if isinstance(other, (str, int)):
            return self.value == str(other)
        if not isinstance(other, EStatusAtividade):
            return False
        return self.value == other.value

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
