import base64
import os
from github import Github
from codebuddy.model.dataclasses import APIkeys, FileDetails
import tiktoken

class PromptCoster:

    def __init__(self):
        self.git_api_key = APIkeys.git
        self.openai_api_key = APIkeys.openai

    def count_tokens(self, input: str) -> int:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        encoding.encode(input)

        token_count = len(encoding.encode(input))

        return int(token_count)
    
    def calculate_cost(self, token_count: int, rate: int = 1000, price_per_rate_in_pounds: float = 0.06) -> float:
        cost = (token_count / rate) * price_per_rate_in_pounds

        
        return "{0:.1g}".format(cost)