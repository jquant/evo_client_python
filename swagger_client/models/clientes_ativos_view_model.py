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

class ClientesAtivosViewModel(object):
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
        'id_filial': 'int',
        'filial': 'str',
        'id_cliente': 'int',
        'nome_completo': 'str',
        'telefone': 'str',
        'email': 'str',
        'id_cliente_contrato_ativo': 'int',
        'contrato_ativo': 'str',
        'dt_inicio_contrato_ativo': 'datetime',
        'dt_fim_contrato_ativo': 'datetime',
        'id_cliente_contrato_futuro': 'int',
        'contrato_futuro': 'str',
        'dt_inicio_contrato_futuro': 'datetime',
        'dt_fim_contrato_futuro': 'datetime'
    }

    attribute_map = {
        'id_filial': 'idFilial',
        'filial': 'filial',
        'id_cliente': 'idCliente',
        'nome_completo': 'nomeCompleto',
        'telefone': 'telefone',
        'email': 'email',
        'id_cliente_contrato_ativo': 'idClienteContratoAtivo',
        'contrato_ativo': 'contratoAtivo',
        'dt_inicio_contrato_ativo': 'dtInicioContratoAtivo',
        'dt_fim_contrato_ativo': 'dtFimContratoAtivo',
        'id_cliente_contrato_futuro': 'idClienteContratoFuturo',
        'contrato_futuro': 'contratoFuturo',
        'dt_inicio_contrato_futuro': 'dtInicioContratoFuturo',
        'dt_fim_contrato_futuro': 'dtFimContratoFuturo'
    }

    def __init__(self, id_filial=None, filial=None, id_cliente=None, nome_completo=None, telefone=None, email=None, id_cliente_contrato_ativo=None, contrato_ativo=None, dt_inicio_contrato_ativo=None, dt_fim_contrato_ativo=None, id_cliente_contrato_futuro=None, contrato_futuro=None, dt_inicio_contrato_futuro=None, dt_fim_contrato_futuro=None):  # noqa: E501
        """ClientesAtivosViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_filial = None
        self._filial = None
        self._id_cliente = None
        self._nome_completo = None
        self._telefone = None
        self._email = None
        self._id_cliente_contrato_ativo = None
        self._contrato_ativo = None
        self._dt_inicio_contrato_ativo = None
        self._dt_fim_contrato_ativo = None
        self._id_cliente_contrato_futuro = None
        self._contrato_futuro = None
        self._dt_inicio_contrato_futuro = None
        self._dt_fim_contrato_futuro = None
        self.discriminator = None
        if id_filial is not None:
            self.id_filial = id_filial
        if filial is not None:
            self.filial = filial
        if id_cliente is not None:
            self.id_cliente = id_cliente
        if nome_completo is not None:
            self.nome_completo = nome_completo
        if telefone is not None:
            self.telefone = telefone
        if email is not None:
            self.email = email
        if id_cliente_contrato_ativo is not None:
            self.id_cliente_contrato_ativo = id_cliente_contrato_ativo
        if contrato_ativo is not None:
            self.contrato_ativo = contrato_ativo
        if dt_inicio_contrato_ativo is not None:
            self.dt_inicio_contrato_ativo = dt_inicio_contrato_ativo
        if dt_fim_contrato_ativo is not None:
            self.dt_fim_contrato_ativo = dt_fim_contrato_ativo
        if id_cliente_contrato_futuro is not None:
            self.id_cliente_contrato_futuro = id_cliente_contrato_futuro
        if contrato_futuro is not None:
            self.contrato_futuro = contrato_futuro
        if dt_inicio_contrato_futuro is not None:
            self.dt_inicio_contrato_futuro = dt_inicio_contrato_futuro
        if dt_fim_contrato_futuro is not None:
            self.dt_fim_contrato_futuro = dt_fim_contrato_futuro

    @property
    def id_filial(self):
        """Gets the id_filial of this ClientesAtivosViewModel.  # noqa: E501


        :return: The id_filial of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_filial

    @id_filial.setter
    def id_filial(self, id_filial):
        """Sets the id_filial of this ClientesAtivosViewModel.


        :param id_filial: The id_filial of this ClientesAtivosViewModel.  # noqa: E501
        :type: int
        """

        self._id_filial = id_filial

    @property
    def filial(self):
        """Gets the filial of this ClientesAtivosViewModel.  # noqa: E501


        :return: The filial of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: str
        """
        return self._filial

    @filial.setter
    def filial(self, filial):
        """Sets the filial of this ClientesAtivosViewModel.


        :param filial: The filial of this ClientesAtivosViewModel.  # noqa: E501
        :type: str
        """

        self._filial = filial

    @property
    def id_cliente(self):
        """Gets the id_cliente of this ClientesAtivosViewModel.  # noqa: E501


        :return: The id_cliente of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, id_cliente):
        """Sets the id_cliente of this ClientesAtivosViewModel.


        :param id_cliente: The id_cliente of this ClientesAtivosViewModel.  # noqa: E501
        :type: int
        """

        self._id_cliente = id_cliente

    @property
    def nome_completo(self):
        """Gets the nome_completo of this ClientesAtivosViewModel.  # noqa: E501


        :return: The nome_completo of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: str
        """
        return self._nome_completo

    @nome_completo.setter
    def nome_completo(self, nome_completo):
        """Sets the nome_completo of this ClientesAtivosViewModel.


        :param nome_completo: The nome_completo of this ClientesAtivosViewModel.  # noqa: E501
        :type: str
        """

        self._nome_completo = nome_completo

    @property
    def telefone(self):
        """Gets the telefone of this ClientesAtivosViewModel.  # noqa: E501


        :return: The telefone of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: str
        """
        return self._telefone

    @telefone.setter
    def telefone(self, telefone):
        """Sets the telefone of this ClientesAtivosViewModel.


        :param telefone: The telefone of this ClientesAtivosViewModel.  # noqa: E501
        :type: str
        """

        self._telefone = telefone

    @property
    def email(self):
        """Gets the email of this ClientesAtivosViewModel.  # noqa: E501


        :return: The email of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ClientesAtivosViewModel.


        :param email: The email of this ClientesAtivosViewModel.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def id_cliente_contrato_ativo(self):
        """Gets the id_cliente_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501


        :return: The id_cliente_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_cliente_contrato_ativo

    @id_cliente_contrato_ativo.setter
    def id_cliente_contrato_ativo(self, id_cliente_contrato_ativo):
        """Sets the id_cliente_contrato_ativo of this ClientesAtivosViewModel.


        :param id_cliente_contrato_ativo: The id_cliente_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :type: int
        """

        self._id_cliente_contrato_ativo = id_cliente_contrato_ativo

    @property
    def contrato_ativo(self):
        """Gets the contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501


        :return: The contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: str
        """
        return self._contrato_ativo

    @contrato_ativo.setter
    def contrato_ativo(self, contrato_ativo):
        """Sets the contrato_ativo of this ClientesAtivosViewModel.


        :param contrato_ativo: The contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :type: str
        """

        self._contrato_ativo = contrato_ativo

    @property
    def dt_inicio_contrato_ativo(self):
        """Gets the dt_inicio_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501


        :return: The dt_inicio_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_inicio_contrato_ativo

    @dt_inicio_contrato_ativo.setter
    def dt_inicio_contrato_ativo(self, dt_inicio_contrato_ativo):
        """Sets the dt_inicio_contrato_ativo of this ClientesAtivosViewModel.


        :param dt_inicio_contrato_ativo: The dt_inicio_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :type: datetime
        """

        self._dt_inicio_contrato_ativo = dt_inicio_contrato_ativo

    @property
    def dt_fim_contrato_ativo(self):
        """Gets the dt_fim_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501


        :return: The dt_fim_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_fim_contrato_ativo

    @dt_fim_contrato_ativo.setter
    def dt_fim_contrato_ativo(self, dt_fim_contrato_ativo):
        """Sets the dt_fim_contrato_ativo of this ClientesAtivosViewModel.


        :param dt_fim_contrato_ativo: The dt_fim_contrato_ativo of this ClientesAtivosViewModel.  # noqa: E501
        :type: datetime
        """

        self._dt_fim_contrato_ativo = dt_fim_contrato_ativo

    @property
    def id_cliente_contrato_futuro(self):
        """Gets the id_cliente_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501


        :return: The id_cliente_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_cliente_contrato_futuro

    @id_cliente_contrato_futuro.setter
    def id_cliente_contrato_futuro(self, id_cliente_contrato_futuro):
        """Sets the id_cliente_contrato_futuro of this ClientesAtivosViewModel.


        :param id_cliente_contrato_futuro: The id_cliente_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :type: int
        """

        self._id_cliente_contrato_futuro = id_cliente_contrato_futuro

    @property
    def contrato_futuro(self):
        """Gets the contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501


        :return: The contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: str
        """
        return self._contrato_futuro

    @contrato_futuro.setter
    def contrato_futuro(self, contrato_futuro):
        """Sets the contrato_futuro of this ClientesAtivosViewModel.


        :param contrato_futuro: The contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :type: str
        """

        self._contrato_futuro = contrato_futuro

    @property
    def dt_inicio_contrato_futuro(self):
        """Gets the dt_inicio_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501


        :return: The dt_inicio_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_inicio_contrato_futuro

    @dt_inicio_contrato_futuro.setter
    def dt_inicio_contrato_futuro(self, dt_inicio_contrato_futuro):
        """Sets the dt_inicio_contrato_futuro of this ClientesAtivosViewModel.


        :param dt_inicio_contrato_futuro: The dt_inicio_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :type: datetime
        """

        self._dt_inicio_contrato_futuro = dt_inicio_contrato_futuro

    @property
    def dt_fim_contrato_futuro(self):
        """Gets the dt_fim_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501


        :return: The dt_fim_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_fim_contrato_futuro

    @dt_fim_contrato_futuro.setter
    def dt_fim_contrato_futuro(self, dt_fim_contrato_futuro):
        """Sets the dt_fim_contrato_futuro of this ClientesAtivosViewModel.


        :param dt_fim_contrato_futuro: The dt_fim_contrato_futuro of this ClientesAtivosViewModel.  # noqa: E501
        :type: datetime
        """

        self._dt_fim_contrato_futuro = dt_fim_contrato_futuro

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
        if issubclass(ClientesAtivosViewModel, dict):
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
        if not isinstance(other, ClientesAtivosViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
