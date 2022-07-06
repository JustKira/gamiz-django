
from pyexpat import model
from venv import create
from rest_framework import serializers
from orders.models import Order, CustomImage


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomImage
        fields = '__all__'
