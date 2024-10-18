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

class EmpresasFiliaisOcupacaoViewModel(object):
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
        'occupation': 'int',
        'max_occupation': 'int',
        'qty_minutes_out': 'int'
    }

    attribute_map = {
        'id_branch': 'idBranch',
        'name': 'name',
        'occupation': 'occupation',
        'max_occupation': 'maxOccupation',
        'qty_minutes_out': 'qtyMinutesOut'
    }

    def __init__(self, id_branch=None, name=None, occupation=None, max_occupation=None, qty_minutes_out=None):  # noqa: E501
        """EmpresasFiliaisOcupacaoViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_branch = None
        self._name = None
        self._occupation = None
        self._max_occupation = None
        self._qty_minutes_out = None
        self.discriminator = None
        if id_branch is not None:
            self.id_branch = id_branch
        if name is not None:
            self.name = name
        if occupation is not None:
            self.occupation = occupation
        if max_occupation is not None:
            self.max_occupation = max_occupation
        if qty_minutes_out is not None:
            self.qty_minutes_out = qty_minutes_out

    @property
    def id_branch(self):
        """Gets the id_branch of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501


        :return: The id_branch of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_branch

    @id_branch.setter
    def id_branch(self, id_branch):
        """Sets the id_branch of this EmpresasFiliaisOcupacaoViewModel.


        :param id_branch: The id_branch of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :type: int
        """

        self._id_branch = id_branch

    @property
    def name(self):
        """Gets the name of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501


        :return: The name of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EmpresasFiliaisOcupacaoViewModel.


        :param name: The name of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def occupation(self):
        """Gets the occupation of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501


        :return: The occupation of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :rtype: int
        """
        return self._occupation

    @occupation.setter
    def occupation(self, occupation):
        """Sets the occupation of this EmpresasFiliaisOcupacaoViewModel.


        :param occupation: The occupation of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :type: int
        """

        self._occupation = occupation

    @property
    def max_occupation(self):
        """Gets the max_occupation of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501


        :return: The max_occupation of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :rtype: int
        """
        return self._max_occupation

    @max_occupation.setter
    def max_occupation(self, max_occupation):
        """Sets the max_occupation of this EmpresasFiliaisOcupacaoViewModel.


        :param max_occupation: The max_occupation of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :type: int
        """

        self._max_occupation = max_occupation

    @property
    def qty_minutes_out(self):
        """Gets the qty_minutes_out of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501


        :return: The qty_minutes_out of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :rtype: int
        """
        return self._qty_minutes_out

    @qty_minutes_out.setter
    def qty_minutes_out(self, qty_minutes_out):
        """Sets the qty_minutes_out of this EmpresasFiliaisOcupacaoViewModel.


        :param qty_minutes_out: The qty_minutes_out of this EmpresasFiliaisOcupacaoViewModel.  # noqa: E501
        :type: int
        """

        self._qty_minutes_out = qty_minutes_out

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
        if issubclass(EmpresasFiliaisOcupacaoViewModel, dict):
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
        if not isinstance(other, EmpresasFiliaisOcupacaoViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other