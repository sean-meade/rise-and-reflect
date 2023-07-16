from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='home'),
    path('daily-commit/', views.daily_commit, name='daily-commit')
]
