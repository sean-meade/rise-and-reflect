from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('create_routine/', views.create_routine, name='create_routine')
]
