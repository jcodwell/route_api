import imp
from django.test import TestCase
from delivery.models import Order, Delivery 
from delivery.services.delivery import DeliveryRouteInfo
from delivery.services.fileupload_service import FileUploadService


class UtilsTestCase(TestCase):
    def setUp(self):
        Order.objects.create(order_time="2022-02-11T01:00:00Z", address="1580 Benton St, Sunnyvale, CA 94087", lat=37.34100095746418, lng=-122.00009185940078, home=False, delivered=False)
        # Address is in range but cannot make return trip: so it should be out of range...
        Order.objects.create(order_time="2022-02-11T01:01:00Z", address="Address", lat=37.49683284818266, lng=-122.22764400961752, home=False, delivered=False)
        Order.objects.create(order_time="2022-02-11T01:02:00Z", address="10239 E Estates Dr, Cupertino, CA 95014", lat=37.32003392780869, lng=-122.01633925755007, home=False, delivered=False)
        print(Order.objects.all().values)
    
    def test_distance_calc(self):
        """Test to see if the distance is returning correctly"""
        dr = DeliveryRouteInfo()
        curr_order = Order.objects.get(id=1)
        dest_order = Order.objects.get(id=5)
        far_order = Order.objects.get(id=6)
        result = round(dr.get_destination_distance(dest_order, curr_order))        
        self.assertEqual(result, 4)
 
    def test_check_range(self):
        """Check if orders are in range"""
        dr = DeliveryRouteInfo()
        home_order = Order.objects.get(id=1)
        dest_order = Order.objects.get(id=2)
        out_of_range_order = Order.objects.get(id=3)
        success_result = dr.check_range_is_invalid(dest_order, home_order)
        failed_result =  dr.check_range_is_invalid(out_of_range_order, home_order)
        self.assertEqual(success_result, False) 
        self.assertEqual(failed_result, True) 
        
    
    
