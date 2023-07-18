from django.conf import settings
from django.db import models
from daily_commitments.models import UserHealthArea

User = settings.AUTH_USER_MODEL

class Tasks(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='user_to_task', 
                             on_delete=models.CASCADE)
    health_area = models.ForeignKey(UserHealthArea, verbose_name='user',
                                related_name='task_health_area', on_delete=models.CASCADE)

class UserRoutine(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='user_routine', on_delete=models.CASCADE)
    task_id_1 = models.ForeignKey(Tasks, verbose_name='task1',
                                related_name='task1', on_delete=models.CASCADE)
    duration_1 = models.IntegerField(blank=True, null=True)
    task_id_2 = models.ForeignKey(Tasks, verbose_name='task2',
                                related_name='task2', on_delete=models.CASCADE)
    duration_2 = models.IntegerField(blank=True, null=True)
    task_id_3 = models.ForeignKey(Tasks, verbose_name='task3',
                                related_name='task3', on_delete=models.CASCADE)
    duration_3 = models.IntegerField(blank=True, null=True)
    task_id_4 = models.ForeignKey(Tasks, verbose_name='task4',
                                related_name='task4', on_delete=models.CASCADE)
    duration_4 = models.IntegerField(blank=True, null=True)
    task_id_5 = models.ForeignKey(Tasks, verbose_name='task5',
                                related_name='task5', on_delete=models.CASCADE)
    duration_5 = models.IntegerField(blank=True, null=True)
    task_id_6 = models.ForeignKey(Tasks, verbose_name='task6',
                                related_name='task6', on_delete=models.CASCADE)
    duration_6 = models.IntegerField(blank=True, null=True)
    task_id_7 = models.ForeignKey(Tasks, verbose_name='task7',
                                related_name='task7', on_delete=models.CASCADE)
    duration_7 = models.IntegerField(blank=True, null=True)
    task_id_8 = models.ForeignKey(Tasks, verbose_name='task8',
                                related_name='task8', on_delete=models.CASCADE)
    duration_8 = models.IntegerField(blank=True, null=True)
