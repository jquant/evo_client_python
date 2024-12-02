import io
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
    get_args,
    get_origin,
    overload,
)

from pydantic import BaseModel
from requests import Response

T = TypeVar("T", bound=BaseModel)


class RESTResponse(io.IOBase):
    """Wrapper for requests Response object."""

    def __init__(self, response: Response):
        self.requests_response = response
        self.status = response.status_code
        self.reason = response.reason
        self.data = response.content

    def getheaders(self) -> Dict[str, str]:
        """Returns response headers dictionary."""
        return dict(self.requests_response.headers)

    def getheader(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Returns specific response header."""
        return self.requests_response.headers.get(name, default)

    def json(self) -> Any:
        """Returns response data as JSON."""
        content_type = self.getheader("Content-Type", "")
        if content_type and "application/json" in content_type:
            return self.requests_response.json()
        raise ValueError("Response content is not in JSON format")

    @overload
    def deserialize(self, response_type: Type[T]) -> T: ...

    @overload
    def deserialize(self, response_type: Type[Iterable[T]]) -> List[T]: ...

    def deserialize(self, response_type: Type[T] | Type[Iterable[T]]) -> T | List[T]:
        """Deserialize response data into the specified type."""
        if isinstance(response_type, type) and issubclass(response_type, BaseModel):
            return response_type.model_validate(self.json())

        # Handle generic types like List[SomeBaseModel]
        origin = get_origin(response_type)
        if origin is list:
            item_type = get_args(response_type)[0]
            return list(item_type.model_validate(item) for item in self.json())

        # Direct construction for simple types
        return response_type(**self.json())  # type: ignore
