"""Utils for the SDK."""

import os
import time
from typing import Dict

import requests

from xpulsai.mixins.exceptions import RequestTimedOut, ConnectionError_, ExpiredToken


def get_env(key):
    """Get environment variable."""
    return os.environ.get(key)


def make_request(url, **kwargs) -> requests.Response:
    """Make a request."""

    method = kwargs.pop("method")
    data = kwargs.pop("data")
    headers = kwargs.pop("headers")
    token = kwargs.pop("token")

    if token:
        if headers is None:
            headers = {"Authorization": f"Bearer {token}"}
        else:
            headers["Authorization"] = f"Bearer {token}"

    if method == "get":
        return requests.get(url, headers=headers)
    if method == "post":
        return requests.post(url, data=data, headers=headers)
    if method == "put":
        return requests.put(url, data=data, headers=headers)
    if method == "delete":
        return requests.delete(url, headers=headers)

    raise ValueError(f"Unsupported HTTP method: {method}")


def make_request_with_retries(url, method="get", max_retries=3, **kwargs) -> Dict:  # type: ignore
    """Wrapper around requests"""

    for i in range(max_retries):
        response = None
        try:
            response = make_request(url, method=method, **kwargs)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if i < max_retries and getattr(response, "status_code") == 408:
                # Exponential backoff
                time.sleep((i + 1) * 5)
                continue

            if isinstance(e, requests.exceptions.Timeout):
                raise RequestTimedOut(exception=e) from e
            if isinstance(e, requests.exceptions.ConnectionError):
                raise ConnectionError_(exception=e) from e
            if getattr(response, "reason") == "Token Expired":
                raise ExpiredToken(exception=e) from e

            raise e
