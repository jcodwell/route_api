
# Third Party Imports
import imp
import pandas as pd 

#DRF Imports
from rest_framework import viewsets, response, parsers, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status


# imports
from .models import Order, Delivery, FileUpload
from .serializers import OrderSerializer, DeliverySerializer, FileUploadSerializer

#import utils
from.services.delivery import DeliveryRouteInfo
from.services.fileupload_service import FileUploadService
from delivery.services.customerrors import NoMoreOrders, OrderOutOfRange


file_upload_service = FileUploadService()


class FileUploadView(viewsets.ModelViewSet):
    #filter_backends = [StrictDjangoFilterBackend]
    parser_classes = [parsers.FileUploadParser] 
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()
    
    def create(self, request):
        data_frame = pd.read_csv(request.FILES.get('file'))
        file_upload_service.add_csv_to_Order_table(data_frame)
        responseMsg = "Orders Successfully Submitted"
        return response.Response(responseMsg)


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('order_time')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['delivered']
 
 
class DeliveryView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all().order_by('-id')
    
    delivery_info = DeliveryRouteInfo()
    delivery = Delivery(
        is_delivered = False,
        next_dest = "",  
        order_id=0,
        is_home = True,  
           
    )  
    def create(self, request):  
       try:
           order_obj = Order.objects.filter(delivered=False).order_by('order_time').first() 
           next_order_obj = Order.objects.filter(delivered=False, id__gt=order_obj.id).order_by('order_time').first() 
           print(next_order_obj, order_obj)      
           if next_order_obj == None or order_obj == None :        
            home_order = Order.objects.filter(address="Home", lat=33.751037297317836, lng=-84.26494314420918).first()
            home_order.delivered= True
            order_obj.delivered = True 
            order_obj.save() 
            home_order.save() 
            raise NoMoreOrders     
           if order_obj.home == True :  
               self.delivery.next_dest = self.delivery_info.get_next_destination(next_order_obj, order_obj, self.delivery)
               responseMsg = self.delivery.next_dest
               order_obj.delivered = True
               order_obj.save()   
               return response.Response(responseMsg)   
           elif order_obj.home == False :
            self.delivery.next_dest = self.delivery_info.get_next_destination(next_order_obj, order_obj, self.delivery)
            order_obj.delivered = True
            order_obj.save()          
            responseMsg = self.delivery.next_dest 
            return response.Response(responseMsg)       
           else:  
               next_order_obj.delivered = True
               next_order_obj.save()
               next_order_obj = Order.objects.filter(delivered=False, order_time__gt=order_obj.order_time).order_by('order_time').first()
        
       except OrderOutOfRange:  
        responseMsg = "Order id Out of Range: Removing order from queue", (37.308941481697225, -122.00122455940141)          
        return response.Response(responseMsg, status=status.HTTP_202_ACCEPTED)
       except NoMoreOrders:
        responseMsg = "All Orders Completed: Heading Home", self.delivery_info.home_geo_loc  
        return response.Response(responseMsg)
       except AttributeError:
        responseMsg = "No Orders", self.delivery_info.home_geo_loc   
        return response.Response(responseMsg)
            
    