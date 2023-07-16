from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('daily-commit/', views.daily_commit, name='daily-commit')
]
