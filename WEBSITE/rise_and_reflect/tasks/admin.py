from django.contrib import admin
from .models import Tasks, PersonalTasks, TrackedTasks

class PersonalTasksAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_id', 'duration', 'order']
    search_fields = ['user', 'task_id', 'duration', 'order']

class TasksAdmin(admin.ModelAdmin):
    list_display = ['task', 'custom', 'task_type', 'health_area']
    search_fields = ['task', 'custom', 'task_type', 'health_area']

admin.site.register(PersonalTasks,PersonalTasksAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(TrackedTasks)