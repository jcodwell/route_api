from django.contrib import admin
from django.urls import path,include,re_path

from .views import DeliveryView, FileUploadView, OrderView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderView)
router.register(r'delivery', DeliveryView)
router.register(r'upload', FileUploadView)
urlpatterns = [
    path('', include(router.urls)),
   
]