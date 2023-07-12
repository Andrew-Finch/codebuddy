import base64
import os
from github import Github
from codebuddy.model.dataclasses import APIkeys, FileDetails
from codebuddy.services.promptcoster import PromptCoster

class RepoWrangler:

    def __init__(self):
        self.git_api_key = APIkeys.git
        self.pc = PromptCoster()

    def get_python_file_contents(self, contents, repo, filetypes=None):

        if filetypes is None:
            filetypes = []

        python_files = []
        allowed_files = ['py', 'html']

        for content in contents:
            if content.type == 'dir':  # If the content is a directory, recurse into it
                new_contents = repo.get_contents(content.path, ref='master')

                new_python_files, new_filetypes = self.get_python_file_contents(new_contents, repo, filetypes)
                python_files.extend(new_python_files)
                filetypes.extend(new_filetypes)

            elif content.type == 'file' and content.name.split(".", 1)[1] in allowed_files:

                # grab and decode content
                file_content = repo.get_contents(content.path, ref='master').content
                decoded_content = base64.b64decode(file_content).decode('utf-8')

                # get file extension
                extension = content.name.split(".", 1)[1]
  
                # get file length
                length = len(decoded_content)

                # get file size
                file_size = repo.get_contents(content.path, ref='master').size

                # get url
                url = repo.get_contents(content.path, ref='master').html_url

                # get token length
                tokens = self.pc.count_tokens(decoded_content)

                # get token length
                cost = self.pc.calculate_cost(tokens)

                file_object = FileDetails(
                    filename=content.name,
                    path=content.path,
                    repo=repo,
                    fileextension='.' + extension,
                    filelength=length,
                    filesize=file_size,
                    repolink=url,
                    tokens=tokens,
                    cost=cost,
                    decoded_content=decoded_content)
                
                python_files.append(file_object)
                if extension not in filetypes:
                    filetypes.append(extension)

        return python_files, list(set(filetypes))
    

    def get_directory_structure(self, token, repo_path):

        def get_directory_contents(self, contents):
            result = []
            for item in contents:
                if item.type == "dir":
                    sub_contents = repo.get_contents(item.path, ref="master")
                    result.append({"name": item.name, "type": "dir", "children": get_directory_contents(self, sub_contents)})
                else:
                    result.append({"name": item.name, "type": "file", "url": item.html_url})
            return result

        g = Github(token)
        repo = g.get_repo(repo_path)
        contents = repo.get_contents("", ref="master")

        return get_directory_contents(self, contents)
    
    def generate_html_structure(self, data):
        html = "<ul>"
        for item in data:
            if item["type"] == "dir":
                html += f'<li><strong>{item["name"]}</strong>'
                html += self.generate_html_structure(item["children"])
                html += "</li>"
            else:
                html += f'<li> <a href="{item["url"]}" >{item["name"]}</a> </li>'
        html += "</ul>"
        return html


    def get_repo(self, repo, token):

        g = Github(token)
        repo = g.get_repo(repo)
        contents = repo.get_contents("", ref='master')

        # Get all Python files as strings
        python_files, filetypes = self.get_python_file_contents(contents, repo)

        dir_structure = self.get_directory_structure(token, repo.full_name)
        dir_structure_html = self.generate_html_structure(dir_structure)

        return python_files, filetypes, dir_structure_html
