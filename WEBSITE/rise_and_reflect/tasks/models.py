from django.conf import settings
from django.db import models
from track_routine.models import RoutineTasks
from daily_commitments.models import UserHealthArea

User = settings.AUTH_USER_MODEL

# Two categories for tasks
TASK_TYPE = [
    ("Evening", "Evening"),
    ("Morning", "Morning"),
]


# All tasks either suggested or custom
class Tasks(models.Model):
    health_area = models.ForeignKey(
        UserHealthArea,
        verbose_name="health_area",
        to_field="health_area",
        related_name="task_health_area",
        on_delete=models.PROTECT,
    )
    task = models.CharField(max_length=50)
    task_type = models.CharField(max_length=9, choices=TASK_TYPE)
    custom = models.BooleanField(default=False)


# What tasks a user has selected or created and with what duration
class PersonalTasks(models.Model):
    user = models.ManyToManyField(
        User, verbose_name="user", related_name="user_routine", through="PersonalTasksOrdered"
    )
    task_id = models.ForeignKey(
        Tasks, verbose_name="task_id", related_name="task_id", on_delete=models.CASCADE
    )
    duration = models.IntegerField(blank=True, null=True)

class TrackedTasks(models.Model):
    
    personal_task = models.ForeignKey(
        PersonalTasks, verbose_name="personal_task", related_name="personal_task", on_delete=models.CASCADE
    )
    personal_routine = models.ForeignKey(
        RoutineTasks,
        verbose_name="personal_routine",
        related_name="personal_routine",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    completed = models.BooleanField(default=False)

class PersonalTasksOrdered(models.Model):
    user = models.ForeignKey(User, verbose_name='user',
                                related_name='pt_order_fid', on_delete=models.CASCADE)
    personal_task = models.ForeignKey(
        PersonalTasks, verbose_name="personal_task_order", related_name="personal_task_order", on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']