from ast import Delete
import json
import re
from webbrowser import get
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import EventSerializer, ImageListSerializer
from adminsys.models import Event, ImageList
# from adminsys.imageProcessing import customizeMockup, customizeMockup_console
from adminsys.onedriveapi import refreshLaptops
from pathlib import Path
import requests
import os
import re
BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(['GET'])
def getEvent(request, pk):
    queryset = Event.objects.get(id=pk)
    serializer = EventSerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getEvents(request):
    queryset = Event.objects.all()
    serializer = EventSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def eventCreate(request):

    serializer = EventSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer._errors)


@api_view(['PATCH'])
def eventUpdate(request, pk):
    event = Event.objects.get(id=pk)
    serializer = EventSerializer(
        instance=event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def eventDelete(request, pk):
    event = Event.objects.get(id=pk)
    print(f"{settings.MEDIA_ROOT}\{event.image}")
    try:
        os.remove(f"{settings.MEDIA_ROOT}\{event.image}")
    except:
        try:
            os.remove(f"{settings.MEDIA_ROOT}/{event.image}")
        except:
            pass
    event.delete()
    return Response('Deleted')


@api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUser])
def refresh(request):
    data = request.data
    rl_download = refreshLaptops(data['code'])
    index = 0

    for rl in rl_download:
        url = rl
        r = requests.get(url, allow_redirects=True)
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0]
        #example : media/products/raw/product7.png
        open(os.path.join(settings.MEDIA_ROOT,
                          'products/raw/product{}.png'.format(fname[:fname.find('.')].strip("'").strip('"'))),
             'wb').write(r.content)
        print(fname[:fname.find('.')].strip("'").strip('"'))
        # customizeMockup(os.path.join(settings.MEDIA_ROOT,
        #                              'products/raw/product{}.png'.format(index)), os.path.join(settings.MEDIA_ROOT,
        #                                                                                        'products/done/product{}'.format(index)))
        # customizeMockup_console(os.path.join(settings.MEDIA_ROOT,
        #                                      'products/raw/product{}.png'.format(index)), os.path.join(settings.MEDIA_ROOT,
        #                                                                                                'products/done/product_console{}'.format(index)))
        index += 1
    try:
        list = ImageList.objects.get(id=1)
        list.list = index
        list.save()
    except:
        list = ImageList.create(index)
        list.save()

    return Response('Refreshed')


@api_view(['GET'])
def getImagesCount(request):
    queryset = ImageList.objects.get(id=1)
    serializer = ImageListSerializer(queryset, many=False)
    return Response(serializer.data)
