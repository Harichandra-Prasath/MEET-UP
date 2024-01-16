from django.urls import path
from .views import *

urlpatterns = [
    path("" ,JoinRoom,name="index"),
    path("room/<str:room_name>/" ,Room),
    path("api/getServer/",getservers),
    path("accounts/login/",login_view,name="login"),
    path("accounts/register/",register_view,name="register"),
    path("accounts/logout/",logout_view,name="logout")
]