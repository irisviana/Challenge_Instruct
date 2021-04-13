
from django.urls import reverse, resolve
from api .models import Organization
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

class TestOrganizationView(APITestCase):
    
    def setUp(self):
        self.org_test=Organization.objects.create(login='logintest', name='test',score=10)
        self.org_py=Organization.objects.create(login='pythonbrasil', name='py',score=94)
         
    def test_list_orgs_stored(self):
        url=reverse("Organization-list")
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

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
        
        

