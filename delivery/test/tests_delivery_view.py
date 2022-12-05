from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

class OrderViewsTestCase(TestCase):


    def test_get(self):
        """
        testing the order view
        """
        client = APIClient()
        url = '/api/delivery'
        client.login(username='root', password='1234')
        response = client.get(url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
    
 