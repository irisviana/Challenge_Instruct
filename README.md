# Teste Técnico Desenvolvedor(a) Python Júnior [REMOTO] da [Instruct](https://instruct.com.br/)!

Clique [aqui](https://github.com/instruct-br/teste-python-jr-remoto) para observar o enunciado original do teste:

Clique [aqui](http://vough-api-iris.herokuapp.com/) para vizualizar a Vough API no Heroku

Execução do teste base com o k6:
-Foi baixado o binário para o windows e executado o comando k6 run -e API_BASE=http://localhost:8000/ tests-open.js em Challenge_Instruct\teste-python-jr-remoto-main

## INSTRUÇÕES DE COMO EXECUTAR A APLICAÇÃO E OS TESTES.
- Clonar o repositório: git clone https://github.com/irisviana/Challenge_Instruct.git
- Depois de clonar, para executar é necessário navegar no terminal ou onde você executa os programas, Challenge_Instruct/teste-python-jr-remoto-main/vough_backend/ 
- Rodar aplicação:
    - Execute, pip install -r requirements.txt
    - Execute, python manage.py makemigrations.
    - Execute, python manage.py migrate.
    - Execute, python manage.py runserver.
    - Copie http://127.0.0.1:8000/ e cole no browser.
- Rodar os testes de unidade:
    - Execute, python manage.py test 
 
## RESOLUÇÃO DA IMPLEMENTAÇÃO
A solução final do teste pode ser dividida em quatro partes, integração da Vough API com a API do Github, implementação dos endpoints,testes de unidade e documentação da Vough API.

### Integração da Vough API com a API do Github
```
/vough_backend/api/integrations/github.py
```
Foi complementado as funções já existentes na API base disponibilizada. Na função get_organization_public_members foi tomado cuidados para que o número de mebros públicos fossem capturados corretamente, utilizando paginação no request.

```
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

        return requests.get(self.url_default+login, headers = {"Authorization": self.GITHUB_TOKEN})

    def get_organization_public_members(self, login: str) -> int:
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """

        res = requests.get(self.url_default+login+"/public_members",
                           headers={"Authorization": self.GITHUB_TOKEN})
        response = res.json()

        while 'next' in res.links.keys():
            res = requests.get(res.links['next']['url'], headers = {
                               "Authorization": self.GITHUB_TOKEN})
            response.extend(res.json())

        return response
```
### Implementação dos endpoints
```
/vough_backend/api/views.py
```
Foi implementado uma função chamada get_info_github_api_organization que busca informações da api do github e retornar o dado encontrado e o status da requisição.Foi tomado cuidados em possiveis errors no banco de dados causados por organização sem nome ou nome null e também foi calculado o score e adicionado diretamente no dicionário data.

```
def get_info_github_api_organization(self, login: str) -> (dict, int):
        """Buscar organização e mebros da organização pelo login através da API do Github
        :login: login da organização no Github
        """

        github = GithubApi()
        org_response = github.get_organization(login)
        public_members = github.get_organization_public_members(login)
        org_data = org_response.json()
        org_status = org_response.status_code
        data = {"login": "", "name": "", "score": 0}

        if (org_status == 200):

            data["login"] = org_data["login"]

            if("name" in org_data):
                
                if(org_data["name"] is not None):

                    data["name"] = org_data["name"]

            data["score"] = len(public_members) + org_data["public_repos"]

        return data, org_status

```
Foi sobrescrito a função retrieve:
```
def retrieve(self, request, login=None):
        """Armazenar os dados atualizados da organização no banco e
        Retornar corretamente os dados da organização
        """

        org_inf, org_status = self.get_info_github_api_organization(login)
        serialized_org = {}

        if (org_status == 200):
            try:
                org = models.Organization.objects.get(pk=org_inf['login'])
                org.score = org_inf['score']
                org.name = org_inf["name"]
                org.save()

            except models.Organization.DoesNotExist:
                org = models.Organization.objects.create(**org_inf)

            serializer = self.serializer_class(org)
            serialized_org = serializer.data

        return Response(serialized_org, status=org_status)
```
Foi sobrescrito a função get_queryset, para retornar os dados ordenados pelo maior score.
```
def get_queryset(self):
        """Retornar os dados de organizações ordenados pelo score na listagem da API
        """

        return models.Organization.objects.all().order_by('-score')
```

### Testes de unidade
```
\vough_backend\api\tests
```
Foi criado 4 testes de model
```
from django.test import TestCase
from api import models

# Create your tests here.

class OrganizationTest(TestCase):
    """ Test module for Organization model """

    def setUp(self):
        self.org=models.Organization.objects.create(
            login='logintest', name='test',score=10)

    def test_get_existent_org_successfully(self):
        org = models.Organization.objects.get(login='logintest')
        self.assertEqual(
            org.login, "logintest")

    def test_update_org_name_successfully(self):
        self.org.name = 'new test name'
        self.org.save()
        self.assertEqual(self.org.name, 'new test name')

    def test_update_org_score_successfully(self):
        self.org.score =20
        self.org.save()
        self.assertEqual(self.org.score, 20)

    def test_create_org_successfully(self):
        new_org=models.Organization.objects.create(
        login='login_new_org', name='new_org',score=100)
        self.assertEqual(new_org.login,'login_new_org')
```
Foi criado 8 de views.
```
from django.urls import reverse
from api .models import Organization
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from api.integrations.github import GithubApi
import numpy as np

class TestOrganizationView(APITestCase):
    
    def setUp(self):
        self.org_test=Organization.objects.create(login='logintest', name='test',score=10)
        self.org_py=Organization.objects.create(login='pythonbrasil', name='py',score=94)
        self.org_so=Organization.objects.create(login='loginso', name='SO',score=1)
        self.org_covid=Organization.objects.create(login='logincovid', name='covid',score=100)
        self.github = GithubApi()
    
    def test_list_orgs_stored(self):
        url=reverse("Organization-list")
        response=self.client.get(url)
        all_orgs=Organization.objects.all()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.json()),len(all_orgs))

    def test_get_org_success_status_code(self):
        url = '/api/orgs/{0}/'.format(self.org_py.login)
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_org_failure_status_code(self):
        url = '/api/orgs/{0}/'.format('notexist')
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_org_delete_success_status_code(self):
        url = '/api/orgs/{0}/'.format(self.org_test.login)
        request = self.client.delete(url)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_org_delete_failure_status_code(self):
        url = '/api/orgs/{0}/'.format('notexist')
        request = self.client.delete(url)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_org_github_api_successfully(self):
        response = self.github.get_organization("instruct-br")
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_retrieve_org_github_api_unsuccessfully(self):
        response = self.github.get_organization("dhjdhjdhj")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_list_orgs_ordered_by_score_successfully(self):
        url=reverse("Organization-list")
        response=self.client.get(url)
        all_orgs=Organization.objects.all()
        scores=[]
        for org in all_orgs:
            scores.append(org.score)
        self.assertEqual(np.max(scores),response.json()[0]['score'])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
```
### Documentação da Vough API.
Foi usado Swagger.
```
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Vough API",
      default_version='v1',
      description=" A Vough API:\n"+
      "1 - Buscar organização pelo login através da API do Github\n"+
      "2 - Armazenar os dados atualizados da organização no banco\n"+
      "3 - Retornar corretamente os dados da organização\n"+
      "4 - Retornar os dados de organizações ordenados pelo score na listagem da API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vianasantana21@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.routes"), name="api"),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```
