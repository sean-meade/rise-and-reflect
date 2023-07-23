from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('profile.html', views.profile, name='profile'),
    path('user-homepage.html', views.user_homepage, name='user-homepage'),
    path('daily-commit/', views.daily_commit, name='daily-commit'),
    path('set_goals/', views.set_goals, name='set_goals'),
]
