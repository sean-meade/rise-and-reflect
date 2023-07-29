from . import views
from django.urls import path

urlpatterns = [
    path('track_routine/', views.track_routine, name='track_routine'),
    path('<int:pk>/', views.RoutineSortingView.as_view(), name='task_sorting')
]
