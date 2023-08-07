from . import views
from django.urls import path
from daily_commitments.views import health_areas

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='profile'),
    path('user-homepage/', views.user_homepage, name='user-homepage'),
    path('set_goals/', views.set_goals, name='set_goals'),
    path('profile_summary/', views.profile_summary, name='profile_summary'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('accounts/login/profile/', views.profile_summary),
    path('accounts/login/health-area/', health_areas),
    path('app_login', views.app_login, name='app_login'),
    path('display_tasks/', views.display_tasks, name='display_tasks'),
]