from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
# Create your views here.

@login_required
def room(request, room_name):
    # Check if private room
    if room_name.startswith("private_"):
        try:
            _, id1, id2 = room_name.split("_")
            id1 = int(id1)
            id2 = int(id2)

            # If current user not part of this private room
            if request.user.id not in [id1, id2]:
                return HttpResponseForbidden("You are not allowed to access this private chat.")

        except:
            return HttpResponseForbidden("Invalid private room.")

    room = get_object_or_404(Room, name=room_name)
    messages = room.messages.order_by('timestamp')[:50]

    return render(
        request,
        'chat_room.html',
        {
            'room_name': room_name,
            'messages': messages
        }
    )


def register(request):
    if request.method == 'POST':
        username  =    request.POST['username']
        email     =    request.POST['email']
        password  =    request.POST['password']
        cnf_password = request.POST['cnf_password']

        if password == cnf_password:
            User.objects.create_user(username=username , password=password , email=email)
            return redirect('login')
        else:
            return render(request,'register.html',{'error':'Invalid Credentials'})
    return render(request,'register.html')

def login_user(request):
    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']

        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email = username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                return render(request,'login.html',{'error':'Invalid Credentials'})
        else:
            username = username_or_email
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('user_list')
        else:
            return render(request,'login.html',{'error':'Invalid Credentials'})
        
    return render(request,'login.html')
            

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def rooms(request):

    if request.method == 'POST':
        room_name = request.POST['room_name'].strip()

        room, created = Room.objects.get_or_create(
            name=room_name,
            defaults={"created_by": request.user}
        )

        # add user to room members
        room.members.add(request.user)

        return redirect('chat_room', room_name=room_name)

    # show rooms user created OR joined
    rooms = Room.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    return render(request, 'rooms.html', {'rooms': rooms})
    

            

    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def user_list(request):
    users = User.objects.exclude(id = request.user.id)
    return render(request, 'users.html', {'users' : users})

@login_required
def private_chat(request, user_id):

    other_user = User.objects.get(id = user_id)

    min_id = min(request.user.id, other_user.id)
    max_id = max(request.user.id, other_user.id)

    room_name = f"private_{min_id}_{max_id}"

    Room.objects.get_or_create(name = room_name)

    return redirect('chat_room', room_name=room_name)

    
