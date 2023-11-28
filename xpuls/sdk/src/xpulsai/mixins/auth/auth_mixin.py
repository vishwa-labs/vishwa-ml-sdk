"""Auth Mixin."""

from abc import ABC

from xpulsai.utils import get_env, make_request_with_retries
from xpulsai.constants.endpoints import SDK_AUTH_ENDPOINT
from xpulsai.mixins.exceptions import InvalidCredentials, NotFoundError


class AuthenticateMixin(ABC):
    """Authenticate Mixin."""

    def __init__(self):
        """Initialize."""

        self._set_credentials()
        self._authenticate()

    def _set_credentials(self):
        """Set Credentials."""
        try:
            self._access_key = get_env("XPULSAI_ACCESS_KEY")
        except Exception as e:
            raise NotFoundError(message="Credentials Not Found", exception=e) from e

    def _authenticate(self):
        """Authenticate."""
        try:
            self._token = make_request_with_retries(
                url=SDK_AUTH_ENDPOINT,
                method="post",
                data={"access_key": self._access_key},
            )["data"]["token"]
            self.is_authenticated = True

        except Exception as e:
            raise InvalidCredentials(exception=e) from e

    @staticmethod
    def re_authenticate(obj):
        """Re-Authenticate."""
        obj.is_authenticated = False
        obj._authenticate()

    def check_auth(self):
        """Check if authenticated."""
        if not self.is_authenticated:
            self.re_authenticate(self)
        return True
