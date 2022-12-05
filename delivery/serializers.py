from rest_framework import serializers

from .models import FileUpload, Order, Delivery

class FileUploadSerializer(serializers.ModelSerializer):
         class Meta:
             model = FileUpload
             fields = '__all__'
  

class OrderSerializer(serializers.ModelSerializer):
     class Meta:
        model = Order
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
         class Meta:
             model = Delivery
             fields = '__all__'


