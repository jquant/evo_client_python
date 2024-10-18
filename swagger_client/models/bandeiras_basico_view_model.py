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

class BandeirasBasicoViewModel(object):
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
        'value': 'str',
        'text': 'str',
        'logo_url': 'str'
    }

    attribute_map = {
        'value': 'value',
        'text': 'text',
        'logo_url': 'logoUrl'
    }

    def __init__(self, value=None, text=None, logo_url=None):  # noqa: E501
        """BandeirasBasicoViewModel - a model defined in Swagger"""  # noqa: E501
        self._value = None
        self._text = None
        self._logo_url = None
        self.discriminator = None
        if value is not None:
            self.value = value
        if text is not None:
            self.text = text
        if logo_url is not None:
            self.logo_url = logo_url

    @property
    def value(self):
        """Gets the value of this BandeirasBasicoViewModel.  # noqa: E501


        :return: The value of this BandeirasBasicoViewModel.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this BandeirasBasicoViewModel.


        :param value: The value of this BandeirasBasicoViewModel.  # noqa: E501
        :type: str
        """

        self._value = value

    @property
    def text(self):
        """Gets the text of this BandeirasBasicoViewModel.  # noqa: E501


        :return: The text of this BandeirasBasicoViewModel.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this BandeirasBasicoViewModel.


        :param text: The text of this BandeirasBasicoViewModel.  # noqa: E501
        :type: str
        """

        self._text = text

    @property
    def logo_url(self):
        """Gets the logo_url of this BandeirasBasicoViewModel.  # noqa: E501


        :return: The logo_url of this BandeirasBasicoViewModel.  # noqa: E501
        :rtype: str
        """
        return self._logo_url

    @logo_url.setter
    def logo_url(self, logo_url):
        """Sets the logo_url of this BandeirasBasicoViewModel.


        :param logo_url: The logo_url of this BandeirasBasicoViewModel.  # noqa: E501
        :type: str
        """

        self._logo_url = logo_url

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
        if issubclass(BandeirasBasicoViewModel, dict):
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
        if not isinstance(other, BandeirasBasicoViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
