from abc import ABC


class Base(ABC):
    """Base Class."""

    def __init__(self):
        """Initialize."""

        super().__init__()
        self._access_key = None
        self._access_key = None
        self._secret_key = None
        self._token = None
        self.is_authenticated = False

        self.user_info = None
