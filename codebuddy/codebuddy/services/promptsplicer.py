from github import Github
import textwrap
from codebuddy.model.dataclasses import APIkeys, FileDetails, PromptConfiguration, Prompt


class PromptSplicer:

    def __init__(self):
        self.git_api_key = APIkeys.git
        self.openai_api_key = APIkeys.openai

    def unpack_optimisations(self, input):

        optimisations = ''

        if len(input.optimisations) != 0:
            for optimisation in input.optimisations:
                optimisations = optimisations + f'\n - {optimisation}'
            
        return optimisations


    def build_prompt(self, input: list) -> list:

        prompts = []
        
        for file in input:
            
            optimisations = self.unpack_optimisations(file)

            if len(optimisations) != 0:
                prompt = f'''
                    \nPlease see the below code
                    \n{file.decoded_content}
                    \nYour task is to optimise it for
                    \n{optimisations}
                    \nPlease return only the edited code file
                    '''

            else:
                prompt = f'''                
                    \nPlease see the below code
                    \n{file.decoded_content}
                    \nThere are no specific optimisations to be made
                    \nPlease return only the edited code file
                    '''
                
            new_prompt = Prompt(
                filename=file.filename,
                path=file.path,
                repolink=file.repolink,
                prompt=prompt,
                decoded_content=file.decoded_content,
                temperatureValue=file.temperatureValue,
                presence_penalty=file.presence_penalty,
                frequency_penalty=file.frequency_penalty
            )

            prompts.append(new_prompt)
        
        return prompts