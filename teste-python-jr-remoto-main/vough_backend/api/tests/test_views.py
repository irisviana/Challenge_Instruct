
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

        

