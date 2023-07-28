from . import views
from django.urls import path

urlpatterns = [
    path('create_routine/', views.create_routine, name='create_routine'),
    path('set_evening_tasks/', views.set_evening_tasks, name='set_evening_tasks'),
    path('set_morning_tasks/', views.set_morning_tasks, name='set_morning_tasks'),
]
