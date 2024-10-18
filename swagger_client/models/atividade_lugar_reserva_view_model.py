# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class AtividadeLugarReservaViewModel(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'number': 'int',
        'available': 'bool',
        'name_spot': 'str'
    }

    attribute_map = {
        'number': 'number',
        'available': 'available',
        'name_spot': 'nameSpot'
    }

    def __init__(self, number=None, available=None, name_spot=None):  # noqa: E501
        """AtividadeLugarReservaViewModel - a model defined in Swagger"""  # noqa: E501
        self._number = None
        self._available = None
        self._name_spot = None
        self.discriminator = None
        if number is not None:
            self.number = number
        if available is not None:
            self.available = available
        if name_spot is not None:
            self.name_spot = name_spot

    @property
    def number(self):
        """Gets the number of this AtividadeLugarReservaViewModel.  # noqa: E501


        :return: The number of this AtividadeLugarReservaViewModel.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this AtividadeLugarReservaViewModel.


        :param number: The number of this AtividadeLugarReservaViewModel.  # noqa: E501
        :type: int
        """

        self._number = number

    @property
    def available(self):
        """Gets the available of this AtividadeLugarReservaViewModel.  # noqa: E501


        :return: The available of this AtividadeLugarReservaViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this AtividadeLugarReservaViewModel.


        :param available: The available of this AtividadeLugarReservaViewModel.  # noqa: E501
        :type: bool
        """

        self._available = available

    @property
    def name_spot(self):
        """Gets the name_spot of this AtividadeLugarReservaViewModel.  # noqa: E501


        :return: The name_spot of this AtividadeLugarReservaViewModel.  # noqa: E501
        :rtype: str
        """
        return self._name_spot

    @name_spot.setter
    def name_spot(self, name_spot):
        """Sets the name_spot of this AtividadeLugarReservaViewModel.


        :param name_spot: The name_spot of this AtividadeLugarReservaViewModel.  # noqa: E501
        :type: str
        """

        self._name_spot = name_spot

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(AtividadeLugarReservaViewModel, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AtividadeLugarReservaViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
