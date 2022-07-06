from django.urls import path
from . import views

urlpatterns = [
    path('event/<pk>', views.getEvent, name="user"),
    path('events', views.getEvents, name="events"),
    path('event-create', views.eventCreate, name="user-create"),
    path('event-update/<pk>', views.eventUpdate, name="user-update"),
    path('event-delete/<pk>', views.eventDelete, name="user-delete"),
    path('prod-refresh', views.refresh, name="refresh"),
    path('prod-list', views.getImagesCount, name="prod-list")

]
