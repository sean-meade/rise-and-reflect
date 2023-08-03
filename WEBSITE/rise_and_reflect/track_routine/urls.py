from . import views
from django.urls import path

urlpatterns = [
    path('track_routine/', views.track_routine, name='track_routine'),
]
