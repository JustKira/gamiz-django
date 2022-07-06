import imp
from pyexpat import model
from django.db import models
from customUser.models import CustomUser
# Create your models here.


class Order(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_json = models.TextField(null=False)

    def __str__(self):
        return "Order_Num" + str(self.id)


def upload_path(instance, filename):
    return '/'.join(['products/custom/raw', filename])


class CustomImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)
