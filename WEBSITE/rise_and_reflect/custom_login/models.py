from django.conf import settings
from django.db import models
from daily_commitments.models import UserHealthArea
from django.contrib.auth.models import AbstractUser

User = settings.AUTH_USER_MODEL

# Database table that holds extra information on the user
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    logged_in = models.BooleanField(default=False)
    health_area = models.ForeignKey(UserHealthArea, verbose_name='user_health_area', 
                                    to_field='health_area', null=True,
                                    related_name='user_health_area', on_delete=models.PROTECT)
    
    def __str__(self):
        # Return a string that represents the instance
        return f"{self.name}"

class CustomUser(AbstractUser):

    auth_token = models.CharField(max_length=255, null=True, blank=True)

    def set_auth_token(self, auth_token):
        self.auth_token = auth_token
        self.save()