from typing import Dict, Any, Type, Optional, ClassVar
from datetime import datetime, date


class SwaggerModel:
    """Base class for all Swagger-generated models."""

    # Class variables that should be defined by child classes
    swagger_types: ClassVar[Dict[str, str]] = {}
    attribute_map: ClassVar[Dict[str, str]] = {}

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a model with given attributes."""
        # Set all properties to None by default
        for attr in self.swagger_types:
            setattr(self, attr, None)

        # Update with any provided values
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    @classmethod
    def get_real_child_model(
        cls, data: Dict[str, Any]
    ) -> Optional[Type["SwaggerModel"]]:
        """
        Get the real child model for discriminator.
        Should be overridden by child classes that implement discriminator.
        """
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        result = {}

        for attr, _ in self.swagger_types.items():
            value = getattr(self, attr)
            if value is not None:
                if isinstance(value, list):
                    result[self.attribute_map[attr]] = [
                        x.to_dict() if hasattr(x, "to_dict") else x for x in value
                    ]
                elif hasattr(value, "to_dict"):
                    result[self.attribute_map[attr]] = value.to_dict()
                elif isinstance(value, (datetime, date)):
                    result[self.attribute_map[attr]] = value.isoformat()
                else:
                    result[self.attribute_map[attr]] = value

        return result

    def to_str(self) -> str:
        """Returns string representation of the model."""
        return str(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: Any) -> bool:
        """Returns true if both objects are equal."""
        if not isinstance(other, SwaggerModel):
            return False
        return self.to_dict() == other.to_dict()

    def __ne__(self, other: Any) -> bool:
        """Returns true if both objects are not equal."""
        return not self == other
