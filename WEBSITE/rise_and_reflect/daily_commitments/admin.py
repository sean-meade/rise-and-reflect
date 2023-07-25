from django.contrib import admin
from .models import UserTimeCommitments, UserHealthArea

admin.site.register(UserHealthArea)
admin.site.register(UserTimeCommitments)