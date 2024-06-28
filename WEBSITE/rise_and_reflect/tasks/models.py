from django.db import models
from custom_login.models import UserProfile
from track_routine.models import RoutineTasks
from daily_commitments.models import UserHealthArea

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
    task = models.CharField(max_length=80)
    task_type = models.CharField(max_length=9, choices=TASK_TYPE)
    custom = models.BooleanField(default=False)
    users = models.ManyToManyField(UserProfile, related_name='users_ptasks', through='PersonalTasks')

    # TODO: Custom save method limit tasks number

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.id} | {self.task} | {self.task_type}"


# What tasks a user has selected or created and with what duration
class PersonalTasks(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task_id = models.ForeignKey(
        Tasks, verbose_name="task_id", related_name="task_id", on_delete=models.CASCADE
    )
    duration = models.IntegerField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.task_id.task}"

    class Meta:
        ordering = ['order']


class TrackedTasks(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    personal_task = models.ForeignKey(
        PersonalTasks, verbose_name="personal_task", related_name="personal_task", on_delete=models.CASCADE
    )
    personal_routine = models.ForeignKey(
        RoutineTasks,
        verbose_name="personal_routine",
        related_name="personal_routine",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    completed = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):

        self.personal_task.delete()

        super(RoutineTasks, self).delete(*args, **kwargs)

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.personal_task.task_id.task} | {self.completed}"