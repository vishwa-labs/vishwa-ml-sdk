from typing import List

from pydantic import BaseModel


class PromptVariable(BaseModel):
    variable: str
    default: str


class PromptResponseData(BaseModel):
    prompt_version_id: str
    prompt_id: str
    prompt_external_id: str
    prompt: str
    prompt_variables: List[PromptVariable]


class XPPrompt(BaseModel):
    prompt_version_id: str
    prompt_id: str
    prompt_external_id: str
    prompt: str

