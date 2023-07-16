from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class UserTimeCommitments(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='commitments', on_delete=models.CASCADE)
    hours_of_sleep = models.IntegerField(blank=True, null=True)
    work_time_from = models.TimeField(blank=True, null=True)
    work_time_to = models.TimeField(blank=True, null=True)
    commute_time = models.IntegerField(blank=True, null=True)
    wake_time = models.TimeField(blank=True, null=True)
    
    