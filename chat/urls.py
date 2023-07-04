from django.urls import path
from .views import *

urlpatterns = [
    path("" ,JoinRoom ),
    path("<str:room_name>/" ,Room)
]