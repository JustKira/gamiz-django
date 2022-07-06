import json
from random import randint
import os
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from adminsys.imageProcessing import customizeMockup
from adminsys.imageProcessing import customizeMockup_console
from .serializers import CISerializer, OrderSerializer
from orders.models import Order, CustomImage
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from customUser.models import CustomUser
import shutil
from adminsys.gsheet import update_order_sheet


@api_view(['GET'])
def getOrder(request, pk):
    queryset = Order.objects.get(id=pk)
    serializer = OrderSerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getOrderAll(request, pk):
    user = CustomUser.objects.get(id=pk)
    queryset = Order.objects.filter(user=user)
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data)

#os.path.join(settings.BASE_DIR, 'media')


@api_view(['POST'])
def orderCreate(request, pk):

    if(pk != "0"):
        try:
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'tmp\done\customProduct{}_b.png'.format(
                pk)), os.path.join(settings.MEDIA_ROOT, 'products\custom\done\customProduct{}_b.png'.format(pk)))
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'tmp\done\customProduct{}_k.png'.format(
                pk)), os.path.join(settings.MEDIA_ROOT, 'products\custom\done\customProduct{}_k.png'.format(pk)))
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'tmp\customProduct{}.png'.format(
                pk)), os.path.join(settings.MEDIA_ROOT, 'products/custom/raw/customProduct{}.png'.format(pk)))
        except:
            return Response("Error with CustomImage Please Try again")

    serializer = OrderSerializer(data=request.data)
    userid = request.data.get('user')
    userData = CustomUser.objects.get(id=userid)

    if serializer.is_valid():
        obj = serializer.save()
        searchOrder = ['prod', 'model', 'year', 'back', 'keyboard', 'customimage', 'modelimage', 'back_dims_x', 'back_dims_y', 'keyboard_dims_x', 'keyboard_dims_y',
                       'other1_part', 'other1_dims_x', 'other1_dims_y', 'other2_part', 'other2_dims_x', 'other2_dims_y', 'other3_part', 'other3_dims_x', 'other3_dims_y', 'withLogo']
        orderList = json.loads(obj.order_json)
        userdata_cleaned = [userData.email, userData.firstname,
                            userData.lastname, str(userData.birthday), str(userData.phone), userData.location]
        res = []

        for key in searchOrder:
            if orderList.get(key, None):
                res.append(orderList.get(key, None))
            else:
                res.append("N/A")

        final_res = userdata_cleaned + res
        print(final_res)
        update_order_sheet(final_res)
        return Response("Order Was Sent Succesfully")
    else:
        return Response("Error please try again")


@api_view(['POST'])
def orderCreate_console(request, pk):

    if(pk != "0"):
        try:
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'tmp\done\customProduct_console{}_console_l.png'.format(
                pk)), os.path.join(settings.MEDIA_ROOT, 'products\custom\done\customProduct_console{}_console_l.png'.format(pk)))
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'tmp\done\customProduct_console{}_console_r.png'.format(
                pk)), os.path.join(settings.MEDIA_ROOT, 'products\custom\done\customProduct_console{}_console_r.png'.format(pk)))
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'tmp\customProduct_console{}.png'.format(
                pk)), os.path.join(settings.MEDIA_ROOT, 'products/custom/raw/customProduct_console{}.png'.format(pk)))
        except:
            return Response("Error with CustomImage Please Try again")

    serializer = OrderSerializer(data=request.data)
    userid = request.data.get('user')
    userData = CustomUser.objects.get(id=userid)

    if serializer.is_valid():
        obj = serializer.save()

        searchOrder = ['model', 'type', 'body', 'control',
                       'modelimage', 'customimage', 'modelimage', 'withLogo']
        orderList = json.loads(obj.order_json)

        userdata_cleaned = [userData.email, userData.firstname,
                            userData.lastname, str(userData.birthday), str(userData.phone), userData.location]
        res = []

        for key in searchOrder:
            if orderList.get(key, None):
                res.append(orderList.get(key, None))
            else:
                res.append("N/A")

        final_res = userdata_cleaned + res
        print(final_res)
        # update_order_sheet(final_res)
        return Response("Order Was Sent Succesfully")
    else:
        return Response("Error please try again")


@api_view(['PATCH'])
def orderUpdate(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(
        instance=order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def orderDelete(request, pk):
    user = CustomUser.objects.get(id=pk)
    queryset = Order.objects.filter(user=user)
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def custom_image(request, pk):

    user = CustomUser.objects.get(id=pk)
    data = request.FILES['image']
    value = randint(0, 100)

    if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'tmp/customProduct{}.png'.format(value))):
        os.remove(os.path.join(settings.MEDIA_ROOT,
                  'tmp/customProduct{}.png'.format(value)))

    path = default_storage.save(
        'tmp/customProduct{}.png'.format(value), ContentFile(data.read()))

    print('>>>> ' + os.path.join(settings.MEDIA_ROOT, path))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    customizeMockup(
        tmp_file, f"{settings.MEDIA_ROOT}/tmp/done/customProduct{value}")

    return JsonResponse({"id": value})


@api_view(['POST'])
def custom_image_console(request, pk):

    user = CustomUser.objects.get(id=pk)
    data = request.FILES['image']
    value = randint(0, 100)

    if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'tmp/customProduct_console{}.png'.format(value))):
        os.remove(os.path.join(settings.MEDIA_ROOT,
                  'tmp/customProduct_console{}.png'.format(value)))

    path = default_storage.save(
        'tmp/customProduct_console{}.png'.format(value), ContentFile(data.read()))

    print('>>>> ' + os.path.join(settings.MEDIA_ROOT, path))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    customizeMockup_console(
        tmp_file, f"{settings.MEDIA_ROOT}/tmp/done/customProduct_console{value}")

    return JsonResponse({"id": value})


def get_custom_image(request, pk):
    queryset = CustomImage.objects.all()
    serializer = CISerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def clear_image(request, pk):
    print(os.path.join(settings.MEDIA_ROOT,
          'products/done/customProduct{}_k.png'.format(pk)))
    if (os.path.exists(os.path.join(settings.MEDIA_ROOT, 'products/done/customProduct{}_k.png'.format(pk))) | os.path.exists(os.path.join(settings.MEDIA_ROOT, 'products/done/customProduct{}_k.png'.format(pk)))):
        os.remove(os.path.join(settings.MEDIA_ROOT,
                  'products/done/customProduct{}_k.png'.format(pk)))
        os.remove(os.path.join(settings.MEDIA_ROOT,
                  'products/done/customProduct{}_b.png'.format(pk)))
        return Response("Deleted")
    else:
        return Response("Couldnt find file")
