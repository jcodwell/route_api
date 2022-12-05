

from math import cos, sqrt
from turtle import distance

from delivery.models import Delivery, Order
from delivery.services.customerrors import OrderOutOfRange

class DeliveryRouteInfo:
     def __init__(self):
         self.home_geo_loc = (37.308941481697225, -122.00122455940141)
                    
     def get_destination_distance(self, dest_geo_loc: Order, current_geo_loc: Order):
        """ Takes the current location and the destination location.
            returns the distance between the cordinates.
         Args:
             dest_geo_loc (Order):Order
             current_geo_loc (Order): Order

         Returns:
             _type_: Float
        """
        x = dest_geo_loc.lat -  current_geo_loc.lat
        y = (dest_geo_loc.lng -  current_geo_loc.lng) * cos((dest_geo_loc.lat +   current_geo_loc.lat)*0.00872664626)  
        return 111.319 * sqrt(x*x + y*y)
    
     def get_distance_home(self,current_geo_loc: Order):
        """ 
         Takes the current location and returns the distance to return to pizza shop.
         Args:
             current_geo_loc (Order): Order
         Returns:
             _type_: float
        """
        x =  self.home_geo_loc[0] -  current_geo_loc.lat
        y = (self.home_geo_loc[1] -  current_geo_loc.lng) * cos((self.home_geo_loc[0] +   current_geo_loc.lat)*0.00872664626)  
        return 111.319 * sqrt(x*x + y*y)
    
     def check_range_is_invalid(self, dest, curr):
        """ 
        Check if distance is in range. 
         Args:
             dest (Order): Order
             curr (Order): Order
         Returns:
             _type_: Boolean
        """         
        if self.get_destination_distance(dest, curr) + self.get_destination_distance(curr, dest) > 40:
            return True
        else:
            return False
         
         
     def get_next_destination(self, dest_geo_loc: Order, current_order: Order, delivery: Delivery):
            """ 
             Get the next destination for the drone.
             Args:
               dest_geo_loc (Order): Order
               current_geo_loc (Order): Order
               delivery (Delivery): delivery
             Returns:
               _type_: String
           """              
            if self.check_range_is_invalid(dest_geo_loc, current_order) == False:
             last_delivery = Delivery.objects.all().first()
             distance = self.get_destination_distance(dest_geo_loc, current_order)
             if current_order.home == True:
                 rd = last_delivery.rd - distance
                 delivery.order_id = current_order.id
                 delivery.is_home = False
                 delivery.next_dest = str((dest_geo_loc.lat, dest_geo_loc.lng))          
                 delivery.is_delivered = True 
                 delivery.rd = rd
                 delivery.save()
                 return(dest_geo_loc.lat, dest_geo_loc.lng)
             else:
                 last_delivery = Delivery.objects.all().first() 

                 distance_to_home = self.get_distance_home(current_order) 
                 rd = last_delivery.rd - distance
                 if rd > distance and rd > distance_to_home:
                   delivery.order_id = current_order.id
                   delivery.is_home = False
                   delivery.next_dest = str((dest_geo_loc.lat, dest_geo_loc.lng))       
                   delivery.is_delivered = True
                   delivery.rd = rd 
                   delivery.save() 
                   return(dest_geo_loc.lat, dest_geo_loc.lng)
                 else:
                   delivery.order_id = current_order.id
                   delivery.is_home = True
                   delivery.next_dest = "(" + str(self.home_geo_loc) + ")"          
                   delivery.is_delivered = True
                   delivery.rd = 40 
                   delivery.save()
                   return self.home_geo_loc
            else:
                Order.objects.create (order_time="2022-01-11T01:00:00Z", 
                               address="Home", 
                               lat=37.308941481697225, 
                               lng=-122.00122455940141, 
                               home=True, 
                               delivered=False)
    
                delivery.order_id = current_order.id
                delivery.is_home = False
                delivery.next_dest = "(" + str(self.home_geo_loc) + ")"          
                delivery.is_delivered = False
                delivery.rd = 40 
                delivery.save()  
                dest_geo_loc.delete()
                raise OrderOutOfRange
               



                  
             

