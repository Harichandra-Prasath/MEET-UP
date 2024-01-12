from django.urls import path
from .views import *

urlpatterns = [
    path("" ,JoinRoom,name="index"),
    path("<str:room_name>/" ,Room),
    path("api/getServer/",getservers)
]