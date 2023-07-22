from datetime import date
from django.conf import settings
from django.db import models
from daily_commitments.models import UserHealthArea
from tasks.models import PersonalTasks

User = settings.AUTH_USER_MODEL
    

# All tasks either suggested or custom
class RoutineTasks(models.Model):
    
    personal_task_id = models.ForeignKey(PersonalTasks, verbose_name='personal_task_id', 
                                         related_name='personal_task_id', on_delete=models.PROTECT)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, verbose_name='user',
                                related_name='user_routine_fid', on_delete=models.PROTECT)
    day = models.DateField(verbose_name='routine_day', default=date.today())
