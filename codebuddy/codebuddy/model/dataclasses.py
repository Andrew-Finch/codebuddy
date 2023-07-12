
from dataclasses import dataclass
import os

@dataclass
class FileDetails:
    filename: str
    path: str
    repo: str
    fileextension: str
    filelength: str
    filesize: str
    repolink: str
    tokens: int
    cost: float
    decoded_content: str

@dataclass
class Order:
    order_id: str
    filetypes: list
    repo: str
    files: list[FileDetails]

@dataclass
class PromptConfiguration:
    filename: str
    path: str
    repolink: str
    decoded_content: str
    optimisations: list
    temperatureValue: float
    presence_penalty: float
    frequency_penalty: float

@dataclass
class Prompt:
    filename: str
    path: str
    repolink: str
    decoded_content: str
    prompt: str
    temperatureValue: float
    presence_penalty: float
    frequency_penalty: float

@dataclass
class OptimisedOutputs:
    filename: str
    path: str
    repolink: str
    decoded_content: str
    optimised_content: str
    temperatureValue: float
    presence_penalty: float
    frequency_penalty: float




@dataclass(frozen=True)
class APIkeys:
    openai: str = os.environ.get('openai_api_key')
    git: str = os.environ.get('git_api_key') 
