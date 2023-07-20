from django.conf import settings
from django.db import models
from daily_commitments.models import UserHealthArea

User = settings.AUTH_USER_MODEL

# Two categories for tasks
TASK_TYPE = [
    ("Evening", "Evening"),
    ("Morning", "Morning"),
    ("Custom", "Custom"),
]

# All tasks either suggested or custom
class Tasks(models.Model):
    health_area = models.ForeignKey(UserHealthArea, verbose_name='health_area', to_field='health_area',
                                related_name='task_health_area', on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    task_type = models.CharField(max_length=9, choices=TASK_TYPE)

# What tasks a user has selected or created and with what duration
class PersonalTasks(models.Model):
    user = models.ForeignKey(User, verbose_name='user',
                                related_name='user_routine', on_delete=models.CASCADE)
    task_id = models.ForeignKey(Tasks, verbose_name='task_id',
                                related_name='task_id', on_delete=models.CASCADE)
    duration = models.IntegerField(blank=True, null=True)
