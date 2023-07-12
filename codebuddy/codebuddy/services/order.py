from codebuddy.model.dataclasses import APIkeys, FileDetails, Order, PromptConfiguration
import ast
import base64
import os
import random
import datetime
from github import Github

class OrderCreator:
    def __init__(self):
        self.git_api_key = APIkeys.git
        self.openai_api_key = APIkeys.openai

    def review_order(self, input):

        order_files = []
        filetypes = []
        repo = str
        today = datetime.date.today()

        g = Github(self.git_api_key)

        for file in input:
            
            dictionary_obj = ast.literal_eval(input[file])
            repo = g.get_repo(dictionary_obj['repo'])

            file_object = FileDetails(       
                filename=dictionary_obj['filename'],
                path=dictionary_obj['path'],
                repo=dictionary_obj['repo'],
                fileextension=dictionary_obj['fileextension'],
                filelength=dictionary_obj['filesize'],
                filesize=dictionary_obj['filesize'],
                repolink=dictionary_obj['repolink'],
                tokens=dictionary_obj['tokens'],
                cost=dictionary_obj['cost'],
                decoded_content= base64.b64decode(repo.get_contents(dictionary_obj['path'], ref='master').content).decode('utf-8')
                )
            

            order_files.append(file_object)
            filetypes.append(file_object.fileextension)
            repo = file_object.repo

        order = Order(
            order_id=f'{random.randint(1,10000)}-{today.strftime("%Y-%m-%d")}',
            repo=repo,
            filetypes=list(set(filetypes)),
            files=order_files
        )

        return order
    
    def process_order(self, input_dict):
        files_in_order = list(set(file.split("-", 1)[0] for file in input_dict if '.' in file))
        print(files_in_order)
        
        prompts = []

        g = Github(self.git_api_key)
        repo = g.get_repo(input_dict['repo'])

        for file in files_in_order:

            prompting = [prompt for prompt in ['speed', 'readability', 'sustainability'] if f'{file}-{prompt}' in input_dict.keys()]
            
            if '.' in file:
                decoded_content=base64.b64decode(repo.get_contents(input_dict[f'{file}-path'], ref='master').content).decode('utf-8')
                prompt_config = PromptConfiguration(
                    filename=file,
                    path=input_dict[f'{file}-path'],
                    repolink=repo.get_contents(input_dict[f'{file}-path'], ref='master').html_url,
                    decoded_content=decoded_content,
                    optimisations=prompting,
                    temperatureValue=float(input_dict[f'{file}-temperatureValue']),
                    presence_penalty=float(input_dict[f'{file}-presence_penalty']),
                    frequency_penalty=float(input_dict[f'{file}-frequency_penalty'])
                )

            prompts.append(prompt_config)
        
        return prompts






