from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50,unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(User, related_name="joined_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.room.name}"