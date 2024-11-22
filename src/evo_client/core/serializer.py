from typing import Any, Type, Dict, Union
import datetime
import six


class Serializer:
    """Handles data serialization and deserialization."""

    PRIMITIVE_TYPES = (float, bool, bytes, str, int)
    NATIVE_TYPES_MAPPING = {
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "object": object,
    }

    def serialize(self, obj: Any) -> Any:
        """Serialize data for API transmission."""
        if obj is None:
            return None

        if isinstance(obj, self.PRIMITIVE_TYPES):
            return obj

        if isinstance(obj, list):
            return [self.serialize(sub_obj) for sub_obj in obj]

        if isinstance(obj, tuple):
            return tuple(self.serialize(sub_obj) for sub_obj in obj)

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        if isinstance(obj, dict):
            return {key: self.serialize(val) for key, val in obj.items()}

        # Handle Swagger models
        return {
            obj.attribute_map[attr]: self.serialize(getattr(obj, attr))
            for attr, _ in obj.swagger_types.items()
            if getattr(obj, attr) is not None
        }

    def deserialize(self, data: Any, klass: Type) -> Any:
        """Deserialize data from API response."""
        if data is None:
            return None

        if klass in self.PRIMITIVE_TYPES:
            return self._deserialize_primitive(data, klass)

        if klass == datetime.date:
            return self._deserialize_date(data)

        if klass == datetime.datetime:
            return self._deserialize_datetime(data)

        if hasattr(klass, "__origin__"):  # Handle typing annotations
            return self._deserialize_generic(data, klass)

        return self._deserialize_model(data, klass)

    def _deserialize_model(self, data: Any, klass: Type) -> Any:
        """Deserialize a dict to a model instance."""
        instance = klass()

        for attr, attr_type in instance.swagger_types.items():
            if attr in data:
                value = data[instance.attribute_map[attr]]
                setattr(instance, attr, self.deserialize(value, attr_type))

        return instance

    def _deserialize_date(self, string: str) -> datetime.date:
        """Deserialize a date string to a datetime.date object."""
        return datetime.datetime.strptime(string, "%Y-%m-%d").date()

    def _deserialize_primitive(self, data: Any, klass: Type) -> Any:
        """Deserialize primitive types (str, int, float, bool, bytes)."""
        try:
            return klass(data)
        except UnicodeEncodeError:
            return six.text_type(data)
        except TypeError:
            return data

    def _deserialize_generic(self, data: Any, klass: Type) -> Any:
        """Deserialize a generic type (list, tuple, dict)."""
        if klass == list:
            return [self.deserialize(item, list) for item in data]
        return data

    def _deserialize_datetime(self, string: str) -> datetime.datetime:
        """Deserialize a datetime string to a datetime.datetime object."""
        return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%f")
