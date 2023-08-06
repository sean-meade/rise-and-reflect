from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Choices for health areas ('name', 'value')
HEALTH_AREAS = [
    ("Relieve Stress or Anxiety", "Relieve Stress or Anxiety"),
    ("Improve Self-Awareness", "Improve Self-Awareness"),
    ("Have a Balanced Lifestyle", "Have a Balanced Lifestyle"),
    ("Manage Time Effectively", "Manage Time Effectively"),
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

class UserHealthArea(models.Model):
    
    health_area = models.CharField(max_length=30, choices=HEALTH_AREAS, unique=True, primary_key=True, default='None')