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

class InstallmentViewModel(object):
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
        'total_value': 'float',
        'value': 'float',
        '_date': 'datetime',
        'service_name': 'str',
        'service_value': 'float',
        'loyalty_monthly_payment_description': 'str',
        'loyalty_monthly_payment_value_description': 'str',
        'annuity_service_name': 'str',
        'annuity_service_value': 'float'
    }

    attribute_map = {
        'total_value': 'totalValue',
        'value': 'value',
        '_date': 'date',
        'service_name': 'serviceName',
        'service_value': 'serviceValue',
        'loyalty_monthly_payment_description': 'loyaltyMonthlyPaymentDescription',
        'loyalty_monthly_payment_value_description': 'loyaltyMonthlyPaymentValueDescription',
        'annuity_service_name': 'annuityServiceName',
        'annuity_service_value': 'annuityServiceValue'
    }

    def __init__(self, total_value=None, value=None, _date=None, service_name=None, service_value=None, loyalty_monthly_payment_description=None, loyalty_monthly_payment_value_description=None, annuity_service_name=None, annuity_service_value=None):  # noqa: E501
        """InstallmentViewModel - a model defined in Swagger"""  # noqa: E501
        self._total_value = None
        self._value = None
        self.__date = None
        self._service_name = None
        self._service_value = None
        self._loyalty_monthly_payment_description = None
        self._loyalty_monthly_payment_value_description = None
        self._annuity_service_name = None
        self._annuity_service_value = None
        self.discriminator = None
        if total_value is not None:
            self.total_value = total_value
        if value is not None:
            self.value = value
        if _date is not None:
            self._date = _date
        if service_name is not None:
            self.service_name = service_name
        if service_value is not None:
            self.service_value = service_value
        if loyalty_monthly_payment_description is not None:
            self.loyalty_monthly_payment_description = loyalty_monthly_payment_description
        if loyalty_monthly_payment_value_description is not None:
            self.loyalty_monthly_payment_value_description = loyalty_monthly_payment_value_description
        if annuity_service_name is not None:
            self.annuity_service_name = annuity_service_name
        if annuity_service_value is not None:
            self.annuity_service_value = annuity_service_value

    @property
    def total_value(self):
        """Gets the total_value of this InstallmentViewModel.  # noqa: E501


        :return: The total_value of this InstallmentViewModel.  # noqa: E501
        :rtype: float
        """
        return self._total_value

    @total_value.setter
    def total_value(self, total_value):
        """Sets the total_value of this InstallmentViewModel.


        :param total_value: The total_value of this InstallmentViewModel.  # noqa: E501
        :type: float
        """

        self._total_value = total_value

    @property
    def value(self):
        """Gets the value of this InstallmentViewModel.  # noqa: E501


        :return: The value of this InstallmentViewModel.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this InstallmentViewModel.


        :param value: The value of this InstallmentViewModel.  # noqa: E501
        :type: float
        """

        self._value = value

    @property
    def _date(self):
        """Gets the _date of this InstallmentViewModel.  # noqa: E501


        :return: The _date of this InstallmentViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this InstallmentViewModel.


        :param _date: The _date of this InstallmentViewModel.  # noqa: E501
        :type: datetime
        """

        self.__date = _date

    @property
    def service_name(self):
        """Gets the service_name of this InstallmentViewModel.  # noqa: E501


        :return: The service_name of this InstallmentViewModel.  # noqa: E501
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """Sets the service_name of this InstallmentViewModel.


        :param service_name: The service_name of this InstallmentViewModel.  # noqa: E501
        :type: str
        """

        self._service_name = service_name

    @property
    def service_value(self):
        """Gets the service_value of this InstallmentViewModel.  # noqa: E501


        :return: The service_value of this InstallmentViewModel.  # noqa: E501
        :rtype: float
        """
        return self._service_value

    @service_value.setter
    def service_value(self, service_value):
        """Sets the service_value of this InstallmentViewModel.


        :param service_value: The service_value of this InstallmentViewModel.  # noqa: E501
        :type: float
        """

        self._service_value = service_value

    @property
    def loyalty_monthly_payment_description(self):
        """Gets the loyalty_monthly_payment_description of this InstallmentViewModel.  # noqa: E501


        :return: The loyalty_monthly_payment_description of this InstallmentViewModel.  # noqa: E501
        :rtype: str
        """
        return self._loyalty_monthly_payment_description

    @loyalty_monthly_payment_description.setter
    def loyalty_monthly_payment_description(self, loyalty_monthly_payment_description):
        """Sets the loyalty_monthly_payment_description of this InstallmentViewModel.


        :param loyalty_monthly_payment_description: The loyalty_monthly_payment_description of this InstallmentViewModel.  # noqa: E501
        :type: str
        """

        self._loyalty_monthly_payment_description = loyalty_monthly_payment_description

    @property
    def loyalty_monthly_payment_value_description(self):
        """Gets the loyalty_monthly_payment_value_description of this InstallmentViewModel.  # noqa: E501


        :return: The loyalty_monthly_payment_value_description of this InstallmentViewModel.  # noqa: E501
        :rtype: str
        """
        return self._loyalty_monthly_payment_value_description

    @loyalty_monthly_payment_value_description.setter
    def loyalty_monthly_payment_value_description(self, loyalty_monthly_payment_value_description):
        """Sets the loyalty_monthly_payment_value_description of this InstallmentViewModel.


        :param loyalty_monthly_payment_value_description: The loyalty_monthly_payment_value_description of this InstallmentViewModel.  # noqa: E501
        :type: str
        """

        self._loyalty_monthly_payment_value_description = loyalty_monthly_payment_value_description

    @property
    def annuity_service_name(self):
        """Gets the annuity_service_name of this InstallmentViewModel.  # noqa: E501


        :return: The annuity_service_name of this InstallmentViewModel.  # noqa: E501
        :rtype: str
        """
        return self._annuity_service_name

    @annuity_service_name.setter
    def annuity_service_name(self, annuity_service_name):
        """Sets the annuity_service_name of this InstallmentViewModel.


        :param annuity_service_name: The annuity_service_name of this InstallmentViewModel.  # noqa: E501
        :type: str
        """

        self._annuity_service_name = annuity_service_name

    @property
    def annuity_service_value(self):
        """Gets the annuity_service_value of this InstallmentViewModel.  # noqa: E501


        :return: The annuity_service_value of this InstallmentViewModel.  # noqa: E501
        :rtype: float
        """
        return self._annuity_service_value

    @annuity_service_value.setter
    def annuity_service_value(self, annuity_service_value):
        """Sets the annuity_service_value of this InstallmentViewModel.


        :param annuity_service_value: The annuity_service_value of this InstallmentViewModel.  # noqa: E501
        :type: float
        """

        self._annuity_service_value = annuity_service_value

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
        if issubclass(InstallmentViewModel, dict):
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
        if not isinstance(other, InstallmentViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
