
from rest_framework import viewsets, status
from rest_framework.views import Response
from api import models, serializers
from api.integrations.github import GithubApi
from django.db import IntegrityError
# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API

class OrganizationViewSet(viewsets.ModelViewSet):

	#queryset = models.Organization.objects.all()
	serializer_class = serializers.OrganizationSerializer
	lookup_field = "login"
	http_method_names = ["get","delete"]



	def retrieve(self, request, login=None):
		"""
		   Armazenar os dados atualizados da organização no banco e

		   Retornar corretamente os dados da organização
        """

		org_inf, org_status = self.get_info_github_api_organization(login)
		serialized_org = {}
  
		if (org_status==200):
			try:
				org =  models.Organization.objects.get(pk=org_inf['login'])
				org.score = org_inf['score']
				org.name = org_inf['name']
				org.save()
				
			except models.Organization.DoesNotExist :
				org= models.Organization.objects.create(**org_inf)

			serializer = self.serializer_class(org)
			serialized_org = serializer.data

		return Response(serialized_org, status=org_status)

	def get_queryset(self):
		"""
			Retornar os dados de organizações ordenados pelo score na listagem da API
		"""
		
		return models.Organization.objects.all().order_by('-score')
	 	

	def get_info_github_api_organization(self, login: str) -> (dict, int):
		"""Buscar organização e mebros da organização pelo login através da API do Github

        :login: login da organização no Github
        """
        
		github = GithubApi()
		org_response = github.get_organization(login)
		public_members = github.get_organization_public_members(login)
		org_data = org_response.json()
		org_status= org_response.status_code
		data = {}

		if (org_status==200):

			data["login"] = org_data["login"]

			if(("name" in org_data) & (org_data["name"] is not None)):
				
				data["name"] = org_data["name"]
				
			else:
				data["name"]=""

			data["score"] = len(public_members) + org_data["public_repos"]

		return data, org_status
