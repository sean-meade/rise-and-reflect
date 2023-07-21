from django.contrib import admin
from .models import Tasks, PersonalTasks

admin.site.register(PersonalTasks)
admin.site.register(Tasks)