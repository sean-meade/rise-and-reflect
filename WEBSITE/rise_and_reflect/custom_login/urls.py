from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='home'),
<<<<<<< HEAD
    path('profile.html', views.profile, name='profile'),
    path('user-homepage.html', views.user_homepage, name='user-homepage'),
    
=======
    path('daily-commit/', views.daily_commit, name='daily-commit'),
    path('set_goals/', views.set_goals, name='set_goals'),
>>>>>>> 18cee19a05c8c7f1fc883881d48f62023f5619a1
]
