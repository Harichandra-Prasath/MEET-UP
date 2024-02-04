from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponseRedirect
import json
from .forms import *

import django
django.setup()

from django.contrib.auth.models import User
from django.urls import reverse
import jwt
from django.db import IntegrityError
import os
import time

maps = [{}]
secret = os.getenv("SECRET")
with open('credentials.json',"r") as json_file:
    data = json.load(json_file)
servers = data.get('servers',[])

def JoinRoom(request):
    if request.method=="POST":
        room = request.POST.get('room')
        url = "/room/"+room+'/'
        return HttpResponseRedirect(url)
    return render(request , "chat/index.html")


def Room(request , room_name):
    if request.COOKIES.get('jwt'):
        print("Session based")
        payload = jwt.decode(request.COOKIES['jwt'],secret,algorithms="HS256")
        print(f"{payload['user']} Joined the room")
        Process(payload['user'],room_name,maps)
        return render(request , 'chat/room.html' , {
            "room_name":room_name,
            "users": maps[0][room_name],
            "username":payload['user']
        })
    if request.method=="POST":
        print("Not session Based")
        user = request.POST.get('user')
        Process(user,room_name,maps)
        print(f"{user} Joined the room")
        return render(request , 'chat/room.html' , {
            "room_name":room_name,
            "users": maps[0][room_name],
            "username":user
        })
    return render(request , "chat/lobby.html")






def getservers(request):
    print("Servers fetched successfully")
    return JsonResponse({"ice_servers":servers})

# internal util function
def Process(user,room,maps):
    if room not in maps[0]:
        maps[0][room] = []
    maps[0][room].append(user)

def register_view(request):
    if request.method=="POST":
        form = Register_form(request.POST)

        # Form validation 
        if form.is_valid():
            username = form.cleaned_data["Username"]            
            # Password Matching check
            if form.cleaned_data["Password"]!=form.cleaned_data["ConfirmPassword"]:
                return render(request,"chat/register.html",{
                    "message":"Passwords did not match.Try again",     # sending error context
                    "form":form
                })            
            password = form.cleaned_data["Password"] # password after check

            # User Creation
            try:
                user = User.objects.create_user(username=username,password=password)
                # Above create_user function calls make_password() on itself for hashing 
                # It is same as using set_password() method on the user for password hashing
                user.save()
            except IntegrityError:
                if User.objects.filter(username=username).exists():
                    return render(request,"chat/register.html",{
                        "message":"Username already Exists.Try again",
                        "form":form
                    })            
                # we are using integrity error to catch the duplication in db
            return HttpResponseRedirect(reverse("login"))
    else:
        form = Register_form()
        return render(request,"chat/register.html",{"form":form})

def login_view(request):
    if request.method=="POST":
        form = Login_form(request.POST)

        if form.is_valid():
            Username = form.cleaned_data["Username"] # Can be either username or email
            password = form.cleaned_data["Password"]

            user = User.objects.get(username=Username)
            if user.check_password(password):
                token = jwt.encode({"user":Username},secret,algorithm="HS256")
                response = HttpResponseRedirect(reverse("index"))
                response.set_cookie('jwt',token,max_age=30*24*60*60)
                return response
            else:
                return render(request,"chat/login.html",{
                        "message":"Invalid Credentials",
                        "form":form
                    })

    else:
        form = Login_form()
        return render(request,"chat/login.html",{"form":form})

def logout_view(request):
    response = HttpResponseRedirect(reverse('index'))
    response.set_cookie("jwt","",expires=time.time()-24*60*60)
    return response

@csrf_exempt
def remove_user(request,room_name):
    if request.method=="DELETE":
        user = json.loads(request.body.decode())['user']

        maps[0][room_name].remove(user)
        if len(maps[0][room_name])==0:     ## No user in current room
            #remove the room
            maps[0].pop(room_name)
            print(maps[0])

        return JsonResponse({"Status":"Success","Message":"User removed"})
    return JsonResponse({"Status":"Error","Message":"Method now allowed"})