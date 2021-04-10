import os
import requests


class GithubApi:
    API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

    def __init__(self):
        
        self.url_default = f"{self.API_URL}/orgs/"


    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
       
        return requests.get(self.url_default+login)


    def get_organization_public_members(self, login: str) -> int:
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        return requests.get(self.url_default+login+"/public_members")
        
        