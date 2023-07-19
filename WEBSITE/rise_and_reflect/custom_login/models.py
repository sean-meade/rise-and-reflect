from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    logged_in = models.BooleanField(default=False)

    
    