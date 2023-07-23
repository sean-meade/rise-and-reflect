from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Choices for health areas
HEALTH_AREAS = [
    ("Choice 1", "Choice 1"),
    ("Choice 2", "Choice 2"),
    ("Choice 3", "Choice 3"),
    ("Choice 4", "Choice 4"),
]

# Database table that holds all the users info on their time commitments
class UserTimeCommitments(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='commitments', on_delete=models.CASCADE)
    hours_of_sleep = models.IntegerField(blank=True, null=True)
    work_time_from = models.TimeField(blank=True, null=True)
    work_time_to = models.TimeField(blank=True, null=True)
    commute_time = models.IntegerField(blank=True, null=True)
    get_ready_time = models.IntegerField(blank=True, null=True, default=0)
    wake_time = models.TimeField(blank=True, null=True)
    
# TODO: Either find a better way to represent health areas (currently have to create every time you reset
# the database) or find a way to automatically create on migrate
# Table of Health areas
class UserHealthArea(models.Model):
    
    health_area = models.CharField(max_length=9, choices=HEALTH_AREAS, unique=True, primary_key=True, default='None')