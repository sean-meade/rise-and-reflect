from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'logged_in', 'health_area']
    search_fields = ['user', 'name', 'logged_in', 'health_area']

admin.site.register(UserProfile, UserProfileAdmin)