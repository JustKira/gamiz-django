
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('order/<pk>', views.getOrder, name="user"),
    path('order-list/<pk>', views.getOrderAll, name="user-update"),
    path('order-create/<pk>', views.orderCreate, name="user-create"),
    path('order-create-console/<pk>',
         views.orderCreate_console, name="user-create"),
    path('order-update/<pk>', views.orderUpdate, name="user-update"),
    path('order-delete/<pk>', views.orderDelete, name="user-delete"),
    path('custom-image/<pk>', views.custom_image, name="user-update"),
    path('custom-image-console/<pk>',
         views.custom_image_console, name="user-update"),
    path('get-custom-list/<pk>', views.get_custom_image, name="user-update"),
    path('custom-image-clear/<pk>', views.clear_image, name="user-update")
]
