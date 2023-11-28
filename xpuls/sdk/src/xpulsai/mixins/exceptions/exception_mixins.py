"""Exception Mixins."""

from xpulsai.client import Client


class ExceptionMixins(Exception):
    """Exception Mixins."""

    def __init__(
        self,
        message: str,
        error_code: int | None = None,
        exception: Exception | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return_str = [f"{self.__class__.__name__}: {self.message}"]
        if self.error_code:
            return_str.append(f"Error Code: {self.error_code}")
        if self.exception:
            return_str.append(f"Exception: {self.exception}")
        return "\n".join(return_str)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"


class InvalidCredentials(ExceptionMixins):
    """Invalid Credentials."""

    def __init__(
        self,
        message: str = "Invalid Credentials.",
        error_code: int | None = 401,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class InvalidMethod(ExceptionMixins):
    """Invalid Method."""

    def __init__(
        self,
        message: str = "Invalid Method.",
        error_code: int | None = 405,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class InvalidParameter(ExceptionMixins):
    """Invalid Parameter."""

    def __init__(
        self,
        message: str = "Invalid Parameter.",
        error_code: int | None = 400,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class InvalidRequest(ExceptionMixins):
    """Invalid Request."""

    def __init__(
        self,
        message: str = "Invalid Request.",
        error_code: int | None = 400,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class InvalidResponse(ExceptionMixins):
    """Invalid Response."""

    def __init__(
        self,
        message: str = "Invalid Response.",
        error_code: int | None = 400,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class SubscriptionExpired(ExceptionMixins):
    """Subscription Expired."""

    def __init__(
        self,
        message: str = "Subscription Expired.",
        error_code: int | None = 401,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class ExpiredToken(ExceptionMixins):
    """Expired Token."""

    def __init__(
        self,
        message: str = "Invalid Token.",
        error_code: int | None = 401,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class AuthenticationError(ExceptionMixins):
    """Authentication Error."""

    def __init__(
        self,
        message: str = "Authentication Error.",
        error_code: int | None = 401,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class NotFoundError(ExceptionMixins):
    """Not Found Error."""

    def __init__(
        self,
        message: str = "Not Found Error.",
        error_code: int | None = 404,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class InternalServerError(ExceptionMixins):
    """Internal Server Error."""

    def __init__(
        self,
        message: str = "Internal Server Error.",
        error_code: int | None = 500,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class RequestTimedOut(ExceptionMixins):
    """Request Timed Out."""

    def __init__(
        self,
        message: str = "Request Timed Out.",
        error_code: int | None = 408,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class ConnectionError_(ExceptionMixins, ConnectionError):
    """Connection Error."""

    def __init__(
        self,
        message: str = "Connection Error.",
        error_code: int | None = 408,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)


class UserNotAuthenticated(ExceptionMixins):
    """User Not Authenticated."""

    def __init__(
        self,
        message: str = "User Not Authenticated.",
        error_code: int | None = 401,
        exception: Exception | None = None,
    ):
        super().__init__(message, error_code, exception)
