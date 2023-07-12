from github import Github
import textwrap
import openai
from codebuddy.model.dataclasses import APIkeys, FileDetails, PromptConfiguration, Prompt, OptimisedOutputs
from textwrap import dedent


class PromptSender:

    def __init__(self):
        self.git_api_key = APIkeys.git
        self.openai_api_key = APIkeys.openai

    def send_prompt_to_model(self, system_message, prompt_object):
        openai.api_key = self.openai_api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt_object.prompt
                }
            ],
            temperature=prompt_object.temperatureValue,
            frequency_penalty=prompt_object.frequency_penalty,
            presence_penalty=prompt_object.presence_penalty
        )

        return response["choices"][0]["message"]["content"].strip()
    

    def optimise_code_batch(self, prompt_list: list, system_prompt: str) -> list:

        optimised_outputs = []

        for prompt in prompt_list:
            optimised_output = OptimisedOutputs(
                filename=prompt.filename,
                path=prompt.path,
                repolink=prompt.repolink,
                decoded_content=f'\n{prompt.decoded_content}',
                optimised_content = f'\n{self.send_prompt_to_model(system_prompt, prompt)}',
                temperatureValue=prompt.temperatureValue,
                presence_penalty=prompt.presence_penalty,
                frequency_penalty=prompt.frequency_penalty,
            )
            optimised_outputs.append(optimised_output)

            print(optimised_output.optimised_content)

        return optimised_outputs