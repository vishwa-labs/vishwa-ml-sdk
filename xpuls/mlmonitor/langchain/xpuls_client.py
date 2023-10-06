import functools
import os
import weakref
from typing import Optional, Mapping

import requests
from langsmith import Client
from langsmith import utils as ls_utils
from urllib3 import Retry
from requests import adapters as requests_adapters
from urllib import parse as urllib_parse
import socket


def _is_localhost(url: str) -> bool:
    """Check if the URL is localhost.

    Parameters
    ----------
    url : str
        The URL to check.

    Returns
    -------
    bool
        True if the URL is localhost, False otherwise.
    """
    try:
        netloc = urllib_parse.urlsplit(url).netloc.split(":")[0]
        ip = socket.gethostbyname(netloc)
        return ip == "127.0.0.1" or ip.startswith("0.0.0.0") or ip.startswith("::")
    except socket.gaierror:
        return False


def _get_api_key(api_key: Optional[str]) -> Optional[str]:
    api_key = api_key if api_key is not None else os.getenv("XPULSAI_API_KEY")
    if api_key is None or not api_key.strip():
        return None
    return api_key.strip().strip('"').strip("'")


def _get_api_url(api_url: Optional[str], api_key: Optional[str]) -> str:
    _api_url = (
        api_url
        if api_url is not None
        else os.getenv(
            "XPULSAI_ENDPOINT",
            "https://api.xpuls.ai" if api_key else "http://localhost:8000",
        )
    )
    if not _api_url.strip():
        raise Exception("XpulsAI API URL cannot be empty")
    return _api_url.strip().strip('"').strip("'").rstrip("/")


def _default_retry_config() -> Retry:
    """Get the default retry configuration.

    Returns
    -------
    Retry
        The default retry configuration.
    """
    return Retry(
        total=3,
        allowed_methods=None,  # Retry on all methods
        status_forcelist=[502, 503, 504, 408, 425, 429],
        backoff_factor=0.5,
        # Sadly urllib3 1.x doesn't support backoff_jitter
        raise_on_redirect=False,
        raise_on_status=False,
    )


def close_session(session: requests.Session) -> None:
    """Close the session.

    Parameters
    ----------
    session : Session
        The session to close.
    """
    session.close()


class XpulsAILangChainClient(Client):

    def __init__(
            self,
            api_url: Optional[str] = None,
            *,
            api_key: Optional[str] = None,
            retry_config: Optional[Retry] = None,
            timeout_ms: Optional[int] = None,
    ) -> None:
        self.api_key = _get_api_key(api_key)
        self.api_url = _get_api_url(api_url, self.api_key)
        self.retry_config = retry_config or _default_retry_config()
        self.timeout_ms = timeout_ms or 7000
        # Create a session and register a finalizer to close it
        self.session = requests.Session()
        weakref.finalize(self, close_session, self.session)

        # Mount the HTTPAdapter with the retry configuration
        adapter = requests_adapters.HTTPAdapter(max_retries=self.retry_config)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self._get_data_type_cached = functools.lru_cache(maxsize=10)(
            self._get_data_type
        )

    @property
    def _host_url(self) -> str:
        """The web host url."""
        if _is_localhost(self.api_url):
            link = "http://localhost"
        else:
            link = self.api_url
        return link

    def request_with_retries(
        self,
        request_method: str,
        url: str,
        request_kwargs: Mapping,
    ) -> requests.Response:
        """Send a request with retries.

        Parameters
        ----------
        request_method : str
            The HTTP request method.
        url : str
            The URL to send the request to.
        request_kwargs : Mapping
            Additional request parameters.

        Returns
        -------
        Response
            The response object.

        Raises
        ------
        LangSmithAPIError
            If a server error occurs.
        LangSmithUserError
            If the request fails.
        LangSmithConnectionError
            If a connection error occurs.
        LangSmithError
            If the request fails.
        """
        try:
            response = self.session.request(
                request_method, url, stream=False, **request_kwargs
            )
            ls_utils.raise_for_status_with_text(response)
            return response
        except requests.HTTPError as e:
            if response is not None and response.status_code == 500:
                raise Exception(
                    f"Server error caused failure to {request_method} {url} in"
                    f" XpulsAI API. {e}"
                )
            else:
                raise Exception(
                    f"Failed to {request_method} {url} in XpulsAI API. {e}"
                )
        except requests.ConnectionError as e:
            raise Exception(
                f"Connection error caused failure to {request_method} {url}"
                "  in XpulsAI API. Please confirm your XPULSAI_ENDPOINT."
                f" {e}"
            ) from e
        except ValueError as e:
            args = list(e.args)
            msg = args[1] if len(args) > 1 else ""
            msg = msg.replace("session", "session (project)")
            emsg = "\n".join([args[0]] + [msg] + args[2:])
            raise ls_utils.LangSmithError(
                f"Failed to {request_method} {url} in XpulsAI API. {emsg}"
            ) from e

