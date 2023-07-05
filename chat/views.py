from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

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
        "users": users  
       
    })