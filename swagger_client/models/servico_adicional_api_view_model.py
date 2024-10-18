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

class ServicoAdicionalApiViewModel(object):
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
        'id_service': 'int',
        'name': 'str',
        'value': 'float'
    }

    attribute_map = {
        'id_service': 'idService',
        'name': 'name',
        'value': 'value'
    }

    def __init__(self, id_service=None, name=None, value=None):  # noqa: E501
        """ServicoAdicionalApiViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_service = None
        self._name = None
        self._value = None
        self.discriminator = None
        if id_service is not None:
            self.id_service = id_service
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value

    @property
    def id_service(self):
        """Gets the id_service of this ServicoAdicionalApiViewModel.  # noqa: E501


        :return: The id_service of this ServicoAdicionalApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_service

    @id_service.setter
    def id_service(self, id_service):
        """Sets the id_service of this ServicoAdicionalApiViewModel.


        :param id_service: The id_service of this ServicoAdicionalApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_service = id_service

    @property
    def name(self):
        """Gets the name of this ServicoAdicionalApiViewModel.  # noqa: E501


        :return: The name of this ServicoAdicionalApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ServicoAdicionalApiViewModel.


        :param name: The name of this ServicoAdicionalApiViewModel.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def value(self):
        """Gets the value of this ServicoAdicionalApiViewModel.  # noqa: E501


        :return: The value of this ServicoAdicionalApiViewModel.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ServicoAdicionalApiViewModel.


        :param value: The value of this ServicoAdicionalApiViewModel.  # noqa: E501
        :type: float
        """

        self._value = value

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
        if issubclass(ServicoAdicionalApiViewModel, dict):
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
        if not isinstance(other, ServicoAdicionalApiViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
