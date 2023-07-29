from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

TASK_TYPE = [
    ("Evening", "Evening"),
    ("Morning", "Morning"),
]

# Table to link TrackedTasks and the day
class RoutineTasks(models.Model):
    
    user = models.ForeignKey(User, verbose_name='user',
                                related_name='user_routine_fid', on_delete=models.CASCADE)
    day = models.DateField(verbose_name='routine_day', default=timezone.now)
    routine_type = models.CharField(max_length=9, choices=TASK_TYPE)
