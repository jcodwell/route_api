#Python and other imports 
import pandas as pd 
import datetime

#App Imports
from delivery.models import Order

#Utils Imports
from .geoloaction import GeoLocation
        
class FileUploadService: 
       def __init__(self):
           self.geo_location=GeoLocation()
       
       def add_csv_to_Order_table(self, data_frame):
        for orders in data_frame.values:  
            location = self.geo_location.get_geolocation_by_address(str(orders[1]))
            order = Order (
             order_time= datetime.datetime.strptime(orders[0], "%d/%m/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S'),
             address=orders[1][:-6],
             lat = 0,
             lng = 0,
             home=False,
             delivered=False       
         )
            order.lat = location[0]
            order.lng = location[1]
            order.save()
        return order