"""Module for the features endpoint."""

from xpulsai.client import Client
from xpulsai.utils import make_request_with_retries
from xpulsai.mixins.exceptions import ExpiredToken
from xpulsai.constants.endpoints import USER_GET_LAST_K_INTERACTIONS_ENDPOINT


class Features(Client):
    """Features API for Xpulsai"""

    def __init__(self):
        """Features API for Xpulsai"""
        super().__init__()

    def get_last_k_interactions(self, k: int = 10):
        """Get the last k interactions."""
        try:
            return make_request_with_retries(
                USER_GET_LAST_K_INTERACTIONS_ENDPOINT,
                method="GET",
                token=self._token,
                data={"k": k},
            )

        except ExpiredToken:
            ExpiredToken.handler(self)

        except Exception as e:
            raise e
