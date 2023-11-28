from xpulsai.base import Base
from xpulsai.utils import make_request_with_retries
from xpulsai.constants.endpoints import USER_DETAILS_ENDPOINT
from xpulsai.mixins.auth import AuthenticateMixin
from xpulsai.mixins.exceptions import UserNotAuthenticated


class Client(Base, AuthenticateMixin):
    """Xpulseai Client Class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self._set_credentials()
        self._authenticate()

        if not self.is_authenticated:
            raise UserNotAuthenticated

        self.user_info = self._fetch_user_details()

    def _fetch_user_details(self):
        """Get User Details."""
        return make_request_with_retries(
            url=USER_DETAILS_ENDPOINT,
            method="get",
            token=self._token,
        )
