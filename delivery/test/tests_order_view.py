from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.test import force_authenticate
from django.urls import reverse
from rest_framework import status

class OrderViewsTestCase(TestCase):


    def test_get(self):
        """
        testing the order view
        """
        client = APIClient()
        url = '/api/orders'
        response = client.get(url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
    
    def test_post(self):
        """ 
        testing the order view
        """
        client = APIClient()
        order =   {"order_time":"2022-02-11T01:01:00Z", "address":"Address", "lat":37.49683284818266, "lng":-122.22764400961752, "home":False, "delivered":False}
        url = '/api/orders'
        response = client.post(url, order, format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)    
      
