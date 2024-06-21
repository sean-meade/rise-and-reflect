from django.conf import settings
from django.db import models
from custom_login.models import UserProfile


TASK_TYPE = [
    ("Evening", "Evening"),
    ("Morning", "Morning"),
]

# Table to link TrackedTasks and the day
class RoutineTasks(models.Model):

    user = models.ForeignKey(UserProfile, verbose_name='user',
                                related_name='user_routine_fid', on_delete=models.CASCADE)
    day = models.DateField(verbose_name='routine_day', auto_now=True)
    routine_type = models.CharField(max_length=9, choices=TASK_TYPE)

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.routine_type}"

