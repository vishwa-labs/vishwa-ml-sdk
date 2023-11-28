"""Manage API for Xpulsai"""

from xpulsai.client import Client
from xpulsai.utils import make_request_with_retries
from xpulsai.constants.endpoints import (
    USER_GET_KEYS_ENDPOINT,
    USER_MANAGE_KEYS_ENDPOINT,
)
from xpulsai.mixins.exceptions import ExpiredToken


class Manage(Client):
    """Manage API for Xpulsai"""

    def __init__(self):
        super().__init__()
        self.saved_keys = self.get_saved_keys()

    def get_user_details(self):
        return self.user_info

    def get_saved_keys(self):
        try:
            return make_request_with_retries(
                USER_GET_KEYS_ENDPOINT, method="GET", token=self._token
            )
        except ExpiredToken:
            ExpiredToken.handler(self)

    def add_key(self, key: str):
        """Add a key to your account."""
        try:
            return make_request_with_retries(
                USER_MANAGE_KEYS_ENDPOINT,
                method="POST",
                token=self._token,
                data={"key": key},
            )
        except ExpiredToken:
            ExpiredToken.handler(self)

        except Exception as e:
            raise e

    def delete_key(self, key: str):
        """Delete a key from your account."""
        try:
            return make_request_with_retries(
                USER_MANAGE_KEYS_ENDPOINT,
                method="DELETE",
                token=self._token,
                data={"key": key},
            )
        except ExpiredToken:
            ExpiredToken.handler(self)

        except Exception as e:
            raise e
