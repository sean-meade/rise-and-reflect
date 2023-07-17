from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='home'),
    path('daily-commit/', views.daily_commit, name='daily-commit'),
    path('set_goals/', views.set_goals, name='set_goals'),
]

#STATIC_URL = '/static/'
#STATICFILES_DIRS = [
   # os.path.join(BASE_DIR, 'rise_and_reflect/static'),
#]
