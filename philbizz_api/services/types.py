from typing import Any, Optional

class RepositoryResponse:
    def __init__(self, success: bool, message: str, data: Optional[Any] = None):
        self.success = success
        self.message = message
        self.data = data

    def __repr__(self):
        return f"<RepositoryResponse {self.success} {self.message} {self.data}>"