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

class BankAccountsViewModel(object):
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
        'id_bank_account': 'int',
        'description': 'str',
        'account_type': 'bool',
        'bank_code': 'int',
        'agency': 'str',
        'account': 'str',
        'observations': 'str',
        'inactive': 'bool',
        'bank_integration': 'bool'
    }

    attribute_map = {
        'id_bank_account': 'idBankAccount',
        'description': 'description',
        'account_type': 'accountType',
        'bank_code': 'bankCode',
        'agency': 'agency',
        'account': 'account',
        'observations': 'observations',
        'inactive': 'inactive',
        'bank_integration': 'bankIntegration'
    }

    def __init__(self, id_bank_account=None, description=None, account_type=None, bank_code=None, agency=None, account=None, observations=None, inactive=None, bank_integration=None):  # noqa: E501
        """BankAccountsViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_bank_account = None
        self._description = None
        self._account_type = None
        self._bank_code = None
        self._agency = None
        self._account = None
        self._observations = None
        self._inactive = None
        self._bank_integration = None
        self.discriminator = None
        if id_bank_account is not None:
            self.id_bank_account = id_bank_account
        if description is not None:
            self.description = description
        if account_type is not None:
            self.account_type = account_type
        if bank_code is not None:
            self.bank_code = bank_code
        if agency is not None:
            self.agency = agency
        if account is not None:
            self.account = account
        if observations is not None:
            self.observations = observations
        if inactive is not None:
            self.inactive = inactive
        if bank_integration is not None:
            self.bank_integration = bank_integration

    @property
    def id_bank_account(self):
        """Gets the id_bank_account of this BankAccountsViewModel.  # noqa: E501


        :return: The id_bank_account of this BankAccountsViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_bank_account

    @id_bank_account.setter
    def id_bank_account(self, id_bank_account):
        """Sets the id_bank_account of this BankAccountsViewModel.


        :param id_bank_account: The id_bank_account of this BankAccountsViewModel.  # noqa: E501
        :type: int
        """

        self._id_bank_account = id_bank_account

    @property
    def description(self):
        """Gets the description of this BankAccountsViewModel.  # noqa: E501


        :return: The description of this BankAccountsViewModel.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this BankAccountsViewModel.


        :param description: The description of this BankAccountsViewModel.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def account_type(self):
        """Gets the account_type of this BankAccountsViewModel.  # noqa: E501


        :return: The account_type of this BankAccountsViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._account_type

    @account_type.setter
    def account_type(self, account_type):
        """Sets the account_type of this BankAccountsViewModel.


        :param account_type: The account_type of this BankAccountsViewModel.  # noqa: E501
        :type: bool
        """

        self._account_type = account_type

    @property
    def bank_code(self):
        """Gets the bank_code of this BankAccountsViewModel.  # noqa: E501


        :return: The bank_code of this BankAccountsViewModel.  # noqa: E501
        :rtype: int
        """
        return self._bank_code

    @bank_code.setter
    def bank_code(self, bank_code):
        """Sets the bank_code of this BankAccountsViewModel.


        :param bank_code: The bank_code of this BankAccountsViewModel.  # noqa: E501
        :type: int
        """

        self._bank_code = bank_code

    @property
    def agency(self):
        """Gets the agency of this BankAccountsViewModel.  # noqa: E501


        :return: The agency of this BankAccountsViewModel.  # noqa: E501
        :rtype: str
        """
        return self._agency

    @agency.setter
    def agency(self, agency):
        """Sets the agency of this BankAccountsViewModel.


        :param agency: The agency of this BankAccountsViewModel.  # noqa: E501
        :type: str
        """

        self._agency = agency

    @property
    def account(self):
        """Gets the account of this BankAccountsViewModel.  # noqa: E501


        :return: The account of this BankAccountsViewModel.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this BankAccountsViewModel.


        :param account: The account of this BankAccountsViewModel.  # noqa: E501
        :type: str
        """

        self._account = account

    @property
    def observations(self):
        """Gets the observations of this BankAccountsViewModel.  # noqa: E501


        :return: The observations of this BankAccountsViewModel.  # noqa: E501
        :rtype: str
        """
        return self._observations

    @observations.setter
    def observations(self, observations):
        """Sets the observations of this BankAccountsViewModel.


        :param observations: The observations of this BankAccountsViewModel.  # noqa: E501
        :type: str
        """

        self._observations = observations

    @property
    def inactive(self):
        """Gets the inactive of this BankAccountsViewModel.  # noqa: E501


        :return: The inactive of this BankAccountsViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._inactive

    @inactive.setter
    def inactive(self, inactive):
        """Sets the inactive of this BankAccountsViewModel.


        :param inactive: The inactive of this BankAccountsViewModel.  # noqa: E501
        :type: bool
        """

        self._inactive = inactive

    @property
    def bank_integration(self):
        """Gets the bank_integration of this BankAccountsViewModel.  # noqa: E501


        :return: The bank_integration of this BankAccountsViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._bank_integration

    @bank_integration.setter
    def bank_integration(self, bank_integration):
        """Sets the bank_integration of this BankAccountsViewModel.


        :param bank_integration: The bank_integration of this BankAccountsViewModel.  # noqa: E501
        :type: bool
        """

        self._bank_integration = bank_integration

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
        if issubclass(BankAccountsViewModel, dict):
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
        if not isinstance(other, BankAccountsViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
