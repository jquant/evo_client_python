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

class ConfiguracaoApiViewModel(object):
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
        'id_branch': 'int',
        'name': 'str',
        'internal_name': 'str',
        'cnpj': 'str',
        'address': 'str',
        'neighborhood': 'str',
        'telephone': 'str',
        'number': 'str',
        'id_state': 'int',
        'state': 'str',
        'state_short': 'str',
        'city': 'str',
        'complement': 'str',
        'zip_code': 'str',
        'website': 'str',
        'latitude': 'float',
        'longitude': 'float',
        'opening_date': 'datetime',
        'business_hours': 'list[BusinessHoursViewModel]',
        'search_terms': 'list[str]'
    }

    attribute_map = {
        'id_branch': 'idBranch',
        'name': 'name',
        'internal_name': 'internalName',
        'cnpj': 'cnpj',
        'address': 'address',
        'neighborhood': 'neighborhood',
        'telephone': 'telephone',
        'number': 'number',
        'id_state': 'idState',
        'state': 'state',
        'state_short': 'stateShort',
        'city': 'city',
        'complement': 'complement',
        'zip_code': 'zipCode',
        'website': 'website',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'opening_date': 'openingDate',
        'business_hours': 'businessHours',
        'search_terms': 'searchTerms'
    }

    def __init__(self, id_branch=None, name=None, internal_name=None, cnpj=None, address=None, neighborhood=None, telephone=None, number=None, id_state=None, state=None, state_short=None, city=None, complement=None, zip_code=None, website=None, latitude=None, longitude=None, opening_date=None, business_hours=None, search_terms=None):  # noqa: E501
        """ConfiguracaoApiViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_branch = None
        self._name = None
        self._internal_name = None
        self._cnpj = None
        self._address = None
        self._neighborhood = None
        self._telephone = None
        self._number = None
        self._id_state = None
        self._state = None
        self._state_short = None
        self._city = None
        self._complement = None
        self._zip_code = None
        self._website = None
        self._latitude = None
        self._longitude = None
        self._opening_date = None
        self._business_hours = None
        self._search_terms = None
        self.discriminator = None
        if id_branch is not None:
            self.id_branch = id_branch
        if name is not None:
            self.name = name
        if internal_name is not None:
            self.internal_name = internal_name
        if cnpj is not None:
            self.cnpj = cnpj
        if address is not None:
            self.address = address
        if neighborhood is not None:
            self.neighborhood = neighborhood
        if telephone is not None:
            self.telephone = telephone
        if number is not None:
            self.number = number
        if id_state is not None:
            self.id_state = id_state
        if state is not None:
            self.state = state
        if state_short is not None:
            self.state_short = state_short
        if city is not None:
            self.city = city
        if complement is not None:
            self.complement = complement
        if zip_code is not None:
            self.zip_code = zip_code
        if website is not None:
            self.website = website
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if opening_date is not None:
            self.opening_date = opening_date
        if business_hours is not None:
            self.business_hours = business_hours
        if search_terms is not None:
            self.search_terms = search_terms

    @property
    def id_branch(self):
        """Gets the id_branch of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The id_branch of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_branch

    @id_branch.setter
    def id_branch(self, id_branch):
        """Sets the id_branch of this ConfiguracaoApiViewModel.


        :param id_branch: The id_branch of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_branch = id_branch

    @property
    def name(self):
        """Gets the name of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The name of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConfiguracaoApiViewModel.


        :param name: The name of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def internal_name(self):
        """Gets the internal_name of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The internal_name of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._internal_name

    @internal_name.setter
    def internal_name(self, internal_name):
        """Sets the internal_name of this ConfiguracaoApiViewModel.


        :param internal_name: The internal_name of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._internal_name = internal_name

    @property
    def cnpj(self):
        """Gets the cnpj of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The cnpj of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        """Sets the cnpj of this ConfiguracaoApiViewModel.


        :param cnpj: The cnpj of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._cnpj = cnpj

    @property
    def address(self):
        """Gets the address of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The address of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this ConfiguracaoApiViewModel.


        :param address: The address of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def neighborhood(self):
        """Gets the neighborhood of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The neighborhood of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._neighborhood

    @neighborhood.setter
    def neighborhood(self, neighborhood):
        """Sets the neighborhood of this ConfiguracaoApiViewModel.


        :param neighborhood: The neighborhood of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._neighborhood = neighborhood

    @property
    def telephone(self):
        """Gets the telephone of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The telephone of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._telephone

    @telephone.setter
    def telephone(self, telephone):
        """Sets the telephone of this ConfiguracaoApiViewModel.


        :param telephone: The telephone of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._telephone = telephone

    @property
    def number(self):
        """Gets the number of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The number of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this ConfiguracaoApiViewModel.


        :param number: The number of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._number = number

    @property
    def id_state(self):
        """Gets the id_state of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The id_state of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_state

    @id_state.setter
    def id_state(self, id_state):
        """Sets the id_state of this ConfiguracaoApiViewModel.


        :param id_state: The id_state of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_state = id_state

    @property
    def state(self):
        """Gets the state of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The state of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ConfiguracaoApiViewModel.


        :param state: The state of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def state_short(self):
        """Gets the state_short of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The state_short of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._state_short

    @state_short.setter
    def state_short(self, state_short):
        """Sets the state_short of this ConfiguracaoApiViewModel.


        :param state_short: The state_short of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._state_short = state_short

    @property
    def city(self):
        """Gets the city of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The city of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this ConfiguracaoApiViewModel.


        :param city: The city of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def complement(self):
        """Gets the complement of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The complement of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._complement

    @complement.setter
    def complement(self, complement):
        """Sets the complement of this ConfiguracaoApiViewModel.


        :param complement: The complement of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._complement = complement

    @property
    def zip_code(self):
        """Gets the zip_code of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The zip_code of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        """Sets the zip_code of this ConfiguracaoApiViewModel.


        :param zip_code: The zip_code of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._zip_code = zip_code

    @property
    def website(self):
        """Gets the website of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The website of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._website

    @website.setter
    def website(self, website):
        """Sets the website of this ConfiguracaoApiViewModel.


        :param website: The website of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: str
        """

        self._website = website

    @property
    def latitude(self):
        """Gets the latitude of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The latitude of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this ConfiguracaoApiViewModel.


        :param latitude: The latitude of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: float
        """

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The longitude of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this ConfiguracaoApiViewModel.


        :param longitude: The longitude of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: float
        """

        self._longitude = longitude

    @property
    def opening_date(self):
        """Gets the opening_date of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The opening_date of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self._opening_date

    @opening_date.setter
    def opening_date(self, opening_date):
        """Sets the opening_date of this ConfiguracaoApiViewModel.


        :param opening_date: The opening_date of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: datetime
        """

        self._opening_date = opening_date

    @property
    def business_hours(self):
        """Gets the business_hours of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The business_hours of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: list[BusinessHoursViewModel]
        """
        return self._business_hours

    @business_hours.setter
    def business_hours(self, business_hours):
        """Sets the business_hours of this ConfiguracaoApiViewModel.


        :param business_hours: The business_hours of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: list[BusinessHoursViewModel]
        """

        self._business_hours = business_hours

    @property
    def search_terms(self):
        """Gets the search_terms of this ConfiguracaoApiViewModel.  # noqa: E501


        :return: The search_terms of this ConfiguracaoApiViewModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._search_terms

    @search_terms.setter
    def search_terms(self, search_terms):
        """Sets the search_terms of this ConfiguracaoApiViewModel.


        :param search_terms: The search_terms of this ConfiguracaoApiViewModel.  # noqa: E501
        :type: list[str]
        """

        self._search_terms = search_terms

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
        if issubclass(ConfiguracaoApiViewModel, dict):
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
        if not isinstance(other, ConfiguracaoApiViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
