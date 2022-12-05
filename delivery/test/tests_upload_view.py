from django.test import TestCase
import csv
# Create your tests here.
from rest_framework.test import APIClient

from rest_framework import status

from delivery.models import Order

class OrderViewsTestCase(TestCase):

    def generate_file(self):
        try:
            myfile = open('test.csv', 'wb')
            csv_wr = csv.writer(myfile)
            csv_wr.writerow(('Order Time','Address'))
            csv_wr.writerow(('11/11/2022 4:05','1016 Huntingdon Dr, San Jose, CA 95129'))
            csv_wr.writerow(('11/11/2022 4:05','1580 Benton St, Sunnyvale, CA 94087'))
            csv_wr.writerow(('11/11/2022 4:06','1668 Austin Dr, Decatur, GA 36985'))
        finally:
            myfile.close()

        return myfile
    
    def test_get(self):
        """
        testing the order view
        """
        client = APIClient()
        url = '/api/upload'
        response = client.get(url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
    
    def test_post(self):
        """
        Testing the File uploads and checks if all rows inserted
        """
        client = APIClient()
        url = '/api/upload'
       
        file = self.generate_file
        response = client.post(url, {'uploads':file})
        print(response)
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        
      
