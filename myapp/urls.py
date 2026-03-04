from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/',views.room,name='chat_room'),
    path('users/', views.user_list , name = 'user_list'),
    path('private/<int:user_id>/', views.private_chat, name='private_chat'),

    path('register/',views.register , name = 'register'),
    path('',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('rooms/',views.rooms, name='rooms')
]