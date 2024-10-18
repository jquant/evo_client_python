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

class AtividadeBasicoApiViewModel(object):
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
        'id_group_activity': 'int',
        'id_activity_session': 'int',
        'id_configuration': 'int',
        'name': 'str',
        '_date': 'datetime',
        'capacity': 'int',
        'ocupation': 'int',
        'instructor': 'str',
        'instructor_photo': 'str',
        'area': 'str',
        'status': 'EStatusAtividade',
        'selected_spot': 'str',
        'exibir_participantes': 'bool',
        'code': 'str',
        'status_name': 'str',
        'week_day': 'int',
        'allow_choosing_spot': 'bool',
        'time_tick': 'int',
        'duration_tick': 'int',
        'start_time': 'str',
        'end_time': 'str',
        'branch_name': 'str',
        'color': 'str',
        'description': 'str',
        'image_url': 'str',
        'enrollments': 'list[AtividadeSessaoParticipanteApiViewModel]',
        'spots': 'list[AtividadeLugarReservaViewModel]',
        'title': 'str',
        'json_config_vaga_personalizada': 'str'
    }

    attribute_map = {
        'id_group_activity': 'idGroupActivity',
        'id_activity_session': 'idActivitySession',
        'id_configuration': 'idConfiguration',
        'name': 'name',
        '_date': 'date',
        'capacity': 'capacity',
        'ocupation': 'ocupation',
        'instructor': 'instructor',
        'instructor_photo': 'instructorPhoto',
        'area': 'area',
        'status': 'status',
        'selected_spot': 'selectedSpot',
        'exibir_participantes': 'exibirParticipantes',
        'code': 'code',
        'status_name': 'statusName',
        'week_day': 'weekDay',
        'allow_choosing_spot': 'allowChoosingSpot',
        'time_tick': 'timeTick',
        'duration_tick': 'durationTick',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'branch_name': 'branchName',
        'color': 'color',
        'description': 'description',
        'image_url': 'imageUrl',
        'enrollments': 'enrollments',
        'spots': 'spots',
        'title': 'title',
        'json_config_vaga_personalizada': 'jsonConfigVagaPersonalizada'
    }

    def __init__(self, id_group_activity=None, id_activity_session=None, id_configuration=None, name=None, _date=None, capacity=None, ocupation=None, instructor=None, instructor_photo=None, area=None, status=None, selected_spot=None, exibir_participantes=None, code=None, status_name=None, week_day=None, allow_choosing_spot=None, time_tick=None, duration_tick=None, start_time=None, end_time=None, branch_name=None, color=None, description=None, image_url=None, enrollments=None, spots=None, title=None, json_config_vaga_personalizada=None):  # noqa: E501
        """AtividadeBasicoApiViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_group_activity = None
        self._id_activity_session = None
        self._id_configuration = None
        self._name = None
        self.__date = None
        self._capacity = None
        self._ocupation = None
        self._instructor = None
        self._instructor_photo = None
        self._area = None
        self._status = None
        self._selected_spot = None
        self._exibir_participantes = None
        self._code = None
        self._status_name = None
        self._week_day = None
        self._allow_choosing_spot = None
        self._time_tick = None
        self._duration_tick = None
        self._start_time = None
        self._end_time = None
        self._branch_name = None
        self._color = None
        self._description = None
        self._image_url = None
        self._enrollments = None
        self._spots = None
        self._title = None
        self._json_config_vaga_personalizada = None
        self.discriminator = None
        if id_group_activity is not None:
            self.id_group_activity = id_group_activity
        if id_activity_session is not None:
            self.id_activity_session = id_activity_session
        if id_configuration is not None:
            self.id_configuration = id_configuration
        if name is not None:
            self.name = name
        if _date is not None:
            self._date = _date
        if capacity is not None:
            self.capacity = capacity
        if ocupation is not None:
            self.ocupation = ocupation
        if instructor is not None:
            self.instructor = instructor
        if instructor_photo is not None:
            self.instructor_photo = instructor_photo
        if area is not None:
            self.area = area
        if status is not None:
            self.status = status
        if selected_spot is not None:
            self.selected_spot = selected_spot
        if exibir_participantes is not None:
            self.exibir_participantes = exibir_participantes
        if code is not None:
            self.code = code
        if status_name is not None:
            self.status_name = status_name
        if week_day is not None:
            self.week_day = week_day
        if allow_choosing_spot is not None:
            self.allow_choosing_spot = allow_choosing_spot
        if time_tick is not None:
            self.time_tick = time_tick
        if duration_tick is not None:
            self.duration_tick = duration_tick
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if branch_name is not None:
            self.branch_name = branch_name
        if color is not None:
            self.color = color
        if description is not None:
            self.description = description
        if image_url is not None:
            self.image_url = image_url
        if enrollments is not None:
            self.enrollments = enrollments
        if spots is not None:
            self.spots = spots
        if title is not None:
            self.title = title
        if json_config_vaga_personalizada is not None:
            self.json_config_vaga_personalizada = json_config_vaga_personalizada

    @property
    def id_group_activity(self):
        """Gets the id_group_activity of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The id_group_activity of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_group_activity

    @id_group_activity.setter
    def id_group_activity(self, id_group_activity):
        """Sets the id_group_activity of this AtividadeBasicoApiViewModel.


        :param id_group_activity: The id_group_activity of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_group_activity = id_group_activity

    @property
    def id_activity_session(self):
        """Gets the id_activity_session of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The id_activity_session of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_activity_session

    @id_activity_session.setter
    def id_activity_session(self, id_activity_session):
        """Sets the id_activity_session of this AtividadeBasicoApiViewModel.


        :param id_activity_session: The id_activity_session of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_activity_session = id_activity_session

    @property
    def id_configuration(self):
        """Gets the id_configuration of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The id_configuration of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_configuration

    @id_configuration.setter
    def id_configuration(self, id_configuration):
        """Sets the id_configuration of this AtividadeBasicoApiViewModel.


        :param id_configuration: The id_configuration of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._id_configuration = id_configuration

    @property
    def name(self):
        """Gets the name of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The name of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AtividadeBasicoApiViewModel.


        :param name: The name of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def _date(self):
        """Gets the _date of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The _date of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this AtividadeBasicoApiViewModel.


        :param _date: The _date of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: datetime
        """

        self.__date = _date

    @property
    def capacity(self):
        """Gets the capacity of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The capacity of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this AtividadeBasicoApiViewModel.


        :param capacity: The capacity of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._capacity = capacity

    @property
    def ocupation(self):
        """Gets the ocupation of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The ocupation of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._ocupation

    @ocupation.setter
    def ocupation(self, ocupation):
        """Sets the ocupation of this AtividadeBasicoApiViewModel.


        :param ocupation: The ocupation of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._ocupation = ocupation

    @property
    def instructor(self):
        """Gets the instructor of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The instructor of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._instructor

    @instructor.setter
    def instructor(self, instructor):
        """Sets the instructor of this AtividadeBasicoApiViewModel.


        :param instructor: The instructor of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._instructor = instructor

    @property
    def instructor_photo(self):
        """Gets the instructor_photo of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The instructor_photo of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._instructor_photo

    @instructor_photo.setter
    def instructor_photo(self, instructor_photo):
        """Sets the instructor_photo of this AtividadeBasicoApiViewModel.


        :param instructor_photo: The instructor_photo of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._instructor_photo = instructor_photo

    @property
    def area(self):
        """Gets the area of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The area of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._area

    @area.setter
    def area(self, area):
        """Sets the area of this AtividadeBasicoApiViewModel.


        :param area: The area of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._area = area

    @property
    def status(self):
        """Gets the status of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The status of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: EStatusAtividade
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this AtividadeBasicoApiViewModel.


        :param status: The status of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: EStatusAtividade
        """

        self._status = status

    @property
    def selected_spot(self):
        """Gets the selected_spot of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The selected_spot of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._selected_spot

    @selected_spot.setter
    def selected_spot(self, selected_spot):
        """Sets the selected_spot of this AtividadeBasicoApiViewModel.


        :param selected_spot: The selected_spot of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._selected_spot = selected_spot

    @property
    def exibir_participantes(self):
        """Gets the exibir_participantes of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The exibir_participantes of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._exibir_participantes

    @exibir_participantes.setter
    def exibir_participantes(self, exibir_participantes):
        """Sets the exibir_participantes of this AtividadeBasicoApiViewModel.


        :param exibir_participantes: The exibir_participantes of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: bool
        """

        self._exibir_participantes = exibir_participantes

    @property
    def code(self):
        """Gets the code of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The code of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this AtividadeBasicoApiViewModel.


        :param code: The code of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def status_name(self):
        """Gets the status_name of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The status_name of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._status_name

    @status_name.setter
    def status_name(self, status_name):
        """Sets the status_name of this AtividadeBasicoApiViewModel.


        :param status_name: The status_name of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._status_name = status_name

    @property
    def week_day(self):
        """Gets the week_day of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The week_day of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._week_day

    @week_day.setter
    def week_day(self, week_day):
        """Sets the week_day of this AtividadeBasicoApiViewModel.


        :param week_day: The week_day of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._week_day = week_day

    @property
    def allow_choosing_spot(self):
        """Gets the allow_choosing_spot of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The allow_choosing_spot of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._allow_choosing_spot

    @allow_choosing_spot.setter
    def allow_choosing_spot(self, allow_choosing_spot):
        """Sets the allow_choosing_spot of this AtividadeBasicoApiViewModel.


        :param allow_choosing_spot: The allow_choosing_spot of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: bool
        """

        self._allow_choosing_spot = allow_choosing_spot

    @property
    def time_tick(self):
        """Gets the time_tick of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The time_tick of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._time_tick

    @time_tick.setter
    def time_tick(self, time_tick):
        """Sets the time_tick of this AtividadeBasicoApiViewModel.


        :param time_tick: The time_tick of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._time_tick = time_tick

    @property
    def duration_tick(self):
        """Gets the duration_tick of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The duration_tick of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: int
        """
        return self._duration_tick

    @duration_tick.setter
    def duration_tick(self, duration_tick):
        """Sets the duration_tick of this AtividadeBasicoApiViewModel.


        :param duration_tick: The duration_tick of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: int
        """

        self._duration_tick = duration_tick

    @property
    def start_time(self):
        """Gets the start_time of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The start_time of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this AtividadeBasicoApiViewModel.


        :param start_time: The start_time of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The end_time of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this AtividadeBasicoApiViewModel.


        :param end_time: The end_time of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._end_time = end_time

    @property
    def branch_name(self):
        """Gets the branch_name of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The branch_name of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._branch_name

    @branch_name.setter
    def branch_name(self, branch_name):
        """Sets the branch_name of this AtividadeBasicoApiViewModel.


        :param branch_name: The branch_name of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._branch_name = branch_name

    @property
    def color(self):
        """Gets the color of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The color of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this AtividadeBasicoApiViewModel.


        :param color: The color of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._color = color

    @property
    def description(self):
        """Gets the description of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The description of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AtividadeBasicoApiViewModel.


        :param description: The description of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def image_url(self):
        """Gets the image_url of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The image_url of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url):
        """Sets the image_url of this AtividadeBasicoApiViewModel.


        :param image_url: The image_url of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._image_url = image_url

    @property
    def enrollments(self):
        """Gets the enrollments of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The enrollments of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: list[AtividadeSessaoParticipanteApiViewModel]
        """
        return self._enrollments

    @enrollments.setter
    def enrollments(self, enrollments):
        """Sets the enrollments of this AtividadeBasicoApiViewModel.


        :param enrollments: The enrollments of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: list[AtividadeSessaoParticipanteApiViewModel]
        """

        self._enrollments = enrollments

    @property
    def spots(self):
        """Gets the spots of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The spots of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: list[AtividadeLugarReservaViewModel]
        """
        return self._spots

    @spots.setter
    def spots(self, spots):
        """Sets the spots of this AtividadeBasicoApiViewModel.


        :param spots: The spots of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: list[AtividadeLugarReservaViewModel]
        """

        self._spots = spots

    @property
    def title(self):
        """Gets the title of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The title of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this AtividadeBasicoApiViewModel.


        :param title: The title of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def json_config_vaga_personalizada(self):
        """Gets the json_config_vaga_personalizada of this AtividadeBasicoApiViewModel.  # noqa: E501


        :return: The json_config_vaga_personalizada of this AtividadeBasicoApiViewModel.  # noqa: E501
        :rtype: str
        """
        return self._json_config_vaga_personalizada

    @json_config_vaga_personalizada.setter
    def json_config_vaga_personalizada(self, json_config_vaga_personalizada):
        """Sets the json_config_vaga_personalizada of this AtividadeBasicoApiViewModel.


        :param json_config_vaga_personalizada: The json_config_vaga_personalizada of this AtividadeBasicoApiViewModel.  # noqa: E501
        :type: str
        """

        self._json_config_vaga_personalizada = json_config_vaga_personalizada

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
        if issubclass(AtividadeBasicoApiViewModel, dict):
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
        if not isinstance(other, AtividadeBasicoApiViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other