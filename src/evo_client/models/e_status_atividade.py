# coding: utf-8

"""
EVO API

Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

OpenAPI spec version: v1

Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from enum import IntEnum


class EStatusAtividade(IntEnum):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Livre = 0,
    Disponivel = 1,
    Lotada = 2,
    ReservaEncerrada = 3,
    Restrita = 4,
    Cadastrado = 5,
    Finalizada = 6,
    Cancelada = 7,
    NaFila = 8,
    LivreEncerrada = 10,
    RestritaEncerrada = 11,
    RestritaNaoPermiteParticipar = 12
    LotadaSemFilaEspera = 15
    """

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15

    @classmethod
    def get_description(cls, value: int) -> str:
        """Get the description for a contract type value."""
        try:
            enum_value = cls(value)
            descriptions = {
                0: "Livre",
                1: "Disponível",
                2: "Lotada",
                3: "Reserva Encerrada",
                4: "Restrita",
                5: "Cadastrado",
                6: "Finalizada",
                7: "Cancelada",
                8: "Na Fila",
                9: "Livre Encerrada",
                10: "Restrita Encerrada",
                11: "Restrita Não Permite Participar",
                12: "Lotada Sem Fila Espera",
                13: "Anual com Data de Término Específica",
                14: "Contrato Adicional",
                15: "Lotada Sem Fila Espera",
            }
            return descriptions.get(enum_value.value, "Unknown")
        except ValueError:
            return "Unknown"

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.value

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if isinstance(other, (str, int)):
            return self.value == str(other)
        if not isinstance(other, EStatusAtividade):
            return False
        return self.value == other.value

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
