from django.shortcuts import render,redirect

users = []

# Create your views here.
def JoinRoom(request):
    if request.method=="POST":
        users.append(request.POST.get('user'))
        url = '/'+request.POST.get('room')
        return redirect(url)
    return render(request , "chat/lobby.html")

def Room(request , room_name):
 
    return render(request , 'chat/room.html' , {
        "room_name":room_name,
        "users": users  
       
    })