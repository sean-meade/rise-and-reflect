from django.contrib import admin
from .models import RoutineTasks

class RoutineTasksAdmin(admin.ModelAdmin):
    list_display = ['user', 'day', 'routine_type']
    search_fields = ['user', 'day', 'routine_type']

admin.site.register(RoutineTasks, RoutineTasksAdmin)