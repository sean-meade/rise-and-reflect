from django.contrib import admin
from .models import Tasks, PersonalTasks, TrackedTasks

admin.site.register(PersonalTasks)
admin.site.register(Tasks)
admin.site.register(TrackedTasks)