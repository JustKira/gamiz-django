import imp
from django.contrib import admin
from .models import CustomImage, Order
# Register your models here.
admin.site.register(Order)
admin.site.register(CustomImage)
