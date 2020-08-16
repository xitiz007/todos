from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_save

def add_to_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user = instance
        )

post_save.connect(add_to_userprofile, sender= User)

