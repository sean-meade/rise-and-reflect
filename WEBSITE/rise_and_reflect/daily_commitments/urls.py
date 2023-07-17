from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('daily-commit-submit/', views.submit_commitments, name='daily-commit-submit'),
    path('accounts/login/setup/daily-commit/', views.daily_commit, name='daily-commit')
]
