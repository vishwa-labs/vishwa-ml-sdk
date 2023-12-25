import os
from typing import Optional

import requests
import time
import logging

import xpuls
from xpuls.client import constants
from xpuls.client.models import PromptResponseData


class XpulsAIClient:
    def __init__(self):
        self._host_url = xpuls.host_url
        self._api_key = xpuls.api_key

        self._headers = {"XP-API-Key": self._api_key}

    def _make_request_with_retries(self, endpoint, method='GET', data=None, retries=3, backoff_factor=2):
        """
        Make an API request with auto-retries and crashloop backoff.
        Supports GET, POST, PUT, and DELETE requests.
        """
        if endpoint.startswith("/"):
            url = f"{self._host_url}/{endpoint[1:]}"
        else:
            url = f"{self._host_url}/{endpoint}"
        for attempt in range(retries):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self._headers)
                elif method == 'POST':
                    response = requests.post(url, headers=self._headers, json=data)
                elif method == 'PUT':
                    response = requests.put(url, headers=self._headers, json=data)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=self._headers)
                else:
                    raise ValueError("Unsupported HTTP method")

                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logging.warning(f"Request failed with error {e}, attempt {attempt + 1} of {retries}")
                time.sleep(backoff_factor ** attempt)

        raise Exception("Max retries exceeded")

    def get_live_prompt(self, prompt_id: str, env_name: str) -> PromptResponseData:
        data = self._make_request_with_retries(
            endpoint=f"/v1/prompt/{prompt_id}/env/{env_name}",
            method="GET",

        )

        return PromptResponseData(**data)
