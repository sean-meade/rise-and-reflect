from . import views
from django.urls import path

urlpatterns = [
    path('get_commitments/', views.get_commitments, name='get_commitments'),
    path('health-area/', views.health_areas, name='health-areas'),
    path('daily-commit/', views.daily_commit, name='daily-commit')
]
