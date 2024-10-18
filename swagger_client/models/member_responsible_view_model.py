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

class MemberResponsibleViewModel(object):
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
        'id_responsible': 'int',
        'id_member': 'int',
        'name': 'str',
        'cpf': 'str',
        'email': 'str',
        'phone': 'str',
        'observation': 'str',
        'id_member_responsible': 'int',
        'acess_fiti': 'bool',
        'financial_responsible': 'bool'
    }

    attribute_map = {
        'id_responsible': 'idResponsible',
        'id_member': 'idMember',
        'name': 'name',
        'cpf': 'cpf',
        'email': 'email',
        'phone': 'phone',
        'observation': 'observation',
        'id_member_responsible': 'idMemberResponsible',
        'acess_fiti': 'acessFiti',
        'financial_responsible': 'financialResponsible'
    }

    def __init__(self, id_responsible=None, id_member=None, name=None, cpf=None, email=None, phone=None, observation=None, id_member_responsible=None, acess_fiti=None, financial_responsible=None):  # noqa: E501
        """MemberResponsibleViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_responsible = None
        self._id_member = None
        self._name = None
        self._cpf = None
        self._email = None
        self._phone = None
        self._observation = None
        self._id_member_responsible = None
        self._acess_fiti = None
        self._financial_responsible = None
        self.discriminator = None
        if id_responsible is not None:
            self.id_responsible = id_responsible
        if id_member is not None:
            self.id_member = id_member
        if name is not None:
            self.name = name
        if cpf is not None:
            self.cpf = cpf
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if observation is not None:
            self.observation = observation
        if id_member_responsible is not None:
            self.id_member_responsible = id_member_responsible
        if acess_fiti is not None:
            self.acess_fiti = acess_fiti
        if financial_responsible is not None:
            self.financial_responsible = financial_responsible

    @property
    def id_responsible(self):
        """Gets the id_responsible of this MemberResponsibleViewModel.  # noqa: E501


        :return: The id_responsible of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_responsible

    @id_responsible.setter
    def id_responsible(self, id_responsible):
        """Sets the id_responsible of this MemberResponsibleViewModel.


        :param id_responsible: The id_responsible of this MemberResponsibleViewModel.  # noqa: E501
        :type: int
        """

        self._id_responsible = id_responsible

    @property
    def id_member(self):
        """Gets the id_member of this MemberResponsibleViewModel.  # noqa: E501


        :return: The id_member of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_member

    @id_member.setter
    def id_member(self, id_member):
        """Sets the id_member of this MemberResponsibleViewModel.


        :param id_member: The id_member of this MemberResponsibleViewModel.  # noqa: E501
        :type: int
        """

        self._id_member = id_member

    @property
    def name(self):
        """Gets the name of this MemberResponsibleViewModel.  # noqa: E501


        :return: The name of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MemberResponsibleViewModel.


        :param name: The name of this MemberResponsibleViewModel.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def cpf(self):
        """Gets the cpf of this MemberResponsibleViewModel.  # noqa: E501


        :return: The cpf of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: str
        """
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        """Sets the cpf of this MemberResponsibleViewModel.


        :param cpf: The cpf of this MemberResponsibleViewModel.  # noqa: E501
        :type: str
        """

        self._cpf = cpf

    @property
    def email(self):
        """Gets the email of this MemberResponsibleViewModel.  # noqa: E501


        :return: The email of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this MemberResponsibleViewModel.


        :param email: The email of this MemberResponsibleViewModel.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def phone(self):
        """Gets the phone of this MemberResponsibleViewModel.  # noqa: E501


        :return: The phone of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this MemberResponsibleViewModel.


        :param phone: The phone of this MemberResponsibleViewModel.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def observation(self):
        """Gets the observation of this MemberResponsibleViewModel.  # noqa: E501


        :return: The observation of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: str
        """
        return self._observation

    @observation.setter
    def observation(self, observation):
        """Sets the observation of this MemberResponsibleViewModel.


        :param observation: The observation of this MemberResponsibleViewModel.  # noqa: E501
        :type: str
        """

        self._observation = observation

    @property
    def id_member_responsible(self):
        """Gets the id_member_responsible of this MemberResponsibleViewModel.  # noqa: E501


        :return: The id_member_responsible of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_member_responsible

    @id_member_responsible.setter
    def id_member_responsible(self, id_member_responsible):
        """Sets the id_member_responsible of this MemberResponsibleViewModel.


        :param id_member_responsible: The id_member_responsible of this MemberResponsibleViewModel.  # noqa: E501
        :type: int
        """

        self._id_member_responsible = id_member_responsible

    @property
    def acess_fiti(self):
        """Gets the acess_fiti of this MemberResponsibleViewModel.  # noqa: E501


        :return: The acess_fiti of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._acess_fiti

    @acess_fiti.setter
    def acess_fiti(self, acess_fiti):
        """Sets the acess_fiti of this MemberResponsibleViewModel.


        :param acess_fiti: The acess_fiti of this MemberResponsibleViewModel.  # noqa: E501
        :type: bool
        """

        self._acess_fiti = acess_fiti

    @property
    def financial_responsible(self):
        """Gets the financial_responsible of this MemberResponsibleViewModel.  # noqa: E501


        :return: The financial_responsible of this MemberResponsibleViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._financial_responsible

    @financial_responsible.setter
    def financial_responsible(self, financial_responsible):
        """Sets the financial_responsible of this MemberResponsibleViewModel.


        :param financial_responsible: The financial_responsible of this MemberResponsibleViewModel.  # noqa: E501
        :type: bool
        """

        self._financial_responsible = financial_responsible

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
        if issubclass(MemberResponsibleViewModel, dict):
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
        if not isinstance(other, MemberResponsibleViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
