from enum import Enum


class EStatusAtividadeSessao(str, Enum):
    """Status for member/prospect attendance in an activity.
    Used in change_status() method.

    Values:
    - _0: Attending
    - _1: Absent
    - _2: Justified absence
    """

    _0 = "0"  # Attending
    _1 = "1"  # Absent
    _2 = "2"  # Justified absence

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.value

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EStatusAtividadeSessao):
            return False

        return self.value == other.value

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


class EStatusAtividadeAgendamento(str, Enum):
    """Status for activity schedule.
    Used in get_schedule() method.
    """

    LIVRE = "0"  # Free
    DISPONIVEL = "1"  # Available
    LOTADA = "2"  # Full
    RESERVA_ENCERRADA = "3"  # Reservation Closed
    RESTRITA = "4"  # Restricted
    CADASTRADO = "5"  # Registered
    FINALIZADA = "6"  # Finished
    CANCELADA = "7"  # Cancelled
    NA_FILA = "8"  # In Queue
    LIVRE_ENCERRADA = "10"  # Free Closed
    RESTRITA_ENCERRADA = "11"  # Restricted Closed
    RESTRITA_NAO_PERMITE_PARTICIPAR = "12"  # Restricted Not Allowed
    LOTADA_SEM_FILA_ESPERA = "15"  # Full No Waiting List

    def to_dict(self):
        """Returns the model properties as a dict"""
        return self.value

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EStatusAtividadeAgendamento):
            return False

        return self.value == other.value

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
