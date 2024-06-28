from django.db import models
from custom_login.models import UserProfile
from django.apps import apps


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
    
    def delete(self, *args, **kwargs):
        TrackedTasks = apps.get_model('tasks', 'TrackedTasks')

        # Find all tracked tasks associated with this routine
        tracked_tasks = TrackedTasks.objects.filter(personal_routine=self)

        # For each tracked task, find the personal tasks and delete custom tasks
        for tracked_task in tracked_tasks:
            personal_task = tracked_task.personal_task

            # If the task is custom, delete it
            if personal_task.task_id.custom:
                personal_task.task_id.delete()

            # Delete the personal task itself
            personal_task.delete()

        # Delete the routine task
        super(RoutineTasks, self).delete(*args, **kwargs)