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

class TelefoneApiViewModel(object):
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
        'id_phone': 'int',
        'id_member': 'int',
        'id_employee': 'int',
        'id_prospect': 'int',
        'id_provider': 'int',
        'id_contact_type': 'EFormaContato',
        'contact_type': 'str',
        'description': 'str'
    }

    attribute_map = {
        'id_phone': 'idPhone',
        'id_member': 'idMember',
        'id_employee': 'idEmployee',
        'id_prospect': 'idProspect',
        'id_provider': 'idProvider',
        'id_contact_type': 'idContactType',
        'contact_type': 'contactType',
        'description': 'description'
    }

    def __init__(self, id_phone=None, id_member=None, id_employee=None, id_prospect=None, id_provider=None, id_contact_type=None, contact_type=None, description=None):  # noqa: E501
        """TelefoneApiViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_phone = None
        self._id_member = None
        self._id_employee = None
        self._id_prospect = None
        self._id_provider = None
        self._id_contact_type = None
        self._contact_type = None
        self._description = None
        self.discriminator = None
        if id_phone is not None:
            self.id_phone = id_phone
        if id_member is not None:
            self.id_member = id_member
        if id_employee is not None:
            self.id_employee = id_employee
        if id_prospect is not None:
            self.id_prospect = id_prospect
        if id_provider is not None:
            self.id_provider = id_provider
        if id_contact_type is not None:
            self.id_contact_type = id_contact_type
        if contact_type is not None:
            self.contact_type = contact_type
        if description is not None:
            self.description = description

    @property
    def id_phone(self):
        """Gets the id_phone of this TelefoneApiViewModel.  # noqa: E501


        :return: The id_phone of this TelefoneApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_phone

    @id_phone.setter
    def id_phone(self, id_phone):
        """Sets the id_phone of this TelefoneApiViewModel.


        :param id_phone: The id_phone of this TelefoneApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_phone = id_phone

    @property
    def id_member(self):
        """Gets the id_member of this TelefoneApiViewModel.  # noqa: E501


        :return: The id_member of this TelefoneApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_member

    @id_member.setter
    def id_member(self, id_member):
        """Sets the id_member of this TelefoneApiViewModel.


        :param id_member: The id_member of this TelefoneApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_member = id_member

    @property
    def id_employee(self):
        """Gets the id_employee of this TelefoneApiViewModel.  # noqa: E501


        :return: The id_employee of this TelefoneApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_employee

    @id_employee.setter
    def id_employee(self, id_employee):
        """Sets the id_employee of this TelefoneApiViewModel.


        :param id_employee: The id_employee of this TelefoneApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_employee = id_employee

    @property
    def id_prospect(self):
        """Gets the id_prospect of this TelefoneApiViewModel.  # noqa: E501


        :return: The id_prospect of this TelefoneApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_prospect

    @id_prospect.setter
    def id_prospect(self, id_prospect):
        """Sets the id_prospect of this TelefoneApiViewModel.


        :param id_prospect: The id_prospect of this TelefoneApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_prospect = id_prospect

    @property
    def id_provider(self):
        """Gets the id_provider of this TelefoneApiViewModel.  # noqa: E501


        :return: The id_provider of this TelefoneApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_provider

    @id_provider.setter
    def id_provider(self, id_provider):
        """Sets the id_provider of this TelefoneApiViewModel.


        :param id_provider: The id_provider of this TelefoneApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_provider = id_provider

    @property
    def id_contact_type(self):
        """Gets the id_contact_type of this TelefoneApiViewModel.  # noqa: E501


        :return: The id_contact_type of this TelefoneApiViewModel.  # noqa: E501
        :rtype: EFormaContato
        """
        return self._id_contact_type

    @id_contact_type.setter
    def id_contact_type(self, id_contact_type):
        """Sets the id_contact_type of this TelefoneApiViewModel.


        :param id_contact_type: The id_contact_type of this TelefoneApiViewModel.  # noqa: E501
        :type: EFormaContato
        """

        self._id_contact_type = id_contact_type

    @property
    def contact_type(self):
        """Gets the contact_type of this TelefoneApiViewModel.  # noqa: E501


        :return: The contact_type of this TelefoneApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._contact_type

    @contact_type.setter
    def contact_type(self, contact_type):
        """Sets the contact_type of this TelefoneApiViewModel.


        :param contact_type: The contact_type of this TelefoneApiViewModel.  # noqa: E501
        :type: str
        """

        self._contact_type = contact_type

    @property
    def description(self):
        """Gets the description of this TelefoneApiViewModel.  # noqa: E501


        :return: The description of this TelefoneApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TelefoneApiViewModel.


        :param description: The description of this TelefoneApiViewModel.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if issubclass(TelefoneApiViewModel, dict):
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
        if not isinstance(other, TelefoneApiViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
