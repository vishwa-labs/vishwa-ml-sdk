from xpulsai.base import Base
from xpulsai.utils import make_request_with_retries
from xpulsai.constants.endpoints import USER_DETAILS_ENDPOINT
from xpulsai.mixins.auth import AuthenticateMixin


class Client(Base, AuthenticateMixin):
    """Xpulseai Client Class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self._set_credentials()
        self._authenticate()

    def _fetch_user_details(self):
        """Get User Details."""
        make_request_with_retries(
            url=USER_DETAILS_ENDPOINT,
            method="get",
            token=self._token,
        )
