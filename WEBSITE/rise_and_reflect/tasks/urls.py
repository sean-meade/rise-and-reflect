from . import views
from django.urls import path

urlpatterns = [
    path('create_routine/<str:routine_type>', views.create_routine, name='create_routine'),
    path('edit_tasks/<str:routine_type>', views.edit_tasks, name='edit_tasks'),
    path('sort/', views.sort, name='sort'),
    path('update_tasks/<str:routine_type>', views.update_tasks, name='update_tasks')
]
