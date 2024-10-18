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

class LogTefApiViewModel(object):
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
        'authorization': 'str',
        'tef_id': 'str',
        'merchant_checkout_guid': 'str'
    }

    attribute_map = {
        'authorization': 'authorization',
        'tef_id': 'tefId',
        'merchant_checkout_guid': 'merchantCheckoutGuid'
    }

    def __init__(self, authorization=None, tef_id=None, merchant_checkout_guid=None):  # noqa: E501
        """LogTefApiViewModel - a model defined in Swagger"""  # noqa: E501
        self._authorization = None
        self._tef_id = None
        self._merchant_checkout_guid = None
        self.discriminator = None
        if authorization is not None:
            self.authorization = authorization
        if tef_id is not None:
            self.tef_id = tef_id
        if merchant_checkout_guid is not None:
            self.merchant_checkout_guid = merchant_checkout_guid

    @property
    def authorization(self):
        """Gets the authorization of this LogTefApiViewModel.  # noqa: E501


        :return: The authorization of this LogTefApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._authorization

    @authorization.setter
    def authorization(self, authorization):
        """Sets the authorization of this LogTefApiViewModel.


        :param authorization: The authorization of this LogTefApiViewModel.  # noqa: E501
        :type: str
        """

        self._authorization = authorization

    @property
    def tef_id(self):
        """Gets the tef_id of this LogTefApiViewModel.  # noqa: E501


        :return: The tef_id of this LogTefApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._tef_id

    @tef_id.setter
    def tef_id(self, tef_id):
        """Sets the tef_id of this LogTefApiViewModel.


        :param tef_id: The tef_id of this LogTefApiViewModel.  # noqa: E501
        :type: str
        """

        self._tef_id = tef_id

    @property
    def merchant_checkout_guid(self):
        """Gets the merchant_checkout_guid of this LogTefApiViewModel.  # noqa: E501


        :return: The merchant_checkout_guid of this LogTefApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._merchant_checkout_guid

    @merchant_checkout_guid.setter
    def merchant_checkout_guid(self, merchant_checkout_guid):
        """Sets the merchant_checkout_guid of this LogTefApiViewModel.


        :param merchant_checkout_guid: The merchant_checkout_guid of this LogTefApiViewModel.  # noqa: E501
        :type: str
        """

        self._merchant_checkout_guid = merchant_checkout_guid

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
        if issubclass(LogTefApiViewModel, dict):
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
        if not isinstance(other, LogTefApiViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
