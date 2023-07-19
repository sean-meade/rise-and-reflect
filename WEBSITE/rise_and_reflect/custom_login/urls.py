from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='home'),
    path('profile.html', views.profile, name='profile'),
    path('user-homepage.html', views.user_homepage, name='user-homepage'),
    
]
