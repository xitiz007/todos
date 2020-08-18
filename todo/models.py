from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

User._meta.get_field('email')._unique = True
# User._meta.get_field('email').required = True

class Todo(models.Model):
    title = models.CharField(max_length= 100)
    memo = models.TextField(blank= True)
    important = models.BooleanField(default= False)
    created = models.DateTimeField(auto_now_add= True)
    datecompleted = models.DateTimeField(blank= True, null = True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null= True)
    profile_picture = models.ImageField(default= 'user.png', null= True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.profile_picture.path)
        if image.height > 200 or image.width > 200 :
            image.thumbnail((200, 200))
            image.save(self.profile_picture.path)
