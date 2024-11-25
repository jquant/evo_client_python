import io
import json
from typing import Any, Dict, Optional


class RESTResponse(io.IOBase):
    """Wrapper for urllib3 response object."""

    def __init__(self, response):
        self.urllib3_response = response
        self.status = response.status
        self.reason = response.reason
        self.data = response.data

    def getheaders(self) -> Dict[str, str]:
        """Returns response headers dictionary."""
        return self.urllib3_response.headers

    def getheader(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Returns specific response header."""
        return self.urllib3_response.headers.get(name, default)

    def json(self) -> Any:
        """Returns response data as JSON."""
        content_type = self.getheader("Content-Type", "")
        if content_type and "application/json" in content_type:
            return json.loads(self.data)
        raise ValueError("Response content is not in JSON format")
