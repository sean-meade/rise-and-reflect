from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('daily-commit-submit/', views.submit_commitments, name='daily-commit-submit'),
    path('health-goals/', views.health_goals, name='health-goals'),
    path('accounts/login/setup/daily-commit/', views.submit_commitments, name='daily-commit')
]
