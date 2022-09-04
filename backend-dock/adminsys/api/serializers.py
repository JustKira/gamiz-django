
from rest_framework import serializers
from adminsys.models import Event, ImageList


class EventSerializer(serializers.ModelSerializer):

    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Event
        fields = '__all__'


class ImageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageList
        fields = '__all__'
