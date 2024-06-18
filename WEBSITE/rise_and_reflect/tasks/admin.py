from django.contrib import admin
from .models import Tasks, PersonalTasks, TrackedTasks

class PersonalTasksAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_id', 'duration', 'order']
    search_fields = ['user', 'task_id', 'duration', 'order']

admin.site.register(PersonalTasks,PersonalTasksAdmin)
admin.site.register(Tasks)
admin.site.register(TrackedTasks)