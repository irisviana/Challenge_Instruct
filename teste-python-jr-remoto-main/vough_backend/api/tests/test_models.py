from django.test import TestCase
from api import models

# Create your tests here.

class OrganizationTest(TestCase):
    """ Test module for Organization model """

    def setUp(self):
        self.org=models.Organization.objects.create(
            login='logintest', name='test',score=10)

    def test_get_existent_org(self):
        org = models.Organization.objects.get(login='logintest')
        self.assertEqual(
            org.login, "logintest")

    def test_update_org_name(self):
        self.org.name = 'new test name'
        self.org.save()
        self.assertEqual(self.org.name, 'new test name')

    def test_update_org_score(self):
        self.org.score =20
        self.org.save()
        self.assertEqual(self.org.score, 20)

    def test_create_org_successfully(self):
        new_org=models.Organization.objects.create(
        login='login_new_org', name='new_org',score=100)
        self.assertEqual(new_org.login,'login_new_org')

    

