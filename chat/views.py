from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

Usersmap = {}

maps = [Usersmap]

def JoinRoom(request):
    if request.method=="POST":
        room = request.POST.get('room')
        url = "/"+room+'/'
        return redirect(url)
    return render(request , "chat/index.html")


def Room(request , room_name):
    if request.method=="POST":
        user = request.POST.get('user')
        Process(user,room_name,maps)
        return render(request , 'chat/room.html' , {
            "room_name":room_name,
            "users": maps[0][room_name],
        })
    return render(request , "chat/lobby.html")



with open('credentials.json',"r") as json_file:
    data = json.load(json_file)
servers = data.get('servers',[])


def getservers(request):
    print("Servers fetched successfully")
    return JsonResponse({"ice_servers":servers})

# internal util function
def Process(user,room,maps):
    if room not in maps[0]:
        maps[0][room] = []
    maps[0][room].append(user)