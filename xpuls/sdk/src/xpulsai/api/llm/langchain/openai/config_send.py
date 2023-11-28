import json
import os
from typing import Dict, Optional


class XpulsaiConfig:
    """Portkey configuration.

    Attributes:
        base: The base URL for the Portkey API.
          Default: "https://xpulsai.com/api/v1/proxy"
    """

    base = "https://xpulsai.com/api/v1/proxy"

    @staticmethod
    def Config(
        api_key: str,
        user: Optional[str] = None,
        prompt: Optional[str] = None,
        retry_count: Optional[int] = None,
    ) -> Dict[str, str]:
        assert retry_count is None or retry_count in range(
            1, 6
        ), "retry_count must be an integer and in range [1, 2, 3, 4, 5]"

        os.environ["OPENAI_API_BASE"] = XpulsaiConfig.base

        headers = {
            "xpulsai-key": api_key,
            "xpulsai-proxy": "proxy openai",
        }

        if retry_count:
            headers["xpulsai-retry-count"] = str(retry_count)

        metadata = {}
        if user:
            metadata["_user"] = user
        if prompt:
            metadata["_prompt"] = prompt

        if metadata:
            headers.update({"xpulsai-metadata": json.dumps(metadata)})

        return headers
