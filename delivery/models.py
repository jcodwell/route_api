from django.db import models


class FileUpload(models.Model):
    upload = models.FileField(upload_to='downloads/')


class Order(models.Model):
    order_time = models.DateTimeField()
    address = models.CharField(max_length=255)
    lat = models.FloatField()	
    lng = models.FloatField()
    home = models.BooleanField()
    delivered = models.BooleanField()
    
class Delivery(models.Model):
    is_delivered = models.BooleanField(blank=True, null=True)
    rd = models.IntegerField()
    next_dest = models.CharField(max_length=255)
    order_id = models.IntegerField()
    is_home = models.BooleanField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
