from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

users = []

# Create your views here.

@csrf_exempt
def JoinRoom(request):
    if request.method=="POST":
        users.append(request.POST.get('user'))
        url = '/'+request.POST.get('room')
        print(users)
        return redirect(url)
    print(users)
    return render(request , "chat/lobby.html")

def Room(request , room_name): 
    return render(request , 'chat/room.html' , {
        "room_name":room_name,
        "users": users,
    })


with open('credentials.json',"r") as json_file:
    data = json.load(json_file)
servers = data.get('servers',[])


def getservers(request):
    return JsonResponse({"ice_servers":servers})