
import requests

class GeoLocation:
     """
     Class to Call Google API, to get Lat, Lng cordinates
     """
     def __init__(self):
         self.google_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAHhqER0xLh3n4essDlZ_1yoE87ssweWb0'
         self.payload={}
         self.headers = {}
          
     def get_geolocation_by_address(self, address):
         formatted_address = '+'.join(address.split(' '))
         url = self.google_url + '&address='+ formatted_address
         response = requests.request("GET",url, headers=self.headers, data=self.payload)
         data = response.json()
         lat =data['results'][0]['geometry']['location']['lat'] 
         lng =data['results'][0]['geometry']['location']['lng']
         return (lat, lng)

         