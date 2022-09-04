
from venv import create
from rest_framework import serializers
from customUser.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            username=validated_data['username'],
            birthday=validated_data['birthday'],
            phone=validated_data['phone'],
            governorate=validated_data['governorate'],
            area=validated_data['area'],
            district=validated_data['district'],
        )

        return user
