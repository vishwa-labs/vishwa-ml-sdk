from typing import Dict
import re

from xpuls.client import XpulsAIClient
from xpuls.client.models import XPPrompt


class PromptClient:
    def __init__(self, prompt_id: str, environment_name: str):
        self._client = XpulsAIClient()
        self._prompt_id = prompt_id
        self._env_name = environment_name

    def get_prompt(self, variables: Dict[str, str]) -> XPPrompt:
        data = self._client.get_live_prompt(
            prompt_id=self._prompt_id,
            env_name=self._env_name
        )
        """
        Substitute variables in the prompt.
    
        Args:
        prompt (str): The prompt string with placeholders for variables.
        variables (Dict[str, str]): A dictionary of variable names and their values.
    
        Returns:
        str: The prompt with variables substituted.
        """
        default_value = ""  # Default value for variables not provided in the dictionary

        # Extracting variable names from the prompt
        prompt_variables = set(re.findall(r'\{\{(.+?)\}\}', data.prompt))
        prompt = data.prompt
        for variable in prompt_variables:
            # Substitute the variable with its value or default value
            value = variables.get(variable, default_value)
            prompt = prompt.replace(f'{{{{{variable}}}}}', value)

        return XPPrompt(
            **{
                "prompt_version_id": data.prompt_version_id,
                "prompt_id": data.prompt_id,
                "prompt_external_id": data.prompt_external_id,
                "prompt": prompt
            }
        )
