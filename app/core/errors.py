from fastapi import status


class CoreError(Exception):
    detail: str = "An internal server error occurred."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers : dict[str,str] | None = None

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

# 4xx
class BadRequest(CoreError):
    status_code = status.HTTP_400_BAD_REQUEST

class Unauthorized(CoreError):
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate" : "Bearer"}

class Forbidden(CoreError):
    status_code = status.HTTP_403_FORBIDDEN
class NotFound(CoreError):
    status_code = status.HTTP_404_NOT_FOUND
class Conflict(CoreError):
    status_code = status.HTTP_409_CONFLICT
class TooManyRequests(CoreError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

# 5xx
class InternalServerError(CoreError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
class ServiceUnavailable(CoreError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


