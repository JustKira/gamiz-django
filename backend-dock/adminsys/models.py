
from django.db import models


def upload_path(instance, filename):
    return '/'.join(['events', str(instance.name), filename])

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=100)
    describe = models.TextField()
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class ImageList(models.Model):
    list = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
