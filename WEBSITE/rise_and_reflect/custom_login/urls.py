from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('daily-commit/', views.daily_commit, name='daily-commit'),
    path('set_goals/', views.set_goals, name='set_goals'),
]
