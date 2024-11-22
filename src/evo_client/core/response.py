from typing import Optional, Dict
import io


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
