from . import views
from django.urls import path

urlpatterns = [
    path('create_routine/', views.create_routine, name='create_routine')
]
