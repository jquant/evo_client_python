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

class ProspectIdViewModel(object):
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
        'id_prospect': 'int'
    }

    attribute_map = {
        'id_prospect': 'idProspect'
    }

    def __init__(self, id_prospect=None):  # noqa: E501
        """ProspectIdViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_prospect = None
        self.discriminator = None
        if id_prospect is not None:
            self.id_prospect = id_prospect

    @property
    def id_prospect(self):
        """Gets the id_prospect of this ProspectIdViewModel.  # noqa: E501


        :return: The id_prospect of this ProspectIdViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_prospect

    @id_prospect.setter
    def id_prospect(self, id_prospect):
        """Sets the id_prospect of this ProspectIdViewModel.


        :param id_prospect: The id_prospect of this ProspectIdViewModel.  # noqa: E501
        :type: int
        """

        self._id_prospect = id_prospect

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
        if issubclass(ProspectIdViewModel, dict):
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
        if not isinstance(other, ProspectIdViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
